"""Citation network building and management."""

import networkx as nx
from typing import List, Dict, Tuple
import requests
import time


class CitationNetwork:
    """Build and visualize citation networks from paper metadata."""

    def __init__(self, papers: List[Dict], batch_size: int = 50):
        """
        Initialize citation network.

        Parameters
        ----------
        papers : List[Dict]
            List of paper dictionaries with 'doi', 'id', 'title' fields
        batch_size : int
            Number of papers to fetch per API request
        """
        self.papers = papers
        self.batch_size = batch_size
        self.graph = nx.DiGraph()
        self.doi_to_id = {}
        self.connections = []

    def build_doi_index(self) -> Dict[str, str]:
        """Build mapping of normalized DOIs to paper IDs."""
        for paper in self.papers:
            doi = paper.get("doi") or paper.get("DOI")
            paper_id = paper.get("id") or paper.get("ID")
            if doi and paper_id:
                norm_doi = self._normalize_doi(doi)
                self.doi_to_id[norm_doi] = paper_id
        return self.doi_to_id

    def build_connections(self) -> List[Tuple]:
        """Fetch references and build citation connections."""
        self.build_doi_index()
        self.connections = self._fetch_and_link_citations()
        return self.connections

    def _normalize_doi(self, doi: str) -> str:
        """Normalize DOI string."""
        if not doi:
            return ""
        d = doi.lower().strip()
        d = d.replace("https://doi.org/", "").replace("doi:", "").replace("http://dx.doi.org/", "")
        return d

    def _fetch_and_link_citations(self) -> List[Tuple]:
        """Fetch citations and link papers in dataset."""
        connections = []
        all_dois = list(self.doi_to_id.keys())
        doi_to_references = {}

        # Batch fetch OpenAlex records
        for i in range(0, len(all_dois), self.batch_size):
            batch = all_dois[i : i + self.batch_size]
            filter_str = "|".join([f"https://doi.org/{d}" for d in batch])
            url = f"https://api.openalex.org/works?filter=doi:{filter_str}&per-page={self.batch_size}"

            try:
                r = requests.get(url, timeout=30)
                if r.status_code == 200:
                    results = r.json().get("results", [])
                    for rec in results:
                        rec_doi = rec.get("doi")
                        if rec_doi:
                            norm_doi = self._normalize_doi(rec_doi)
                            doi_to_references[norm_doi] = rec.get("referenced_works", [])
                time.sleep(1)
            except Exception:
                continue

        # Fetch DOIs for all referenced works
        openalex_id_to_doi = {}
        all_refs = set()
        for refs in doi_to_references.values():
            all_refs.update(refs)
        all_refs = list(all_refs)

        for i in range(0, len(all_refs), self.batch_size):
            batch = all_refs[i : i + self.batch_size]
            filter_str = "|".join(batch)
            url = f"https://api.openalex.org/works?filter=openalex_id:{filter_str}&per-page={self.batch_size}"

            try:
                r = requests.get(url, timeout=30)
                if r.status_code == 200:
                    results = r.json().get("results", [])
                    for rec in results:
                        rec_id = rec.get("id")
                        rec_doi = rec.get("doi")
                        if rec_id and rec_doi:
                            openalex_id_to_doi[rec_id] = self._normalize_doi(rec_doi)
                time.sleep(1)
            except Exception:
                continue

        # Build connections
        for src_doi, refs in doi_to_references.items():
            src_id = self.doi_to_id.get(src_doi)
            for ref in refs:
                tgt_doi = openalex_id_to_doi.get(ref)
                if tgt_doi and tgt_doi in self.doi_to_id:
                    tgt_id = self.doi_to_id[tgt_doi]
                    connections.append((src_id, tgt_id))

        return connections

    def build_graph(self) -> nx.DiGraph:
        """Build NetworkX graph from connections."""
        for paper in self.papers:
            paper_id = paper.get("id") or paper.get("ID")
            title = paper.get("title") or paper.get("Title", "")
            year = paper.get("year") or paper.get("Year", "")
            self.graph.add_node(paper_id, title=title, year=year)

        for src, tgt in self.connections:
            self.graph.add_edge(src, tgt)

        return self.graph

    def get_stats(self) -> Dict:
        """Get network statistics."""
        if not self.graph.nodes():
            self.build_graph()

        return {
            "nodes": len(self.graph.nodes()),
            "edges": len(self.graph.edges()),
            "density": nx.density(self.graph),
        }
