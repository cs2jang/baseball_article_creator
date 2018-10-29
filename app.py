import globals as g
from sentence_template import Template
from lib.classes.game import GameVariables


class GameApp(object):
    def __init__(self, game_id):
        g.initialize(game_id)
        self.game_var = GameVariables()
        self.game_dict = self.game_var.get_dict_var()
        self.template_sentence = Template(self.game_var)

    def main(self):
        return ','.join(self.template_sentence.get_sentence())


if __name__ == "__main__":
    df_gameinfo = g.m.get_df_gameinfo(start_date='20170410', end_date='20170910')
    for i, row in df_gameinfo.iterrows():
        game_app = GameApp(row['GmKey'])
        print(game_app.main())
