from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import DocsInfoView, DocsView, DocDetailView, DisplayPdfView


urlpatterns = [
    path('', DocsInfoView.as_view(), name='index'),
    path('list/', DocsView.as_view(), name='docs-list'),
    path('list/details/<int:pk>/', DocDetailView.as_view(), name='doc-detail'),
    path('list/pdf/<int:pk>/', DisplayPdfView.as_view(), name='con-pdf-view'),
]
