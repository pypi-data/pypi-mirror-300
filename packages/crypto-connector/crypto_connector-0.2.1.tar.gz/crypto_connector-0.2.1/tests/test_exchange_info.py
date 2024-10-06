import sys

import pytest

# cannot currently run tests on github runners (because hosted in the US)
pytestmark = pytest.mark.skipif(
    not sys.platform.startswith("win"), reason="tests for windows only"
)


def test_get_server_time(exchanges):
    for _, exc in exchanges.items():
        assert exc.get_server_time() > 1


if __name__ == "__main__":
    pytest.main([__file__])
