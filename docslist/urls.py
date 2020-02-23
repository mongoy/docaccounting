from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import DocsInfoView


urlpatterns = [
    path('', DocsInfoView.as_view(), name='index'),
]