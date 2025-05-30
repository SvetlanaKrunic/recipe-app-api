"""
Django command to wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command to wait for database."""
    
    # when we run our command it will call this method
    def handle(self, *args, **options):
        """Entrypoint for command"""
        # ispis
        self.stdout.write('Waiting for database...')
        # assume that DB is not up, until we know it is
        db_up = False
        while db_up is False:
            try:
                # if we call this and it is not up, we go to exception
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        # this is optional!
        self.stdout.write(self.style.SUCCESS('Database available!'))