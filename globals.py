import re
import models
import random
from korean import l10n

m = models.Lab2AIConn()

AWAY_ID = None
HOME_ID = None
AWAY_TEAM = None  # 원정팀
HOME_TEAM = None  # 홈팀
AWAY_SCORE = None  # 원정팀 득점
HOME_SCORE = None  # 홈팀 득점
WIN_TEAM = None  # 승리팀
LOSE_TEAM = None  # 패배팀
WIN_TEAM_SCORE = None  # 승리팀 득점
LOSE_TEAM_SCORE = None  # 패배팀 득점
IS_DRAW = False
GAME_DATE = None
GAME_ID = None
team_name_dict = None
team_method = None
sub_team_method = None
player_method = None
game_method = None
event_method = None
hitter_method = None
pitcher_method = None
df_gamecontapp = None
HIT = ['H1', 'HI', 'HB', 'H2', 'H3', 'HR']
HOW_KOR_DICT = {'BB': '볼넷', 'BN': '번트', 'H1': '안타', 'H2': '2루타', 'H3': '3루타', 'HB': '번트안타',
                'HI': '내야안타', 'HP': '사구', 'HR': '홈런', 'IB': '고의4구', 'KP': '포일',
                'KW': '폭투', 'SF': '희생플라이', 'SH': '희생번트', 'B2': '보크', 'PB': '패스트볼', 'GR': '땅볼',
                'P2': '포일', 'SB': '도루', 'SD': '더블스틸', 'ST': '트리플스틸', 'WP': '폭투', 'W2': '폭투'}

#  HOW_CODE_TO_PITCHER_TOP_RANKING_POINT_CODE
P_TOP_RANK_POINT_DICT = {
    'BB': 'BB',  # 볼넷
    'BN': 'NONE',  # 번트
    'FC': 'NONE',  # 야수선택
    'FE': 'NONE',  # 파울실책
    'FF': 'NONE',  # 파울플라이
    'FL': 'NONE',  # 플라이
    'GR': 'NONE',  # 땅볼
    'GD': 'GD',  # 병살타
    'H1': 'HIT',  # 1루타
    'H2': 'HIT',  # 2루타
    'H3': 'HIT',  # 3루타
    'HB': 'HIT',  # 번트안타
    'HI': 'HIT',  # 내야안타
    'HP': 'HP',  # 사구
    'HR': 'HR',  # 홈런
    'IB': 'NONE',  # 고의4구
    'IN': 'NONE',  # 타격방해
    'IF': 'NONE',  # 인필드플라이
    'IP': 'NONE',  # 규칙위반 ???
    'KB': 'KK',  # 쓰리번트
    'KK': 'KK',  # 삼진
    'KN': 'KK',  # 낫아웃
    'KP': 'KK',  # 낫아웃포일 ???
    'KW': 'KK',  # 낫아웃폭투 ???
    'LL': 'NONE',  # 라인드라이브
    'OB': 'NONE',  # 주루방해
    'SF': 'NONE',  # 희생플라이
    'SH': 'NONE',  # 희생번트(희생타)
    'TP': 'GD',  # 삼중살
    'XX': 'NONE',  # 타구맞음(타자) : 자기 타구에 맞음
    'AO': 'NONE',  # 어필아웃
    'BH': 'NONE',  # 타자의 도움
    'BK': 'BK',  # 보크
    'B2': 'BK',  # (기록된) 보크
    'CS': 'NONE',  # 도루실패
    'ER': 'NONE',  # 실책진루
    'FD': 'NONE',  # 주자의재치
    'FO': 'NONE',  # 포스아웃
    'NS': 'NONE',  # 무관심도루
    'OS': 'NONE',  # 도루실패 진루
    'PB': 'NONE',  # 패스트볼
    'P2': 'NONE',  # (기록된)포일
    'PO': 'NONE',  # 견제 아웃
    'RF': 'NONE',  # 선택수비
    'SB': 'NONE',  # 도루
    'SD': 'NONE',  # 더블스틸
    'ST': 'NONE',  # 트리플스틸
    'TO': 'NONE',  # 태그아웃
    'WP': 'WP',  # 폭투
    'W2': 'WP',  # (기록된) 폭투
    'XT': 'NONE',  # 타구맞음(주자)
    'RB': 'NONE'
}

# PITCHER_POINT_HASH
PITCHER_POINT = {
    'WP': -4,
    'BK': -4,
    'HIT': -4,
    'HR': -8,
    'BB': -4,
    'HP': -4,
    'KK': 1,
    'GD': 3,
    'NONE': 0
}

#  HOW_CODE_TO_HITTER_AND_RUNNER_TOP_RANKING_POINT_CODE
H_R_TOP_RANK_POINT_DICT = {
    'BB': 'BB',  # 볼넷
    'BN': 'OUT',  # 번트
    'FC': 'NONE',  # 야수선택
    'FE': 'NONE',  # 파울실책
    'FF': 'OUT',  # 파울플라이
    'FL': 'OUT',  # 플라이
    'GD': 'GD',  # 병살타
    'GR': 'OUT',  # 땅볼
    'H1': 'HIT',  # 1루타
    'H2': 'H2',  # 2루타
    'H3': 'H3',  # 3루타
    'HB': 'HIT',  # 번트안타
    'HI': 'HIT',  # 내야안타
    'HP': 'HP',  # 사구
    'HR': 'HR',  # 홈런
    'IB': 'IB',  # 고의4구
    'IN': 'NONE',  # 타격방해
    'IF': 'OUT',  # 인필드플라이
    'IP': 'OUT',  # 규칙위반 ???
    'KB': 'KK',  # 쓰리번트
    'KK': 'KK',  # 삼진
    'KN': 'KK',  # 낫아웃
    'KP': 'KK',  # 낫아웃포일
    'KW': 'KK',  # 낫아웃폭투
    'LL': 'OUT',  # 라인드라이브
    'OB': 'NONE',  # 주루방해
    'SF': 'SF',  # 희생플라이
    'SH': 'SH',  # 희생번트(희생타)
    'TP': 'GD',  # 삼중살
    'XX': 'OUT',  # 타구맞음(타자) : 자기 타구에 맞음
    'AO': 'OUT',  # 어필아웃
    'BH': 'NONE',  # 타자의 도움
    'BK': 'NONE',  # 보크
    'B2': 'NONE',  # (기록된) 보크
    'CS': 'CS',  # 도루실패
    'ER': 'NONE',  # 실책진루
    'FD': 'NONE',  # 주자의재치
    'FO': 'OUT',  # 포스아웃
    'NS': 'NONE',  # 무관심도루
    'OS': 'NONE',  # 도루실패 진루
    'PB': 'NONE',  # 패스트볼
    'P2': 'NONE',  # (기록된)포일
    'PO': 'OUT',  # 견제 아웃
    'RF': 'NONE',  # 선택수비
    'SB': 'SB',  # 도루
    'SD': 'SB',  # 더블스틸
    'ST': 'SB',  # 트리플스틸
    'TO': 'OUT',  # 태그아웃
    'WP': 'NONE',  # 폭투
    'W2': 'NONE',  # (기록된) 폭투
    'XT': 'NONE',  # 타구맞음(주자)
    'RB': 'NONE'  # 주루방해
}

# HITTER_AND_RUNNER_POINT
H_R_POINT = {
    'HIT': 2,
    'H2': 4,
    'H3': 6,
    'HR': 10,
    'BB': 2,
    'HP': 2,
    'IB': 2.4,
    'SH': 1.2,
    'SF': 1.6,
    'KK': -1.2,
    'GD': -5,
    'SB': 1.6,
    'CS': -1.2,
    'OUT': -1,
    'NONE': 0
}


def initialize(game_id):
    global AWAY_ID
    global HOME_ID
    global AWAY_TEAM
    global HOME_TEAM
    global WIN_TEAM
    global LOSE_TEAM
    global team_name_dict
    global IS_DRAW
    global AWAY_SCORE
    global HOME_SCORE
    global WIN_TEAM_SCORE
    global LOSE_TEAM_SCORE
    global GAME_DATE
    global GAME_ID
    global team_method
    global sub_team_method
    global player_method
    global game_method
    global event_method
    global hitter_method
    global pitcher_method
    global df_gamecontapp

    team_name_dict = m.get_team_name()
    game_score = m.get_score(game_id)
    df_gamecontapp = m.get_df_gamecontapp(game_id)

    GAME_ID = game_id
    GAME_DATE = game_id[0:8]
    AWAY_SCORE = game_score['tpoint']
    HOME_SCORE = game_score['bpoint']
    team_method = m.get_method('team')
    sub_team_method = m.get_method('sub_team')
    player_method = m.get_method('player')
    game_method = m.get_method('game')
    event_method = m.get_method('event')
    hitter_method = m.get_method('hitter_record')
    pitcher_method = m.get_method('pitcher_record')

    AWAY_ID = game_id[8:10]
    AWAY_TEAM = team_name_dict[AWAY_ID]
    HOME_ID = game_id[10:12]
    HOME_TEAM = team_name_dict[HOME_ID]

    if AWAY_SCORE > HOME_SCORE:
        WIN_TEAM = AWAY_TEAM
        LOSE_TEAM = HOME_TEAM
        WIN_TEAM_SCORE = AWAY_SCORE
        LOSE_TEAM_SCORE = HOME_SCORE
    elif AWAY_SCORE < HOME_SCORE:
        WIN_TEAM = HOME_TEAM
        LOSE_TEAM = AWAY_TEAM
        WIN_TEAM_SCORE = HOME_SCORE
        LOSE_TEAM_SCORE = AWAY_SCORE
    else:
        WIN_TEAM = AWAY_TEAM
        LOSE_TEAM = HOME_TEAM
        WIN_TEAM_SCORE = HOME_SCORE
        LOSE_TEAM_SCORE = AWAY_SCORE
        IS_DRAW = True


def define_method(obj, method_dict):
    for k, v in method_dict.items():
        setattr(obj, k, getattr(obj, v))


def get_random_sentence(text):
    temp_list = [d.strip() for d in text.split('@') if d]  # 공백제거
    if not temp_list:
        temp_list.append('')
    return random.choice(temp_list)


def get_josa(text):
    result = text
    for _, s_str in enumerate(result):
        if s_str == '#':
            index = result.index(s_str)
            l_str = result[index - 1]
            c_str = result[index + 1]
            change_form = "{0:%s}" % c_str
            change_words = l10n.Template(change_form).format(l_str)[1:]
            result = "".join((result[:index], change_words, result[index + 2:]))
    return result


def set_dynamic_variable(var, tab_name):
    df_dynamic = m.get_df_spread_template(tab_name)
    df_dynamic_group = df_dynamic.groupby(['order', 'name', 'rank'])

    for d in df_dynamic_group:
        var_name = d[0][1]  # name key
        var_list = d[1].to_dict('record')  # data value list

        if var_name in var.__dict__ or var_name == '':
            continue

        var_dict = random.choice(var_list)
        if var_dict['use'] == 'F':
            continue

        if eval(var_dict['condition'].format(**var.__dict__)):
            if var_dict['eval'] == 'T':
                setattr(var, var_dict['name'], eval(var_dict['sentence'].format(**var.__dict__)))
            else:
                text = var_dict['sentence'].format(**var.__dict__)
                text = get_josa(text)
                setattr(var, var_dict['name'], text)


def set_dynamic_variable_v2(var, tab_name):
    df_dynamic = m.get_df_spread_template(tab_name)
    df_dynamic_group = df_dynamic.groupby(['order', 'name', 'rank'])

    for d in df_dynamic_group:
        var_name = d[0][1]  # name key
        var_list = d[1].to_dict('record')  # data value list

        if var_name in var.__dict__ or var_name == '':
            continue

        var_dict = random.choice(var_list)
        if var_dict['use'] == 'F':
            continue

        str_condition = get_result_string(var_dict['condition'], var)
        if eval(str_condition):
            str_sentence = get_result_string(var_dict['sentence'], var)
            if var_dict['eval'] == 'T':
                setattr(var, var_dict['name'], eval(str_sentence))
            else:
                text = str_sentence
                text = get_josa(text)
                setattr(var, var_dict['name'], text)


def get_attr(value, str_list):
    if str_list:
        s = str_list.pop(0)
        attr_value = getattr(value, s)
        if type(attr_value) == str or type(attr_value) == int:
            var = attr_value
        else:
            # var_attr = getattr(value, s)
            if callable(attr_value):
                var = attr_value()
            else:
                var = attr_value
        if str_list:
            return get_attr(var, str_list)
        else:
            return var


def get_result_string(string, var):
    result = string
    reg = r"\{(.+?)\}"
    param_list = re.findall(reg, result)

    param_dict = {}
    if param_list:
        for param in param_list:
            p = param.split('.')
            param_dict.update({param: get_attr(var, p)})

    if param_dict:
        for k, v in param_dict.items():
            result = result.replace("{%s}" % k, "%s" % v)

    return result
