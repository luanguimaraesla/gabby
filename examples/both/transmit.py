import logging
from gabby import Gabby, Topic, Message


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

    topics = [
        Topic('qa', 'i', 'udp'),
        Topic('qb', 'i', 'udp'),
        Topic('wa', 'i', 'tcp'),
        Topic('wb', 'i', 'tcp'),
    ]

    g = Gabby(output_topics=topics, transmission=['tcp'])
    g.send(Message((1,), g.output_topics))
