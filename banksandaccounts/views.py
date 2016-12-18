from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Avg, Sum, Min, Max, Count

from django.contrib.auth.decorators import login_required

# Create your views here.

def accounts_info(account_id=0):
    if account_id == 0:
        accounts_info = Accounts.objects.annotate(total_amount_by_account = Sum('transactions__amount_of_transaction'),
                                           avg_amount_by_account = Avg('transactions__amount_of_transaction'),
                                           min_amount_by_account = Min('transactions__amount_of_transaction'),
                                           max_amount_by_account = Max('transactions__amount_of_transaction'),
                                           num_transac_by_account = Count('transactions'))
    elif account_id != 0:
        accounts_info = Accounts.objects.filter(id=account_id).annotate(total_amount_by_account=Sum('transactions__amount_of_transaction'),
                                                  avg_amount_by_account=Avg('transactions__amount_of_transaction'),
                                                  min_amount_by_account=Min('transactions__amount_of_transaction'),
                                                  max_amount_by_account=Max('transactions__amount_of_transaction'),
                                                  num_transac_by_account=Count('transactions'))
    return accounts_info


@login_required
def banks_and_accounts_list(request):
    banks_list = Banks.objects.all()
    accounts_list = Accounts.objects.all()
    account_total = Transactions.objects.aggregate(total = Sum('amount_of_transaction'))

    context = {'accounts_list': accounts_list, 'banks_list': banks_list,
               'account_total': account_total, 'accounts_info': accounts_info() }
    return render(request, 'BanksAndAccounts/banks_and_accounts_list.html', context)


@login_required
def transactions_list(request):
    banks = Banks.objects.all()
    accounts = Accounts.objects.all()
    transaction_list = Transactions.objects.all()
    account_total = Transactions.objects.aggregate(Sum('amount_of_transaction'))

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
    #TODO: vérifier si on a vraiment besoin de tout ce contexte
    #all_accounts is used for sidebar - accounts_info is used for selection of one account
    context = {'banks': banks,                      #used for dispatching accounts by bank in sidebar
               #'accounts': accounts,                # ???
               'transactions': transactions,        #used to list transactions related to account(s)
               'account_total': account_total,      #sum of all transactions ==> not really used in fact
               'accounts_info': accounts_info(0),   #general information related to all accounts (due to "0")
               'all_accounts': accounts_info(0)     #general information related to all accounts (due to "0") and used in sidebar
               }
    return render(request, 'BanksAndAccounts/transactions_list.html', context)

@login_required
def account_list(request, account_id):
    transaction_list = Transactions.objects.filter(account_id=account_id)

    account_total = Transactions.objects.filter(account_id=account_id).aggregate(Sum('amount_of_transaction'))

    # Page de 25 lignes
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

    context = {'banks': banks,                              #used for dispatching accounts by bank in sidebar
               #'accounts': accounts,
               'transactions': transactions,                #used to list transactions related to account(s)
               'account_total':account_total,               #sum of all transactions ==> not really used in fact
               'accounts_info': accounts_info(account_id),  #general information related to selectede account
               'all_accounts': accounts_info(0)             #general information related to alla accounts (due to "0") and used in sidebar
               }

    return render(request, 'BanksAndAccounts/transactions_list.html', context)

@login_required
def transaction_detail(request, transaction_id):
    transaction = Transactions.objects.get(id=transaction_id)
    context = {'transaction': transaction}
    return render(request, 'BanksAndAccounts/transaction_detail.html', context)
