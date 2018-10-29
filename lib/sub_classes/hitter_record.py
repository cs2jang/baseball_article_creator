import globals as g


class HitterRecord(object):
    def __init__(self, hitter_code=None):
        self.hitter_code = hitter_code
        self.game_id = g.GAME_ID
        self.consecutive_hr = []
        self.winning_hit_kor = ''
        self.df_today_record = None
        self.df_season_record = None
        self.df_total_record = None
        self.df_hitter_record_matrix = None
        self.df_record_matrix = None
        if hitter_code:
            self.set_hitter_record()

        g.define_method(self, g.hitter_method)

    def set_hitter_record(self):
        self.df_total_record = g.m.get_df_hitter(self.game_id, self.hitter_code)
        self.df_today_record = self.df_total_record[self.df_total_record['GDAY'] == self.game_id[0:8]]
        self.df_season_record = self.df_total_record[self.df_total_record['GYEAR'] == self.game_id[0:4]]
        self.df_hitter_record_matrix = g.m.get_df_hitter_record_matrix_mix(self.game_id, self.hitter_code)
        self.df_record_matrix = g.m.get_df_record_matrix_mix(self.game_id)

    def name(self):
        if self.hitter_code:
            return g.m.get_df_person_info(self.hitter_code).iloc[0]['NAME']
        else:
            return False

    # region [오늘기록]
    def ab(self):
        if self.hitter_code:
            return self.df_today_record.iloc[0]['AB']
        else:
            return False

    def bb(self):
        if self.hitter_code:
            return self.df_today_record.iloc[0]['BB']
        else:
            return False

    def hit(self):
        if self.hitter_code:
            return self.df_today_record.iloc[0]['HIT']
        else:
            return False

    def hr(self):
        if self.hitter_code:
            return self.df_today_record.iloc[0]['HR']
        else:
            return False

    def kk(self):
        if self.hitter_code:
            return self.df_today_record.iloc[0]['KK']
        else:
            return False

    def pa(self):
        if self.hitter_code:
            return self.df_today_record.iloc[0]['PA']
        else:
            return False

    def rbi(self):
        if self.hitter_code:
            return self.df_today_record.iloc[0]['RBI']
        else:
            return False

    def run(self):
        if self.hitter_code:
            return self.df_today_record.iloc[0]['RUN']
        else:
            return False

    def err(self):
        if self.hitter_code:
            return self.df_today_record.iloc[0]['ERR']
        else:
            return False

    def obn(self):
        if self.hitter_code:
            return self.hit() + self.bb() + self.df_today_record.iloc[0]['HP']
        else:
            return False

    def tb(self):
        if self.hitter_code:
            return self.df_today_record.iloc[0]['TB']
        else:
            return False

    def is_cycling_hit(self):
        if self.hitter_code:
            if self.hit() > 3:
                if self.hr() > 0 and self.df_today_record.iloc[0]['H2'] > 0 and self.df_today_record.iloc[0]['H3'] > 0 and\
                        (self.hit() > self.hr() + self.df_today_record.iloc[0]['H2'] + self.df_today_record.iloc[0]['H3']):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def is_consecutive_hr(self):
        if self.hitter_code:
            df_hitter_record = self.df_hitter_record_matrix[self.df_hitter_record_matrix['GAMEID'] == self.game_id]
            counter = 0
            self.consecutive_hr = []
            for i, row in df_hitter_record.iterrows():
                if row['HOW_ID'] == 'HR':
                    counter += 1
                elif counter > 1:
                    self.consecutive_hr.append(counter)
                    counter = 0
                else:
                    counter = 0

            if self.consecutive_hr:
                return True
            else:
                return False
        else:
            return False

    def consecutive_hr_num(self):
        if self.hitter_code:
            if self.is_consecutive_hr():
                return max(self.consecutive_hr)
            else:
                return 0
        else:
            return False

    def is_winning_hit(self):
        if self.hitter_code:
            df_record = self.df_record_matrix.sort_values(by='SEQNO', ascending=False)

            if df_record.iloc[0]['AFTER_AWAY_SCORE_CN'] > df_record.iloc[0]['AFTER_HOME_SCORE_CN']:
                tb_win = 'T'
            else:
                tb_win = 'B'

            index_cnt = 0
            for i, row in df_record.iterrows():
                if index_cnt == 0 and row['AFTER_SCORE_GAP_CN'] == 0 :
                    return False

                index_cnt += 1
                if (tb_win == 'T' and row['AFTER_SCORE_GAP_CN'] >= 0) or (tb_win == 'B' and row['AFTER_SCORE_GAP_CN'] <=0 ):
                    s_record = df_record.iloc[index_cnt - 2]
                    if '실책으로' in s_record['LIVETEXT_IF']:
                        return False

                    bat_code = s_record['BAT_P_ID']
                    if self.hitter_code != bat_code:
                        return False

                    if s_record['HOW_ID'] not in g.HIT:
                        return False
                    else:
                        self.winning_hit_kor = g.HOW_KOR_DICT[s_record['HOW_ID']]
                        return True

            return False
        else:
            return False

    def how_winning_hit(self):
        if self.hitter_code:
            self.is_winning_hit()
            return self.winning_hit_kor
        else:
            return False
    # endregion [오늘기록]

    # region [시즌기록]
    def season_avg(self):
        return 0

    def game_num(self):
        return 0

    def season_obn(self):
        return 0

    def season_obp(self):
        return 0

    def season_slg(self):
        return 0
    # endregion [시즌기록]
