import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import MagicMock
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def mock_config():
    """Mock configuration object."""
    config = MagicMock()
    config.API_KEY = "test_api_key"
    config.OUTPUT_DIR = "/tmp/test_output"
    config.LOG_LEVEL = "INFO"
    config.TIMEOUT = 30
    config.MAX_RETRIES = 3
    return config


@pytest.fixture
def mock_response():
    """Mock HTTP response object."""
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {"status": "success", "data": []}
    response.text = '{"status": "success", "data": []}'
    response.headers = {"Content-Type": "application/json"}
    return response


@pytest.fixture
def sample_data():
    """Provide sample data for testing."""
    return {
        "users": [
            {"id": 1, "name": "Test User 1", "email": "test1@example.com"},
            {"id": 2, "name": "Test User 2", "email": "test2@example.com"},
        ],
        "servers": [
            {"ip": "192.168.1.1", "port": 80, "service": "http"},
            {"ip": "192.168.1.2", "port": 443, "service": "https"},
        ],
        "domains": [
            {"domain": "example.com", "ips": ["192.168.1.1"]},
            {"domain": "test.com", "ips": ["192.168.1.2", "192.168.1.3"]},
        ],
    }


@pytest.fixture
def mock_file_system(temp_dir):
    """Create a mock file system structure."""
    structure = {
        "config": ["config.json", "rules.yaml"],
        "logs": ["app.log", "error.log"],
        "data": ["input.csv", "output.json"],
    }
    
    for directory, files in structure.items():
        dir_path = temp_dir / directory
        dir_path.mkdir(exist_ok=True)
        for file_name in files:
            file_path = dir_path / file_name
            file_path.write_text(f"Mock content for {file_name}")
    
    return temp_dir


@pytest.fixture
def mock_api_client():
    """Mock API client for external service testing."""
    client = MagicMock()
    client.search.return_value = {"results": [], "total": 0}
    client.get_info.return_value = {"status": "ok", "data": {}}
    client.is_authenticated = True
    return client


@pytest.fixture
def capture_logs():
    """Capture log messages during tests."""
    import logging
    
    class LogCapture:
        def __init__(self):
            self.records = []
            self.handler = logging.Handler()
            self.handler.emit = lambda record: self.records.append(record)
        
        def __enter__(self):
            logging.root.addHandler(self.handler)
            return self
        
        def __exit__(self, *args):
            logging.root.removeHandler(self.handler)
        
        def get_messages(self, level=None):
            if level:
                return [r.getMessage() for r in self.records if r.levelname == level]
            return [r.getMessage() for r in self.records]
    
    return LogCapture()


@pytest.fixture
def mock_color_output(monkeypatch):
    """Mock colorama for testing colored output."""
    from unittest.mock import Mock
    
    mock_colorama = Mock()
    mock_colorama.Fore = Mock()
    mock_colorama.Back = Mock()
    mock_colorama.Style = Mock()
    
    for color in ['RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE', 'BLACK']:
        setattr(mock_colorama.Fore, color, '')
        setattr(mock_colorama.Back, color, '')
    
    mock_colorama.Style.RESET_ALL = ''
    mock_colorama.Style.BRIGHT = ''
    mock_colorama.Style.DIM = ''
    
    monkeypatch.setattr('colorama.Fore', mock_colorama.Fore)
    monkeypatch.setattr('colorama.Back', mock_colorama.Back)
    monkeypatch.setattr('colorama.Style', mock_colorama.Style)
    
    return mock_colorama


@pytest.fixture
def mock_proxy_settings():
    """Mock proxy configuration."""
    return {
        "http": "http://proxy.example.com:8080",
        "https": "https://proxy.example.com:8080",
        "no_proxy": "localhost,127.0.0.1",
    }


@pytest.fixture(autouse=True)
def reset_singleton_instances():
    """Reset any singleton instances between tests."""
    yield