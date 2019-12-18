import datetime
from random import randint
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views import generic
from django.views.generic.dates import DayArchiveView, MonthArchiveView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.base import TemplateView
from .models import Expense, Category, Income
from .forms import ExpenseForm, IncomeForm, CategoryForm, SearchForm
from django.forms.formsets import formset_factory

@login_required
def index(request):
    expenses = Expense.objects.all()[:5]
    incomes = Income.objects.all()[:5]
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.author = request.user
            new_cat = form.cleaned_data["new_cat"]
            if new_cat and (not new_cat in Category.objects.all()):
                new_category = Category.objects.create(name = new_cat)
                expense.category = new_category
            if expense.created_date.date()<expense.payment_date: expense.planned = True
            if form.cleaned_data["planned_monthly"]:
                for i in range(1, 3):
                    Expense.objects.create(author = expense.author, name = expense.name, amount = expense.amount, created_date = expense.created_date, category = expense.category, planned = True, payment_date =add_month(expense.payment_date, i))
            expense.save()
            phrase = ""
            if request.user == "Regina": phrase = phrases[randint(0, len(phrases))]
            if expense.planned: plan = 'Planned'
            messages.add_message(request, messages.SUCCESS, "%s Expense added%s!" %('Planned', phrase))
            return redirect('index')
    else:
        form = ExpenseForm()
    return render(request, 'bookkeeper/index.html', {'expenses': expenses, 'incomes': incomes,'form': form})

@login_required
def income_add(request):
    expenses = Expense.objects.all()[:5]
    incomes = Income.objects.all()[:5]
    
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.author = request.user
            if income.created_date.date()<income.income_date: income.planned = True
            if form.cleaned_data["planned_monthly"]:
                for i in range(1, 3):
                    Income.objects.create(author = income.author, name = income.name, amount = income.amount, created_date = income.created_date, planned = True, income_date = add_month(income.income_date, i))
            income.save()
            phrase = ""
            if request.user == "Regina": phrase = phrases[randint(0, len(phrases))]
            if income.planned: plan = 'Planned'
            messages.add_message(request, messages.SUCCESS, "%s Income added%s!" %('Planned', phrase))
            return redirect('income_add')
    else:
        form = IncomeForm()
    return render(request, 'bookkeeper/income_add.html', {'expenses': expenses, 'incomes': incomes, 'form':form})

class ExpenseList(generic.ListView):
    template_name = "/bookkeeper/expense_list.html"
    model = Expense
    queryset = Expense.objects.order_by("-created_date")
    paginate_by = 30

class IncomeList(generic.ListView):
    template_name = "/bookkeeper/income_list.html"
    model = Income
    paginate_by = 30

class CategoryList(generic.ListView):
    template_name = "/bookkeeper/category_list.html"
    model = Category

class ExpenseDayView(DayArchiveView):
    model = Expense
    date_field = "payment_date"
    template_name = "bookkeeper/expense_list_day.html"
    allow_future = True
    allow_empty = True
    month_format = "%m"

class ExpenseMonthView(MonthArchiveView):
    model = Expense
    date_field = "payment_date"
    template_name = "bookkeeper/summary_list.html"
    allow_empty = True
    allow_future = True
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
    allow_future = True
    allow_empty = True
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
        return context

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
                    if expense.created_date.date()<expense.payment_date: expense.planned = True
                    if form.cleaned_data["planned_monthly"]:
                        for i in range(1, 3):
                            Expense.objects.create(author = expense.author, name = expense.name, amount = expense.amount, created_date = expense.created_date, category = expense.category, planned = True, payment_date =add_month(expense.payment_date, i))
                    expense.save()
                    i+=1
        if i==1: 
            end = ""
        else: 
            end = "s"
        if i!=0: 
            messages.add_message(request, messages.SUCCESS, "%s expense%s added " %(i, end))
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
        if expense.created_date.date()<expense.payment_date: expense.planned = True
        if form.cleaned_data["planned_monthly"]:
            for i in range(1, 3):
                Expense.objects.create(author = expense.author, name = expense.name, amount = expense.amount, created_date = expense.created_date, category = expense.category, planned = True, payment_date =add_month(expense.payment_date, i))
        expense.save()
        phrase = ""
        if request.user == "Regina":  phrase = phrases[randint(0, len(phrases))]
        messages.add_message(self.request, messages.SUCCESS, "Expense added! %s" %phrase)
        return redirect('expense_list')
    

class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'bookkeeper/category_add.html'
    success_url = '/category_list'

class CategoryDelete(DeleteView):
    model = Category
    success_url = '/category_list'
    template_name = 'bookkeeper/confirm_delete.html'

class CategoryUpdate(UpdateView):
    model = Category
    form_class = CategoryForm
    success_url ='/category_list'
    template_name = 'bookkeeper/category_add.html'

class IncomeDelete(DeleteView):
    model = Income
    success_url = '/income_list/'
    template_name = 'bookkeeper/confirm_delete.html'

class IncomeUpdate(UpdateView):
    model = Income
    form_class = IncomeForm
    success_url ='/income_list'
    template_name = 'bookkeeper/income_add.html'
    
    def form_valid(self, form):
        income = form.save(commit=False)
        income.author = self.request.user
        if income.created_date.date() < income.income_date: income.planned = True
        if income.created_date.date() >= income.income_date: income.planned = False
        if form.cleaned_data["planned_monthly"]:
            for i in range(1, 3):
                Income.objects.create(author = income.author, name = income.name, amount = income.amount, created_date = income.created_date, planned = True, income_date = add_month(income.income_date, i))
        income.save()
        phrase = ""
        if request.user == "Regina": phrase = phrases[randint(0, len(phrases))]
        if income.planned: plan = 'Planned'
        messages.add_message(self.request, messages.SUCCESS, "%s Income updated%s!" %('Planned', phrase))
        income.save()
        return redirect('income_list')
    
class ExpenseDelete(DeleteView):
    model = Expense
    success_url = '/expense_list/'
    template_name = 'bookkeeper/confirm_delete.html'

class ExpenseUpdate(UpdateView):
    model = Expense
    form_class = ExpenseForm
    success_url ='/expense_list'
    template_name = 'bookkeeper/expense_add.html'
    
    def form_valid(self, form):
        expense = form.save(commit=False)
        new_cat = form.cleaned_data["new_cat"]
        if new_cat and (not new_cat in Category.objects.all()):
            new_category = Category.objects.create(name = new_cat)
            expense.category = new_category
        expense.author = self.request.user
        if timezone.now().date()<expense.payment_date: expense.planned = True
        if timezone.now().date()>=expense.payment_date: expense.planned = False
        if form.cleaned_data["planned_monthly"]:
            for i in range(1, 3):
                Expense.objects.create(author = expense.author, name = expense.name, amount = expense.amount, created_date = expense.created_date, category = expense.category, planned = True, payment_date =add_month(expense.payment_date, i))
        expense.save()
        messages.add_message(self.request, messages.SUCCESS, "Expense updated!")
        return redirect('expense_list')
    
class ExpenseCopy(UpdateView):
    model = Expense
    form_class = ExpenseForm
    success_url ='/expense_list'
    template_name = 'bookkeeper/expense_add.html'
    
    def form_valid(self, form):
        expense = form.save(commit=False)
        expense.pk = None
        expense.created_date = timezone.now()
        new_cat = form.cleaned_data["new_cat"]
        if new_cat and (not new_cat in Category.objects.all()):
            new_category = Category.objects.create(name = new_cat)
            expense.category = new_category
        expense.author = self.request.user
        if timezone.now().date() < expense.payment_date: expense.planned = True
        if timezone.now().date() >= expense.payment_date: expense.planned = False
        if form.cleaned_data["planned_monthly"]:
            for i in range(1, 3):
                Expense.objects.create(author = expense.author, name = expense.name, amount = expense.amount, created_date = expense.created_date, category = expense.category, planned = True, payment_date =add_month(expense.payment_date, i))
        expense.save()
        phrase = ""
        if self.request.user == "Regina": phrase = phrases[randint(0, len(phrases))]
        messages.add_message(self.request, messages.SUCCESS, "Expense added%s!" %phrase)
        return redirect('expense_list')

class IncomeCopy(UpdateView):
    model = Income
    form_class = IncomeForm
    success_url ='/income_list'
    template_name = 'bookkeeper/income_add.html'
    
    def form_valid(self, form):
        income = form.save(commit=False)
        income.pk = None
        income.created_date = timezone.now()
        income.author = self.request.user
        if income.created_date.date() < income.income_date: income.planned = True
        if income.created_date.date() >= income.income_date: income.planned = False
        if form.cleaned_data["planned_monthly"]:
            for i in range(1, 3):
                Income.objects.create(author = income.author, name = income.name, amount = income.amount, created_date = income.created_date, planned = True, income_date = add_month(income.income_date, i))

        income.save()
        messages.add_message(self.request, messages.SUCCESS, "Income added!:)")
        return redirect('income_list')

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


def add_month(date, your_month):
    year = date.year
    month = date.month
    day = date.day
    year+=int((month+your_month)//12.001)
    month = int(month+your_month-12*((month+your_month)//12.001))
    return datetime.date(year, month, day)


#month_list = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

phrases = [
    ', Любимая',
    ", моя Звездочка",
    ", моя Лапушка",
    ", мое Солнышко",
    ", Региночка",
    ", Женушка:)",
    ", Женушка:)",
    ", Женушка:)",
    ", мое Счастье",
    ", мое Сокровище",
    ", мое Чудо",
    ", моя Радость",
]

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
"""Планирование расходов:
1. Расход автоматически копируется на год вперед на определенное число каждого месяца
2. У запланированнгого расхода должна быть метка planned
3. По прошествии даты планирования должно появляться сообщение для подтверждения, был ли этот расход реально произведен
4. Запланированные расходы должны вноситься через отдельную форму, чтобы избежать путаницы. Или через ту же, для краткости?
5. Опция планирования расходов на определенную дату или ежемесячно
6. Функция копирования расходов +
"""
