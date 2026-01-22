# Contributing to GraphAvalanche

Thank you for your interest in contributing to GraphAvalanche! This document provides guidelines and instructions for contributing.

## 🎯 Ways to Contribute

### 1. Report Bugs
- Use the [GitHub Issues](https://github.com/HaroldMate1/GraphAvalanche/issues) page
- Include: Python version, OS, error message, steps to reproduce
- Provide sample data if possible (anonymized)

### 2. Suggest Features
- Open an issue with `[Feature Request]` in the title
- Describe the use case and expected behavior
- Include mockups or examples if applicable

### 3. Improve Documentation
- Fix typos, clarify instructions
- Add examples or tutorials
- Translate documentation to other languages

### 4. Submit Code
- Bug fixes
- New features
- Performance improvements
- Test coverage

## 🚀 Getting Started

### Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/GraphAvalanche.git
cd GraphAvalanche

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

### Run Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=graphavalanche tests/
```

### Code Style

We use:
- **Black** for formatting: `black .`
- **Flake8** for linting: `flake8 graphavalanche/`
- **MyPy** for type checking: `mypy graphavalanche/`

Before committing, run:
```bash
black .
flake8 graphavalanche/
mypy graphavalanche/
pytest tests/
```

## 📋 Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

- Write clear, concise commit messages
- Follow existing code style
- Add tests for new features
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run tests
pytest tests/

# Test the Streamlit app manually
streamlit run app_v2.py
```

### 4. Submit Pull Request

- Push to your fork
- Open a pull request to `main` branch
- Fill out the PR template
- Wait for review

## 📝 Commit Message Guidelines

Use conventional commits format:

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(network): add hierarchical layout algorithm
fix(export): resolve GraphML encoding issue
docs(readme): update installation instructions
```

## 🏗️ Project Structure

```
GraphAvalanche/
├── app_v2.py                 # Main Streamlit application
├── app.py                    # Legacy version
├── graphavalanche/           # Core modules
│   ├── __init__.py
│   ├── loader.py            # Data loading utilities
│   └── network.py           # Network building logic
├── tests/                    # Test suite
│   └── test_graphavalanche.py
├── examples/                 # Usage examples
│   └── basic_usage.py
├── docs/                     # Documentation
│   └── API.md
├── requirements.txt          # Dependencies
├── README.md                 # Main documentation
├── CONTRIBUTING.md           # This file
└── LICENSE                   # MIT License
```

## 🧪 Testing Guidelines

### Writing Tests

```python
import pytest
from graphavalanche import CitationNetwork, MetadataLoader

def test_load_excel():
    """Test Excel file loading."""
    papers = MetadataLoader.load_excel('test_data.xlsx')
    assert len(papers) > 0
    assert 'Title' in papers[0]

def test_build_network():
    """Test network building."""
    papers = [
        {'id': '1', 'doi': '10.1234/test', 'title': 'Test Paper'},
        {'id': '2', 'doi': '10.1234/test2', 'title': 'Test Paper 2'}
    ]
    network = CitationNetwork(papers)
    graph = network.build_graph()
    assert len(graph.nodes()) == 2
```

### Test Data

- Use anonymized or synthetic data
- Keep test files small (<100 KB)
- Include various edge cases

## 🎨 Feature Development

### Adding a New Layout Algorithm

1. **Add to options** in `app_v2.py`:
```python
layout_algorithm = st.sidebar.selectbox(
    "Layout Algorithm",
    ["spring", "kamada_kawai", "circular", "spectral", "hierarchical"],  # Add here
    index=0
)
```

2. **Implement layout** in `create_network_visualization()`:
```python
elif layout_algo == "hierarchical":
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
```

3. **Add tests**:
```python
def test_hierarchical_layout():
    # Test implementation
    pass
```

4. **Update documentation** in README.md

### Adding Export Formats

1. **Add export function**:
```python
def export_to_gexf(graph: nx.DiGraph, filename: str):
    """Export graph to GEXF format for Gephi."""
    nx.write_gexf(graph, filename)
```

2. **Add UI button** in app_v2.py:
```python
if st.button("📥 Download GEXF"):
    export_to_gexf(G, 'network.gexf')
```

3. **Document** in README usage section

## 🐛 Bug Fix Process

1. **Reproduce the bug**
   - Create a minimal test case
   - Document expected vs actual behavior

2. **Write a failing test**
```python
def test_bug_fix():
    """Test for issue #123."""
    # Arrange
    data = create_test_data()

    # Act
    result = buggy_function(data)

    # Assert
    assert result == expected_value
```

3. **Fix the bug**
   - Make minimal changes
   - Ensure test passes

4. **Verify no regressions**
   - Run full test suite
   - Test manually with real data

## 📖 Documentation Standards

### Code Comments

```python
def fetch_citation_data(papers_df: pd.DataFrame, batch_size: int = 50) -> Tuple[Dict, Dict]:
    """
    Fetch citation relationships from OpenAlex API.

    Args:
        papers_df: DataFrame with paper metadata (must have 'DOI' column)
        batch_size: Number of papers to fetch per API request (default: 50)

    Returns:
        Tuple of (doi_to_references, openalex_id_to_doi) dictionaries

    Raises:
        ValueError: If papers_df lacks required columns
        ConnectionError: If OpenAlex API is unreachable

    Example:
        >>> df = pd.read_excel('papers.xlsx')
        >>> refs, ids = fetch_citation_data(df)
        >>> print(f"Found {len(refs)} citation mappings")
    """
    pass
```

### README Updates

When adding features:
- Update Features section
- Add usage example
- Include in Table of Contents
- Update screenshots if UI changed

## 🔐 Security

### Reporting Security Issues

**Do NOT open public issues for security vulnerabilities.**

Email: [your-email@university.edu] with:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Security Best Practices

- Never commit API keys or credentials
- Validate all user inputs
- Use HTTPS for API calls
- Sanitize file uploads
- Follow least privilege principle

## 📊 Performance Optimization

### Guidelines

- Profile before optimizing: `python -m cProfile app_v2.py`
- Optimize hot paths first
- Batch API requests
- Cache expensive computations
- Use appropriate data structures

### Example: Caching API Calls

```python
@st.cache_data
def fetch_citation_data(papers_df: pd.DataFrame, batch_size: int = 50):
    # Cached for same inputs
    pass
```

## 🌍 Internationalization

We welcome translations! To add a new language:

1. Create `locales/{language_code}.json`:
```json
{
  "app_title": "GraphAvalanche - Visualizador de Red de Citas",
  "upload_button": "Subir Resultados de AVALANCHE",
  "fetch_network": "Obtener Red de Citas"
}
```

2. Load in app:
```python
import json

with open(f'locales/{lang}.json') as f:
    strings = json.load(f)

st.title(strings['app_title'])
```

## 🎓 Code of Conduct

### Our Pledge

We pledge to make participation in GraphAvalanche a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, experience level, nationality, personal appearance, race, religion, or sexual identity.

### Our Standards

**Positive behavior:**
- Using welcoming and inclusive language
- Respecting differing viewpoints
- Accepting constructive criticism
- Focusing on what's best for the community

**Unacceptable behavior:**
- Trolling, insults, or derogatory comments
- Public or private harassment
- Publishing others' private information
- Other unprofessional conduct

### Enforcement

Report violations to [maintainer-email]. All reports will be reviewed and investigated promptly and fairly.

## 📅 Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: New features (backward-compatible)
- **PATCH**: Bug fixes

### Creating a Release

1. **Update version** in `setup.py` and `__init__.py`
2. **Update CHANGELOG.md**
3. **Create release branch**: `git checkout -b release/v1.2.0`
4. **Tag release**: `git tag -a v1.2.0 -m "Release v1.2.0"`
5. **Push tag**: `git push origin v1.2.0`
6. **Create GitHub release** with change notes

## 🙏 Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- GitHub contributors page
- Release notes
- Annual acknowledgments

## 📧 Questions?

- **General questions**: Open a [GitHub Discussion](https://github.com/HaroldMate1/GraphAvalanche/discussions)
- **Bug reports**: [GitHub Issues](https://github.com/HaroldMate1/GraphAvalanche/issues)
- **Feature requests**: [GitHub Issues](https://github.com/HaroldMate1/GraphAvalanche/issues) with `[Feature Request]`
- **Security issues**: Email [maintainer-email]

---

**Thank you for contributing to GraphAvalanche!** 🚀

Every contribution, no matter how small, helps make literature review better for researchers worldwide.
