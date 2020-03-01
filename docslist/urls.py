from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import DocsInfoView, DocsListView, DocDetailView, DisplayPdfView, SearchResultsView, FilterDocsView, \
    DocCreateView, DocUpdateView


urlpatterns = [
    path('', DocsInfoView.as_view(), name='index'),
    path('list/', DocsListView.as_view(), name='docs-list'),
    path('list/details/<int:pk>/', DocDetailView.as_view(), name='doc-detail'),
    path('list/pdf/<int:pk>/', DisplayPdfView.as_view(), name='doc-pdf-view'),
    path('search/', SearchResultsView.as_view(), name='search-results'),
    path('filter/', FilterDocsView.as_view(), name='filter'),
    path('update/<int:pk>', DocUpdateView.as_view(), name='doc-update'),
    path('create/', DocCreateView.as_view(), name='doc-create'),
]
