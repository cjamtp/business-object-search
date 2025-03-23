"""Configuration settings for the application."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Neo4j database settings
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_WORKERS = int(os.getenv("API_WORKERS", "4"))

# Rule schema settings
RULE_CATEGORIES = [
    "data",
    "validation", 
    "calculation", 
    "process", 
    "reporting", 
    "compliance"
]

OBLIGATION_LEVELS = [
    "mandatory", 
    "conditional", 
    "optional"
]

# Debug settings
DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1", "t"]
