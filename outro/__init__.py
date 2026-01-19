from otree.api import *

import random
import math

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'outro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    lottery = models.IntegerField(initial=0)
    earning = models.IntegerField()

    # Data quality tracking fields
    blur_count = models.IntegerField(initial=0)
    blur_log = models.LongStringField(initial='{}')
    blur_warned = models.BooleanField(initial=False)


class Results(Page):
    form_model = 'player'
    form_fields = ['blur_count', 'blur_log', 'blur_warned']

    @staticmethod
    def vars_for_template(player):
        investment = player.participant.investment
        die = player.participant.die
        if die < 3:
            player.lottery = 1
        else:
            player.lottery = 0
        kept = 200 - investment
        earning = kept + math.ceil(player.lottery * 3.5 * investment)
        player.earning = earning
        if earning % 10 == 0:
            bonus = f"{earning / 100}0"
        else:
            bonus = f"{earning / 100}"
        return {
            'kept': kept,
            'inv': investment,
            'die': die,
            'earning': earning,
            'bonus': bonus,
            'hidden_fields': ['blur_log', 'blur_count', 'blur_warned'],
        }

class Redirect(Page):
    @staticmethod
    def js_vars(player):
        return dict(
            completionlinkfull=player.subsession.session.config['completionlinkfull']
        )


page_sequence = [Results, Redirect]
