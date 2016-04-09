from django.shortcuts import render
from .models import *

from django.contrib.auth.decorators import login_required

# Create your views here.

#TODO: le nom du compte n'est pas remonté car il est inclus ds chaque transaction mais pas dans la liste de transaction
#TODO: c'est le N° du compte qui doit générer le listing des transactions (?)

@login_required
def transactions_list(request):
    transactions = Transactions.objects.all()
    accounts = Accounts.objects.all()
    banks = Banks.objects.all()
    context = {'transactions': transactions, 'accounts': accounts, 'banks': banks }
    return render(request, 'BanksAndAccounts/transactions_list.html', context)
