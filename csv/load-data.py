#!/usr/bin/env python
import sys, os
from django.conf import settings

import csv

# settings.configure()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# CSV_FILEPATHNAME = BASE_DIR + '/csv/compta.csv'
CSV_FILEPATHNAME = BASE_DIR + '/csv/00056149140.csv'

# TODO: récupérer le nom du fichier qui est aussi le numéro du compte
# COMPTE = os.path.basename(__file__)
COMPTE = os.path.basename(CSV_FILEPATHNAME).split('.')[0]

print('**************************************')
print(BASE_DIR)
print(CSV_FILEPATHNAME)
print(COMPTE)
print('**************************************')

# Full path and name to your csv file
###csv_filepathname = "/home/xavier/Programmation/djangogirls/mysite/csv/compta.csv"
# Full path to your django project directory
###your_djangoproject_home = "/home/xavier/Programmation/djangogirls/mysite/"


###sys.path.append(your_djangoproject_home)
sys.path.append(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from gesfi.models import Transactions, Accounts

# from django.core.management import setup_environ
# import settings
# setup_environ(settings)

###dataReader = csv.reader(open(csv_filepathname), delimiter=';', quotechar='"')
dataReader = csv.reader(open(CSV_FILEPATHNAME), delimiter=';', quotechar='"')

# if Accounts.objects.filter(num_of_account='00056149140'):
#    compte = Accounts.objects.get(num_of_account = '00056149140' )

if Accounts.objects.filter(num_of_account=COMPTE):
    compte = Accounts.objects.get(num_of_account=COMPTE)

for row in dataReader:
    transactions = Transactions()

    ddmmyyyy = row[0]
    yyyymmdd = ddmmyyyy[6:] + "-" + ddmmyyyy[3:5] + "-" + ddmmyyyy[:2]
    transactions.date_of_transaction = yyyymmdd

    transactions.type_of_transaction = row[1]
    transactions.name_of_transaction = row[2]

    transactions.amount_of_transaction = row[3].replace(',', '.')
    transactions.currency_of_transaction = row[4]
    transactions.account = compte
    #    transactions.bank_of_account = "Toto"
    transactions.save()
