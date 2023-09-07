from django.urls import path, include
from . import views

urlpatterns = [
    path('space/', views.SearchSpace.as_view()),
    path('sbt/', include('search.search_by_time')),
    path('ajax/', include('search.ajax_handler')),
]
