from django.db import models
# from decimal import Decimal
from categories.models import Category
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.


import datetime


class Banks(models.Model):
    name_of_bank = models.CharField(
        'Nom de la banque',
        default='Nom de la banque',
        max_length=256)

    num_of_bank = models.CharField(
        'Identifiant de la banque',
        default='Identifiant',
        max_length=256)

    def __str__(self):
        return "%s" % self.name_of_bank

    class Meta:
        verbose_name = _('bank')
        verbose_name_plural = _('banks')
        ordering = ['name_of_bank']


class Accounts(models.Model):
    name_of_account = models.CharField(
        'Nom du compte',
        default='Nom du compte en banque',
        max_length=256
    )

    def get_users(self):
        return "\n".join([u.username for u in User.objects.all()])

    num_of_account = models.CharField(
        'Identifiant du compte',
        default='Identifiant',
        max_length=256)
    # TODO: remplacement de null=True par models.CASCADE pour compatibilité Django 2.0 (à vérifier)
    bank = models.ForeignKey('Banks', null=True, blank=True)
    # bank = models.ForeignKey('Banks', models.CASCADE, blank=True)
    # owner_of_account = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # TODO: Il faut pouvoir affecter un User à un 'Bank account' (ce n'est pas le cas: tout le monde est 'owner'
    # Nota: remplacer "get_users" par "owner_of_account" dans "AccountsAdmin" pour revenir à la solution "ForeignKey"
    owner_of_account = models.ManyToManyField(User)

    def __str__(self):
        return "%s" % self.name_of_account

    class Meta:
        verbose_name = _('bank account')
        verbose_name_plural = _('bank accounts')
        ordering = ['name_of_account']


class Transactions(models.Model):
    date_of_transaction = models.DateField(
        'Date de la transaction',
        default=datetime.datetime.now)

    type_of_transaction = models.CharField(
        'Type de transaction',
        max_length=64)

    name_of_transaction = models.CharField('Fournisseur', max_length=256)

    amount_of_transaction = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Montant de la transaction ",
        blank=True, null=True)

    currency_of_transaction = models.CharField(
        'Devise',
        max_length=3)

    creation_date = models.DateField(
        'Date de saisie',
        default=datetime.datetime.now)

    # TODO: remplacement de null=True par models.CASCADE pour compatibilité Django 2.0 (à vérifier)
    account = models.ForeignKey('Accounts', null=True, blank=True)
    # account = models.ForeignKey('Accounts', models.CASCADE, blank=True)

    # TODO: remplacement de null=True par models.CASCADE pour compatibilité Django 2.0 (à vérifier)
    category_of_transaction = models.ForeignKey(
        Category,
        null=True,
        # models.CASCADE,
        blank=True)

    # transcat = models.ForeignKey(Category, null=True,
    # blank=True) #to be used in case of transversal categorization need

    #    def get_tags(self):
    #        tags = str.split(self.name_of_transaction)
    #        for tag in tags:
    #            tag = tag.lower(tag)
    #            if len(tag) < 2 or tag.isdecimal():
    #                tags.remove(self, tag)
    #        return tags

    def __str__(self):
        return "[%s] -- %s ===>  %s" % (
            self.date_of_transaction,
            self.name_of_transaction,
            self.amount_of_transaction,)

    #    def __init__(self):
    #        tags = self.tags
    #        super(Transactions, self).__init__(self, *args, **kwargs)

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')
        ordering = ['-date_of_transaction']
