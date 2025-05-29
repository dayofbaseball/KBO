from django.shortcuts import render, redirect
from datetime import datetime, timedelta, date
from django.utils.safestring import mark_safe
from django.db.models import Max
import calendar
from .models import *
from .utils import Calendar
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

def calendar_view(request):
    user_team = None
    user_attendance_game_ids = []
    if request.user.is_authenticated:
        user_team = request.user.team
        user_attendance_game_ids = list(request.user.attendance_game.values_list('id', flat=True))
    d = get_date(request.GET.get('day', None))
    cal = Calendar(d.year, d.month, team=user_team)
    cal_data = cal.get_month_data()

    context = {
        'cal_data': cal_data,
        'prev_month': prev_month(d),
        'next_month': next_month(d),
        'user_team': user_team,
        'user_attendance_game_ids': user_attendance_game_ids,
    }
    return render(request, 'calendar.html', context)

def get_date(req_day):
    try:
        if req_day:
            year, month, day = (int(x) for x in req_day.split('-'))
            return date(year, month, day=1)
    except (ValueError, TypeError):
        pass
    return datetime.today().date()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    a = 'day=' + str(prev_month.year) + '-' + str(prev_month.month) + '-' + str(prev_month.day)
    return a

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    a = 'day=' + str(next_month.year) + '-' + str(next_month.month) + '-' + str(next_month.day)
    return a

def lineup(request, game_id):
    game = Game.objects.get(id=game_id)
    lineups = Lineup.objects.filter(game=game).order_by('id')
    lineup = Lineup.objects.filter(game=game).first()
    user_team = request.user.team
    stamina_percent = int(lineup.pitcher.stamina * 100)
    control_percent = int(lineup.pitcher.control * 100)
    max_speed_data = Pitcher.objects.aggregate(max_speed=Max('speed'))
    max_speed = 154
    min_speed = 130

    # 선발투수 2명 위치 파악 (batting_order == 1)
    pitcher_indexes = [i for i, l in enumerate(lineups) if l.batting_order == 1]

    if len(pitcher_indexes) != 2:
        raise ValueError("선발투수가 2명 아닙니다.")

    # 각 팀 라인업 분리
    away_lineup = lineups[pitcher_indexes[0]:pitcher_indexes[0]+10]
    home_lineup = lineups[pitcher_indexes[1]:pitcher_indexes[1]+10]

    # 선호팀 기준으로 나누기
    if user_team == game.team1:
        user_lineup = away_lineup
        opponent_lineup = home_lineup
    else:
        user_lineup = home_lineup
        opponent_lineup = away_lineup

    pitcher = lineup.pitcher

    if pitcher:
        raw_speed = pitcher.speed
        normalized_velocity = max(0, min(100, ((raw_speed - min_speed) / (max_speed - min_speed)) * 100))

    context = {
        'game': game,
        'lineup': lineup,
        'user_lineup': user_lineup,
        'opponent_lineup': opponent_lineup,
        'user_team': user_team,
        'away_team': game.team1,
        'home_team': game.team2,
        'game': game,
        'pitcher': pitcher,
        'stamina_percent': stamina_percent,
        'control_percent': control_percent,
        'normalized_velocity': normalized_velocity,
    }
    return render(request, 'lineup.html', context)

@login_required
def attendance(request, game_id):
    user = request.user
    game = Game.objects.get(id=game_id)

    if user in game.attendance_users.all():
        game.attendance_users.remove(user)
    else:
        game.attendance_users.add(user)

    return redirect('cal:lineup', game_id=game_id)