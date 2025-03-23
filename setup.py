from setuptools import setup, find_packages

setup(
    name="business-object-search",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "neo4j>=5.14.0",
        "fastapi>=0.109.0",
        "uvicorn>=0.25.0",
        "pydantic>=2.5.2",
        "python-dotenv>=1.0.0",
        "typer>=0.9.0",
        "pandas>=2.1.3",
        "openpyxl>=3.1.2",
        "click>=8.1.7",
        "rich>=13.7.0",
        "jinja2>=3.1.2",
    ],
    entry_points={
        "console_scripts": [
            "business-object-search=business_object_search.cli:app",
        ],
    },
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="Python-based system for managing business rules in a Neo4j graph database",
    keywords="neo4j, business rules, graph database",
    url="https://github.com/cjamtp/business-object-search",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
