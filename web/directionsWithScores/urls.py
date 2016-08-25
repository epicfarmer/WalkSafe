from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.directions_with_scores, name='directions_with_scores'),
]
