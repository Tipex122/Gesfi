from django.db import models
from decimal import Decimal

# Create your models here.


import datetime


class Banks(models.Model):
    name_of_bank = models.CharField('Nom de la banque', default = 'Nom de la banque', max_length=256)
    num_of_bank = models.CharField('Identifiant de la banque', default = 'Identifiant', max_length=256)

    def __str__(self):
        return "%s" %(self.name_of_bank)

    class Meta:
        verbose_name = 'bank'
        verbose_name_plural = 'banks'
        ordering = ['name_of_bank']


class Accounts(models.Model):
    name_of_account = models.CharField('Nom du compte', default = 'Nom du compte en banque', max_length=256)
    num_of_account = models.CharField('Identifiant du compte', default = 'Identifiant', max_length=256)
    bank = models.ForeignKey('Banks', null=True, blank=True)

    def __str__(self):
        return "%s" %(self.name_of_account)

    class Meta:
        ordering = ['name_of_account']


class Transactions(models.Model):
    date_of_transaction = models.DateField('Date de la transaction', default = datetime.datetime.now)
    type_of_transaction = models.CharField('Type de transaction', max_length=64)
    name_of_transaction = models.CharField('Fournisseur', max_length=256)
    amount_of_transaction = models.DecimalField(max_digits = 12, decimal_places = 2, default = Decimal('0.00'), verbose_name = "Montant de la transaction ", blank=True, null=True)
    currency_of_transaction = models.CharField('Devise',max_length=3)
    creation_date = models.DateField('Date de saisie', default = datetime.datetime.now)

    account = models.ForeignKey('Accounts', null=True, blank=True)

    def __str__(self):
        return "[%s] -- %s ===>  %s" % (self.date_of_transaction, self.name_of_transaction, self.amount_of_transaction, )

    class Meta:
        ordering = ['date_of_transaction']
