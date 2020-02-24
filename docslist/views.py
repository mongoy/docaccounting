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


class DocsView(ListView):
    """ Список документов"""
    # def get(self, request):
    #     docs = Docs.objects.all()
    #     return render(request, 'docslist/docs_list.html', {"docs_list": docs})
    model = Docs
    # рабочие контракты без КС
    queryset = Docs.objects.all().filter(work_contract=True).exclude(type_doc=3)

    template_name = 'docslist/docs_list.html'
    paginate_by = 5


class Year:
    """год подписания документа"""
    def get_years(self):
        return Docs.objects.filter(work_contract=True).values("year")


class Ispolnenie:
    """год подписания документа"""
    def get_isp(self):
        return Docs.objects.filter(work_contract=True, type_doc=3).aggregate(Sum('c_contract'))


class DocDetailView(DetailView):
    """Полное описание документа"""
    # def get(self, request, pk):
    #     doc = Docs.objects.get(pk=id)
    #     return render(request, 'docslist/docs_detail.html', {"doc": doc})

    model = Docs
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d_today = datetime.date.today()
        context['d_today'] = d_today
        # исполнение = сумма всех КС
        context['isp'] = 0
        sum_isp = Docs.objects.filter(work_contract=True, type_doc=3, num_contract=kwargs['object'].num_contract).aggregate(Sum('c_contract'))
        # проверка QuerySet []
        if sum_isp['c_contract__sum'] is None:
            context['isp'] = 0
        else:
            context['isp'] = sum_isp['c_contract__sum']
        # остатки по документу
        context['sum_ost'] = kwargs['object'].c_contract - context['isp']

        obj_key = self.kwargs.get('pk', None)
        c_num = Docs.objects.filter(work_contract=True, id=obj_key).exclude(type_doc=3)
        # if self.request.user.is_authenticated:
        #     return context
        # else:
        #     return Contracts.objects.none()
        return context


class DisplayPdfView(BaseDetailView):
    """ Вывод на экран скана контракта в формате PDF"""

    def get(self, request, *args, **kwargs):
        obj_key = self.kwargs.get('pk', None)  # обращение к именованному аргументу pk, переданному по URL-адресу
        pdf = get_object_or_404(Docs, id=obj_key)  # Эта строка получает фактический объект модели pdf
        # if pdf.type_doc_id == 1:
        # file_name = pdf.y_contract + '\\' + pdf.num_contract + '.pdf'  # Папка год + имя файла + расширение
        file_name = 'files\\' + str(pdf.year) + '\\' + str(pdf.file_obj.name)  # Папка год + имя файла
        print(file_name)
        # else:
        #     file_name = pdf.y_contract + '\\' + pdf.num_contract + '.' + pdf.name_object + '.pdf'
        # Папка год + имя файла + расширение
        path = os.path.join(settings.MEDIA_ROOT, file_name)  # полный путь к файлу
        response = FileResponse(open(path, 'rb'), content_type="application/pdf")
        response["Content-Disposition"] = "filename={}".format(file_name)
        return response
