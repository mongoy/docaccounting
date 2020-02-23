from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import DocsInfoView, DocsViev


urlpatterns = [
    path('', DocsInfoView.as_view(), name='index'),
    path('list/', DocsViev.as_view(), name='docs-list')
]