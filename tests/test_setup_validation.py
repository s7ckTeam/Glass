import pytest
import sys
import os
from pathlib import Path


class TestSetupValidation:
    """Validation tests to ensure the testing infrastructure is properly configured."""
    
    def test_python_version(self):
        """Verify Python version meets requirements."""
        assert sys.version_info >= (3, 7, 3), "Python 3.7.3 or higher is required"
    
    def test_project_imports(self):
        """Verify main project modules can be imported."""
        try:
            import config
            import lib
            import mod
        except ImportError as e:
            pytest.fail(f"Failed to import project modules: {e}")
    
    def test_fixtures_available(self, temp_dir, mock_config, mock_response):
        """Verify pytest fixtures are working."""
        assert isinstance(temp_dir, Path)
        assert temp_dir.exists()
        assert hasattr(mock_config, 'API_KEY')
        assert mock_response.status_code == 200
    
    def test_coverage_configured(self):
        """Verify coverage is properly configured."""
        import coverage
        assert coverage.__version__, "Coverage package should be available"
    
    def test_pytest_markers(self, pytestconfig):
        """Verify custom markers are registered."""
        markers = pytestconfig.getini('markers')
        marker_names = [m.split(':')[0].strip() for m in markers]
        assert 'unit' in marker_names
        assert 'integration' in marker_names
        assert 'slow' in marker_names
    
    @pytest.mark.unit
    def test_unit_marker(self):
        """Test that unit marker works."""
        assert True
    
    @pytest.mark.integration
    def test_integration_marker(self):
        """Test that integration marker works."""
        assert True
    
    @pytest.mark.slow
    def test_slow_marker(self):
        """Test that slow marker works."""
        assert True
    
    def test_test_directory_structure(self):
        """Verify test directory structure is correct."""
        test_root = Path(__file__).parent
        assert (test_root / '__init__.py').exists()
        assert (test_root / 'conftest.py').exists()
        assert (test_root / 'unit' / '__init__.py').exists()
        assert (test_root / 'integration' / '__init__.py').exists()
    
    def test_project_structure(self):
        """Verify main project structure."""
        project_root = Path(__file__).parent.parent
        assert (project_root / 'Glass.py').exists()
        assert (project_root / 'config').is_dir()
        assert (project_root / 'lib').is_dir()
        assert (project_root / 'mod').is_dir()
    
    def test_mock_fixtures(self, mock_file_system, sample_data, mock_api_client):
        """Test that mock fixtures provide expected data."""
        assert (mock_file_system / 'config' / 'config.json').exists()
        assert 'users' in sample_data
        assert len(sample_data['users']) == 2
        assert hasattr(mock_api_client, 'search')
        assert mock_api_client.is_authenticated is True
    
    def test_logging_fixture(self, capture_logs):
        """Test the logging capture fixture."""
        import logging
        
        # Set logging level to ensure INFO messages are captured
        logging.getLogger().setLevel(logging.INFO)
        
        with capture_logs as logs:
            logging.info("Test info message")
            logging.error("Test error message")
        
        messages = logs.get_messages()
        assert len(messages) >= 1  # At least error message should be captured
        assert "Test error message" in messages


def test_basic_assertion():
    """A simple test to ensure pytest is working."""
    assert 1 + 1 == 2
    assert "Glass" in "Glass Security Tool"
    assert True is not False


@pytest.mark.parametrize("input_val,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_parametrized(input_val, expected):
    """Test parametrized tests work correctly."""
    assert input_val ** 2 == expected