# 📊 GraphAvalanche

**Interactive Citation Network Visualizer for AVALANCHE Literature Discovery Results**

Transform your AVALANCHE literature search into beautiful, interactive citation networks with automatic tier-based highlighting. Create Connected Papers-style visualizations for your systematic reviews and meta-analyses.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.10+-FF4B4B.svg)](https://streamlit.io)

---

## 🌟 Features

### Interactive Citation Networks
- **Connected Papers-style visualization** - Navigate citation relationships intuitively
- **Tier-based color coding** - Automatically highlights high-impact papers
- **Multiple layout algorithms** - Spring, Kamada-Kawai, Circular, Spectral
- **Interactive exploration** - Zoom, pan, hover for details

### Smart Analysis
- **Automatic tiering** - Papers categorized by citation impact (customizable thresholds)
- **Network statistics** - Density, connectivity, influential papers
- **Timeline view** - Chronological publication trends
- **OpenAlex integration** - Fetches citation relationships automatically

### Export & Share
- **GraphML export** - Import to Gephi, Cytoscape, or igraph
- **CSV export** - Data analysis in R/Python/Excel
- **Publication-ready figures** - High-quality visualizations for papers

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/HaroldMate1/GraphAvalanche.git
cd GraphAvalanche

# Install dependencies
pip install -r requirements.txt
```

### Run the App

python -m streamlit --version
python -m streamlit run app_v2.py


---

## 📖 Usage

### 1. Generate AVALANCHE Results

First, run [AVALANCHE](https://github.com/HaroldMate1/AVALANCHE) to discover literature:

```bash
python avalanche.py 10.1038/s41586-020-2649-2
```

This creates `avalanche_results.xlsx` with your papers.

### 2. Upload to GraphAvalanche

1. Launch GraphAvalanche: `streamlit run app_v2.py`
2. Click "Upload AVALANCHE Excel Results" in the sidebar
3. Select your `avalanche_results.xlsx` file

### 3. Customize Tiers (Optional)

Adjust citation thresholds in the sidebar:
- **Tier 1 (Gold)**: Default ≥100 citations
- **Tier 2 (Silver)**: Default ≥50 citations
- **Tier 3 (Bronze)**: Default ≥40 citations

### 4. Build Citation Network

Click "🔄 Fetch Citation Network" button. The app will:
- Query OpenAlex API for citation data (~2-3 minutes)
- Build directed citation graph
- Calculate network statistics

### 5. Explore & Export

- **Interact**: Hover over nodes, zoom, pan
- **Adjust**: Change layout algorithm, edge opacity, labels
- **Export**: Download GraphML or CSV for further analysis

---

## 📊 Citation Tier System

Papers are automatically categorized into visual tiers based on citation impact:

| Tier | Color | Default Threshold | Description |
|------|-------|-------------------|-------------|
| **Tier 1** | 🟡 Gold | ≥100 citations | Landmark papers |
| **Tier 2** | ⚪ Silver | ≥50 citations | High-impact papers |
| **Tier 3** | 🟤 Bronze | ≥40 citations | Core papers |
| **Other** | 🔵 Blue | <40 citations | Supporting literature |

Thresholds are fully customizable via the sidebar.

---

## 📋 Input Requirements

GraphAvalanche works with any Excel file that has these columns:

### Required Columns
- **Title**: Paper title (string)
- **DOI**: Digital Object Identifier (string)
- **Cited_By**: Citation count (integer)

### Optional Columns
- **Year**: Publication year (integer) - enables timeline view
- **Venue**: Journal/conference (string) - shown in hover info
- **Abstract**: Paper abstract (string) - shown in hover info
- **Relevance**: Relevance score (float) - from AVALANCHE scoring

### Example Input Format

```
Title,Year,DOI,Cited_By,Venue
"Strategies for enzyme prodrug therapy",2017,10.1016/j.addr.2016.09.005,278,Advanced Drug Delivery Reviews
"ADEPT: Trials and tribulations",2012,10.1016/j.bmc.2011.12.021,129,Bioorganic Chemistry
"Prodrugs for Targeted Tumor Therapies",2011,10.2174/138161211795428985,100,Current Pharmaceutical Design
```

---

## 🎨 Visualization Controls

### Sidebar Controls

| Control | Options | Purpose |
|---------|---------|---------|
| **Layout Algorithm** | Spring, Kamada-Kawai, Circular, Spectral | Graph arrangement style |
| **Show Labels** | On/Off | Display paper titles on nodes |
| **Edge Opacity** | 0.1 - 1.0 | Citation line transparency |
| **Show Timeline** | On/Off | Toggle chronological view |
| **Tier Thresholds** | Custom integers | Adjust tier boundaries |

### Interactive Features

- **Zoom**: Mouse scroll wheel
- **Pan**: Click and drag
- **Hover**: View paper details
- **Legend**: Click to show/hide tiers

---

## 🔬 Use Cases

### Academic Research
- **Literature Reviews**: Visualize research landscapes
- **Gap Analysis**: Identify underexplored areas
- **Trend Analysis**: Track field evolution over time

### Manuscript Preparation
- **Figures**: Publication-ready citation networks
- **Methods**: Document systematic search process
- **Discussion**: Illustrate research connections

### Teaching & Learning
- **Course Material**: Teach citation analysis
- **Student Projects**: Guide literature discovery
- **Research Training**: Demonstrate systematic reviews

---

## 📊 Network Analysis

### Statistics Provided

- **Node Count**: Total papers in network
- **Edge Count**: Citation relationships within dataset
- **Network Density**: Connectivity measure (0-1)
- **Most Cited**: Influential papers within network
- **Connected Components**: Research clusters

### Export Formats

#### GraphML (for network analysis)
```python
# Use in Python with NetworkX
import networkx as nx
G = nx.read_graphml('network.graphml')
```

#### CSV (for data analysis)
```r
# Use in R
library(tidyverse)
data <- read_csv('citation_network_data.csv')
```

---

## 🛠️ Advanced Usage

### Programmatic Access

Use the GraphAvalanche modules in your own code:

```python
from graphavalanche import CitationNetwork, MetadataLoader

# Load papers
papers = MetadataLoader.load_excel('avalanche_results.xlsx')

# Build network
network = CitationNetwork(papers)
network.build_connections()
graph = network.build_graph()

# Get statistics
stats = network.get_stats()
print(f"Network has {stats['nodes']} nodes and {stats['edges']} edges")
```

### Custom Visualization

```python
import networkx as nx
import plotly.graph_objects as go

# Load your graph
G = nx.read_graphml('network.graphml')

# Custom analysis
communities = nx.community.greedy_modularity_communities(G)
betweenness = nx.betweenness_centrality(G)

# Create custom visualization
# ... your code here
```

---

## 📖 Example Workflows

### Workflow 1: Quick Visualization

```bash
# 1. Run AVALANCHE
python avalanche.py 10.1038/nature12373

# 2. Launch GraphAvalanche
streamlit run app_v2.py

# 3. Upload avalanche_results.xlsx
# 4. Click "Fetch Citation Network"
# 5. Export figure for your paper
```

### Workflow 2: Custom Thresholds

```bash
# For niche fields with lower citation counts:
# 1. Upload your Excel file
# 2. Set Tier 1 = 20, Tier 2 = 10, Tier 3 = 5
# 3. Build network
# 4. Analyze tier distribution
```

### Workflow 3: Multiple Datasets

```bash
# Compare different literature searches:
# 1. Run AVALANCHE for Topic A → topicA_results.xlsx
# 2. Run AVALANCHE for Topic B → topicB_results.xlsx
# 3. Visualize each in GraphAvalanche
# 4. Compare network structures, densities, tier distributions
```

---

## 🔧 Configuration

### API Settings

GraphAvalanche uses the OpenAlex API (no key required). For faster access:

1. Add your email to get "polite pool" access:
```python
# In app_v2.py, line ~140
headers = {"User-Agent": "GraphAvalanche/1.0 (mailto:your.email@university.edu)"}
```

2. Rate limiting is built-in (1 second between requests)

### Customizing Tier Colors

Edit `tier_colors` dictionary in `app_v2.py`:

```python
tier_colors = {
    'Tier 1': '#FFD700',  # Gold
    'Tier 2': '#C0C0C0',  # Silver
    'Tier 3': '#CD7F32',  # Bronze
    'Other': '#87CEEB'    # Sky Blue
}
```

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Additional layout algorithms (hierarchical, force-atlas)
- [ ] Export to other formats (PDF, PNG)
- [ ] Clustering analysis (community detection)
- [ ] Comparative network analysis (multiple datasets)
- [ ] Theme customization (dark mode)
- [ ] Performance optimization (large networks >1000 nodes)

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📚 Citation

If you use GraphAvalanche in your research, please cite:

```
GraphAvalanche: Interactive Citation Network Visualizer for AVALANCHE
Harold Mateo Mojica Urrego, University of Navarra-TECNUN, 2026
GitHub: https://github.com/HaroldMate1/GraphAvalanche
```

For AVALANCHE itself:
```
AVALANCHE: Automated Federated Literature Discovery Tool
Harold Mateo Mojica Urrego, University of Navarra-TECNUN, 2026
GitHub: https://github.com/HaroldMate1/AVALANCHE
```

---

## 🐛 Troubleshooting

### Issue: "Missing required columns: DOI, Cited_By"

**Solution**: Ensure your Excel file has columns named exactly `Title`, `DOI`, and `Cited_By` (case-sensitive).

### Issue: "Network appears empty" (no edges)

**Cause**: Papers don't cite each other, or OpenAlex doesn't have citation data.

**Solutions**:
- Try a different seed paper with more citations
- Check that DOIs are valid
- Verify papers are within the same research domain

### Issue: "API request timeout"

**Solutions**:
- Check internet connection
- Wait a few minutes and retry (rate limits)
- Reduce batch size in code (line ~150: `batch_size=25`)

### Issue: "Very slow performance"

**Solutions**:
- Reduce number of papers (<200 recommended for smooth UI)
- Set edge opacity to 0.2 or lower
- Turn off node labels
- Use "circular" layout (faster than "spring")

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🔗 Related Projects

- **[AVALANCHE](https://github.com/HaroldMate1/AVALANCHE)** - Automated literature discovery tool
- **[Connected Papers](https://www.connectedpapers.com/)** - Inspiration for visualization style
- **[Gephi](https://gephi.org/)** - Advanced network visualization
- **[VOSviewer](https://www.vosviewer.com/)** - Bibliometric network visualization
- **[OpenAlex](https://openalex.org/)** - Open citation database

---

## 📧 Contact

- **Author**: Harold Mateo Mojica Urrego
- **Institution**: University of Navarra-TECNUN
- **GitHub**: [@HaroldMate1](https://github.com/HaroldMate1)
- **Issues**: [GitHub Issues](https://github.com/HaroldMate1/GraphAvalanche/issues)

---

## 🙏 Acknowledgments

- **OpenAlex** for providing open citation data
- **Plotly** for interactive visualization capabilities
- **NetworkX** for graph algorithms
- **Streamlit** for the web framework
- **Connected Papers** for visualization inspiration

---

**Made with ❤️ for the research community**

*Transform your literature reviews into interactive visual insights* 🚀
