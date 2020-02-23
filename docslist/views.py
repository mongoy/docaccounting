import datetime
import os
import django_filters

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.views.generic.base import View
from django.views.generic.detail import BaseDetailView
# from .forms import ContractCreatForm, ContractForm
# пагинация
from django.shortcuts import render, get_object_or_404

from .models import Docs
from django.http import FileResponse, Http404


class DocsInfoView(View):
    """ Сводная информация на главной странице """

    # def get(self, request, *args, **kwargs):
    @staticmethod
    def get(request):
        # рабочие контракты без допов
        info = Docs.objects.all().filter(work_contract=True).exclude(type_doc=3).aggregate(
            Count('id', distinct=True), Sum('c_contract'))
        qs = Docs.objects.all().filter(work_contract=True, type_doc=1)
        d_today = datetime.date.today()
        sum_ost = 0
        for rw in qs:
            sum_ost += rw.c_contract
        info['ogk__sum'] = sum_ost
        info['date__today'] = d_today
        return render(request, 'index.html', context=info)
