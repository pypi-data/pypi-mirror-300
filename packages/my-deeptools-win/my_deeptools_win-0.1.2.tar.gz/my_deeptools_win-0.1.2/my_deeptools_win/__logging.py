import logging
from logging import CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET

def set_logging_level(level="NOTSET"):

    level = level.upper()
    print(f"set logging level = {level}")
    dt_level = {
        k:v
        for k,v in zip(["CRITICAL","ERROR","WARNING","INFO","DEBUG","NOTSET"],
                      [CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET])
    }
    logging.basicConfig(level=dt_level[level])

if __name__=='__main__':
    set_logging_level()
    logging.info("hello world")
    logging.debug("hello world")
    logging.warning("hello world")
    logging.error("hello world")
    logging.critical("hello world")