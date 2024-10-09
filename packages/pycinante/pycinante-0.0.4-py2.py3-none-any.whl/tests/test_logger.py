from pycinante.log import logger

def test_logger():
    print()
    logger.load_cfg("cfg.json")
    logger.debug("not shown in console")
    logger.info("Hello, {name} !", name="Word")
    logger.critical("Hello, {name} !", "Have a good fun with new logger.", name="Word")

    @logger.catch(ZeroDivisionError, level=logger.ERROR)
    def f():
        return 1 / 0

    f()
