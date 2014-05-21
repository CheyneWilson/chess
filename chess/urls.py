from django.conf.urls import patterns, include, url
from chess import views


urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Wire up our API using automatic URL routing.
    # Additionally, we include login URLs for the browseable API.
    url(r'^$', views.index, name='index'),
    # url(r'^login/$', views.login_logout, name='index'),
    url(r'^login/$', views.LoginLogout.as_view()),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^user/(?P<username>[0-9a-zA-Z_]+)/game/$', views.GameCreateOrList.as_view()),
    url(r'^user/(?P<username>[0-9a-zA-Z_]+)/game/(?P<game_id>[0-9]+)$', views.GameDetail.as_view()),
    url(r'^user/(?P<username>[0-9a-zA-Z]+)/game/(?P<game_id>[0-9]+)/move/$', views.MoveList.as_view()),
    url(r'^user/(?P<username>[0-9a-zA-Z_]+)/game/(?P<game_id>[0-9]+)/move/(?P<from_loc>[a-hA-H][1-8])$',
        views.MoveDetail.as_view()),
    url(r'^user/(?P<username>[0-9a-zA-Z]+)/game/(?P<game_id>[0-9]+)/move/(?P<from_loc>[a-hA-H][1-8])'
        r'/(?P<to_loc>[a-hA-H][1-8])$', views.MovePiece.as_view()),
    url(r'^user/(?P<username>[0-9a-zA-Z]+)/game/(?P<game_id>[0-9]+)/previous/$', views.PreviousMoves.as_view()),
    url(r'^user/(?P<username>[0-9a-zA-Z]+)/game/(?P<game_id>[0-9]+)/promote/$', views.PromotablePieces.as_view()),
    url(r'^user/(?P<username>[0-9a-zA-Z]+)/game/(?P<game_id>[0-9]+)/promote/(?P<piece>[0-9a-zA-Z]+)$',
        views.PromotePiece.as_view()),
    # url(r'^user/(?P<username>[0-9a-zA-Z]+)/matchmake/', views.MatchMake.as_view()),
    # url(r'^user/(?P<username>[0-9a-zA-Z]+)/matchmake/(?P<id>[0-9]+)', views.MatchMake.as_view()),
    url(r'^user/(?P<username>[0-9a-zA-Z]+)/challenge/$', views.ChallengeList.as_view()),
    url(r'^user/(?P<username>[0-9a-zA-Z]+)/challenge2/(?P<opponent>[0-9a-zA-Z]+)$', views.Challenge.as_view()),

    url(r'^user/(?P<username>[0-9a-zA-Z]+)/players/$', views.ActivePlayers.as_view()),
    url(r'^user/(?P<username>[0-9a-zA-Z]+)/agents/$', views.AiAgents.as_view()),
    # url(r'^login/$', views.AuthView.as_view()),
    # url(r'^login/$', views.LogInOut),
)
