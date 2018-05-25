import sys
from src.gabby.gabby import Gabby, Topic
from src.gabby.controller import Controller

class LoggerGabby(Gabby):
    def transform(self, message):
        print("CHEGOU", file=sys.stderr)
        print(f"Data: {message.data}", file=sys.stderr)
        exit(1)
        return []

if __name__ == "__main__":
    controller = Controller()

    topic_A = Topic('A', 'queue/a', 'i')
    topic_B = Topic('B', 'queue/b', 'i')

    logger_gabby = LoggerGabby([topic_A], [topic_B])

    controller.add_gabby(logger_gabby)
    controller.run()
