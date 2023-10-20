from log_file import LogFile

class ILog:
    def write(self, message: str) -> None:
        pass

    def stop(self, wait: bool = False) -> None:
        pass

class LogComponent(ILog):
    def __init__(self, log_directory: str):
        self.log_file = LogFile(log_directory)

    def write(self, message: str) -> None:
        self.log_file.write(message)

    def stop(self, wait: bool = False) -> None:
        if wait:
            self.log_file.flush()
        self.log_file.create_new_file()
        self.log_file.current_log_file.close()
