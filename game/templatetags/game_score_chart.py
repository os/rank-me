from django.template.defaulttags import register
from datetime import datetime, timedelta
import pygal
from game.models import HistoricalScore


@register.inclusion_tag('score_chart.html', takes_context=True)
def score_chart(context, *args, **kwargs):
    try:
        time_range = kwargs['time_range']
        if time_range == 'last_week':
            delta = timedelta(days=7)
    except KeyError as e:
        delta = timedelta(days=30)

    start_date = datetime.now() - delta

    chart = pygal.DateY(
        x_label_rotation=20,
        disable_xml_declaration=True,
        width=1000,
        show_legend=True,
        style=pygal.style.RedBlueStyle,
        dots_size=5,
    )

    scores = HistoricalScore.objects.filter(date__gt=start_date)
    scores_for_chart = {}
    for score in scores:
        team_name = score.team.get_name()
        if team_name not in scores_for_chart:
            scores_for_chart[team_name] = []
        scores_for_chart[team_name].append((score.date, score.score))

    for team_name, score_values in scores_for_chart.items():
        chart.add(team_name, score_values)

    return {
        'chart': chart
    }
