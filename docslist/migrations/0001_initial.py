# Generated by Django 3.0.3 on 2020-02-23 18:27

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, unique=True, verbose_name='Подрядчик')),
            ],
            options={
                'verbose_name': 'Подрядчик',
                'verbose_name_plural': 'Подрядчики',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Initiator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Инициатор')),
                ('description', models.TextField(verbose_name='Описание')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Инициатор',
                'verbose_name_plural': 'Инициаторы',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='StatusDoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='TypeDoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Документ')),
                ('description', models.TextField(verbose_name='Описание')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Тип документа',
                'verbose_name_plural': 'Типы документов',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Docs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_contract', models.CharField(db_index=True, default='-', max_length=20, verbose_name='Номер контракта')),
                ('title', models.CharField(db_index=True, default='-', max_length=500, verbose_name='Наименование объекта')),
                ('year', models.PositiveSmallIntegerField(default='1970', verbose_name='Год')),
                ('c_contract', models.FloatField(default=0, max_length=50, verbose_name='Цена контракта, руб.')),
                ('in_contract', models.DateField(default=datetime.date.today, verbose_name='Дата подписания контракта')),
                ('in_work', models.DateField(default=datetime.date.today, verbose_name='Дата начала работ')),
                ('out_work', models.DateField(default=datetime.date.today, verbose_name='Дата окончания работ')),
                ('work_contract', models.BooleanField(verbose_name='В работе')),
                ('failures', models.BooleanField(verbose_name='Срыв сроков')),
                ('executed', models.BooleanField(verbose_name='Исполнен')),
                ('file_obj', models.FileField(upload_to='files/', verbose_name='Файл документа')),
                ('url', models.SlugField(max_length=130, unique=True)),
                ('data_stamp', models.DateTimeField(auto_now_add=True)),
                ('ini_contract', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='docslist.Initiator', verbose_name='Инициатор')),
                ('stat_contract', models.ForeignKey(default='-', on_delete=django.db.models.deletion.DO_NOTHING, to='docslist.StatusDoc', verbose_name='Статус')),
                ('type_doc', models.ForeignKey(default='-', on_delete=django.db.models.deletion.DO_NOTHING, to='docslist.TypeDoc', verbose_name='Документ')),
                ('uch_contract', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='docslist.Contractor', verbose_name='Подрядчик')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
                'ordering': ('year', 'num_contract'),
            },
        ),
    ]
