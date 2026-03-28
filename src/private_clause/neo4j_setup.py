from neo4j import GraphDatabase
import logging

logger = logging.getLogger(__name__)

def check_neo4j_connection(user:str, password: str, hostname:str, port:int) -> bool:
    uri = f"bolt://{hostname}:{port}"

    try:
        # The 'with' statement handles closing the driver automatically
        with GraphDatabase.driver(uri, auth=(user, password)) as driver:
            driver.verify_connectivity()
            logger.debug(f"Neo4j connection verified via Python driver at {uri}")
            return True
    except Exception as e:
        logger.error(f"Failed to connect to Neo4j at {uri}: {e}")
        return False