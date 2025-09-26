import logging
import os


def configure_logging(log_directory: str = "logs", log_file_name: str = "excel_logger.log") -> None:
    os.makedirs(log_directory, exist_ok=True)
    log_path = os.path.join(log_directory, log_file_name)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


