from django.conf.urls import url
from rest.views import EventViewSet, Participation, Discord

urlpatterns = [
    url(r'^event/$', EventViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^event/(?P<eid>[0-9]+)/$', EventViewSet.as_view({'delete': 'destroy'})),
    url(r'^participation/$', Participation.as_view()),
    url(r'^discord/$', Discord.as_view()),
]
