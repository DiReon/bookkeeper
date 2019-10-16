from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
                path('', login_required(views.ExpenseList.as_view()), name='expense_list'),
                path('search_results/', login_required(views.SearchResultsView.as_view()), name='search_results'),
                path('category_list/', login_required(views.CategoryList.as_view()), name='category_list'),
                url(r'^(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/$', login_required(views.ExpenseDayView.as_view()), name='expense_day'),
                url(r'^(?P<year>\d{4})/(?P<month>\d+)/$', login_required(views.ExpenseMonthView.as_view()), name='expense_month'),
                url(r'^(?P<year>\d{4})/(?P<month>\d+)/(?P<cat>.+)/$', login_required(views.ExpenseMonthCategoryView.as_view()), name='expense_month_category'),
                #path('summary_list/', views.SummaryListView.as_view(), name='summary_list'),
                path('<int:pk>/expense_delete/', login_required(views.ExpenseDelete.as_view()), name = 'expense_delete'),
                path('<int:pk>/category_delete/', login_required(views.CategoryDelete.as_view()), name = 'category_delete'),
                path('expense_delete_all/', views.expense_delete_all, name = 'expense_delete_all'),
                path('<int:pk>/expense_update/', login_required(views.ExpenseUpdate.as_view()), name="expense_update"),
                path('<int:pk>/category_update/', login_required(views.CategoryUpdate.as_view()), name="category_update"),
                #path('<int:pk>/expense_edit/', views.expense_edit, name="expense_edit"),
                path('expense_add/', login_required(views.ExpenseCreate.as_view()), name="expense_add"),
                path('category_add/', login_required(views.CategoryCreate.as_view()), name="category_add"),
                path('expense_add_formset/', views.expense_add_formset, name="expense_add_formset"),
                path('expense_test_add/', views.expense_test_add, name="expense_test_add"),
]

