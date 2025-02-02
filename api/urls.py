from django.urls import path
from api.views import ClassifyNumbersView


urlpatterns = [
    path('classify-number', ClassifyNumbersView.as_view(), name="classify-number"),
]