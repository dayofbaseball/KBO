from django.core.management.base import BaseCommand
from cal.models import Hitter
from django.conf import settings
import csv

class Command(BaseCommand):
    def handle(self):
        csv_file_path = settings.BASE_DIR / 'data' / 'all_hitter_stats.csv'
        with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            count_created = 0
            count_updated = 0
            for row in reader:
                obj, created = Hitter.objects.update_or_create(
                    player_id=row['player_id'],
                    defaults={
                        'player_name': row.get('player_name', ''),
                        'team_name': row.get('team', '') or row.get('팀', ''),
                        'AVG': float(row.get('AVG', 0) or 0),
                        'G': int(row.get('G', 0) or 0),
                        'PA': int(row.get('PA', 0) or 0),
                        'AB': int(row.get('AB', 0) or 0),
                        'R': int(row.get('R', 0) or 0),
                        'H': int(row.get('H', 0) or 0),
                        'H_2B': int(row.get('2B', 0) or 0),
                        'H_3B': int(row.get('3B', 0) or 0),
                        'HR': int(row.get('HR', 0) or 0),
                        'TB': int(row.get('TB', 0) or 0),
                        'RBI': int(row.get('RBI', 0) or 0),
                        'SAC': int(row.get('SAC', 0) or 0),
                        'SF': int(row.get('SF', 0) or 0),
                        'BB': int(row.get('BB', 0) or 0),
                        'IBB': int(row.get('IBB', 0) or 0),
                        'HBP': int(row.get('HBP', 0) or 0),
                        'SO': int(row.get('SO', 0) or 0),
                        'GDP': int(row.get('GDP', 0) or 0),
                        'SLG': float(row.get('SLG', 0) or 0),
                        'OBP': float(row.get('OBP', 0) or 0),
                        'OPS': float(row.get('OPS', 0) or 0),
                        'MH': float(row.get('MH', 0) or 0),
                        'RISP': float(row.get('RISP', 0) or 0),
                        'PH_BA': float(row.get('PH-BA', 0) or 0),
                        'SBA': float(row.get('SBA', 0) or 0),
                        'SB': float(row.get('SB', 0) or 0),
                        'CS': float(row.get('CS', 0) or 0),
                        'power': float(row.get('power', 0) or 0),
                        'contact': float(row.get('contact', 0) or 0),
                        'batting_eye': float(row.get('batting_eye', 0) or 0),
                        'speed': float(row.get('speed', 0) or 0),
                        'style': int(row.get('style', 0) or 0),
                    }
                )
                if created:
                    count_created += 1
                else:
                    count_updated += 1
            self.stdout.write(self.style.SUCCESS(
                f'완료: {count_created}명 생성, {count_updated}명 갱신'
            ))