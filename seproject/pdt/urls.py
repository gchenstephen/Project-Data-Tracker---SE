from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^activity/$', views.activity, name='activity'),
    url(r'^timer/(?P<did>[0-9]+)/(?P<it_id>[0-9]+)(|/)$', views.timer, name='timer'),
    url(r'^timer_control/(?P<judge>[0-9]+)/(?P<tid>[0-9]+)(|/)$', views.timer_control, name='timer_control'),
    url(r'^timer_review/(?P<did>[0-9]+)/(?P<it_id>[0-9]+)(|/)$', views.timer_review, name='timer_review'),
    url(r'^defect_report/(?P<did>[0-9]+)/(?P<pid>[0-9]+)/(?P<phid>[0-9]+)/(?P<check>[0-9]+)/(?P<it_id>[0-9]+)(|/)$', views.defect_report, name='defect_report'),
    url(r'^defect_review/(?P<did>[0-9]+)/(?P<it_id>[0-9]+)(|/)$', views.defect_review, name='defect_review'),
    url(r'^project/(?P<pid>[0-9]+)(|/)$', views.project, name='project'),
    url(r'^phase/(?P<pid>[0-9]+)/(?P<phid>[0-9]+)(|/)$', views.phase, name='phase'),
    url(r'^iteration/(?P<pid>[0-9]+)/(?P<phid>[0-9]+)/(?P<it_id>[0-9]+)(|/)$', views.iteration, name='iteration'),
    url(r'^report/(?P<pid>[0-9]+)(|/)$', views.report, name='report'),
    url(r'^dev_project/(?P<did>[0-9]+)/(?P<check>[0-9]+)(|/)$', views.dev_project, name='dev_project'),
    url(r'^dev_phase/(?P<did>[0-9]+)/(?P<pid>[0-9]+)/(?P<check>[0-9]+)(|/)$', views.dev_phase, name='dev_phase'),
    url(r'^dev_iteration/(?P<did>[0-9]+)/(?P<pid>[0-9]+)/(?P<phid>[0-9]+)/(?P<check>[0-9]+)(|/)$', views.dev_iteration, name='dev_iteration'),
]
