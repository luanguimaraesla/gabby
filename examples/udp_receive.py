import logging

from gabby.udp_receiver import UDPReceiver
from gabby.topic import Topic

def setup_logging(level):
    """
    Setup logging level
    """
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=getattr(logging, level.upper())
    )

if __name__ == '__main__':
    setup_logging('debug')

    a = Topic('ab', 'f', 'udp')
    b = UDPReceiver(topics=[a])
    b.run()
