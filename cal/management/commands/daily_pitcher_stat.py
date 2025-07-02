import csv
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from cal.models import Pitcher_Daily, Game, Pitcher

class Command(BaseCommand):
    def handle(self):
        file_path = settings.BASE_DIR / 'data' / 'pitchers_records.csv'
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            total, success, failed = 0, 0, 0
            for row in reader:
                total += 1
                try:
                    game = Game.objects.get(id=int(row['game_id']))
                    player_id = Pitcher.objects.get(player_id=row['player_id'])
                except Game.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"❗ Game ID {row['game_id']} 없음 → 건너뜀"))
                    failed += 1
                    continue
                try:
                    Pitcher_Daily.objects.create(
                        game_id=game,
                        date=datetime.datetime.strptime(row['date'], '%Y%m%d').date(),
                        player=player_id,
                        team=row['team'],
                        IP=float(row['IP']),
                        H=int(row['H']),
                        R=int(row['R']),
                        ER=int(row['ER']),
                        BB=int(row['BB']),
                        SO=int(row['SO']),
                        HR=int(row['HR']),
                        BF=int(row['BF']),
                        AB=int(row['AB']),
                        NP=int(row['NP']),
                    )
                    success += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ 저장 실패: {e}"))
                    failed += 1

        self.stdout.write(self.style.SUCCESS(f'✅ 완료: {success}건 저장, {failed}건 실패 (총 {total})'))
