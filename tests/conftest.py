import pytest
import gabby


@pytest.fixture
def topic():
    return gabby.Topic('test/a', 'i')
