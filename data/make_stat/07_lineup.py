import csv
import time
import datetime
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By

TEAM_CODE = {
    'LT': 'LT',
    'HT': 'HT',
    'LG': 'LG',
    'OB': 'OB',
    'SK': 'SK',
    'WO': 'WO',
    'SS': 'SS',
    'HH': 'HH',
    'KT': 'KT',
    'NC': 'NC',
}

def get_lineup(today, team1_code, team2_code, game_id, driver):
    url = f'https://m.sports.naver.com/game/{today}{team1_code}{team2_code}{game_id}/lineup'
    driver.get(url)
    time.sleep(1.5)
    try:
        lineup_boxes = driver.find_elements(By.CSS_SELECTOR, 'div.Lineup_comp_lineup__361i1 > div > div')
        team1 = []
        team2 = []

        for idx, team_box in enumerate(lineup_boxes[:2]):
            players = team_box.find_elements(By.CSS_SELECTOR, 'ol > li > a')
            player_info = []
            for player in players:
                name_elem = player.find_element(By.CSS_SELECTOR, 'div > strong')
                name = name_elem.text.strip()
                href = player.get_attribute('href')

                player_id = ''
                if href:
                    parsed_url = urlparse(href)
                    query = parse_qs(parsed_url.query)
                    player_id = query.get('playerId', [''])[0]

                player_info.append((name, player_id))

            if idx == 0:
                team1 = player_info
            else:
                team2 = player_info

        return team1, team2
    except Exception as e:
        print(f"라인업 크롤링 실패: {e}")
        return [], []

# ⏰ 오늘 날짜
today = datetime.date.today()

# 📁 lineups.csv에서 마지막 날짜와 최대 game_id 찾기
last_date = None
max_game_id = 0
try:
    with open('../lineups.csv', 'r', encoding='utf-8-sig') as f:
        reader = list(csv.DictReader(f))
        if reader:
            last_row = reader[-1]
            last_date = datetime.datetime.strptime(last_row['date'], '%Y%m%d').date()
            max_game_id = max(int(row['game_id']) for row in reader if row['game_id'].isdigit())
except FileNotFoundError:
    pass
print(f"마지막 저장된 날짜: {last_date}, 마지막 game_id: {max_game_id}")

# 📅 kbo_schedule.csv 불러오기 및 game_id 부여
with open('../kbo_schedule.csv', 'r', encoding='utf-8-sig') as infile:
    reader = list(csv.DictReader(infile))
    game_map = {}
    game_info_map = {}
    game_id_lookup = {}
    game_id_counter = max_game_id + 1  # ← 여기서부터 이어서 game_id 부여
    for row in reader:
        date_str = row['day'].replace('.', '')
        game_date = datetime.datetime.strptime(date_str, '%Y%m%d').date()

        if game_date > today or (last_date and game_date <= last_date):
            continue

        team1 = row['team1']
        team2 = row['team2']
        time_str = row['time']
        stadium = row.get('stadium', '')
        key = (date_str, team1, team2, time_str)
        game_map.setdefault((date_str, team1, team2), []).append(row)
        game_id_lookup[key] = game_id_counter
        game_info_map[key] = {
            'stadium': stadium,
            'game_id': game_id_counter
        }
        game_id_counter += 1

# ✅ 크롬 드라이버 시작
driver = webdriver.Chrome()

# ✅ 결과 저장
with open('../lineups.csv', 'a', newline='', encoding='utf-8-sig') as outfile:
    writer = csv.writer(outfile)
    if last_date is None:
        writer.writerow(['date', 'batting_order', 'game_id', 'hitter_id', 'pitcher_id', 'stadium'])

    for key, games in game_map.items():
        games_sorted = sorted(games, key=lambda x: x['time'])
        double_header_failed = False
        first_game_lineup1 = None
        first_game_lineup2 = None

        for idx, row in enumerate(games_sorted):
            date_str = row['day'].replace('.', '')
            time_str = row['time']
            team1 = row['team1']
            team2 = row['team2']
            team1_code = TEAM_CODE.get(team1, '')
            team2_code = TEAM_CODE.get(team2, '')
            if not team1_code or not team2_code:
                print(f"팀 코드 없음: {team1}, {team2}")
                continue

            game_id = game_id_lookup.get((date_str, team1, team2, time_str))
            stadium = row.get('stadium', '')

            if len(games_sorted) == 1:
                naver_game_id = '02025'
            elif idx == 0:
                naver_game_id = '12025'
            else:
                naver_game_id = '22025' if not double_header_failed else '02025'

            print(f"크롤링: {date_str} {team1} vs {team2} ({time_str}) game_id={naver_game_id}")

            team1_lineup, team2_lineup = get_lineup(date_str, team1_code, team2_code, naver_game_id, driver)

            if len(games_sorted) > 1 and idx == 0:
                if not team1_lineup and not team2_lineup:
                    double_header_failed = True
                else:
                    first_game_lineup1 = team1_lineup
                    first_game_lineup2 = team2_lineup

            if len(games_sorted) > 1 and idx == 1 and not team1_lineup and not team2_lineup and naver_game_id == '22025':
                print("22025 라인업 없음, 02025로 재시도")
                team1_lineup, team2_lineup = get_lineup(date_str, team1_code, team2_code, '02025', driver)

            if len(games_sorted) > 1 and idx == 1:
                if len(team1_lineup) == 9 and first_game_lineup1:
                    team1_lineup.insert(0, first_game_lineup1[0])
                if len(team2_lineup) == 9 and first_game_lineup2:
                    team2_lineup.insert(0, first_game_lineup2[0])

            for i, (player_name, player_id) in enumerate(team1_lineup):
                if i == 0:
                    writer.writerow([date_str, 1, game_id, 1, player_id, stadium])
                else:
                    writer.writerow([date_str, i+1, game_id, player_id, 1, stadium])
            for i, (player_name, player_id) in enumerate(team2_lineup):
                if i == 0:
                    writer.writerow([date_str, 1, game_id, 1, player_id, stadium])
                else:
                    writer.writerow([date_str, i+1, game_id, player_id, 1, stadium])

            time.sleep(1.5)

driver.quit()
print("✅ 오늘까지의 라인업 저장 완료")
