import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand

class TestConsole(unittest.TestCase):
    """Defines unittests for the console.py script."""

    def test_quit_command(self):
        """Test the 'quit' command."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().onecmd("quit")
            self.assertEqual(mock_stdout.getvalue(), "")

    def test_EOF_command(self):
        """Test the 'EOF' command."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().onecmd("EOF")
            self.assertEqual(mock_stdout.getvalue(), "")

    def test_create_command(self):
        """Test the 'create' command output."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            # Assuming 'create' command prints the id of the created instance
            HBNBCommand().onecmd("create BaseModel")
            self.assertRegex(mock_stdout.getvalue().strip(), "^[0-9a-fA-F-]+$")

    def test_show_command_error(self):
        """Test the 'show' command with missing class name and id."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().onecmd("show")
            self.assertIn("class name missing", mock_stdout.getvalue().strip())

    def test_destroy_command_error(self):
        """Test the 'destroy' command with missing class name and id."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().onecmd("destroy")
            self.assertIn("class name missing", mock_stdout.getvalue().strip())

    def test_all_command(self):
        """Test the 'all' command output."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().onecmd("all")
            # Check the output format or content as needed
            self.assertIsInstance(mock_stdout.getvalue(), str)

    def test_update_command_error(self):
        """Test the 'update' command with missing arguments."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            HBNBCommand().onecmd("update")
            self.assertIn("class name missing", mock_stdout.getvalue().strip())

    # Add more tests for other commands and edge cases

if __name__ == "__main__":
    unittest.main()
