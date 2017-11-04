from django import forms
from .models import Accounts, Transactions
from categories.models import Category

from mptt.forms import TreeNodeChoiceField


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ('date_of_transaction',
                  'type_of_transaction',
                  'name_of_transaction',
                  'amount_of_transaction',
                  'currency_of_transaction',
                  'account',
                  'category_of_transaction',
                  )
    category_of_transaction = TreeNodeChoiceField(queryset=Category.objects.all(), level_indicator=u'+--')
    # TODO: How to obtain the list of accounts only available for the connected user ?
    # account = forms.ChoiceField(queryset=Accounts.objects.all().filter(owner_of_account=request.user))
