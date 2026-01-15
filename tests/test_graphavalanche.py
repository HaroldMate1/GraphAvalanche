"""Unit tests for GRAPHAVALANCHE."""

import pytest
from graphavalanche.loader import MetadataLoader
from graphavalanche.network import CitationNetwork


class TestMetadataLoader:
    """Test data loading functionality."""

    def test_validate_papers_valid(self):
        """Test validation of valid paper data."""
        papers = [
            {"id": 1, "doi": "10.1234/test.1", "title": "Test Paper 1"},
            {"id": 2, "doi": "10.1234/test.2", "title": "Test Paper 2"},
        ]
        assert MetadataLoader.validate_papers(papers) is True

    def test_validate_papers_missing_doi(self):
        """Test validation fails with missing DOI."""
        papers = [{"id": 1, "title": "Test Paper"}]
        assert MetadataLoader.validate_papers(papers) is False

    def test_clean_papers(self):
        """Test paper cleaning."""
        papers = [
            {"ID": 1, "DOI": "10.1234/TEST.1", "Title": "Test Paper 1"},
        ]
        cleaned = MetadataLoader.clean_papers(papers)
        assert "id" in cleaned[0]
        assert "doi" in cleaned[0]
        assert "title" in cleaned[0]
        assert cleaned[0]["doi"] == "10.1234/test.1"


class TestCitationNetwork:
    """Test citation network functionality."""

    def test_normalize_doi(self):
        """Test DOI normalization."""
        network = CitationNetwork([])
        test_cases = [
            ("10.1234/test", "10.1234/test"),
            ("https://doi.org/10.1234/test", "10.1234/test"),
            ("DOI:10.1234/TEST", "10.1234/test"),
            ("", ""),
        ]
        for input_doi, expected in test_cases:
            assert network._normalize_doi(input_doi) == expected

    def test_build_doi_index(self):
        """Test DOI index building."""
        papers = [
            {"id": 1, "doi": "10.1234/test.1", "title": "Test Paper 1"},
            {"id": 2, "DOI": "10.1234/test.2", "Title": "Test Paper 2"},
        ]
        network = CitationNetwork(papers)
        doi_index = network.build_doi_index()
        assert "10.1234/test.1" in doi_index
        assert "10.1234/test.2" in doi_index
