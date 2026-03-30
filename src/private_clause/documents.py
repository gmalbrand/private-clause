import logging
import json
import ollama
from llama_index.core import SimpleDirectoryReader
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.core.graph_stores.types import EntityNode, Relation

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_from_directory(dir_path: str, user:str, password:str, host:str, port:int):
    # 1. Connect to Neo4j
    graph_store = Neo4jPropertyGraphStore(
        username=user, 
        password=password, 
        url=f"bolt://{host}:{port}"
    )
    
    # 2. Load Docs
    reader = SimpleDirectoryReader(input_dir=dir_path, required_exts=[".pdf"])
    documents = reader.load_data()

    # 3. Define the Prompt (We handle the 'thinking' manually)
    prompt_template = """Extract legal entities and relationships from the text below.
    Entities: CONTRACT, PARTY, CLAUSE, OBLIGATION, DATE
    Relationships: SIGNED_BY, CONTAINS, MODIFIES, EXPIRES_ON, GOVERNS
    
    Output ONLY valid JSON. No conversational text.
    Format:
    {{
      "nodes": [ {{"id": "EntityName", "label": "ENTITY_TYPE"}}, ... ], 
      "rels": [ {{"from": "EntityName", "to": "EntityName", "type": "REL_TYPE"}}, ... ] 
    }}
    
    Text: {text}"""

    logger.info(f"Starting manual extraction for {len(documents)} pages...")

    for i, doc in enumerate(documents):
        logger.info(f"--- Page {i+1}/{len(documents)} ---")
        try:
            # Talk to Ollama DIRECTLY. No LlamaIndex async drama.
            # We limit text to 3000 chars to avoid overwhelming the 3B model
            response = ollama.chat(model='llama3.2:3b', messages=[
                {'role': 'user', 'content': prompt_template.format(text=doc.text[:3000])}
            ])
            
            content = response['message']['content']
            
            # Basic cleanup in case the LLM added markdown triple backticks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            data = json.loads(content.strip())
            
            # 4. Map to Neo4j Objects
            nodes = []
            for n in data.get('nodes', []):
                nodes.append(EntityNode(label=n['label'], name=n['id']))
            
            rels = []
            for r in data.get('rels', []):
                rels.append(Relation(label=r['type'], source_id=r['from'], target_id=r['to']))

            # 5. Push to Neo4j
            if nodes: 
                graph_store.upsert_nodes(nodes)
            if rels: 
                graph_store.upsert_relations(rels)
            
            logger.info(f"Success: Added {len(nodes)} nodes and {len(rels)} relationships.")

        except Exception as e:
            logger.error(f"Page {i+1} failed: {e}")
            # The loop continues to the next page!
            continue

    logger.info("Extraction complete. Check Neo4j Browser.")
    return True