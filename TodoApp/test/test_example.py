def test_if_true():
    assert 3 == 3

def test_if_false():
    assert not 3 == 4

def test_greater_than():
    assert 3 > 2
    assert 3 < 4

def test_in():
    assert 'a' in 'abc'
    assert 'd'  not in 'abc'

def test_is():
    assert 3 is 3
    assert 3 is not 4

def test_is_instance():
    assert isinstance(3, int)
    assert not isinstance("3", int)

def test_is_none():
    assert None is None
    assert None is not 0
    
def test_is_not_none():
    assert 0 is not None
    assert 0 is 0

def test_list():
    num = [1, 2, 3]
    any_list = [False, 1, "", [], {}, (), None]
    assert num
    assert any_list
    assert all(num)
    assert any(any_list)


# Pytest Fixture
import pytest

@pytest.fixture
def num():
    return [1, 2, 3]

def test_fixture(num):
    assert num
    assert all(num)

# Using Class

class TestExample:
    def test_if_true(self):
        assert 3 == 3

    def test_if_false(self):
        assert not 3 == 4

    def test_greater_than(self):
        assert 3 > 2
        assert 3 < 4

    def test_in(self):
        assert 'a' in 'abc'
        assert 'd'  not in 'abc'

    def test_is(self):
        assert 3 is 3
        assert 3 is not 4

    def test_is_instance(self):
        assert isinstance(3, int)
        assert not isinstance("3", int)

    def test_is_none(self):
        assert None is None
        assert None is not 0

    def test_is_not_none(self):
        assert 0 is not None
        assert 0 is 0

    def test_list(self):
        num = [1, 2, 3]
        any_list = [False, 1, "", [], {}, (), None]
        assert num
        assert any_list
        assert all(num)
        assert any(any_list)

