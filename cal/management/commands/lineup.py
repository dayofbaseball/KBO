import csv
from django.core.management.base import BaseCommand
from cal.models import Lineup, Game, Hitter, Pitcher
from django.conf import settings

class Command(BaseCommand):
    help = 'Import or update lineups from CSV'

    def handle(self, *args, **kwargs):
        csv_file_path = settings.BASE_DIR / 'data' / 'lineups.csv'
        with open(csv_file_path,encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            count = 0
            print(reader.fieldnames)
            for row in reader:
                game_obj = Game.objects.get(pk=str(row['game_id']))
                hitter_obj = Hitter.objects.get(pk=str(row['hitter_id']))
                pitcher_obj = Pitcher.objects.get(pk=str(row['pitcher_id']))
                print(game_obj, hitter_obj, pitcher_obj, int(row['batting_order']))
                obj, created = Lineup.objects.update_or_create(
                    batting_order=int(row['batting_order']),
                    game=game_obj,
                    hitter=hitter_obj,
                    pitcher=pitcher_obj,
                    stadium=row['stadium'],
                    defaults={}
                )
                count += 1
            self.stdout.write(self.style.SUCCESS(f'{count} lineups imported or updated.'))