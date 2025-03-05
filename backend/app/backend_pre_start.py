import logging
from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from app.core.db import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5
wait_seconds = 1

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)

def init_db(db_engine: Engine) -> None:
    """Function to initialize the database

    Args:
        db_engine (Engine): SQLAlchemy engine

    Raises:
        e: Exception
    """
    try:
        with Session(db_engine) as session:
             # Try to create session to check if DB is awake
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e
    
def main() -> None:
    """Main function to initialize the database
    """
    logger.info("Initializing database")
    init_db(engine)
    logger.info("Database initialized successfully")

if __name__ == "__main__":
    main()