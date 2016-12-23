from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from banksandaccounts.models import *
from categories.models import *

import re

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

@login_required
def search_keywords(request):
    transaction_list = Transactions.objects.all()
    list_of_tags = Tag.objects.all()

    listoftags = list()
    listoftags_found = list()

    if list_of_tags:
        for t in list_of_tags:
            t.tag.upper()   #In case we forgot to upperize at the very first time
            #t.is_new_tag = False   #Complicated to manage when updating/changing page
            #TODO: to automize new/old Tag without searching each time "new Tags"
            t.save()
            listoftags.append(t.tag)

    for transaction in transaction_list:
        keywords = re.findall(r'\b[a-z,A-Z,\']{3,15}\b', transaction.name_of_transaction)
        for keyword in keywords:
            keyword = keyword.upper()
            listoftags_found.append(keyword)

    #To get a list unique
    listoftags_found = set(listoftags_found)

    #Back to a list
    listoftags_found = list(listoftags_found)
    listoftags_found.sort(key=str.lower)


    tag_already_existing = list()
    tag_new = list()

    for l in listoftags_found:
        if Tag.objects.filter(tag=l):
            tag_already_existing.append(l)
        else:
            tag = Tag()
            tag.tag=l
            tag.is_new_tag = True
            tag.will_be_used_as_tag = True
            listoftags.append(l)
            tag_new.append(l)
            tag.save()

    listoftags.sort(key=str.lower)
    tag_already_existing.sort(key=str.lower)
    tag_new.sort(key=str.lower)

    listtag = Tag.objects.all()
    listtagnew = Tag.objects.filter(is_new_tag = True)
    list_of_categories = Category.objects.all()

    '''
    #TODO: to automize new/old Tag without searching each time "new Tags"
    #Page de 25 lignes
    paginator = Paginator(listtagnew,25)
    page = request.GET.get('page')

    try:
        listtagnew = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        listtagnew = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        listtagnew = paginator.page(paginator.num_pages)
    '''

    return render(request, 'ManageGesfi/keywords.html', {'tag_already_existing':tag_already_existing,
                                                         'tag_new': tag_new,
                                                         "listtag":listtag,
                                                         "listtagnew":listtagnew,
                                                         'list_of_categories':list_of_categories})

