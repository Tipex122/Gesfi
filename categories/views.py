# from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required

# from .models import Category
from banksandaccounts.models import *
from .models import *
from .forms import TagForm


# Create your views here.


def category_list(request):
    categories = Category.objects.all()
    jsondata = serializers.serialize('json', categories)
    context = {'categories': categories, 'jsondata': jsondata}
    return render(request, 'Categories/categories_list.html', context)


def category_json(request):
    categories = Category.objects.all()
    return HttpResponse(serializers.serialize('json', categories), content_type="application/json")


LIST_HEADERS_SEARCH_TAGS = (
    ('Name', 'tag'),
    ('New Tag', 'is_new_tag'),
    ('Used as Tag', 'will_be_used_as_tag'),
    ('Category', 'category'),
)


@login_required
def search_tags(request):
    sort_headers = SortHeaders(request, LIST_HEADERS_SEARCH_TAGS)
    transaction_list = Transactions.objects.all()
    list_of_tags = Tag.objects.all()

    listoftags = list()
    listoftags_found = list()

    if list_of_tags:
        for t in list_of_tags:
            t.tag.upper()  # In case we forgot to upperize at the very first time
            # t.is_new_tag = False   #Complicated to manage when updating/changing page
            # TODO: to automize new/old Tag without searching each time "new Tags"
            t.save()
            listoftags.append(t.tag)

    for transaction in transaction_list:
        key_tags = transaction.name_of_transaction.split()
        for key_tag in key_tags:
            if len(key_tag) > 2 and key_tag.isalpha():
                # print ('=====> ', key_tag)
                key_tag = key_tag.upper()
                if key_tag not in listoftags_found:
                    key_tag.strip(',')
                    listoftags_found.append(key_tag)

                    # keywords = re.findall(r'\b[a-z,A-Z,\']{3,15}\b', transaction.name_of_transaction)
                    # for keyword in keywords:
                    #    keyword = keyword.upper()
                    #    listoftags_found.append(keyword)

    # To get a list unique
    # listoftags_found = set(listoftags_found)

    # Back to a list
    # listoftags_found = list(listoftags_found)

    for tag_found in listoftags_found:
        if tag_found not in listoftags:
            tag = Tag()
            tag.tag = tag_found
            tag.is_new_tag = True
            tag.will_be_used_as_tag = True
            listoftags.append(tag_found)
            tag.save()
            # listoftags.sort()

    listtagnew = Tag.objects.order_by(sort_headers.get_order_by()).filter(is_new_tag=True)
    #    listtagnew = Tag.objects.order_by(sort_headers.get_order_by())

    list_of_headers = list(sort_headers.headers())

    context = {
        "listtagnew": listtagnew,
        'headers': list_of_headers,
    }

    return render(request, 'Categories/search_tags.html', context)


LIST_HEADERS_EDIT_TAG = (
    ('Date', 'date_of_transaction'),
    ('Type', 'type_of_transaction'),
    ('Name', 'name_of_transaction'),
    ('Amount', 'amount_of_transaction'),
)


@login_required
def tag_edit(request, pk):
    sort_headers = SortHeaders(request, LIST_HEADERS_EDIT_TAG)
    tags_list = Tag.objects.filter(will_be_used_as_tag=True)

    if pk == '':
        transactions = Transactions.objects.order_by(sort_headers.get_order_by())
        tag = None
    else:
        tag = get_object_or_404(Tag, pk=pk)
        transactions = Transactions.objects.order_by(sort_headers.get_order_by()).filter(
            name_of_transaction__icontains=tag.tag)

    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)

        if form.is_valid():
            tag = form.save(commit=False)
            tag.is_new_tag = False
            tag.will_be_used_as_tag = True
            tag.save()
            return redirect('tag_edit', pk=tag.pk)
    else:
        form = TagForm(instance=tag)

    list_of_headers = list(sort_headers.headers())

    context = {
        'transactions': transactions,
        'tags_list': tags_list,
        'tag': tag,
        'form': form,
        'headers': list_of_headers,
    }
    return render(request, 'Categories/tag_edit.html', context)

'''
@login_required
def show_category(request, hierarchy=None):
    # Attention: à mettre à jour par la parent de la hierarchy (voir comment le trouver avec MPTT

    nodes = Category.objects.all()

    print(hierarchy)

    if hierarchy == 'None':
        hierarchy = "Budget"
    print("Hierarchy après affectation de Budget: {}".format(hierarchy))

    category_slug = hierarchy.split('/')
    print(category_slug)

    parent = None
    root = Category.objects.all()
    print("***************** 1 ****************")
    print(root)
    print("***************** 1 ****************")


    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug=slug)
        print("================== 1 =======================")
        print(parent)
        print("================== 1 =======================")


    try:
        instance = Category.objects.get(parent=parent,slug=category_slug[-1])
        print(parent)
        # print(slug)
    except:
        # instance = get_object_or_404(Post, slug = category_slug[-1])
        instance = get_object_or_404(Category, slug = category_slug[-1])
        return render(request, "Categories/categoryDetail.html", {'instance': instance,})
    else:
        return render(request, 'Categories/categories.html', {'instance': instance, 'nodes': nodes})
'''

@login_required
def show_category(request, node=None):

    cats = Category.objects.all()
    # used for template recursetree in sidebar block

    #print("Categories -----------------: \n {}".format(cat))

    #print("Node -----------------: \n {}".format(node))

    node = node.split('/')


    #print("Node après split ++++++++++++++++++++: \n {}".format(node))
    #print("Node[-1]         ++++++++++++++++++++: \n {}".format(node[-1]))

    current = Category.objects.filter(name=node[-1])
    #print("Current 000000 -----------------: \n {}".format(current))
    #print("Current 000000 Ancestors -----------------: \n {}".format(current.get_ancestors(include_self=True)))

    #nodes = Category.objects.filter(parent=None)
    #print("Nodes -----------------: \n {}".format(nodes))

    if node[-1] == 'None' : #'Budget':
        # ancestors = nodes

        current = Category.objects.filter(parent=None)
        #print("Current -----------------: \n {}".format(current))

        ancestors = Category.objects.filter(parent=None)
        #print("Ancestors pour node ========================: \n {}".format(ancestors))
        # node = ancestors
        # children = Category.objects.filter(parent=None)
        children = Category.objects.filter(parent=ancestors)
        #print("Children pour node[-1] ========================: \n {}".format(children))

        # toto = Category.objects.filter(parent=None)
        #toto = current.get_ancestors(include_self=True)
        # toto = Category.objects.get(pk=1)
        #print("Toto :::::::::::::::::: \n {}".format(toto))

    else:
        #if node[-1] in node[:-1]:
        #    node = node[:-1]
        # node = set(node)
        #print("Node +++         ++++++++++++++++++++: \n {}".format(node))
        #print("Node[-1] +++         ====================: \n {}".format(node[-1]))
        #print("Node[:-1] +++         ++++++++++++++++++++: \n {}".format(node[:-1]))

        current = Category.objects.filter(name=node[-1])
        #print("Current -----------------: \n {}".format(current))

        children = Category.objects.filter(parent__name=node[-1]) # mettre un get avec un contrôle d'existence
        #print("Children -----------------: \n {}".format(children))

        #ancestors = Category.objects.filter(children__name=node[-1])
        ancestors = current.get_ancestors()
        #print("Ancestors -----------------: \n {}".format(ancestors))

        if not ancestors:
            ancestors = current
            #print("Ancestors 222222 -----------------: \n {}".format(ancestors))
        else:
            ancestors = current.get_ancestors(include_self=True)
        #print("GET_ANCESTORS ------+++++--------: \n".format(children[0].get_ancestors()))

        #toto = Category.objects.filter(name=node[-1]).get_ancestors(include_self=True)
        #print("TOTOTOTOTOTOTOTOTOTO: \n {}".format(toto))


    return render(request, 'Categories/categories2.html',
                  {'cats': cats,
                   'ancestors': ancestors,
                   'children': children,
                   #'node': node,
                   #'toto': toto,
                   'current': current,
                   })
