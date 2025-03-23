"""Database connection and management for Neo4j."""

import logging
from typing import Dict, List, Any, Optional, Union
from contextlib import contextmanager

from neo4j import GraphDatabase, Driver, Session, Result
from neo4j.exceptions import ServiceUnavailable, AuthError

import config

logger = logging.getLogger(__name__)

class Neo4jDatabase:
    """Neo4j database connection manager."""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one database connection."""
        if cls._instance is None:
            cls._instance = super(Neo4jDatabase, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the Neo4j database connection."""
        if self._initialized:
            return
            
        self.uri = config.NEO4J_URI
        self.user = config.NEO4J_USER
        self.password = config.NEO4J_PASSWORD
        self.database = config.NEO4J_DATABASE
        self._driver = None
        self._initialized = True
        
    def connect(self) -> Driver:
        """Connect to Neo4j database.
        
        Returns:
            Driver: Neo4j driver instance
        
        Raises:
            ServiceUnavailable: If connection fails
            AuthError: If authentication fails
        """
        try:
            if not self._driver:
                self._driver = GraphDatabase.driver(
                    self.uri, 
                    auth=(self.user, self.password)
                )
                # Test the connection
                with self._driver.session(database=self.database) as session:
                    result = session.run("RETURN 1 AS test")
                    test_value = result.single()["test"]
                    if test_value != 1:
                        raise ServiceUnavailable("Database connection test failed")
                    logger.info(f"Connected to Neo4j at {self.uri}")
            return self._driver
        except (ServiceUnavailable, AuthError) as e:
            logger.error(f"Failed to connect to Neo4j: {str(e)}")
            raise
    
    def close(self):
        """Close the database connection."""
        if self._driver:
            self._driver.close()
            self._driver = None
            logger.info("Closed Neo4j connection")
    
    @contextmanager
    def get_session(self) -> Session:
        """Get a Neo4j session with automatic cleanup.
        
        Yields:
            Session: Neo4j session object
        """
        driver = self.connect()
        session = driver.session(database=self.database)
        try:
            yield session
        finally:
            session.close()
    
    def execute_query(self, query: str, params: Dict = None) -> Result:
        """Execute a Cypher query.
        
        Args:
            query: Cypher query string
            params: Query parameters
            
        Returns:
            Result: Neo4j result object
        """
        with self.get_session() as session:
            return session.run(query, params or {})
    
    def fetch_all(self, query: str, params: Dict = None) -> List[Dict[str, Any]]:
        """Execute a query and fetch all results as a list of dictionaries.
        
        Args:
            query: Cypher query string
            params: Query parameters
            
        Returns:
            List[Dict[str, Any]]: List of result dictionaries
        """
        with self.get_session() as session:
            result = session.run(query, params or {})
            return [record.data() for record in result]
    
    def fetch_one(self, query: str, params: Dict = None) -> Optional[Dict[str, Any]]:
        """Execute a query and fetch a single result.
        
        Args:
            query: Cypher query string
            params: Query parameters
            
        Returns:
            Optional[Dict[str, Any]]: Result dictionary or None
        """
        with self.get_session() as session:
            result = session.run(query, params or {})
            record = result.single()
            return record.data() if record else None
    
    def create_constraints(self):
        """Create necessary constraints in the database."""
        constraints = [
            "CREATE CONSTRAINT rule_id IF NOT EXISTS FOR (r:Rule) REQUIRE r.rule_id IS UNIQUE",
            "CREATE CONSTRAINT data_element_id IF NOT EXISTS FOR (d:DataElement) REQUIRE d.element_id IS UNIQUE",
            "CREATE CONSTRAINT category_name IF NOT EXISTS FOR (c:Category) REQUIRE c.name IS UNIQUE"
        ]
        
        for constraint in constraints:
            try:
                self.execute_query(constraint)
                logger.info(f"Applied constraint: {constraint}")
            except Exception as e:
                logger.error(f"Failed to create constraint: {str(e)}")
                raise

# Initialize the database singleton
db = Neo4jDatabase()

def get_db() -> Neo4jDatabase:
    """Get the database instance.
    
    Returns:
        Neo4jDatabase: Database instance
    """
    return db
