from django.contrib import admin
from .models import Expense, Category, Income

admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(Category)

# Register your models here.
