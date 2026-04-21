import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from scripts.context_refresher import refresh_governance_context

class TestContextRefresher(unittest.TestCase):
    """
    Standard test suite to ensure 100% coverage and integrity.
    """

    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    def test_refresh_success(self, mock_read, mock_exists):
        """Certifies that logging is issued on successful reads."""
        mock_exists.return_value = True
        mock_read.return_value = "Mock Content"
        
        with self.assertLogs(level='INFO') as cm:
            result = refresh_governance_context()
            self.assertTrue(result)
            self.assertTrue(any("Governance verified and aligned (Rule 10)" in record for record in cm.output))

    @patch('pathlib.Path.exists')
    def test_refresh_failure_missing_files(self, mock_exists):
        """Certifies failure detection when governance files are missing."""
        mock_exists.return_value = False
        
        with self.assertLogs(level='ERROR') as cm:
            result = refresh_governance_context()
            self.assertFalse(result)
            self.assertTrue(any("Mandatory governance files missing or moved" in record for record in cm.output))

if __name__ == '__main__':
    unittest.main()
