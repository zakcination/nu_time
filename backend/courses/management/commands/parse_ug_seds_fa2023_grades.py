from django.core.management.base import BaseCommand
from parser.command import parse_ug_seds_fa2023_grades

class Command(BaseCommand):
    help = 'Parse grades from a CSV file and populate the CourseGetting table'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file containing grade distributions')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        parse_ug_seds_fa2023_grades(file_path=file_path)  # Pass the file_path argument
        self.stdout.write(self.style.SUCCESS('Successfully parsed CSV file and populated the CourseGetting table.'))
    
