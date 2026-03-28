import argparse
import logging
import sys

from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

def init_logging(debug_mode):
    """Configures logging ONLY for the current package."""
    log_level = logging.DEBUG if debug_mode else logging.INFO
    log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    
    # 1. Get the logger for your specific package
    # 'private_clause' should match your folder name in src/
    logger = logging.getLogger("private_clause") 
    logger.setLevel(log_level)

    # 2. Prevent logs from being passed up to the Root Logger
    # This is the "magic" line that stops Ollama logs from showing up
    logger.propagate = False 

    # 3. Create and add your handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    
    # Avoid adding multiple handlers if init_logging is called twice
    if not logger.handlers:
        logger.addHandler(console_handler)


def init_llama_index(host:str, port:int, model:str, embeddings:str):
    ollama_url = f"http://{host}:{port}"

    Settings.llm = Ollama(
        model=model,
        base_url=ollama_url,
        request_timeout=600.0,
        context_window=2048, 
        additional_kwargs={"num_ctx": 2048, "num_thread": 2}
    )

    Settings.embed_model = OllamaEmbedding(
        model_name=embeddings,
        base_url=ollama_url
    )
