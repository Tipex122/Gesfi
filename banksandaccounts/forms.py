from django import forms
from .models import Transactions

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ('date_of_transaction',
                  'type_of_transaction',
                  'name_of_transaction',
                  'amount_of_transaction',
                  'currency_of_transaction',
                  # 'account',
                  'category_of_transaction',)