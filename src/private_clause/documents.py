import logging
from pathlib import Path
from llama_index.core import PropertyGraphIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor
from typing import Literal

logger = logging.getLogger(__name__)

def load_from_directory(dir_path: str, user:str, password:str, host:str, port):
    """Loads all PDFs in a directory and builds a Vector + Graph index."""
    
    # 1. Initialize Neo4j Store
    graph_store = Neo4jPropertyGraphStore(
        username=user,
        password=password,
        url=f"bolt://{host}:{port}"
    )

    # 2. Setup the Legal Extractor
    entities = Literal["CONTRACT", "PARTY", "CLAUSE", "OBLIGATION", "DATE"]
    relations = Literal["SIGNED_BY", "CONTAINS", "MODIFIES", "EXPIRES_ON", "GOVERNS"]
    
    kg_extractor = SchemaLLMPathExtractor(
        llm=Settings.llm,
        possible_entities=entities,
        possible_relations=relations,
        strict=True 
    )

    # 3. Load ALL documents from the directory
    # We use recursive=True in case you have subfolders
    logger.info(f"Scanning directory: {dir_path}")
    reader = SimpleDirectoryReader(
        input_dir=dir_path, 
        required_exts=[".pdf"], 
        recursive=True
    )
    
    documents = reader.load_data()
    splitter = SentenceSplitter(
        chunk_size=512, 
        chunk_overlap=50
    )
    nodes = splitter.get_nodes_from_documents(documents)

    logger.info(f"Found {len(documents)} document pages/sections.")

    # 4. Build/Update the Index
    # PropertyGraphIndex is smart: it will append to the existing Neo4j graph
    index = PropertyGraphIndex.from_documents(
        [],
        property_graph_store=graph_store,
        kg_extractors=[kg_extractor],
        show_progress=False,
        use_async=False,          # Disable parallel processing
        embed_nodes=False,        # Don't embed during graph extraction (do it later)
        transformations=[],       # Disable extra automatic transformations
    )

    for i, node in enumerate(nodes):
        logger.debug(f"Processing chunk {i+1}/{len(nodes)}...")
        index.insert_nodes([node])

    logger.info("Directory ingestion complete.")
    return index