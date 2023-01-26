"""
Django commands to wait for the database to be available
"""
import time
# from psycopg2 import OperationalError as Psycopg2Error
from django.core.management.base import BaseCommand
# from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """Entrypoint for command"""

        self.stdout.write("Waiting for Database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except Exception as exp:
                self.stdout.write('Database unavailable waiting 1 second....')
                print(f'Exception : {exp}')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available'))
