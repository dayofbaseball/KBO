import csv
from django.core.management.base import BaseCommand
from cal.models import Stadium, Parking
from django.conf import settings

class Command(BaseCommand):
    def handle(self):
        csv_path = settings.BASE_DIR / 'data' / 'parking.csv'
        if not csv_path.exists():
            self.stdout.write(self.style.ERROR(f"CSV 파일이 존재하지 않습니다: {csv_path}"))
            return
        with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                stadium_name = row['stadium'].strip()
                try:
                    stadium_obj = Stadium.objects.get(stadium=stadium_name)
                except Stadium.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"[스킵] Stadium '{stadium_name}'이 존재하지 않음"))
                    continue
                Parking.objects.update_or_create(
                    stadium=stadium_obj,
                    parking_name=row['parking_name'].strip(),
                    defaults={
                        'adress': row['adress'].strip(),
                        'note': row['note'].strip()
                    }
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"{count}개의 주차 정보가 성공적으로 저장되었습니다."))
