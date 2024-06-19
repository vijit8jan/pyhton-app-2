# test_hello.py

from hello import main
import pytest

def test_hello():
    assert callable(main)
    # You can add more specific tests here if needed

if __name__ == "__main__":
    pytest.main()
