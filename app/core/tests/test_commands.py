"""Add commentMore actions
Test custom Django management commands.
"""
# mock the behavior of the DB
# because we need to simulate the behavior of responses from DB
from unittest.mock import patch

#one of the posible error that we may get when we try to connect to DB and it is not ready
from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
# another posible error code
from django.db.utils import OperationalError
# test class
# we dont need migrations so we use SimpleTestCase 
# it will not create DB set up behind  
from django.test import SimpleTestCase

# mock the behavior
@patch('django.db.connections.__getitem__')
class CommandTests(SimpleTestCase):
    """Test commands."""
                                    #mock passwd as arg
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        # mock returns just True value
        patched_check.return_value = True

        # execute the code inside DB
        # checks if command is set up corectly and when our DB is ready
        call_command('wait_for_db')

        # is mock object (which is pached method inside our command) called
        patched_check.assert_called_once_with(databases=['default'])

    # mocking the time we are waiting for DB to be ready
    # because we dont want to wait in unit test, we mock the wait
    @patch('time.sleep')
                                #look at how arg are aplied for mocking first the last moc, and then the one before it and so on
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # first 2 times it will raise the Psycopg2OpError, next 5 times OperationalError and 8. time it will return True
        # 2 and 5 are just choosen to be simulation numbers you can change that to any number 
        patched_check.side_effect = [Psycopg2OpError] * 2 + [OperationalError] * 5 + [True]

        call_command('wait_for_db')

        # 8 times called as for explanation beforehand, any more it is unnecessary 
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])