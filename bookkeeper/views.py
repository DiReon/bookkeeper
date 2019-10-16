import datetime
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views import generic
from django.views.generic.dates import DayArchiveView, MonthArchiveView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.base import TemplateView
from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm, SearchForm
from django.forms.formsets import formset_factory

class ExpenseList(generic.ListView):
    template_name = "/bookkeeper/expense_list.html"
    model = Expense
    queryset = Expense.objects.order_by("-created_date")
    paginate_by = 30

class CategoryList(generic.ListView):
    template_name = "/bookkeeper/category_list.html"
    model = Category

class ExpenseDayView(DayArchiveView):
    model = Expense
    date_field = "payment_date"
    template_name = "/bookkeeper/expense_list_day.html"
    allow_future = False
    month_format = "%m"

class ExpenseMonthView(MonthArchiveView):
    model = Expense
    date_field = "payment_date"
    template_name = "bookkeeper/summary_list.html"
    allow_future = False
    month_format = "%m"

    def get_context_data(self, **kwargs):
        context = super(ExpenseMonthView, self).get_context_data(**kwargs)
        year = self.kwargs["year"]
        context["year"] = year
        month = self.kwargs["month"]
        context["month"] = month
        context["month_j"] = month_list[int(month)-1]
        categories = Category.objects.order_by("name")
        expenses = Expense.objects.filter(payment_date__year = int(year), payment_date__month = int(month))
        totals = {}
        for category in categories:
            totals[category] = 0
            for expense in expenses:
                if expense.category == category:
                    totals[category]+=expense.amount
        context["categories"] = categories
        context["totals"] = totals
        return context

class ExpenseMonthCategoryView(MonthArchiveView):
    model = Expense
    date_field = "payment_date"
    template_name = "bookkeeper/expense_list.html"
    allow_future = False
    month_format = "%m"

    def get_context_data(self, **kwargs):
        context = super(ExpenseMonthCategoryView, self).get_context_data(**kwargs)
        year = self.kwargs["year"]
        context["year"] = year
        month = self.kwargs["month"]
        context["month"] = month
        context["month_j"] = month_list[int(month)-1]
        context["cat"] = self.kwargs["cat"]
        categories = Category.objects.order_by("name")
        expenses = Expense.objects.filter(category__name = context["cat"], payment_date__year = int(year), payment_date__month = int(month))
        context["expense_list"] = expenses
        context["expense_1"] = expenses[0]
        context["expense_1_cat"] = expenses[0].category
        return context

"""
class ExpenseListFormView(TemplateView):
    model = Expense
    template_name = "bookkeeper/expense.html"
    formset = ExpenseFormset()
    def get(self, request, *args, **kwargs):
        self.formset = ExpenseFormset(queryset = Expense.objects.order_by("-payment_date"))
        return super(ExpenseListFormView, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(ExpenseListFormView, self).get_context_data(**kwargs)
        context["formset"] =self.formset
        return context
    def post(self, request, *args, **kwargs):
        self.formset = ExpenseFormset(request.POST)
        if self.formset.is_valid():
            self.formset.save()
            return redirect('expense_list')
        else:
            return super(ExpenseListFormView, self).get(request, *args, **kwargs)
"""
@login_required
def expense_add_formset(request):
    user = request.user
    ExpenseFormset = formset_factory(ExpenseForm, extra = 4)
    if request.method == "POST":
        formset = ExpenseFormset(request.POST)
        i = 0
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    expense = form.save(commit=False)
                    new_cat = form.cleaned_data["new_cat"]
                    if new_cat and (not new_cat in Category.objects.all()):
                        new_category = Category.objects.create(name = new_cat)
                        expense.category = new_category
                    expense.author = user
                    expense.payment_date = form.cleaned_data["payment_date"]
                    expense.save()
                    i+=1
        if i==1: 
            end = "сь"
            end2 = "а"
        if i in range (2,5): 
            end = "си"
            end2 = "ы"
        else: 
            end = "сей"
            end2 = "о"
        if i!=0: 
            messages.add_message(request, messages.SUCCESS, "%s запи%s успешно внесен%s, ты молодец! " %(i, end, end2))
        return redirect('expense_list')
    else:
        formset = ExpenseFormset()
    return render(request, 'bookkeeper/expense_add_formset.html', {'formset': formset})



class ExpenseCreate(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'bookkeeper/expense_add.html'
    success_url = '/'

    def form_valid(self, form):
        expense = form.save(commit=False)
        new_cat = form.cleaned_data["new_cat"]
        if new_cat and (not new_cat in Category.objects.all()):
            new_category = Category.objects.create(name = new_cat)
            expense.category = new_category
        expense.author = self.request.user
        expense.save()
        messages.add_message(self.request, messages.SUCCESS, "Запись успешно внесена, ты молодец!")
        return redirect('expense_list')

class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'bookkeeper/category_add.html'
    success_url = '/'

class CategoryDelete(DeleteView):
    model = Category
    success_url = '/category_list'
    template_name = 'bookkeeper/confirm_delete.html'

class CategoryUpdate(UpdateView):
    model = Category
    form_class = CategoryForm
    success_url ='/'
    template_name = 'bookkeeper/category_add.html'

class ExpenseDelete(DeleteView):
    model = Expense
    success_url = '/'
    template_name = 'bookkeeper/confirm_delete.html'

class ExpenseUpdate(UpdateView):
    model = Expense
    form_class = ExpenseForm
    success_url ='/'
    template_name = 'bookkeeper/expense_add.html'
    
    def form_valid(self, form):
        expense = form.save(commit=False)
        new_cat = form.cleaned_data["new_cat"]
        if new_cat and (not new_cat in Category.objects.all()):
            new_category = Category.objects.create(name = new_cat)
            expense.category = new_category
        expense.author = self.request.user
        expense.save()
        messages.add_message(self.request, messages.SUCCESS, "Запись успешно обновлена!")
        return redirect('expense_list')

class SearchResultsView(generic.ListView):
    model = Expense
    template_name = 'bookkeeper/expense_list.html'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        expense_list = Expense.objects.filter(name__icontains = query)
        return expense_list

@login_required
def expense_test_add(request):
    categories = Category.objects.all()
    test_date = datetime.date(2019,1,1)
    for month in range(1, 11):
        for category in categories:
            for item in range(len(test_data_dict[category.name])):
                expense = Expense.objects.create(name = test_data_dict[category.name][item], amount = 1000 + month*100+item, category = category, author = request.user, payment_date = test_date + datetime.timedelta(days = 31*month))
    return redirect('expense_list')
# Create your views here.
@login_required
def expense_delete_all(request):
    Expense.objects.all().delete()
    return redirect('expense_list')

#month_list = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

test_data_dict = {
    "House expenses": ["Rent", "Chemicals", "Cleaning", "Electricity", "Water", "Internet"],
    "Car": ["Gasoline", "Repair", "Consumables"],
    "Clothes": ["Dress", "Boots", "Blouse", "Coat"],
    "Entertaiment": ["Cinema", "Circus", "Theater"],
    "Food": ["Cheese", "Milk", "Vegetables", "Bread", "Butter"],
    "Medical expenses": ["Sun protection cream"],
    "Restaurants and cafe": ["Burger King", "Baskin&Robbins", "PizzaHut"],
    "Taxi and transport": ["taxi 01.01.2019", "bus 02.01.2019", "train 03.01.2019"],
    


}