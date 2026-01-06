from otree.api import *
import random
import math


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'task'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    investment = models.IntegerField(min=0,max=200)
    slider_value = models.IntegerField(min=0, max=200, blank=True)

# PAGES
class TaskIntro(Page):
    form_model = 'player'
    form_fields = ['slider_value']

class Task(Page):
    form_model = 'player'
    form_fields = ['investment']

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.investment = player.investment
        participant.die = random.randint(1, 6)


page_sequence = [
                TaskIntro,
                Task
                ]
