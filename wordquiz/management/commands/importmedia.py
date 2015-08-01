import csv
from django.core.management.base import BaseCommand, CommandError
from wordquiz.models import MediaObject

def save_data(data):
    mo = MediaObject(**data)
    mo.save()

def save_from_file(filename):
    with open(filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            save_data(row)

    return None

class Command(BaseCommand):
    args = '<csvfile>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for csvfile in args:
            self.stdout.write('importing media objects from %s\n' % (csvfile))
            save_from_file(csvfile)
