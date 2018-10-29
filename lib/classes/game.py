import globals as g
from collections import namedtuple
from lib.classes.player import Player
from lib.classes.team import Team
from lib.classes.event import Event
from lib.sub_classes.hitter_record import HitterRecord
from lib.sub_classes.pitcher_record import PitcherRecord


class GameVariables(object):
    def __init__(self):
        self.game_id = g.GAME_ID
        self.df_gamecontapp = g.df_gamecontapp

        self.away_team_info = Team(g.AWAY_ID)
        self.home_team_info = Team(g.HOME_ID)
        self.hitter_record_dict = {}
        self.pitcher_record_dict = {}
        self.df_record_matrix = g.m.get_df_record_matrix_mix(self.game_id)
        self.winning_hit_dict = {}

        self.set_player_record()
        g.define_method(self, g.game_method)
        g.set_dynamic_variable_v2(self, 'dynamic_variable')

    def get_dict_var(self):
        return self.__dict__

    def away_team(self):
        """
        원정팀
        :return:
        """
        return self.away_team_info

    def home_team(self):
        """
        홈팀
        :return:
        """
        return self.home_team_info

    def lose_team(self):
        """
        패배팀
        :return:
        """
        if g.HOME_SCORE < g.AWAY_SCORE:
            return self.home_team_info
        else:
            return self.away_team_info

    def win_team(self):
        """
        승리팀
        :return:
        """
        if g.HOME_SCORE > g.AWAY_SCORE:
            return self.home_team_info
        else:
            return self.away_team_info

    def is_home_win(self):
        if g.HOME_SCORE > g.AWAY_SCORE:
            return True
        else:
            return False

    def top_player(self):
        """
        탑플레이어
        :return:
        """
        df_hitter_group = self.df_record_matrix.groupby(['BAT_P_ID'])
        df_pitcher_group = self.df_record_matrix.groupby(['PIT_P_ID'])

        hitter_list = self.get_hitter_top_point_list(df_hitter_group)
        pitcher_list = self.get_pitcher_top_point_list(df_pitcher_group)

        if self.is_home_win():
            hitters = [h for h in hitter_list if h['TB'] == 'B']
            pitchers = [p for p in pitcher_list if p['TB'] == 'B']
        else:
            hitters = [h for h in hitter_list if h['TB'] == 'T']
            pitchers = [p for p in pitcher_list if p['TB'] == 'T']

        win_team = g.HOME_ID if self.is_home_win() else g.AWAY_ID
        if hitters[0]['POINT'] > pitchers[0]['POINT']:
            top_player = hitters[0]['PCODE']
            pos = 'hitter'
        else:
            top_player = pitchers[0]['PCODE']
            pos = 'pitcher'

        return Player(top_player, win_team, pos)

    def get_hitter_top_point_list(self, df_group):
        hitter_list = []
        for d in df_group:
            p_code = d[0]  # name key
            values = d[1].to_dict('record')  # data value list

            p_point = 0
            p_tb = values[0]['TB_SC']
            for v in values:
                p_point += g.H_R_POINT[g.H_R_TOP_RANK_POINT_DICT[v['HOW_ID']]]

            hitter_record = self.hitter_record_dict[p_code]
            p_point += (
                        hitter_record.ab() * 0.5 + hitter_record.run() * 2 + hitter_record.rbi() * 4 + hitter_record.err() * -5)
            if hitter_record.is_cycling_hit():
                p_point += 40
            if hitter_record.is_winning_hit():
                p_point += 7

            hitter_list.append({'PCODE': p_code, 'POINT': p_point, 'TB': p_tb})
        hitter_list.sort(key=lambda k: k['POINT'], reverse=True)
        return hitter_list

    def get_pitcher_top_point_list(self, df_group):
        pitcher_list = []
        pitcher_penalty = 0.6
        for d in df_group:
            p_code = d[0]  # name key
            values = d[1].to_dict('record')  # data value list

            p_point = 0
            p_tb = 'T' if values[0]['TB_SC'] == 'B' else 'B'
            for v in values:
                li = 1.5 if v['LI_RT'] >= 2 else 1
                p_point += g.PITCHER_POINT[g.P_TOP_RANK_POINT_DICT[v['HOW_ID']]] * li

            pitcher_record = self.pitcher_record_dict[p_code]
            if pitcher_record.is_win():
                p_point += 40 if pitcher_record.is_first_pitcher() else 30

            if pitcher_record.is_perfect_game():
                p_point += 10000
            elif pitcher_record.is_no_hit_no_run():
                p_point += 5000
            elif pitcher_record.is_sho():
                p_point += 2000
            elif pitcher_record.is_cg():
                p_point += 1600
            elif pitcher_record.is_qs_plus():
                p_point += 10
            elif pitcher_record.is_qs():
                p_point += 8

            if pitcher_record.is_lose():
                p_point -= 20
            elif pitcher_record.is_save():
                p_point += 24

            p_point += (pitcher_record.hold() * 16 + pitcher_record.er() * -6 +
                        (pitcher_record.r() - pitcher_record.er()) * -3 + (pitcher_record.inn2() / 3) * 9.6)

            p_point *= pitcher_penalty
            pitcher_list.append({'PCODE': p_code, 'POINT': p_point, 'TB': p_tb})

        pitcher_list.sort(key=lambda k: k['POINT'], reverse=True)
        return pitcher_list

    def is_draw(self):
        """
        무승부?
        :return:
        """
        return g.IS_DRAW

    def last_inning_num(self):
        """
        마지막이닝_회
        :return:
        """
        return self.df_gamecontapp.iloc[-1:]['INN'].values[0]

    def last_inning_tb(self):
        """
        마지막이닝_초말
        :return:
        """
        return self.df_gamecontapp.iloc[-1:]['TB'].values[0]

    def last_event(self):
        """
        마지막타석
        :return:
        """

        return Event(self.df_gamecontapp.iloc[-1])

    # def get_gamecontapp_event(self):
    #     result_dict = {}
    #     seq_no = self.df_gamecontapp['SERNO'].tolist()
    #
    #     for s in seq_no:
    #         s_gamecontapp = self.df_gamecontapp[self.df_gamecontapp['SERNO'] == s]
    #         result_dict.update({s: Event(s_gamecontapp)})
    #
    #     return result_dict

    def hr_players(self):
        """
        홈런선수들
        :return:
        """
        return False

    def hr_players_num(self):
        '''
        홈런선수명수
        :return:
        '''
        return 1

    def is_called_game(self):
        """
        콜드?
        :return:
        """
        return False

    def is_reversal_any(self):
        """
        역전존재?
        :return:
        """
        return False

    def is_rare_record(self):
        """
        진기록?
        :return:
        """
        return False

    def game_date(self):
        """
        당일날짜
        :return:
        """

        Date = namedtuple('game_date',['월','일'])
        g_day = Date("%d" % int(self.game_id[4:6]), "%d" % int(self.game_id[6:8]))
        return g_day


    def stadium_kor(self):
        """
        구장이름
        :return:
        """
        df_gameinfo = g.m.get_df_gameinfo(gmkey=self.game_id)

        return df_gameinfo['Stadium'].values[0]

    def league_name(self):
        """
        리그명
        :return:
        """
        return 'KBO리그'

    def is_winning_hit(self):
        df_record = self.df_record_matrix.sort_values(by='SEQNO', ascending=False)

        if df_record.iloc[0]['AFTER_AWAY_SCORE_CN'] > df_record.iloc[0]['AFTER_HOME_SCORE_CN']:
            tb_win = 'T'
        else:
            tb_win = 'B'

        index_cnt = 0
        for i, row in df_record.iterrows():
            if index_cnt == 0 and row['AFTER_SCORE_GAP_CN'] == 0:
                return False

            index_cnt += 1
            if (tb_win == 'T' and row['AFTER_SCORE_GAP_CN'] >= 0) or (tb_win == 'B' and row['AFTER_SCORE_GAP_CN'] <= 0):
                s_record = df_record.iloc[index_cnt - 2]
                if '실책으로' in s_record['LIVETEXT_IF']:
                    return False

                if s_record['HOW_ID'] not in g.HIT:
                    return False
                else:
                    self.winning_hit_dict = {
                        'HITTER': s_record['BAT_P_ID'],
                        'INNING': s_record['INN_NO'],
                        'HOW_KOR': g.HOW_KOR_DICT[s_record['HOW_ID']]
                    }
                    return True

        return False

    def winning_hit(self):
        if self.is_winning_hit():
            WinningHitter = namedtuple('WinningHitter', ['타자'])
            return WinningHitter(HitterRecord(self.winning_hit_dict['HITTER']))
        else:
            return False

    def winning_hit_kor(self):
        if self.is_winning_hit():
            return self.winning_hit_dict['HOW_KOR']
        else:
            return False

    def winning_hit_inning(self):
        if self.is_winning_hit():
            return self.winning_hit_dict['INNING']
        else:
            return False

    def winning_point_inning(self):
        if not self.is_draw():
            df_record = self.df_record_matrix.sort_values(by='SEQNO', ascending=False)

            if df_record.iloc[0]['AFTER_AWAY_SCORE_CN'] > df_record.iloc[0]['AFTER_HOME_SCORE_CN']:
                tb_win = 'T'
            else:
                tb_win = 'B'

            index_cnt = 0
            for i, row in df_record.iterrows():
                if index_cnt == 0 and row['AFTER_SCORE_GAP_CN'] == 0:
                    return False

                index_cnt += 1
                if (tb_win == 'T' and row['AFTER_SCORE_GAP_CN'] >= 0) or (tb_win == 'B' and row['AFTER_SCORE_GAP_CN'] <= 0):
                    s_record = df_record.iloc[index_cnt - 2]
                    return s_record['INN_NO']
        return False

    def set_player_record(self):
        df_hitter_group = self.df_record_matrix.groupby(['BAT_P_ID'])
        df_pitcher_group = self.df_record_matrix.groupby(['PIT_P_ID'])

        for hitter in df_hitter_group:
            p_code = hitter[0]  # name key
            self.hitter_record_dict.update({p_code: HitterRecord(p_code)})

        for pitcher in df_pitcher_group:
            p_code = pitcher[0]  # name key
            self.pitcher_record_dict.update({p_code: PitcherRecord(p_code)})


    # def get_players_info_dict(self):
    #     df_entry = g.m.get_df_entry(self.game_id)
    #     # df_pitchers = df_entry[df_entry['POSI'].str.endswith('1', na=False)]
    #     # df_hitters = df_entry[df_pitchers['PCODE'].isin(df_entry) == False]
    #     entry_dict = {}
    #     entry_list = df_entry.to_dict('records')
    #
    #     for entry_info in entry_list:
    #         if entry_info['TEAM'] == 'B':
    #             entry_dict.update({
    #                 entry_info['PCODE']: Player(entry_info['PCODE'])
    #             })
    #         else:
    #             entry_dict.update({
    #                 entry_info['PCODE']: Player(entry_info['PCODE'])
    #             })
    #
    #     return entry_dict

