import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Configures and returns a standard logger for microservices.
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured to prevent duplicate logs
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        )
        
        # Stream to stdout so Docker picks it up
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger
