import csv
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from cal.models import Hitter_Daily, Game, Hitter

class Command(BaseCommand):
    def handle(self):
        file_path = settings.BASE_DIR / 'data' / 'hitters_records.csv'
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            total, success, failed = 0, 0, 0
            for row in reader:
                total += 1
                try:
                    game = Game.objects.get(id=int(row['game_id']))
                    player_id = Hitter.objects.get(player_id=row['player_id'])
                except Game.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"❗ Game ID {row['game_id']} 없음 → 건너뜀"))
                    failed += 1
                    continue
                try:
                    Hitter_Daily.objects.create(
                        game_id=game,
                        date=datetime.datetime.strptime(row['date'], '%Y%m%d').date(),
                        player=player_id,
                        team=row['team'],
                        AB=int(row['AB']),
                        R=int(row['R']),
                        H=int(row['H']),
                        RBI=int(row['RBI']),
                        HR=int(row['HR']),
                        BB=int(row['BB']),
                        SO=int(row['SO']),
                        SB=int(row['SB']),
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ 저장 실패: {e}"))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'✅ 완료: {success}건 저장, {failed}건 실패 (총 {total})'))
