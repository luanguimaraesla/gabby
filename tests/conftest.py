import pytest
import gabby


@pytest.fixture
def topic():
    return gabby.Topic('a', 'test/a', 'i')
