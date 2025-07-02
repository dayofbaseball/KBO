from django.core.management.base import BaseCommand
from cal.models import Stadium

class Command(BaseCommand):
    def handle(self):
        stadium_names = [
            '광주',
            '잠실',
            '문학',
            '창원',
            '대전(신)',
            '고척',
            '사직',
            '대구',
            '수원',
            '울산',
            '포항',
        ]

        count = 0
        for name in stadium_names:
            obj, created = Stadium.objects.get_or_create(stadium=name)
            self.stdout.write(f"{'Created' if created else 'Exists'}: {name}")
            count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} stadium(s) processed."))
