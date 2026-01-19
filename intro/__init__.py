from otree.api import *
from common import *

doc = """
Stage 1 Pilot
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.IntegerField(initial=0)
    gender = models.IntegerField(
        choices=[
            [1, 'Female'],
            [2, 'Male'],
            [3, 'Other'],
            [4, 'Prefer not to say']
        ],
        widget=widgets.RadioSelect
    )
    age = models.IntegerField(min=0, max=100)
    KK = models.IntegerField(
        choices=[
            [1, 'Klee'],
            [2, 'Kandinsky'],
        ],
    )
    accepted = models.IntegerField(initial=1)

    # Data quality tracking fields
    blur_log = models.LongStringField(blank=True)
    blur_count = models.IntegerField(initial=0, blank=True)
    blur_warned = models.IntegerField(initial=0, blank=True)


# PAGES
class Intro(Page):
    form_model = 'player'
    form_fields = ['consent', 'blur_count', 'blur_log', 'blur_warned']

    @staticmethod
    def error_message(player, values):
        if values.get('consent') != 1:
            return "Please consent to participation or withdraw from the experiment by closing your browser."

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'hidden_fields': ['blur_log', 'blur_count', 'blur_warned'],
        }

class PDetails(Page):
    form_model = 'player'
    form_fields = ['gender', 'age', 'blur_count', 'blur_log', 'blur_warned']

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.gender > 2:
            player.accepted = 0

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'hidden_fields': ['blur_log', 'blur_count', 'blur_warned'],
        }


class KK(Page):
    form_model = 'player'
    form_fields = ['KK', 'blur_count', 'blur_log', 'blur_warned']

    @staticmethod
    def is_displayed(player):
        return player.accepted == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.gender == 1:
            if player.KK == 2:
                player.accepted = 0
        elif player.gender == 2:
            if player.KK == 1:
                player.accepted = 0

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'hidden_fields': ['blur_log', 'blur_count', 'blur_warned'],
        }


class Screen(Page):

    @staticmethod
    def is_displayed(player):
        return player.accepted == 0


class Redirect_S(Page):

    @staticmethod
    def is_displayed(player):
        return player.accepted == 0

    @staticmethod
    def js_vars(player):
        return dict(
            completionlinkscreenout_invest=
            player.subsession.session.config['completionlinkscreenout_invest']
        )



page_sequence = [
                Intro,
                PDetails,
                 KK,
                Screen,
                Redirect_S
                ]
