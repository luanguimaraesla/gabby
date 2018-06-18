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
    g = Gabby([Topic('queue/b', 'i')], [Topic('queue/a', 'i')])
    g.send(Message((1,), g.output_topics))
