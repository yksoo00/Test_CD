import logging

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[34m',     # Blue
        'INFO': '\033[32m',      # Green
    }
    RESET = '\033[0m'
    LEVEL_LENGTH = 5

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        levelname = record.levelname
        padded_levelname = levelname.ljust(self.LEVEL_LENGTH)
        record.levelname = f"{color}{padded_levelname}{self.RESET}"
        
        asctime = self.formatTime(record, self.datefmt)
        record.asctime = "{color}{asctime}{self.RESET}"
        
        return super().format(record)