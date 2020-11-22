from django import forms
from .models import Expense, Category, Income
from bootstrap_datepicker_plus import DatePickerInput

class ExpenseForm(forms.ModelForm):
    
    payment_date = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y'), required = False)
    name = forms.CharField(
                    max_length=200,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Description...',
                        'class': 'form-control',
                    }),  required = False)
    amount = forms.IntegerField(
                    widget=forms.NumberInput(attrs={
                        'placeholder': 'Amount...',
                        'class': 'form-control',
                    }), required = False)
    comments = forms.CharField(
                    max_length=200,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Comments...' ,
                        'class': 'form-control',
                    }), required = False)
    new_cat = forms.CharField(
                    max_length=200,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Or add new Category',
                        'class': 'form-control',
                    }), required = False)
    
    category = forms.ModelChoiceField(queryset = Category.objects.all(), empty_label="Select Category", widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    planned_monthly = forms.BooleanField(initial = False, required=False)
    class Meta:
        model = Expense
        fields = ('name', 'amount', 'payment_date', 'category', 'comments')

class IncomeForm(forms.ModelForm):
    income_date = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y'), required = False)
    name = forms.CharField(label="", max_length=200, widget=forms.TextInput(
        attrs={
            'placeholder': 'Description...',
            'class': 'form-control',
            }), required = False)
    amount = forms.IntegerField(label="", widget=forms.NumberInput(
        attrs={
            'placeholder': 'Amount...',
            'class': 'form-control',
            }), required = False)
    comments = forms.CharField(label="", max_length=200, widget=forms.TextInput(
        attrs={
            'placeholder': 'Comments...',
            'class': 'form-control',
            }), required = False)
    planned_monthly = forms.BooleanField(initial = False, required=False)
    
    class Meta:
        model = Income
        fields = ('name', 'amount', 'income_date', 'comments')
     

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label="New Category",
                    max_length=200,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Enter category',
                        'class': 'form-control',
                    }))
    class Meta:
        model = Category
        fields = ('name',)

class SearchForm(forms.Form):
    text = forms.CharField(
                    max_length=200,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Search..',
                    }))