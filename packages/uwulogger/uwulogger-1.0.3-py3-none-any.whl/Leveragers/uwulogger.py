import logging
from datetime import datetime
from colorama import init, Fore, Style

init()

class Leveragers:
    def __init__(self):
        self.logger = logging.getLogger('custom_logger')
        self.logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(console_handler)

        file_handler = logging.FileHandler('Leveragers.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)

        self.LB = Fore.LIGHTBLACK_EX
        self.LBL = "\x1b[38;5;27m"  
        self.RD = Fore.RED
        self.R = Fore.RESET

    def log(self, level, msg):
        level = level.upper()
        time = f"{self.LB}{datetime.now().strftime('%H:%M:%S')}{self.R}"
        color = {
            'DEBUG': Fore.LIGHTCYAN_EX,
            'ERROR': Fore.LIGHTRED_EX,
            'WARNING': Fore.LIGHTYELLOW_EX,
            'INFO': self.LBL,
            'SUCCESS': Fore.LIGHTGREEN_EX,
            'CRITICAL': Fore.LIGHTMAGENTA_EX
        }.get(level, Fore.WHITE)
        tag = f"{color}{level}{Style.RESET_ALL}"

        method = {
            'DEBUG': self.logger.debug,
            'ERROR': self.logger.error,
            'WARNING': self.logger.warning,
            'INFO': self.logger.info,
            'SUCCESS': self.logger.info,
            'CRITICAL': self.logger.critical
        }.get(level, self.logger.info)

        log_message = f"{time} - {tag} ● {msg}"
        method(log_message)


    def inp(self, prompt):
        ct = datetime.now().strftime('%H:%M:%S')
        TLG = f"{self.LB}{ct}{self.R}"

        WS = f"{self.RD}INP{Style.RESET_ALL} ● {prompt}\n"
        WS += f"{' ' * 8} {self.RD}└ {Fore.LIGHTWHITE_EX}> {self.R}"
        
        userinput = input(f"{TLG} {WS}")

        try:
            return int(userinput) 
        except ValueError:
            return userinput


    def debug(self, msg):
        self.log('DEBUG', msg)

    def error(self, msg):
        self.log('ERROR', msg)

    def warning(self, msg):
        self.log('WARNING', msg)

    def info(self, msg):
        self.log('INFO', msg)

    def success(self, msg):
        self.log('SUCCESS', msg)

    def critical(self, msg):
        self.log('CRITICAL', msg)
