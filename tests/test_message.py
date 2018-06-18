import pytest
import struct
from gabby import Message, Topic
from gabby.topic import TopicCollection


class TestMessage:
    def test_should_create_message_with_explicit_fmt(self):
        msg = Message((1,), fmt='i')
        assert isinstance(msg, Message)

    def test_should_not_create_message_without_topic_and_fmt(self):
        with pytest.raises(ValueError):
            Message((1,))

    def test_should_create_message_with_topic(self, topic):
        msg = Message((1,), topics=(topic,))
        assert isinstance(msg, Message)

    def test_str_should_show_data_attribute(self):
        msg = Message((1,), fmt='i')
        assert str(msg) == '(1,)'

    def test_should_encode_message(self):
        data = (1,)
        fmt = 'i'
        msg = Message(data, fmt=fmt)
        encoded_data = struct.pack(fmt, *data)
        assert encoded_data == msg.encoded

    def test_message_class_should_decode_an_encoded_message(self):
        msg = Message((1,), fmt='i')
        new_msg = Message.decode(msg.encoded, fmt='i')
        assert new_msg.data == (1,)

    def test_should_filter_topics_with_the_same_fmt(self):
        tpcs = TopicCollection(
            [Topic(n, f) for n, f in zip(['a', 'b'], ['i', 'f'])]
        )
        msg = Message((1,), fmt='i')
        assert list(msg.filter_topics(tpcs)) == tpcs[0:1]

    def test_message_belongs_to(self, topic):
        msg = Message((1,), topics=[topic])
        assert msg.belongs_to(topic.name)
