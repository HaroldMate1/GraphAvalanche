"""Data loading and preprocessing utilities."""

import pandas as pd
from typing import List, Dict


class MetadataLoader:
    """Load and process paper metadata from Excel or CSV."""

    @staticmethod
    def load_excel(filepath: str) -> List[Dict]:
        """
        Load papers from Excel file.

        Parameters
        ----------
        filepath : str
            Path to Excel file

        Returns
        -------
        List[Dict]
            List of paper records
        """
        df = pd.read_excel(filepath)
        return df.to_dict(orient="records")

    @staticmethod
    def load_csv(filepath: str) -> List[Dict]:
        """
        Load papers from CSV file.

        Parameters
        ----------
        filepath : str
            Path to CSV file

        Returns
        -------
        List[Dict]
            List of paper records
        """
        df = pd.read_csv(filepath)
        return df.to_dict(orient="records")

    @staticmethod
    def validate_papers(papers: List[Dict]) -> bool:
        """
        Validate that papers have required fields.

        Parameters
        ----------
        papers : List[Dict]
            List of paper records

        Returns
        -------
        bool
            True if all papers have required fields
        """
        required_fields = ["doi", "id"]
        for paper in papers:
            doi = paper.get("doi") or paper.get("DOI")
            paper_id = paper.get("id") or paper.get("ID")
            if not doi or not paper_id:
                return False
        return True

    @staticmethod
    def clean_papers(papers: List[Dict]) -> List[Dict]:
        """
        Clean and standardize paper data.

        Parameters
        ----------
        papers : List[Dict]
            List of paper records

        Returns
        -------
        List[Dict]
            Cleaned paper records
        """
        cleaned = []
        for paper in papers:
            # Normalize field names
            if "DOI" in paper and "doi" not in paper:
                paper["doi"] = paper["DOI"]
            if "ID" in paper and "id" not in paper:
                paper["id"] = paper["ID"]
            if "Title" in paper and "title" not in paper:
                paper["title"] = paper["Title"]
            if "Year" in paper and "year" not in paper:
                paper["year"] = paper["Year"]

            # Clean DOI
            if paper.get("doi"):
                doi = str(paper["doi"]).lower().strip()
                doi = doi.replace("https://doi.org/", "").replace("doi:", "")
                paper["doi"] = doi

            cleaned.append(paper)

        return cleaned
