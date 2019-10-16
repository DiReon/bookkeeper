from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Expense(models.Model):
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Description")
    amount = models.PositiveIntegerField(blank = True, null = True, verbose_name = "Amount")
    created_date = models.DateTimeField(default = timezone.now)
    payment_date = models.DateField(blank = True, null = True, verbose_name= "Payment date")
    comments = models.CharField(blank = True, null = True, max_length=200, verbose_name="Comments")
    category = models.ForeignKey(Category, blank = True, null = True, on_delete = models.SET_NULL, verbose_name = "Category")

    def __str__(self):
        return self.name

    def get_category(self):
        return self.get_category_display()

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"


class Income(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Description")
    amount = models.PositiveIntegerField(blank = True, null = True, verbose_name = "Amount")
    created_date = models.DateTimeField(default = timezone.now)
    received_date = models.DateField(blank = True, null = True, verbose_name= "Received date")
    comments = models.CharField(blank = True, null = True, max_length=200, verbose_name="Comments")    

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "Income"
        verbose_name_plural = "Incomes"


"""Описание приложения:
мы вносим маленькие расходы, указывая категорию каждого расхода. На главной страничке видим категории, при клике на категорию отображается детализация расходов в категории за указанный где-то период времени"""
