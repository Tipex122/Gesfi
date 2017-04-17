#!/usr/bin/env python3
import sys, os
from django.conf import settings
import django
import csv

os.environ['DJANGO_SETTINGS_MODULE'] = 'gesfi.settings'

django.setup()

from banksandaccounts.models import *

# settings.configure()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# CSV_FILEPATHNAME = BASE_DIR + '/csv/compta.csv'
CSV_FILEPATHNAME = BASE_DIR + '/csv/00056149140-total-clean.csv'

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



print('************************************** ==> 1')


#from banksandaccounts.models import *
#Transactions, Accounts

# from django.core.management import setup_environ
# import settings
# setup_environ(settings)

print('************************************** ==> 2')

###dataReader = csv.reader(open(csv_filepathname), delimiter=';', quotechar='"')

with open(CSV_FILEPATHNAME, mode='r', buffering=-1, encoding='UTF-8') as gesfi_account:
    dataReader = csv.reader(gesfi_account, delimiter=';', quotechar='"')

#dataReader = csv.reader(open(CSV_FILEPATHNAME), delimiter=';', quotechar='"')

    print('************************************** ==> 3')


    if Accounts.objects.filter(num_of_account='00056149140'):
        compte = Accounts.objects.get(num_of_account = '00056149140' )

#    if Accounts.objects.filter(num_of_account=COMPTE):
#        compte = Accounts.objects.get(num_of_account=COMPTE)

    print('************************************** ==> 4')


    for row in dataReader:
        transactions = Transactions()

        ddmmyyyy = row[0]
        yyyymmdd = ddmmyyyy[6:] + "-" + ddmmyyyy[3:5] + "-" + ddmmyyyy[:2]

        #print(yyyymmdd)

        transactions.date_of_transaction = yyyymmdd

        transactions.type_of_transaction = row[1]
        transactions.name_of_transaction = row[2]

        transactions.amount_of_transaction = row[3].replace(',', '.')
        transactions.currency_of_transaction = row[4]
        transactions.account = compte
        #    transactions.bank_of_account = "Toto"
        transactions.save()
