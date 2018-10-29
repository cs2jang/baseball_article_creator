import globals as g
from lib.classes.event import Event


class Team(object):
    def __init__(self, team_cd):
        self.team_code = team_cd
        self.game_id = g.GAME_ID
        self.tb = 'T' if self.game_id[8:10] == team_cd else 'B'
        self.df_gamecontapp = g.df_gamecontapp
        self.df_today_hitters = g.m.get_df_today_hitters(self.game_id, self.tb)
        g.define_method(self, g.team_method)

    def name(self):
        return g.team_name_dict[self.team_code]

    def continue_win(self):
        win_counter = 0
        df_result = g.m.get_df_season_wls(self.game_id, self.team_code)
        for v in df_result['WLS'].values:
            if v == 'W':
                win_counter += 1
            else:
                break
        return win_counter

    def teamrank_daily(self):
        team_name = self.name() if self.name() != '넥센' else '우리'
        teamrank_daily = g.m.get_df_teamrank_daily(g.GAME_DATE, team_name)
        teamrank = teamrank_daily.iloc[0]
        result = teamrank.to_dict()
        return result

    def get_score(self):
        if self.tb == 'T':
            return self.df_gamecontapp.iloc[-1:]['TSCORE'].values[0]
        else:
            return self.df_gamecontapp.iloc[-1:]['BSCORE'].values[0]

    def first_run(self):
        """
        첫득점
        :return:
        """
        gamecontapp = self.df_gamecontapp[self.df_gamecontapp['TB'] == self.tb].to_dict('records')

        for d in gamecontapp:
            if self.tb == 'B':
                if d['BSCORE'] > 0:
                    s_event = self.df_gamecontapp[self.df_gamecontapp['SERNO'] == d['SERNO']].iloc[0]
                    return Event(s_event)
            else:
                if d['TSCORE'] > 0:
                    s_event = self.df_gamecontapp[self.df_gamecontapp['SERNO'] == d['SERNO']].iloc[0]
                    return Event(s_event)

        return None

    def highest_hit_rbi(self):
        """
        최고안타타점
        :return:
        """

        return self.df_today_hitters.loc[self.df_today_hitters['RBI'].idxmax()]['RBI']

    def highest_hit_rbi_hitters(self):
        """
        최고안타타점선수들
        :return:
        """
        names = self.df_today_hitters[self.df_today_hitters['RBI'] == self.highest_hit_rbi()]['NAME']
        return ', '.join(names)

    def game_ab(self):
        """
        타수
        :return:
        """
        total = self.df_today_hitters.iloc[:, 4:].sum()
        return total['AB']

    def game_rbi(self):
        """
        타점
        :return:
        """
        total = self.df_today_hitters.iloc[:, 4:].sum()
        return total['RBI']

    def game_hr(self):
        """
        홈런수
        :return:
        """
        total = self.df_today_hitters.iloc[:, 4:].sum()
        return total['HR']

    def game_hit(self):
        """
        안타수
        :return:
        """
        total = self.df_today_hitters.iloc[:, 4:].sum()
        return total['HIT']

    def is_draw(self):
        """
        무승부?
        :return:
        """
        return g.IS_DRAW

    def is_win(self):
        """
        승리?
        :return:
        """
        return self.name() == g.WIN_TEAM

    def is_lose(self):
        """
        패배?
        :return:
        """
        return self.name() == g.LOSE_TEAM

    def hr_players_num(self):
        """
        홈런선수명수
        :return:
        """

        return self.df_today_hitters[self.df_today_hitters['HR'] > 0].shape[0]

