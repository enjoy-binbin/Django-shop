from django.urls import path
from django.conf.urls import url

from .views import ShopListView


app_name = 'shops'
urlpatterns = [
    path('', ShopListView.as_view(), name='list'),
]
