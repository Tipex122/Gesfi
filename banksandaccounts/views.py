from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required

# Create your views here.

#TODO: le nom du compte n'est pas remonté car il est inclus ds chaque transaction mais pas dans la liste de transaction
#TODO: c'est le N° du compte qui doit générer le listing des transactions (?)

@login_required
def transactions_list(request):
    transaction_list = Transactions.objects.all()
    #Page de 25 lignes
    paginator = Paginator(transaction_list,25)
    page = request.GET.get('page')

    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        transactions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        transactions = paginator.page(paginator.num_pages)

    accounts = Accounts.objects.all()
    banks = Banks.objects.all()
    context = {'transactions': transactions, 'accounts': accounts, 'banks': banks}
    return render(request, 'BanksAndAccounts/transactions_list.html', context)
