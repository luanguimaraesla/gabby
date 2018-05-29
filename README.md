
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

A simple controller for message queue pipelines using Mosquitto

## Installing

You can install the package through pip

```bash
pip install gabby
```

## Examples

Before run examples, please initialize the Mosquitto server.

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
