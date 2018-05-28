# Python Gabby

A simple controller for message queue pipelines

### Installing

```bash
pip install gabby
```

### Examples

#### Receiving messages

Before run examples, please initialize the Mosquitto server.


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

    logger_gabby = PrinterGabby([topic_A], [topic_B])

    controller.add_gabby(logger_gabby)
    controller.run()
```

#### Transmitting messages

```python
from gabby.gabby import Gabby, Topic
from gabby.message import Message


if __name__ == "__main__":
    g = Gabby([Topic('queue/b', 'i')], [Topic('queue/a', 'i')])
    data = (1,)
    g.send(Message(data, g.output_topics))

```
