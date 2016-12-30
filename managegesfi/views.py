from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from banksandaccounts.models import *
from categories.models import *
from categories.forms import TagForm

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


    for l in listoftags_found:
        if l not in listoftags:
            tag = Tag()
            tag.tag=l
            tag.is_new_tag = True
            tag.will_be_used_as_tag = True
            listoftags.append(l)
            tag.save()

    listoftags.sort()

    listtagnew = Tag.objects.filter(is_new_tag = True)

    return render(request, 'ManageGesfi/keywords.html', {"listtagnew":listtagnew,})

@login_required
def tag_edit(request,pk):
    tags_list = Tag.objects.filter(will_be_used_as_tag = True)

    if pk == '':
        transactions = Transactions.objects.all()
        tag = None
    else:
        tag = get_object_or_404(Tag, pk=pk)
        transactions = Transactions.objects.filter(name_of_transaction__icontains = tag.tag)


    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)

        if form.is_valid():
            tag = form.save(commit = False)
            tag.is_new_tag=False
            tag.will_be_used_as_tag = True
            tag.save()
            return redirect('tag_edit', pk=tag.pk)
    else:
        form = TagForm(instance=tag)

    context = {'transactions': transactions, 'tags_list': tags_list, 'tag':tag, 'form': form}
    return render(request, 'ManageGesfi/tag_edit.html', context)

