import csv
from django.core.management.base import BaseCommand, CommandError
from wordquiz.models import SinhalaWord, WordCategory, MediaObject

def save_data(data):
    wc = WordCategory.objects.get(category=data['category'])
    data['category'] = wc
    w = SinhalaWord(**data)
    w.save()
    mo = MediaObject.objects.filter(short_name=data['english'])
    w.media = mo
    w.save()

def save_from_file(filename):
    with open(filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            save_data(row)

    return None

class Command(BaseCommand):
    args = '<csvfile>'
    help = 'Imports list of sinhala words linking available medi'

    def handle(self, *args, **options):
        for csvfile in args:
            self.stdout.write('importing words from %s\n' % (csvfile))
            save_from_file(csvfile)
