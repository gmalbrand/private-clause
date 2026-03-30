import argparse
import logging
import asyncio
import nest_asyncio
import sys

from private_clause.utils import init_logging, init_llama_index
from private_clause.ollama_setup import check_ollama_connection, ollama_setup
from private_clause.neo4j_setup import check_neo4j_connection
from private_clause.documents import load_from_directory

logger = logging.getLogger(__name__)
#nest_asyncio.apply()

def get_args():
    parser = argparse.ArgumentParser(prog="private-clause", description="Legal RAG Management")
    
    # Existing Options
    parser.add_argument("--neo4j-host", default="localhost")
    parser.add_argument("--neo4j-port", type=int, default=7687)
    parser.add_argument("--neo4j-user", default="neo4j")
    parser.add_argument("--neo4j-password", default="privacy-clause-2026")



    parser.add_argument("--ollama-host", default="localhost")
    parser.add_argument("--ollama-port", type=int, default=11434)
    parser.add_argument("--embeddings", default="nomic-embed-text:latest")
    parser.add_argument("--model", default="llama3.2:3b")
    parser.add_argument("--data-dir", default="/opt/docs")
    
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable detailed debug logging"
    )
    

    subparsers = parser.add_subparsers(dest="command", required=True, help="Task to perform")

    # Command: init (Check Ollama & Neo4j)
    init_parser = subparsers.add_parser("init", help="Verify Ollama and Neo4j setup")

    # Command: load (Ingest documents)
    load_parser = subparsers.add_parser("load", help="Load PDF into Neo4j")
    
    
   
    return parser.parse_args()



async def async_main():
    args = get_args()
    init_logging(args.debug)

    # Always check ollama setup
    if not check_ollama_connection(args.ollama_host, args.ollama_port):
        logger.error("Ollama is unreachable")
        sys.exit(-1)
    
    if not ollama_setup(args.model, args.embeddings):
        logger.error("Failed to setup Ollama")
        sys.exit(-1)

    # Always check Neo4j setup
    if not check_neo4j_connection(args.neo4j_user, args.neo4j_password, args.neo4j_host, args.neo4j_port):
        logger.error("Neo4j is unreachable")
        sys.exit(-1)

    # If command is init just stop there
    if args.command == "init":
        return

    # Intialize Llama Index
    init_llama_index(args.ollama_host, args.ollama_port, args.model, args.embeddings)

    if args.command == "load":
        try:
            load_from_directory(args.data_dir, args.neo4j_user, args.neo4j_password, args.neo4j_host, args.neo4j_port)
        except Exception as e:
            logger.error(f"Failed to load documents from {args.data_dir} : {e}")



def sync_main():
    args = get_args()
    init_logging(args.debug)

    # Always check ollama setup
    if not check_ollama_connection(args.ollama_host, args.ollama_port):
        logger.error("Ollama is unreachable")
        sys.exit(-1)
    
    if not ollama_setup(args.model, args.embeddings):
        logger.error("Failed to setup Ollama")
        sys.exit(-1)

    # Always check Neo4j setup
    if not check_neo4j_connection(args.neo4j_user, args.neo4j_password, args.neo4j_host, args.neo4j_port):
        logger.error("Neo4j is unreachable")
        sys.exit(-1)

    # If command is init just stop there
    if args.command == "init":
        return

    # Intialize Llama Index
    init_llama_index(args.ollama_host, args.ollama_port, args.model, args.embeddings)

    if args.command == "load":
        try:
            load_from_directory(args.data_dir, args.neo4j_user, args.neo4j_password, args.neo4j_host, args.neo4j_port)
        except Exception as e:
            logger.error(f"Failed to load documents from {args.data_dir} : {e}")


def main():
    sync_main()
    return
    """Entry point defined in pyproject.toml"""
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(async_main())
    except Exception as e:
        print(f"Failed to load documents: {e}")

if __name__ == "__main__":
    main()

