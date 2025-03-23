# Business Object Search

A Python-based system for managing business rules in a Neo4j graph database. This tool allows you to catalog, search, and evaluate business rules with complex interdependencies.

## Features

- Store business rules in a Neo4j graph database
- Track rule dependencies and relationships
- Catalog rules by category, obligation level, and other attributes
- Search rules by data elements they affect
- Evaluate rule applicability for specific scenarios
- Import and export rules in various formats
- Web-based rule management interface

## Requirements

- Python 3.8+
- Neo4j 4.4+
- Python packages listed in requirements.txt

## Installation

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: 
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure the database connection in `config.py`

## Usage

See the documentation for detailed usage instructions.

```bash
# Initialize the database schema
python -m business_object_search.cli init-db

# Import rules from a CSV file
python -m business_object_search.cli import --file rules.csv

# Start the web interface
python -m business_object_search.cli serve
```

## License

MIT
