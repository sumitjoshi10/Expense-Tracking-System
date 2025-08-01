import logging

def setup_logging(name, filename= "server.log", level=logging.DEBUG):
    # Create a customer logger
    logger = logging.getLogger(name)
    
    # Configure the Custom Logger
    logger.setLevel(level)
    file_handler = logging.FileHandler(filename)
    formatter = logging.Formatter('[ %(asctime)s ] - %(lineno)d - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger