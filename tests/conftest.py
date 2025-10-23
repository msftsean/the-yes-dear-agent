import socket
import pytest


def _port_open(host: str, port: int, timeout: float = 0.8) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def pytest_collection_modifyitems(session, config, items):
    """Skip Playwright-based Streamlit tests when the local app isn't running.

    Tests in `week3/test_agent_status.py` require a Streamlit server on port 8503.
    Tests in `week3/test_realtime_updates.py` require a Streamlit server on port 8507.
    If those ports are not open, mark the corresponding tests as skipped with a clear reason.
    """
    for item in items:
        path = str(item.fspath)
        if 'week3/test_agent_status.py' in path:
            if not _port_open('127.0.0.1', 8503):
                item.add_marker(
                    pytest.mark.skip(
                        reason=(
                            'Skipping Playwright Streamlit test: '
                            'localhost:8503 not reachable'
                        )
                    )
                )
        if 'week3/test_realtime_updates.py' in path:
            if not _port_open('127.0.0.1', 8507):
                item.add_marker(
                    pytest.mark.skip(
                        reason=(
                            'Skipping Playwright Streamlit test: '
                            'localhost:8507 not reachable'
                        )
                    )
                )
