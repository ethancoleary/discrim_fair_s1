from otree.api import *
import random
from common import MyBasePage


class C(BaseConstants):
    NAME_IN_URL = 'task'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    investment = models.IntegerField(min=0, max=200)
    slider_value = models.IntegerField(min=0, max=200, blank=True)

    blur_log = models.LongStringField(blank=True)
    blur_count = models.IntegerField(initial=0, blank=True)
    blur_warned = models.IntegerField(initial=0, blank=True)


class TaskIntro(MyBasePage):
    # add extra fields on top of base tracking fields
    @property
    def form_fields(self):
        return MyBasePage.form_fields + ['slider_value']

    @staticmethod
    def vars_for_template(player: Player):
        ctx = MyBasePage.vars_for_template(player)
        # add any page-specific vars here, then return
        # ctx.update({...})
        return ctx


class Task(MyBasePage):
    @property
    def form_fields(self):
        return MyBasePage.form_fields + ['investment']

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.investment = player.investment
        participant.die = random.randint(1, 6)


page_sequence = [TaskIntro, Task]
