from django.core.management.base import BaseCommand
from parser.command import parse_university_schedule_by_degree

class Command(BaseCommand):
    help = 'Parse University Schedule by Degree CSV file and store the data in the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        parse_university_schedule_by_degree(file_path)
        self.stdout.write(self.style.SUCCESS('Successfully parsed CSV file'))