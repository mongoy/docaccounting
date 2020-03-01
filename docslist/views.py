import datetime
import os
import django_filters

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.contrib import messages, auth
from django.db.models import Sum, Count, Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.views.generic.base import View
from django.views.generic.detail import BaseDetailView
from .forms import DocsForm, DocsCreatForm
# пагинация
from django.shortcuts import render, get_object_or_404

from .models import Docs, Initiator, TypeDoc

from django.http import FileResponse, Http404


class FilterParameters:
    """год подписания документа"""
    def get_years(self):
        return Docs.objects.values('year').annotate(count=Count('year')).order_by()

    """инициатор создания документа"""
    def get_initiator(self):
        return Initiator.objects.all()

    """вид документа"""
    def get_type(self):
        return TypeDoc.objects.exclude(id=3)

    # """год подписания документа"""
    # def get_isp(self):
    #     return Docs.objects.filter(work_contract=True, type_doc=3).aggregate(Sum('c_contract'))

    def home(self, request, page_number=1):
        docs = Docs.objects.all()
        current_page = Paginator(docs, 5)  # создаим переменную, которая будет содержать 2 статьи из всего обьекта
        docs_list = current_page.page(page_number)
        username = auth.get_user(request).username
        context = {'docs': docs_list, 'username': username}
        return render(request, 'docslist/docs_list.html', context)


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


class FilterDocsView(FilterParameters, ListView):
    """Фильтр документов"""
    paginate_by = 5

    def get_queryset(self):
        queryset = Docs.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(ini_contract__name__in=self.request.GET.getlist("initiator")) |
            Q(type_doc__name__in=self.request.GET.getlist("typedoc"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["initiator"] = ''.join([f"initiator={x}&" for x in self.request.GET.getlist("initiator")])
        context["typedoc"] = ''.join([f"typedoc={x}&" for x in self.request.GET.getlist("typedoc")])
        return context


class DocsListView(FilterParameters, ListView):
    """ Список документов"""
    # рабочие контракты, допы без КС
    queryset = Docs.objects.filter(work_contract=True).exclude(type_doc=3)
    context_object_name = 'docs'
    template_name = 'docslist/docs_list.html'
    paginate_by = 5


class DocDetailView(DetailView):
    """Полное описание документа"""
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


class SearchResultsView(View):
    template_name = 'docslist/search_results.html'

    # @login_required
    def get(self, request, *args, **kwargs):
        context = {}

        question = request.GET.get('q')
        if question is not None:  # поиск по номеру, названию и участнику
            search_contracts = Docs.objects.filter(
                Q(num_contract__icontains=question) |
                Q(title__icontains=question) |
                Q(ini_contract__name__icontains=question) |
                Q(uch_contract__name__icontains=question))

            # формируем строку URL, которая будет содержать последний запрос
            # Это важно для корректной работы пагинации
            context['last_question'] = '?q=%s' % question

            current_page = Paginator(search_contracts, 5)

            page = request.GET.get('page')
            try:
                context['docs_lists'] = current_page.page(page)
            except PageNotAnInteger:
                context['docs_lists'] = current_page.page(1)
            except EmptyPage:
                context['docs_lists'] = current_page.page(current_page.num_pages)

        return render(None, template_name=self.template_name, context=context)


class DocUpdateView(UpdateView):
    """Внесение изменений"""
    model = Docs
    # form_class = DocsForm
    fields = '__all__'  # все поля
    template_name_suffix = '_form'
    success_url = reverse_lazy('docs-list')

    #
    # # @login_required
    # def get_queryset(self):
    #     if self.request.user.is_authenticated:
    #         return Docs.objects.all()
    #     else:
    #         return Docs.objects.none()
    #
    # # @login_required
    # def form_valid(self, form):
    #     result = super().form_valid(form)
    #     messages.success(
    #         self.request, '{}'.format(form.instance))
    #     return result


class DocCreateView(CreateView):
    """Заполнение аттрибутов нового документа"""
    model = Docs
    # form_class = DocsCreatForm
    fields = '__all__'  # все поля
    template_name_suffix = '_form'
    success_url = reverse_lazy('docs-list')

    # def form_valid(self, form):
    #     result = super().form_valid(form)
    #     messages.success(
    #         self.request, '{}'.format(form.instance))
    #     return result
