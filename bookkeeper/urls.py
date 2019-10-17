from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
                #Main page with expense adding form and list of recent items
                path('', views.index, name='index'),
                #List views
                path('expense_list/', login_required(views.ExpenseList.as_view()), name='expense_list'),
                path('income_list/', login_required(views.IncomeList.as_view()), name='income_list'),
                path('category_list/', login_required(views.CategoryList.as_view()), name='category_list'),
                #Month and day views
                url(r'^(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/$', login_required(views.ExpenseDayView.as_view()), name='expense_day'),
                url(r'^(?P<year>\d{4})/(?P<month>\d+)/$', login_required(views.ExpenseMonthView.as_view()), name='expense_month'),
                url(r'^(?P<year>\d{4})/(?P<month>\d+)/(?P<cat>.+)/$', login_required(views.ExpenseMonthCategoryView.as_view()), name='expense_month_category'),
                #Adding items
                path('expense_add/', login_required(views.ExpenseCreate.as_view()), name="expense_add"),
                path('income_add/', views.income_add, name="income_add"),
                path('category_add/', login_required(views.CategoryCreate.as_view()), name="category_add"),
                path('expense_add_formset/', views.expense_add_formset, name="expense_add_formset"),
                #Updating items
                path('<int:pk>/expense_update/', login_required(views.ExpenseUpdate.as_view()), name="expense_update"),
                path('<int:pk>/income_update/', login_required(views.IncomeUpdate.as_view()), name="income_update"),
                path('<int:pk>/category_update/', login_required(views.CategoryUpdate.as_view()), name="category_update"),
                #Deleting items
                path('<int:pk>/expense_delete/', login_required(views.ExpenseDelete.as_view()), name = 'expense_delete'),
                path('<int:pk>/category_delete/', login_required(views.CategoryDelete.as_view()), name = 'category_delete'),
                path('<int:pk>/income_delete/', login_required(views.IncomeDelete.as_view()), name = 'income_delete'),
                #Miscellenious
                path('search_results/', login_required(views.SearchResultsView.as_view()), name='search_results'),
                #Only for testing purposes
                path('expense_delete_all/', views.expense_delete_all, name = 'expense_delete_all'),
                path('expense_test_add/', views.expense_test_add, name="expense_test_add"),
]

