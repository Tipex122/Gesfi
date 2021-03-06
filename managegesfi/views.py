from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.db.models import Q
# from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from banksandaccounts.models import *
from categories.models import *
# from categories.forms import TagForm

# import re


# Create your views here.

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
        results = {'banks': Banks.objects.filter(Q(name_of_bank__icontains=querystring) |
                                                 Q(num_of_bank__icontains=querystring)),
                   'accounts': Accounts.objects.filter(Q(name_of_account__icontains=querystring) |
                                                       Q(num_of_account__icontains=querystring)),
                   'transactions': Transactions.objects.filter(
                       Q(name_of_transaction__icontains=querystring) |
                       Q(date_of_transaction__icontains=querystring) |
                       Q(type_of_transaction__icontains=querystring) |
                       Q(amount_of_transaction__icontains=querystring) |
                       Q(type_of_transaction__icontains=querystring)),
                   'categories': Category.objects.filter(Q(name__icontains=querystring) |
                                                         Q(description__icontains=querystring) |
                                                         Q(amount__icontains=querystring))}

        # results['transactions'] = Transactions.objects.filter(name_of_transaction__icontains=querystring, parent=None)
        # TODO: chercher la différence entre une recherche "Q()" et la notion de parent
        # TODO: chercher sur une date ... hé hé

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
def tag_category_edit(request):
    """
    Allocate a category to each transaction containing an identified Tag
    """
    categories_list = Category.objects.all()
    transactions_with_category = list()
    tags_list = Tag.objects.filter(will_be_used_as_tag=True)
    for tag in tags_list:
        transactions_with_tag = Transactions.objects.filter(name_of_transaction__icontains=tag.tag)
        if transactions_with_tag is not None:
            for transaction in transactions_with_tag:
                if tag.category is not None:
                    transaction.category_of_transaction = tag.category
                    transactions_with_category.append(transaction.name_of_transaction)
                    transaction.save()

    transactions = Transactions.objects.all()
    ancestors = Category.objects.filter(parent=None)
    context = {'transactions': transactions, 'categories_list': categories_list, 'ancestors':ancestors}
    return render(request, 'ManageGesfi/tag_category.html', context)


@login_required
def transactions_by_category(request, pk=None):
    """
    List of transactions by category.
    For all categories or category by category selected
    """
    # TODO: In transactions_by_category.html to list transactions of the catagory selected AND descendant of the category
    if pk == '' or get_object_or_404(Category, pk=pk).is_root_node():
        transactions = Transactions.objects.all().order_by('category_of_transaction__name')
        ancestors = Category.objects.filter(parent=None)
    else:
        category_selected = get_object_or_404(Category, pk=pk)
        ancestors = category_selected.get_ancestors(include_self=True)
        transactions = Transactions.objects.filter(category_of_transaction=category_selected)

    categories = Category.objects.all()

    context = {'transactions': transactions, 'ancestors':ancestors, 'categories': categories,}
    return render(request, 'ManageGesfi/transactions_by_category.html', context)

@login_required
def display_meta(request):
    values = request.META.items()
    # values.sort()
    html = []
    for k, v in values:
        html.append(
            '<tr><td>%s</td><td>%s</td></tr>' % (k,v)
        )
    return HttpResponse('<table>%s</table>' % '\n'.join(html))