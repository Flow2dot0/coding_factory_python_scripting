import logging


class Logs:
    """Logs class set logger to None"""
    def __init__(self, ):
        self.logger = None

    def handle_log_cases(self=None, case="set", text="", filename='/logs/fw.log', ):
        """Custom switch for returning the right method from logging lib
        :args: case, text(optional), filename(optional)
        :return: logging method
        """
        if case == 'set':
            # gets or creates a logger
            self.logger = logging.getLogger()
            self.logger.setLevel(logging.DEBUG)

            # create console handler and set level to debug
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

            # create file handler
            file_handler = logging.FileHandler(filename)
            formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

        if case == 'debug':
            self.logger.debug(text)

        if case == 'info':
            self.logger.info(text)

        if case == 'warning':
            self.logger.warning(text)

        if case == 'critical':
            self.logger.critical(text)
