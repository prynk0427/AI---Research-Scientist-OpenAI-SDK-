import logging
from pathlib import Path


def get_logger(name: str = "ai_research_scientist") -> logging.Logger:
    """Create a file-backed logger without duplicating handlers on Streamlit reruns."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        Path("logs").mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler("logs/app.log", encoding="utf-8")
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        )
        logger.addHandler(handler)

    return logger
