import globals as g


class Template(object):
    def __init__(self, game_var):
        self.base_structure = None
        self.game_var = game_var

    def get_sentence(self):
        sentence_list = []
        active_tab_list = []
        base_temp = g.m.get_spread_template('base_template')
        for bt in base_temp:
            if not bt['name']:
                continue
            str_condition = g.get_result_string(bt['condition'], self.game_var)
            if eval(str_condition):
                if bt['template_tab'] not in active_tab_list:
                    active_tab_list.append(bt['template_tab'])
                    g.set_dynamic_variable_v2(self.game_var, bt['template_tab'])
                sentence_list.append(bt['sentence'].format(**self.game_var.__dict__))
        return sentence_list

    def set_tab_info(self, tab_name):
        _temp = g.m.get_df_spread_template(tab_name)
        for t in _temp:
            if not t['name']:
                continue

            if eval(t['condition'].format(**self.game_var)):
                if t['name'] not in self.game_var:
                    s = g.get_random_sentence(t['sentence'])
                    text = s.format(**self.game_var)
                    text = g.get_josa(text)
                    self.game_var[t['name']] = text
