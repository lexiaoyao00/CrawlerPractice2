import logging,traceback

from PyQt5.QtWidgets import QTextEdit

class Logger:
    def __init__(self,name:str = None, level=logging.INFO):
        logger_name = name or __name__
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level)

        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(caller_file)s:%(caller_line)d - %(caller_func)s - %(message)s')

        self.console_handler = None
        self.file_handler = None
        self.qt_handler = None

        self.enable_console = False
        self.enable_file = False
        self.enable_qt = False

    def _get_caller_info(self):
        stack_trace = traceback.extract_stack()
        caller_file, caller_line, caller_func, _ = stack_trace[-3]
        return caller_file, caller_line, caller_func

    def enable_console_output(self, enable=True):
        if enable and not self.console_handler:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.logger.level)
            # console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            # console_handler.setFormatter(console_formatter)
            console_handler.setFormatter(self.formatter)

            self.logger.addHandler(console_handler)
            self.console_handler = console_handler
        elif not enable and self.console_handler:
            self.logger.removeHandler(self.console_handler)
            self.console_handler = None
        self.enable_console = enable

    def enable_file_output(self, log_file, enable=True):
        if enable and not self.file_handler:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(self.logger.level)
            # file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            # file_handler.setFormatter(file_formatter)
            file_handler.setFormatter(self.formatter)

            self.logger.addHandler(file_handler)
            self.file_handler = file_handler
        elif not enable and self.file_handler:
            self.logger.removeHandler(self.file_handler)
            self.file_handler = None
        self.enable_file = enable

    def enable_qt_output(self, text_edit, enable=True):
        if enable and not self.qt_handler:
            qt_handler = QtHandler(text_edit)
            qt_handler.setLevel(self.logger.level)
            qt_formatter = logging.Formatter('%(asctime)s  - %(message)s')
            qt_handler.setFormatter(qt_formatter)
            # qt_handler.setFormatter(self.formatter)

            self.logger.addHandler(qt_handler)
            self.qt_handler = qt_handler
        elif not enable and self.qt_handler:
            self.logger.removeHandler(self.qt_handler)
            self.qt_handler = None
        self.enable_qt = enable

    def debug(self, msg):
        caller_file, caller_line, caller_func = self._get_caller_info()
        self.logger.debug(msg, extra={'caller_file': caller_file, 'caller_line': caller_line, 'caller_func': caller_func})

    def info(self, msg):
        caller_file, caller_line, caller_func = self._get_caller_info()
        self.logger.info(msg, extra={'caller_file': caller_file, 'caller_line': caller_line, 'caller_func': caller_func})

    def warning(self, msg):
        caller_file, caller_line, caller_func = self._get_caller_info()
        self.logger.warning(msg, extra={'caller_file': caller_file, 'caller_line': caller_line, 'caller_func': caller_func})

    def error(self, msg):
        caller_file, caller_line, caller_func = self._get_caller_info()
        self.logger.error(msg, extra={'caller_file': caller_file, 'caller_line': caller_line, 'caller_func': caller_func})

    def critical(self, msg):
        caller_file, caller_line, caller_func = self._get_caller_info()
        self.logger.critical(msg, extra={'caller_file': caller_file, 'caller_line': caller_line, 'caller_func': caller_func})

class QtHandler(logging.Handler):
    def __init__(self, text_edit:QTextEdit):
        super().__init__()
        self.text_edit = text_edit

    def emit(self, record):
        msg = self.format(record)
        self.text_edit.append(msg)



my_logger = Logger("main")
