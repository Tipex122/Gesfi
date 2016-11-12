from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Avg, Sum, Min, Max, Count

from django.contrib.auth.decorators import login_required

# Create your views here.

#TODO: le nom du compte n'est pas remonté car il est inclus ds chaque transaction mais pas dans la liste de transaction
#TODO: c'est le N° du compte qui doit générer le listing des transactions (?)

def accounts_info():
    accounts_info = Accounts.objects.annotate(total_amount_by_account = Sum('transactions__amount_of_transaction'),
                                       avg_amount_by_account = Avg('transactions__amount_of_transaction'),
                                       min_amount_by_account = Min('transactions__amount_of_transaction'),
                                       max_amount_by_account = Max('transactions__amount_of_transaction'),
                                       num_transac_by_account = Count('transactions'))
    return accounts_info


@login_required
def banks_and_accounts_list(request):
    banks_list = Banks.objects.all()
    accounts_list = Accounts.objects.all()
    #transactions_list = Transactions.objects.all()

    #account_total = 0

    #for transac_account in transaction_list:
    #    account_total += transac_account.amount_of_transaction
    #account_total = Transactions.objects.filter(account=account).aggregate(Sum('amount_of_transaction'))
    account_total = Transactions.objects.aggregate(Sum('amount_of_transaction'))

    # account_info = accounts_info()

    #for i in accounts_info:
    #    print('Amount by account: =+=+=+====>:', i.total_amount_by_account)
    #    print('Avg by account: =+=+=+====>:', i.avg_amount_by_account)
    #    print('Min by account: =+=+=+====>:', i.min_amount_by_account)
    #    print('Max by account: =+=+=+====>:', i.max_amount_by_account)
    #    print('Number of transaction by account: =+=+=+====>:', i.num_transac_by_account)

    #for account in accounts_list:
    #    print('Objet "account_total : ====> ', account_total)

    context = {'accounts_list': accounts_list, 'banks_list': banks_list, 'account_total': account_total, 'accounts_info': accounts_info() }
    return render(request, 'BanksAndAccounts/banks_and_accounts_list.html', context)


@login_required
def transactions_list(request):
    transaction_list = Transactions.objects.all()
    account_total = 0
    for transac_account in transaction_list:
        account_total += transac_account.amount_of_transaction

    #account_total = Transactions.objects.all().aggregate(sum('amount_of_transaction'))
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
    context = {'transactions': transactions, 'account_total': account_total, 'accounts': accounts, 'banks': banks,  'accounts_info': accounts_info()}
    return render(request, 'BanksAndAccounts/transactions_list.html', context)

@login_required
def transaction_detail(request, transaction_id):
    transaction = Transactions.objects.get(id=transaction_id)
    #bank = transaction.account.bank
    #account = transaction.account
    #context = {'bank':bank, 'account':account, 'transaction': transaction}
    #TODO: remonter la référence du compte (et son nom) ... voir la banque (via account_id)
    context = {'transaction': transaction}
    return render(request, 'BanksAndAccounts/transaction_detail.html', context)
    #return HttpResponse("You're looking at transaction: ==> %s." % transaction_id)


@login_required
def account_list(request, account_id):
    transaction_list = Transactions.objects.filter(account_id=account_id)

    #TODO: retrouver le nom du compte en fonction de la liste de transactions
    # name_of_account = Transactions.objects.filter(account_id=account_id).name_of_account

    account_total = 0
    for transac_account in transaction_list:
        #print('valeur de la transaction : ', transac_account.amount_of_transaction)
        account_total += transac_account.amount_of_transaction

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
    print('Objet "accounts" : ====> ', accounts)

    banks = Banks.objects.all()
    print('Objet "banks" : ====> ', banks)

    context = {'transactions': transactions, 'account_total':account_total,'accounts': accounts, 'banks': banks}
    return render(request, 'BanksAndAccounts/transactions_list.html', context)
