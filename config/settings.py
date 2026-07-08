import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres@localhost:5432/crowdfunding")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

    @property
    def numeric_log_level(self) -> int:
        return getattr(logging, self.LOG_LEVEL, logging.INFO)

settings = Settings()

# Configure global logging
logging.basicConfig(
    level=settings.numeric_log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("crowdfunding_platform")
