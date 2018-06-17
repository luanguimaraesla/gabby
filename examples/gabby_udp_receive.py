import logging
from gabby import Gabby, Topic, Controller


class LoggerGabby(Gabby):
    def transform(self, message):
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
    topic_F = Topic('qb', 'i', 'udp')
    topic_B = Topic('queue/1', 'i', 'tcp')
    topic_C = Topic('queue/a', 'i', 'tcp')
    topic_D = Topic('queue/b', 'i', 'tcp')
    topic_E = Topic('queue/c', 'i', 'tcp')

    logger_gabby = LoggerGabby(
        [topic_A, topic_F, topic_B, topic_C, topic_D, topic_E],
        transmission=['tcp', 'udp']
    )

    controller.add_gabby(logger_gabby)
    controller.run()
