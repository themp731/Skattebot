"""Generate CSV files from processed fantasy football data."""
import os
import logging
from typing import Dict

import pandas as pd


class CSVGenerator:
    def __init__(self, output_dir: str = "."):
        self.output_dir = output_dir
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """Ensure output directory exists."""
        try:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
        except OSError as e:
            logging.error(f"Failed to create output directory: {e}")
            raise

    def save_dataframe(self, df: pd.DataFrame, filename: str):
        """Save DataFrame to CSV file."""
        try:
            output_path = os.path.join(self.output_dir, filename)
            df.to_csv(output_path, index=False)
            logging.info(f"Successfully saved {filename}")
        except Exception as e:
            logging.error(f"Failed to save {filename}: {e}")
            raise

    def append_to_csv(self, df: pd.DataFrame, filename: str):
        """Append DataFrame to existing CSV file or create new one."""
        try:
            output_path = os.path.join(self.output_dir, filename)

            if os.path.exists(output_path):
                df.to_csv(output_path, mode='a', header=False, index=False)
            else:
                df.to_csv(output_path, index=False)

            logging.info(f"Successfully appended to {filename}")
        except Exception as e:
            logging.error(f"Failed to append to {filename}: {e}")
            raise
