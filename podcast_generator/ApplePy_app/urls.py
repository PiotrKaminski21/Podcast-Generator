from django.urls import path
from .views import HomeView, GenreFormView, ResultView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('form/', GenreFormView.as_view(), name='form'),
    path('result/', ResultView.as_view(), name='result'),
]
