import globals as g
from lib.classes.player import Player


class Event(object):
    def __init__(self, gamecontapp_series):
        self.df_gamecontapp = g.df_gamecontapp
        self.event = gamecontapp_series
        g.define_method(self, g.event_method)

    def score_diff(self):
        pass

    def hitter_code(self):
        return self.event['HITTER']

    def pitcher_code(self):
        return self.event['PITCHER']

    def player_hitter(self):
        if self.event['TB'] == 'T':
            team_code = g.AWAY_ID
        else:
            team_code = g.HOME_ID
        return Player(self.hitter_code(), team_code, 'hitter')

    def player_pitcher(self):
        if self.event['TB'] == 'T':
            team_code = g.HOME_ID
        else:
            team_code = g.AWAY_ID
        return Player(self.pitcher_code(), team_code, 'pitcher')

    def is_hit(self):
        return self.event['HOW'] in ['H1', 'H2', 'H3', 'HI', 'HB']

    def is_hr(self):
        return self.event['HOW'] == 'HR'

    def rbi(self):
        pass

    def hit_name(self):
        pass

    def prev_score_this_event_attack(self):
        pass

    def prev_score_this_event_defense(self):
        pass

    def prev_score_win(self):
        pass

    def prev_score_lose(self):
        pass

    def start_out_count_to_kor(self):
        pass

    def start_out_count(self):
        pass

    def base_before_str(self):
        pass

    def base_before_runner_count(self):
        pass

    def tb_to_kor(self):
        return self.event['TB']

    def inning_num(self):
        return self.event['INN']

    def end_score_attack(self):
        pass

    def end_score_defense(self):
        pass

    def end_score_win(self):
        pass

    def end_score_lose(self):
        pass

    def how_name(self):
        pass
