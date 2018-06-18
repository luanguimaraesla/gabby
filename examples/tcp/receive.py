import logging
from gabby import Gabby, Topic, Controller


class LoggerGabby(Gabby):
    def transform(self, message):
        logging.debug(f"ARRIVED! Data: {message.data}")
        return []


def setup_logging(level):
    """
    Setup logging level
    """
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=getattr(logging, level.upper())
    )


if __name__ == "__main__":
    setup_logging('debug')
    controller = Controller()

    topic_A = Topic('queue/a', 'i')
    topic_B = Topic('queue/b', 'i')

    logger_gabby = LoggerGabby([topic_A], [topic_B])

    controller.add_gabby(logger_gabby)
    controller.run()
