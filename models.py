import pymysql
import config as cfg
import pandas as pd
from common_lib import query_loader
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Lab2AIConn(object):
    def __init__(self):
        self.ql = query_loader.QueryLoader()
        self.gspread_credentials = ServiceAccountCredentials.from_json_keyfile_dict(cfg.GSPREAD_DICT, cfg.GSPREAD_SCOPE)
        self.gc = gspread.authorize(self.gspread_credentials)

    def get_spread_worksheets(self):
        """

        :return: a list of dictionary
        """
        # sheet = self.gc.open_by_url(cfg.GSPREAD_URL).worksheet(tab_name)
        worksheets = self.gc.open_by_url(cfg.GSPREAD_URL).worksheets()

        # result = sheet.get_all_records()
        return worksheets

    def get_df_spread_template(self, tab_name):
        """

        :return: dataframe
        """
        sheet = self.gc.open_by_url(cfg.GSPREAD_URL).worksheet(tab_name)
        result = pd.DataFrame(sheet.get_all_records())
        return result

    def get_score(self, game_id):
        conn = pymysql.connect(**cfg.DB_CONFIG)

        query_format = self.ql.get_query("query_common", "get_score")
        query = query_format.format(GMKEY=game_id)

        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_dict('records')[0]

    def get_team_name(self):
        conn = pymysql.connect(**cfg.DB_CONFIG)

        query_format = self.ql.get_query("query_common", "get_team_name")
        query = query_format

        df = pd.read_sql(query, conn)
        conn.close()
        return df.set_index('team').T.to_dict('records')[0]

    def get_method(self, kinds):
        conn = pymysql.connect(**cfg.LAB2AI_DB_CONFIG)

        query_format = self.ql.get_query("query_common", "get_method")
        query = query_format.format(kinds)

        df = pd.read_sql(query, conn)
        conn.close()
        return df.set_index('kor').T.to_dict('records')[0]

    def get_df_teamrank_daily(self, game_date, team):
        conn = pymysql.connect(**cfg.LAB2AI_DB_CONFIG)

        query_format = self.ql.get_query("query_common", "get_teamrank_daily")
        query = query_format.format(DATE=game_date, TEAM=team)

        df = pd.read_sql(query, conn)
        conn.close()
        return df

    def get_df_gamecontapp(self, game_id):
        conn = pymysql.connect(**cfg.LAB2AI_DB_CONFIG)

        query_format = self.ql.get_query("query_common", "get_gamecontapp")
        query = query_format.format(GMKEY=game_id)

        df = pd.read_sql(query, conn)
        conn.close()
        return df

    def get_df_person_info(self, p_code):
        conn = pymysql.connect(**cfg.LAB2AI_DB_CONFIG)

        query_format = self.ql.get_query("query_common", "get_person_info")
        query = query_format.format(PCODE=p_code)

        df = pd.read_sql(query, conn)
        conn.close()
        return df

    def get_df_entry(self, game_id):
        conn = pymysql.connect(**cfg.LAB2AI_DB_CONFIG)

        query_format = self.ql.get_query("query_common", "get_entry")
        query = query_format.format(GMKEY=game_id)

        df = pd.read_sql(query, conn)
        conn.close()
        return df

    def get_df_season_wls(self, game_id, team_cd):
        conn = pymysql.connect(**cfg.DB_CONFIG)

        query_format = self.ql.get_query("query_common", "get_season_wls")
        query = query_format.format(GYEAR=game_id[0:4], GDAY=game_id[0:8], TEAM_CD=team_cd)

        df = pd.read_sql(query, conn)
        conn.close()
        return df

    def get_df_today_hitters(self, game_id, tb=None):
        conn = pymysql.connect(**cfg.DB_CONFIG)

        if tb is None:
            where_tb = ""
        else:
            where_tb = "AND TB = '{%s}'" % tb

        query_format = self.ql.get_query("query_common", "get_today_hitters")
        query = query_format.format(GMKEY=game_id, TB=where_tb)

        df = pd.read_sql(query, conn)
        conn.close()
        return df

    def get_df_today_pitchers(self, game_id, tb=None):
        conn = pymysql.connect(**cfg.DB_CONFIG)

        if tb is None:
            where_tb = ""
        else:
            where_tb = "AND TB = '{%s}'" % tb

        query_format = self.ql.get_query("query_common", "get_today_pitchers")
        query = query_format.format(GMKEY=game_id, TB=where_tb)

        df = pd.read_sql(query, conn)
        conn.close()
        return df

    def get_df_pitcher_total(self, game_id, pitcher_code):
        conn = pymysql.connect(**cfg.DB_CONFIG)

        query_format = self.ql.get_query("query_common", "get_pitcher_total")
        query = query_format.format(GYEAR=game_id[0:4], PCODE=pitcher_code)

        df = pd.read_sql(query, conn)
        conn.close()
        return df

    def get_df_hitter(self, game_id, hitter_code):
        conn = pymysql.connect(**cfg.DB_CONFIG)

        query_format = self.ql.get_query("query_common", "get_hitter")
        query = query_format.format(GDAY=game_id[0:8], PCODE=hitter_code)

        df = pd.read_sql(query, conn)
        conn.close()
        return df

    def get_df_pitcher(self, game_id, pitcher_code):
        conn = pymysql.connect(**cfg.DB_CONFIG)

        query_format = self.ql.get_query("query_common", "get_pitcher")
        query = query_format.format(GDAY=game_id[0:8], PCODE=pitcher_code)

        df = pd.read_sql(query, conn)
        conn.close()
        return df

    def get_df_hitter_record_matrix_mix(self, game_id, hitter_code):
        conn = pymysql.connect(**cfg.DB_CONFIG)

        query_format = self.ql.get_query("query_common", "get_hitter_record_matrix_mix")
        query = query_format.format(GDAY=game_id[0:8], PCODE=hitter_code)

        df = pd.read_sql(query, conn)
        conn.close()
        return df

    def get_df_record_matrix_mix(self, game_id):
        conn = pymysql.connect(**cfg.DB_CONFIG)

        query_format = self.ql.get_query("query_common", "get_record_matrix_mix")
        query = query_format.format(GMKEY=game_id)

        df = pd.read_sql(query, conn)
        conn.close()
        return df

    def get_df_gameinfo(self, gmkey=None, start_date=None, end_date=None):
        conn = pymysql.connect(**cfg.DB_CONFIG)

        if gmkey:
            where_query = "Gmkey = '%s'" % gmkey
        else:
            where_query = "GDAY BETWEEN '%s' AND '%s'" % (start_date, end_date)

        query_format = self.ql.get_query("query_common", "get_gameinfo_between")
        query = query_format.format(WHERE=where_query)

        df = pd.read_sql(query, conn)
        conn.close()
        return df


if __name__ == "__main__":
    test = Lab2AIConn()
    dv = test.get_spread_worksheets('dynamic_variable')
    print(dv)

