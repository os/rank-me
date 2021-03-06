from django.conf.urls import patterns, url

urlpatterns = patterns(
    'game.views',
    url(r'^$', 'competition_detail', name='competition_detail'),
    url(r'^game/new/$', 'game_add', name='game_add'),
    url(r'^team/(?P<team_id>\d+)/$', 'team_detail', name='team_detail'),
)
