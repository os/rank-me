from django.db.models.signals import post_save
from django.dispatch import receiver
from trueskill import Rating, rate_1vs1

from .models import Game, HistoricalScore, Team


@receiver(post_save, sender=Game)
def update_score(sender, **kwargs):
    """
    On Game creation (ie. when new result is inserted) update both team score and add it to their historical records
    """
    if not kwargs['created']:
        return

    game = kwargs['instance']

    winner = game.winner
    loser = game.loser
    winner_new_score, loser_new_score = rate_1vs1(
        Rating(winner.score, winner.stdev),
        Rating(loser.score, loser.stdev)
    )

    winner.score = winner_new_score.mu
    winner.stdev = winner_new_score.sigma
    winner.save()
    loser.score = loser_new_score.mu
    loser.stdev = loser_new_score.sigma
    loser.save()

    HistoricalScore.objects.create(team=winner, score=winner_new_score.mu)
    HistoricalScore.objects.create(team=loser, score=loser_new_score.mu)


@receiver(post_save, sender=Team)
def set_default_score(sender, **kwargs):
    """
    On Team creation set default historical score
    """
    if not kwargs['created']:
        return

    team = kwargs['instance']

    HistoricalScore.objects.create(team=team, score=team.score)
