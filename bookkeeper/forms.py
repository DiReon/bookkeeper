from django import forms
from .models import Expense, Category, Income
from bootstrap_datepicker_plus import DatePickerInput

class ExpenseForm(forms.ModelForm):
    
    payment_date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y'), required = False)
    name = forms.CharField(
                    max_length=200,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Enter description here...',
                    }), required = False)
    amount = forms.IntegerField(
                    widget=forms.NumberInput(attrs={
                        'placeholder': 'Enter amount here...',
                    }), required = False)
    comments = forms.CharField(
                    max_length=200,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Enter comments' 
                    }), required = False)
    new_cat = forms.CharField(
                    max_length=200,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Add new Category',
                    }), required = False)
    category = forms.ModelChoiceField(queryset = Category.objects.all(), empty_label="Select Category")
    planned_monthly = forms.BooleanField(initial = False, required=False)
    class Meta:
        model = Expense
        fields = ('name', 'amount', 'payment_date', 'category', 'comments')

class IncomeForm(forms.ModelForm):
    income_date = forms.DateField(label="", widget=forms.TextInput(attrs={'placeholder': 'Add date in format mm/dd/yyyy',}), required = False)
    name = forms.CharField(label="", max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Add description here...',}), required = False)
    amount = forms.IntegerField(label="", widget=forms.NumberInput(attrs={'placeholder': 'Enter amount',}), required = False)
    comments = forms.CharField(label="", max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Add comments'}), required = False)
    
    class Meta:
        model = Income
        fields = ('name', 'amount', 'income_date', 'comments')
     

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