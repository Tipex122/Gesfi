from django.db import models

# Create your models here.

from controlcenter import Dashboard, widgets
from banksandaccounts.models import *

class ModelItemList(widgets.ItemList):
    model = Transactions
    list_display = ('pk', 'name_of_transaction', 'amount_of_transaction','category_of_transaction')

class MyDashboard(Dashboard):
    widgets = (
        ModelItemList,
    )