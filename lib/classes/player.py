import globals as g
from lib.sub_classes.hitter_record import HitterRecord
from lib.sub_classes.pitcher_record import PitcherRecord
from lib.sub_classes.sub_team import SubTeam


class Player(object):
    def __init__(self, player_cd, team_code, pos):
        self.player_code = player_cd
        self.team_code = team_code
        self.pos = pos
        self.game_id = g.GAME_ID
        self.s_player_info = g.m.get_df_person_info(self.player_code).iloc[0]

        g.define_method(self, g.player_method)

    def name(self):
        """
        이름
        :return:
        """
        return self.s_player_info['NAME']

    def team(self):
        """
        팀
        :return:
        """

        return SubTeam(self.team_code)

    def vs_team(self):
        """
        상대팀
        :return:
        """
        if self.team_code == g.HOME_ID:
            vs_team_code = g.AWAY_ID
        else:
            vs_team_code = g.HOME_ID
        return SubTeam(vs_team_code)

    def is_hitter(self):
        """
        타자?
        :return:
        """
        if self.pos == 'hitter':
            return True
        else:
            return False

    def is_pitcher(self):
        """
        투수?
        :return:
        """
        if self.pos == 'pitcher':
            return True
        else:
            return False

    def hitter(self):
        """
        타자
        :return:
        """
        if self.is_hitter():
            hitter = HitterRecord(self.player_code)
            return hitter
        else:
            return HitterRecord()

    def pitcher(self):
        if self.is_pitcher():
            pitcher = PitcherRecord(self.player_code)
            return pitcher
        else:
            return PitcherRecord()
