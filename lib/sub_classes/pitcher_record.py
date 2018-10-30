import globals as g


class PitcherRecord(object):
    def __init__(self, pitcher_code=None):
        self.pitcher_code = str(pitcher_code)
        self.game_id = g.GAME_ID
        self.df_today_record = None
        self.df_season_record = None
        self.df_total_record = None

        if self.pitcher_code:
            self.set_hitter_record()
        g.define_method(self, g.pitcher_method)

    def set_hitter_record(self):
        # self.df_total_record = g.m.get_df_pitcher(self.game_id, self.pitcher_code)
        # self.df_today_record = self.df_total_record[self.df_total_record['GDAY'] == self.game_id[0:8]]
        self.df_today_record = g.df_game_pitchers[g.df_game_pitchers['PCODE'] == self.pitcher_code]
        self.df_season_record = g.m.get_df_pitcher_total(self.game_id, self.pitcher_code)
        # self.df_season_record = self.df_total_record[self.df_total_record['GYEAR'] == self.game_id[0:4]]

    def name(self):
        if self.pitcher_code:
            return self.df_today_record.iloc[0]['NAME']
        else:
            return False

    def is_win(self):
        """
        승리투수?
        :return:
        """
        if self.pitcher_code:
            if self.df_today_record.iloc[0]['WLS'] == 'W':
                return True
            return False
        else:
            return False

    def is_lose(self):
        """
        패전투수?
        :return:
        """
        if self.pitcher_code:
            if self.df_today_record.iloc[0]['WLS'] == 'L':
                return True
            return False
        else:
            return False

    def is_save(self):
        if self.pitcher_code:
            if self.df_today_record.iloc[0]['WLS'] == 'S':
                return True
            return False
        else:
            return False

    def is_first_pitcher(self):
        if self.pitcher_code:
            if self.df_today_record.iloc[0]['POS'] == '11':
                return True
            return False
        else:
            return False

    def is_perfect_game(self):
        if self.pitcher_code:
            if self.is_sho_win() and (self.hit() + self.r() + self.bb()) == 0:
                return True
            return False
        else:
            return False

    def is_no_hit_no_run(self):
        """
        노히트노런?
        :return:
        """
        if self.pitcher_code:
            if self.is_sho_win() and self.hit() == 0 and self.r() == 0:
                return True
            return False
        else:
            return False

    def is_sho(self):
        """
        완봉?
        :return:
        """
        if self.pitcher_code:
            if self.df_today_record.iloc[0]['SHO'] > 0:
                return True
            return False
        else:
            return False

    def is_sho_win(self):
        """
        완봉승?
        :return:
        """
        if self.pitcher_code:
            if self.is_sho() and self.is_win():
                return True
            return False
        else:
            return False

    def is_cg(self):
        """
        완투?
        :return:
        """
        if self.pitcher_code:
            if self.df_today_record.iloc[0]['CG'] > 0:
                return True
            return False
        else:
            return False

    def is_cg_win(self):
        """
        완투승?
        :return:
        """
        if self.pitcher_code:
            if self.is_cg() and self.is_win():
                return True
            return False
        else:
            return False

    def is_cg_lose(self):
        """
        완투패?
        :return:
        """
        if self.pitcher_code:
            if self.is_cg() and self.is_lose():
                return True
            return False
        else:
            return False

    def is_qs_plus(self):
        """
        QS_PLUS?
        :return:
        """
        if self.pitcher_code:
            if self.inn2() >= 7 and self.er() <= 3:
                return True
            return False
        else:
            return False

    def is_qs(self):
        """
        QS?
        :return:
        """
        if self.pitcher_code:
            if self.inn2() >= 6 and self.er() <= 3:
                return True
            return False
        else:
            return False

    def hold(self):
        if self.pitcher_code:
            return self.df_today_record.iloc[0]['HOLD']
        else:
            return False

    def er(self):
        """
        자책점
        :return:
        """
        if self.pitcher_code:
            return self.df_today_record.iloc[0]['ER']
        else:
            return False

    def r(self):
        """
        실점
        :return:
        """
        if self.pitcher_code:
            return self.df_today_record.iloc[0]['R']
        else:
            return False

    def inn2(self):
        """
        이닝수
        :return:
        """
        if self.pitcher_code:
            return round(int(self.df_today_record.iloc[0]['INN2']) / 3, 2)
        else:
            return False

    def bb(self):
        """
        볼넷수
        :return:
        """
        if self.pitcher_code:
            return self.df_today_record.iloc[0]['BB']
        else:
            return False

    def kk(self):
        """
        탈삼진수
        :return:
        """
        if self.pitcher_code:
            return self.df_today_record.iloc[0]['KK']
        else:
            return False

    def hit(self):
        """
        피안타수
        :return:
        """
        if self.pitcher_code:
            return self.df_today_record.iloc[0]['HIT']
        else:
            return False

    def game_num(self):
        """
        경기수
        :return:
        """
        if self.pitcher_code:
            return self.df_season_record.shape[0]
        else:
            return False

    def era(self):
        """
        평균자책점
        :return:
        """
        if self.pitcher_code:
            if self.inn2() > 0:
                return round(self.er() * 9 / self.inn2(), 3)
            else:
                return 0
        else:
            return False

    def season_win(self):
        """
        승수
        :return:
        """
        if self.pitcher_code:
            return self.df_season_record[self.df_season_record['WLS'] == 'W'].shape[0]
        else:
            return False

    def season_lose(self):
        """
        패수
        :return:
        """
        if self.pitcher_code:
            return self.df_season_record[self.df_season_record['WLS'] == 'L'].shape[0]
        else:
            return False

    def season_save(self):
        """
        세이브수
        :return:
        """
        if self.pitcher_code:
            return self.df_season_record[self.df_season_record['WLS'] == 'S'].shape[0]
        else:
            return False

    def season_hold(self):
        """
        홀드수
        :return:
        """
        if self.pitcher_code:
            return self.df_season_record['HOLD'].sum()
        else:
            return False
