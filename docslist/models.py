from datetime import date
from django.db import models
from django.urls import reverse


class TypeDoc(models.Model):
    """ Тип документа: госконтракт или допсоглашение """
    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='Документ')
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = "Тип документа"
        verbose_name_plural = "Типы документов"
        ordering = ('name',)  # сортировка


class Initiator(models.Model):
    """ Инициаторы закупки"""
    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='Инициатор')
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = "Инициатор"
        verbose_name_plural = "Инициаторы"
        ordering = ('name',)  # сортировка


class StatusDoc(models.Model):
    """ Статус контракта """
    name = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='Наименование')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ('name',)  # сортировка


class Contractor(models.Model):
    """ Подрядчик """
    name = models.CharField(max_length=200, unique=True, db_index=True, verbose_name='Подрядчик')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = "Подрядчик"
        verbose_name_plural = "Подрядчики"
        ordering = ('name',)  # сортировка


class Docs(models.Model):
    """ Реестр контрактов """
    num_contract = models.CharField('Номер контракта', max_length=20, db_index=True, default='-')
    title = models.CharField('Наименование объекта', max_length=500, db_index=True, default='-')
    type_doc = models.ForeignKey(TypeDoc, on_delete=models.DO_NOTHING, verbose_name='Документ', default='-')
    year = models.PositiveSmallIntegerField('Год', default='1970')
    c_contract = models.FloatField('Цена контракта, руб.', max_length=50, default=0)
    ini_contract = models.ForeignKey(Initiator, on_delete=models.DO_NOTHING, verbose_name='Инициатор', null=True)
    uch_contract = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING, verbose_name='Подрядчик', null=True)
    in_contract = models.DateField('Дата подписания контракта', default=date.today)
    in_work = models.DateField('Дата начала работ', default=date.today)
    out_work = models.DateField('Дата окончания работ', default=date.today)
    stat_contract = models.ForeignKey(StatusDoc, on_delete=models.DO_NOTHING, verbose_name='Статус', default='-')
    work_contract = models.BooleanField('В работе')
    failures = models.BooleanField('Срыв сроков')
    executed = models.BooleanField('Исполнен')
    file_obj = models.FileField('Файл документа', upload_to='')
    url = models.SlugField(max_length=130, unique=True)
    data_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.num_contract

    def get_absolute_url(self):
        return reverse("docs_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ('year', 'num_contract',)  # сортировка

