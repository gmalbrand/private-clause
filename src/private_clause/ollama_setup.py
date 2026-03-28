import ollama
import requests
import logging

logger = logging.getLogger(__name__)

def ollama_setup(model:str, embeddings:str) -> bool:
    """ Pull model and embeddings if not already here """
    is_model_available = True
    is_embeddings_available = True

    if not _is_model_available(model):
        try:
            logger.debug(f"Pulling model {model}")
            ollama.pull(model)
        except Exception as e:
            logger.error(f"Failed to pull model {model}, exception : {e}")
            is_model_available = False   

    if not _is_model_available(embeddings):
        try:
            logger.debug(f"Pulling embeddings {embeddings}")
            ollama.pull(embeddings)
        except Exception as e:
            is_embeddings_available = False
            logger.error(f"Failed to pull embeddings {embeddings}, exception : {e}")

    return is_embeddings_available and is_model_available

def check_ollama_connection(hostname:str, port:int) -> bool:
    """Checking if ollama service is available"""
    try:
        resp = requests.get(f"http://{hostname}:{port}/api/version")

        if resp.status_code != 200:
            return False
        
        logger.debug(f"Ollama version : {resp.json()["version"]}")
        return True
    except Exception as e:
        logger.error(f"Failed to access Ollama at http://{hostname}:{port}, exception : {e}")
    return False


def _is_model_available(model):
    for m in ollama.list().models:
        if m.model == model:
            logger.debug(f"Model : {model} is available")
            return True
    return False
