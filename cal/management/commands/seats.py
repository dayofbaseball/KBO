import csv
from django.core.management.base import BaseCommand
from cal.models import Seat
from django.conf import settings
from cal.models import Stadium

class Command(BaseCommand):
    def handle(self):
        csv_path = settings.BASE_DIR / 'data' / 'seats.csv'
        if not csv_path.exists():
            self.stdout.write(self.style.ERROR(f"CSV 파일이 존재하지 않습니다: {csv_path}"))
            return
        with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                obj, created = Seat.objects.update_or_create(
                    stadium=Stadium.objects.get(stadium=row['stadium']),
                    seat_name=row['seat_name'].strip(),
                    defaults={'note': row['note'].strip()}
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'{count}개의 좌석 정보를 DB에 저장했습니다.'))
