from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from banksandaccounts.models import *
from categories.models import *

# Create your views here.
def site_login(request):
    pass

@login_required
def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if len(querystring) == 0:
            return redirect('/search/')

        try:
            search_type = request.GET.get('type')
            if search_type not in ['banks', 'accounts', 'transactions', 'categories']:
                search_type = 'banks'

        except Exception:
            search_type = 'banks'

        count = {}
        results = {}

        results['banks'] = Banks.objects.filter(Q(name_of_bank__icontains=querystring) |
                                                Q(num_of_bank__icontains=querystring))

        results['accounts'] = Accounts.objects.filter(Q(name_of_account__icontains=querystring) |
                                                      Q(num_of_account__icontains=querystring))

        #results['transactions'] = Transactions.objects.filter(name_of_transaction__icontains=querystring, parent=None)
        #TODO: chercher la différence entre une recherche "Q()" et la notion de parent
        #TODO: chercher sur une date ... hé hé
        results['transactions'] = Transactions.objects.filter(Q(name_of_transaction__icontains=querystring) |
                                                            Q(date_of_transaction__icontains=querystring) |
                                                            Q(type_of_transaction__icontains=querystring) |
                                                                Q(amount_of_transaction__icontains=querystring) |
                                                              Q(type_of_transaction__icontains=querystring))

        results['categories'] = Category.objects.filter(Q(name__icontains=querystring) |
                                                        Q(description__icontains=querystring) |
                                                        Q(amount__icontains=querystring))

        #results['users'] = User.objects.filter(Q(username__icontains=querystring) |
        #                                       Q(first_name__icontains=querystring) |
        #                                       Q(last_name__icontains=querystring))

        count['banks'] = results['banks'].count()
        count['accounts'] = results['accounts'].count()
        count['transactions'] = results['transactions'].count()
        count['categories'] = results['categories'].count()


        return render(request, 'ManageGesfi/results.html', {
            'hide_search': True,
            'querystring': querystring,
            'active': search_type,
            'count': count,
            'results': results[search_type],
        })
    else:
        return render(request, 'ManageGesfi/search.html', {'hide_search': True})
