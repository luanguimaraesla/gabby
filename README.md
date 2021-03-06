
<a href="https://codeclimate.com/github/luanguimaraesla/gabby/maintainability">
    <img src="https://api.codeclimate.com/v1/badges/dc94cbf3854b542d3862/maintainability" />
</a>
<a href="https://travis-ci.org/luanguimaraesla/gabby">
    <img src="https://travis-ci.org/luanguimaraesla/gabby.svg?branch=master" />
</a>
<a href="https://badge.fury.io/py/gabby">
    <img src="https://badge.fury.io/py/gabby.svg" />
</a>
<a href="https://codecov.io/gh/codecov/example-python">
    <img src="https://codecov.io/gh/luanguimaraesla/gabby/branch/master/graph/badge.svg" />
</a>


# Python Gabby

A simple controller for MQTT and MQTT-SN pipelines using Mosquitto and RSMB

## Installing

You can install the package through pip

```bash
pip install gabby
```

## Examples

Before run examples, please initialize the Mosquitto or RSMB server.

#### Receiving messages

```python
from gabby.gabby import Gabby, Topic
from gabby.controller import Controller


class PrinterGabby(Gabby):
    def transform(self, message):
        print(f'ARRIVED! Data: {message.data}')
        return []


if __name__ == "__main__":
    controller = Controller()

    topic_A = Topic('queue/a', 'i')
    topic_B = Topic('queue/b', 'i')

    printer_gabby = PrinterGabby([topic_A], [topic_B])

    controller.add_gabby(printer_gabby)
    controller.run()
```

#### Transmitting messages

```python
from gabby.gabby import Gabby, Topic
from gabby.message import Message


if __name__ == "__main__":
    topic_A = Topic('queue/a', 'i')
    topic_B = Topic('queue/b', 'i')

    g = Gabby([topic_B], [topic_A])
    data = (1,)
    g.send(Message(data, g.output_topics))

```

#### Using UDP broker

```python
from gabby.gabby import Gabby, Topic
from gabby.controller import Controller


class PrinterGabby(Gabby):
    def transform(self, message):
        print(f'ARRIVED! Data: {message.data}')
        return []


if __name__ == "__main__":
    controller = Controller()

    topic_A = Topic('queue/a', 'i', 'udp')
    topic_B = Topic('queue/b', 'i', 'udp')

    printer_gabby = PrinterGabby([topic_A], [topic_B], transmission='udp')

    controller.add_gabby(printer_gabby)
    controller.run()
```


#### Using both UDP and TCP topics

You can use both TCP and UDP brokers

```python
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

```
