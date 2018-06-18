import logging
from gabby import Gabby, Topic, Controller


class LoggerGabby(Gabby):
    def transform(self, client, message):
        logging.debug(f"ARRIVED! Data: {message.data}")


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

    topic_A = Topic('qa', 'i', 'udp')
    topic_B = Topic('qb', 'i', 'udp')
    topic_C = Topic('wa', 'i', 'tcp')
    topic_D = Topic('wb', 'i', 'tcp')

    logger_gabby = LoggerGabby(
        [topic_A, topic_B, topic_C, topic_D],
        transmission=['udp', 'tcp']
    )

    controller.add_gabby(logger_gabby)
    controller.run()
