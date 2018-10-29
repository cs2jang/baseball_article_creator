import globals as g


class SubTeam(object):
    def __init__(self, team_code):
        self.team_code = team_code

        g.define_method(self, g.sub_team_method)

    def name(self):
        return g.team_name_dict[self.team_code]

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

    def is_draw(self):
        return g.IS_DRAW



