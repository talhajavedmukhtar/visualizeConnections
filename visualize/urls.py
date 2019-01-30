from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/getGraph/', views.getGraphForASN, name="get-graph")
]