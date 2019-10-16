from django import forms
from .models import Expense, Category


class ExpenseForm(forms.ModelForm):
    
    payment_date = forms.DateField(required = False)
    name = forms.CharField(
                    max_length=200,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Название',
                    }), required = False)
    amount = forms.IntegerField(
                    widget=forms.NumberInput(attrs={
                        'placeholder': 'Сумма',
                    }), required = False)
    comments = forms.CharField(
                    max_length=200,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Комментарии' 
                    }), required = False)
    new_cat = forms.CharField(
                    max_length=200,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Новая категория',
                    }), required = False)

    class Meta:
        model = Expense
        fields = ('name', 'amount', 'payment_date', 'category', 'comments', 
        #attachments
        )

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label="Категория",
                    max_length=200,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Введите категорию',
                    }))
    class Meta:
        model = Category
        fields = ('name',)

class SearchForm(forms.Form):
    text = forms.CharField(
                    max_length=200,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Искать..',
                    }))