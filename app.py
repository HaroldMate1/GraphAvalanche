import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

st.title("Graph Avalanche: Data Visualization")



# Read data from Excel file
import requests
import time

excel_path = r"C:\Users\haroldmmojica\Downloads\platform\papers_adept.xlsx"
df_excel = pd.read_excel(excel_path)
data = df_excel.to_dict(orient='records')


# --- Optimized: Batch OpenAlex requests and cache results ---
import math

# Build DOI index for fast lookup
doi_to_id = {}
id_to_doi = {}
for item in data:
    doi = item.get('doi') or item.get('DOI')
    node_id = item['id'] if 'id' in item else item.get('ID', None)
    if doi and node_id:
        norm_doi = doi.lower().strip()
        doi_to_id[norm_doi] = node_id
        id_to_doi[node_id] = norm_doi

# Batch fetch OpenAlex records for all DOIs in our dataset
all_dois = list(doi_to_id.keys())
doi_to_references = {}
batch_size = 50
st.info(f"Fetching OpenAlex data in batches for {len(all_dois)} papers. This may take a few minutes...")
for i in range(0, len(all_dois), batch_size):
    batch = all_dois[i:i+batch_size]
    # OpenAlex expects DOIs as filter=doi:doi1|doi2|...
    filter_str = '|'.join([f'https://doi.org/{d}' for d in batch])
    url = f"https://api.openalex.org/works?filter=doi:{filter_str}&per-page={batch_size}"
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            results = r.json().get('results', [])
            for rec in results:
                rec_doi = rec.get('doi')
                if rec_doi:
                    norm_doi = rec_doi.lower().strip()
                    doi_to_references[norm_doi] = rec.get('referenced_works', [])
        # Be nice to the API
        time.sleep(1)
    except Exception:
        continue

# Batch fetch DOIs for all referenced_works that are in our dataset
openalex_id_to_doi = {}
all_referenced_ids = set()
for refs in doi_to_references.values():
    for ref in refs:
        all_referenced_ids.add(ref)
all_referenced_ids = list(all_referenced_ids)

for i in range(0, len(all_referenced_ids), batch_size):
    batch = all_referenced_ids[i:i+batch_size]
    filter_str = '|'.join(batch)
    url = f"https://api.openalex.org/works?filter=openalex_id:{filter_str}&per-page={batch_size}"
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            results = r.json().get('results', [])
            for rec in results:
                rec_id = rec.get('id')
                rec_doi = rec.get('doi')
                if rec_id and rec_doi:
                    openalex_id_to_doi[rec_id] = rec_doi.lower().strip()
        time.sleep(1)
    except Exception:
        continue

# Build connections only between papers in our dataset
connections = []
for src_doi, refs in doi_to_references.items():
    src_id = doi_to_id.get(src_doi)
    for ref in refs:
        tgt_doi = openalex_id_to_doi.get(ref)
        if tgt_doi and tgt_doi in doi_to_id:
            tgt_id = doi_to_id[tgt_doi]
            connections.append((src_id, tgt_id))

# Build the graph
g = nx.DiGraph()
for item in data:
    node_id = item['id'] if 'id' in item else item.get('ID', None)
    g.add_node(node_id, label=item.get('label', item.get('title', '')), date=str(item.get('date', item.get('year', ''))))
for src, tgt in connections:
    g.add_edge(src, tgt)

# Graph Visualization
st.header("Network View (Balls and Sticks)")
pos = nx.spring_layout(g, seed=42)
edges = g.edges()
x_nodes = [pos[n][0] for n in g.nodes()]
y_nodes = [pos[n][1] for n in g.nodes()]

edge_x = []
edge_y = []
for edge in edges:
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='#888'),
    hoverinfo='none',
    mode='lines')

node_trace = go.Scatter(
    x=x_nodes, y=y_nodes,
    mode='markers+text',
    text=[g.nodes[n]['label'] for n in g.nodes()],
    textposition="bottom center",
    marker=dict(
        showscale=False,
        color='skyblue',
        size=30,
        line_width=2))

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False)))
st.plotly_chart(fig, use_container_width=True)

# Timeline Visualization
st.header("Timeline View")
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=df['date'],
    y=[1]*len(df),
    mode='markers+text',
    marker=dict(size=20, color='skyblue'),
    text=df['label'],
    textposition="top center"
))
fig2.update_layout(
    yaxis=dict(showticklabels=False),
    xaxis_title="Date",
    showlegend=False,
    height=200,
    margin=dict(l=20, r=20, t=40, b=20)
)
st.plotly_chart(fig2, use_container_width=True)

st.info("Replace the example data with your own to visualize your network and timeline.")
