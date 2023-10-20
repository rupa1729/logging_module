import os
from datetime import datetime

class LogFile:
    def __init__(self, log_directory: str):
        self.log_directory = log_directory
        self.current_log_file = None
        self.open_log_file()

    def open_log_file(self) -> None:
        current_date = datetime.now().strftime("log_%Y-%m-%d.txt")  # Include "log_" and ".txt"
        file_path = os.path.join(self.log_directory, current_date)
        self.current_log_file = open(file_path, "a")

    def write(self, message: str) -> None:
        if self.check_midnight_rollover():
            self.create_new_file()
        self.current_log_file.write(message + "\n")

    def flush(self) -> None:
        if not self.current_log_file.closed:
            self.current_log_file.flush()

    def create_new_file(self) -> None:
        self.current_log_file.close()
        self.open_log_file()

    def check_midnight_rollover(self) -> bool:
        current_date = datetime.now().strftime("log_%Y-%m-%d.txt")
        return current_date != self.get_current_log_file_name()

    def get_current_log_file_name(self) -> str:
        # Extract the filename from the current log file
        return os.path.basename(self.current_log_file.name)
