from django.core.management.base import BaseCommand
from cal.models import Pitcher
from django.conf import settings
import csv

class Command(BaseCommand):
    def handle(self):
        csv_file_path = settings.BASE_DIR / 'data' / 'all_pitcher_stats.csv'
        with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            count_created = 0
            count_updated = 0
            for row in reader:
                obj, created = Pitcher.objects.update_or_create(
                    player_id=row.get('player_id', ''),
                    defaults={
                        'player_name': row.get('player_name', ''),
                        'team_name': row.get('team', ''),
                        'ERA': float(row.get('ERA', 0) or 0),
                        'G': int(row.get('G', 0) or 0),
                        'W': int(row.get('W', 0) or 0),
                        'L': int(row.get('L', 0) or 0),
                        'SV': int(row.get('SV', 0) or 0),
                        'HLD': int(row.get('HLD', 0) or 0),
                        'WPCT': float(row.get('WPCT', 0) or 0),
                        'IP': float(row.get('IP', 0) or 0),
                        'H': int(row.get('H', 0) or 0),
                        'HR': int(row.get('HR', 0) or 0),
                        'BB': int(row.get('BB', 0) or 0),
                        'HBP': int(row.get('HBP', 0) or 0),
                        'SO': int(row.get('SO', 0) or 0),
                        'R': int(row.get('R', 0) or 0),
                        'ER': int(row.get('ER', 0) or 0),
                        'WHIP': float(row.get('WHIP', 0) or 0),
                        'CG': int(row.get('CG', 0) or 0),
                        'SHO': int(row.get('SHO', 0) or 0),
                        'QS': int(row.get('QS', 0) or 0),
                        'BSV': int(row.get('BSV', 0) or 0),
                        'TBF': int(row.get('TBF', 0) or 0),
                        'NP': int(row.get('NP', 0) or 0),
                        'AVG': float(row.get('AVG', 0) or 0),
                        'H_2B': int(row.get('2B', 0) or 0),
                        'H_3B': int(row.get('3B', 0) or 0),
                        'SAC': int(row.get('SAC', 0) or 0),
                        'SF': int(row.get('SF', 0) or 0),
                        'IBB': int(row.get('IBB', 0) or 0),
                        'WP': int(row.get('WP', 0) or 0),
                        'BK': int(row.get('BK', 0) or 0),
                        'speed': float(row.get('speed', 0) or 0),
                        'stamina': float(row.get('stamina', 0) or 0),
                        'control': float(row.get('control', 0) or 0),
                        'fireball': float(row.get('fireball', 0) or 0),
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