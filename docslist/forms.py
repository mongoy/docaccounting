from django import forms
from .models import Docs


class DocsForm(forms.ModelForm):
    """Форма"""
    class Meta:
        model = Docs
        fields = '__all__' #все поля
        # exclude = ['n'] #должны быть исключены из формы
        # help_texts = {
        #     'nregion': (' - Название района.'),
        #     'lroad': (' км'),
        # }


class DocsCreatForm(forms.ModelForm):
    """Форма"""

    class Meta:
        model = Docs
        # fields = ['nregion', 'iroad', 'troad', 'innroad', 'inroad','proad']
        fields = '__all__'  # все поля
        # fields = ['file_obj']


