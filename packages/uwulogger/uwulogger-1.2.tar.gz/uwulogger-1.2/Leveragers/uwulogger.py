import logging
from datetime import datetime
from colorama import init, Fore, Style

# Initialize Colorama
LBL = "\x1b[38;5;27m"
LB = Fore.LIGHTBLACK_EX
LBL = "\x1b[38;5;27m"
BR = "\x1b[38;5;130m"
WR = "\x1b[38;5;214m"
RD = Fore.RED
R = Fore.RESET

class Leveragers:
    def __init__(self):
        self.logger = logging.getLogger('custom_logger')
        self.logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

        file_handler = logging.FileHandler('Leveragers.log', encoding='utf-8')  # Ensure UTF-8 encoding for file
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)




    def log(self, level, msg):
        level = level.upper()
        time = f"{LB}{datetime.now().strftime('%H:%M:%S')}{R}"
        color = {
            'DBG': Fore.LIGHTCYAN_EX,
            'ERR': Fore.LIGHTRED_EX,
            'WARN': WR,
            'RATELIMIT': Fore.YELLOW,
            'INF': LBL,
            'SUCCESS': Fore.GREEN,
            'CRITICAL': BR
        }.get(level, Fore.WHITE)

        tag = f"{color}{level}{Style.RESET_ALL}"

        method = {
            'DBG': self.logger.debug,
            'ERR': self.logger.error,
            'WARN': self.logger.warning,
            'INF': self.logger.info,
            'SUCCESS': self.logger.info,
            'CRITICAL': self.logger.critical
        }.get(level, self.logger.info)


        log_message = f"{time} - {tag} ● {msg}"
        method(log_message)

    def inp(self, prompt):
        ct = datetime.now().strftime('%H:%M:%S')
        TLG = f"{LB}{ct}{R}"

        WS = f"{RD}INP{Style.RESET_ALL} ● {prompt}\n"
        WS += f"{' ' * 8} {RD}└ {Fore.LIGHTWHITE_EX}> {R}"
        
        userinput = input(f"{TLG} {WS}")

        try:
            return int(userinput) 
        except ValueError:
            return userinput

    def dbg(self, msg):
        self.log('DBG', msg)

    def err(self, msg):
        self.log('ERR', msg)

    def warn(self, msg):
        self.log('WARN', msg)

    def ratelimit(self, msg):
        self.log('RATELIMIT', msg)

    def inf(self, msg):
        self.log('INF', msg)

    def success(self, msg):
        self.log('SUCCESS', msg)

    def crit(self, msg):
        self.log('CRITICAL', msg)
