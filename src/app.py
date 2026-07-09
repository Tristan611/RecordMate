from core.config import Config
from core.logger import setup_logger
from core.state import AppState


def main():

    config = Config()

    logger = setup_logger(config.log_level)

    state = AppState.STARTING

    logger.info("RecordMate starting...")
    logger.info(f"Environment : {config.app_env}")
    logger.info(f"Location    : {config.location_name}")

    state = AppState.IDLE

    logger.info(f"State        : {state.value}")


if __name__ == "__main__":
    main()
