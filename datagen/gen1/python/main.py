"""
Usage:
  python main.py gen_customers <count>
  python main.py gen_products <count>
  python main.py gen_aus_online_txn 2021-02-25 2022-02-25 100 > data\online_txn.json
  python main.py gen_aus_flybuy_txn 2021-02-25 2022-02-25 100 > data\flybuy_txn.json
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "February 2022"

import csv
import json
import os
import random
import sys
import uuid

import arrow 

from docopt import docopt

from faker import Faker  # https://faker.readthedocs.io/en/master/index.html

from pysrc.env import Env
from pysrc.excel import Excel
from pysrc.fs import FS
from pysrc.template import Template


def gen_customers(count):
    print('gen_customers, {}'.format(count))
    fake = Faker()
    json_lines = list()

    for idx in range(count):
        first = fake.first_name().replace(',',' ')
        last  = fake.last_name().replace(',',' ')
        obj = dict()
        obj['customer_id'] = str(uuid.uuid4())
        obj['first_name'] = first
        obj['last_name'] = last
        obj['full_name'] = '{} {}'.format(first, last)
        obj['address'] = fake.street_address().replace(',',' ')
        obj['city'] = fake.city()
        obj['state'] = fake.state_abbr()
        json_lines.append(json.dumps(obj))

    write_lines('data/customers.json', json_lines)

def gen_products(count):
    print('gen_products, {}'.format(count))
    fake = Faker()
    json_lines = list()
    upc_dict = dict()

    for idx in range(count):
        upc   = random_upc(upc_dict, fake)
        price = random_price(fake)
        obj = dict()
        obj['seq_num'] = idx + 1
        obj['upc']   = random_upc(upc_dict, fake)
        obj['desc']  = ' '.join(fake.words(nb=5)).strip()
        obj['price'] = float('{:.2f}'.format(price))
        json_lines.append(json.dumps(obj))

    write_lines('data/products.json', json_lines)

def gen_aus_online_txn(start_date, end_date, avg_per_day):
    calendar_days = read_csv('data/calendar.csv')
    customers = read_json_objects('data/customers.json')
    products  = read_json_objects('data/products.json')
    min = int(float(avg_per_day * 0.75))
    max = int(float(avg_per_day * 1.25))

    for date_row in calendar_days:
        date = date_row[1] 
        if date >= start_date:
            if date <= end_date:
                count = random.randint(min, max)
                for i in range(count):
                    now = arrow.utcnow()
                    customer = random_list_element(customers)
                    product  = random_list_element(products)
                    id_pk = str(uuid.uuid4())
                    txn = dict()
                    txn['id'] = id_pk
                    txn['pk'] = id_pk
                    txn['ccpID'] = customer['customer_id']
                    txn['productID'] = product['upc']
                    txn['productDesc'] = product['desc']
                    txn['productQty'] = random_int(1, 5)
                    txn['transactionDate'] = random_utc_time(date)
                    print(json.dumps(txn))

def gen_aus_flybuy_txn(start_date, end_date, avg_per_day):
    calendar_days = read_csv('data/calendar.csv')
    customers = read_json_objects('data/customers.json')
    products  = read_json_objects('data/products.json')
    min = int(float(avg_per_day * 0.75))
    max = int(float(avg_per_day * 1.25))

    for date_row in calendar_days:
        date = date_row[1] 
        if date >= start_date:
            if date <= end_date:
                count = random.randint(min, max)
                for i in range(count):
                    now = arrow.utcnow()
                    customer = random_list_element(customers)
                    product  = random_list_element(products)
                    id_pk = str(uuid.uuid4())
                    txn = dict()
                    txn['id'] = id_pk
                    txn['pk'] = id_pk
                    txn['flybuyID'] = customer['customer_id']
                    txn['productID'] = product['upc']
                    txn['productDesc'] = product['desc']
                    txn['productQty'] = random_int(1, 5)
                    txn['transactionDate'] = random_utc_time(date)
                    print(json.dumps(txn))

def random_int(min, max):
    return random.randint(min, max)

def random_list_element(elements):
    idx = random.randint(0, len(elements) - 1)
    return elements[idx]

def random_utc_time(date):
    epoch = random_int(0, 1645824823)
    tokens = str(arrow.get(epoch)).split('T')
    tokens[0] = date
    return 'T'.join(tokens)

def random_zero_padded_int(min, max):
    i = random_int(min, max)
    if i < 10:
        return '0{}'.format(i)
    else:
        return str(i)

def random_utc_seconds():
    f = random.uniform(1.5, 1.9)


def random_upc(upc_dict, fake):
    continue_to_process = True
    while continue_to_process:
        ean = fake.localized_ean13()
        if ean in upc_dict.keys():
            pass # try again
        else:
            upc_dict[ean] = ean
            continue_to_process = False
            return ean

def random_price(fake):
    # pyfloat(left_digits=None, right_digits=None, positive=False, min_value=None, max_value=None)
    return fake.pyfloat(positive=True, min_value=1, max_value=1500)

def read_json_objects(infile):
    objects = list()
    it = text_file_iterator(infile)
    for i, line in enumerate(it):
        s = line.strip()
        if len(s) > 3:
            obj = json.loads(line.strip())
            objects.append(obj)        
    return objects

def text_file_iterator(infile):
    # return a line generator that can be iterated with iterate()
    with open(infile, 'rt') as f:
        for line in f:
            yield line.strip()

def write_lines(outfile, lines):
    with open(outfile, 'wt') as out:
        for line in lines:
            out.write("{}{}".format(line.strip(), "\n"))
    print('file_written: {}'.format(outfile))

def read_csv(infile, reader='default', delim=',', dialect='excel', skip=0):
    rows = list()
    if reader == 'dict':
        with open(infile, 'rt') as csvfile:
            rdr = csv.DictReader(csvfile, dialect=dialect, delimiter=delim)
            for row in rdr:
                rows.append(row)
    else:
        with open(infile) as csvfile:
            rdr = csv.reader(csvfile, delimiter=delim)
            for idx, row in enumerate(rdr):
                if idx >= skip:
                    rows.append(row)
    return rows

def read_json(infile):
    with open(infile, 'rt') as f:
        return json.loads(f.read())

def write_obj_as_json_file(outfile, obj):
    txt = json.dumps(obj, sort_keys=False, indent=2)
    with open(outfile, 'wt') as f:
        f.write(txt)
    print("file written: " + outfile)

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)


if __name__ == "__main__":
  func = sys.argv[1].lower()

  if func == 'gen_customers':
      count = int(sys.argv[2])
      gen_customers(count)

  elif func == 'gen_products':
      count = int(sys.argv[2])
      gen_products(count)

  elif func == 'gen_aus_online_txn':
      start_date = sys.argv[2]
      end_date   = sys.argv[3]
      avg_per_day = int(sys.argv[4])
      gen_aus_online_txn(start_date, end_date, avg_per_day)

  elif func == 'gen_aus_flybuy_txn':
      start_date = sys.argv[2]
      end_date   = sys.argv[3]
      avg_per_day = int(sys.argv[4])
      gen_aus_flybuy_txn(start_date, end_date, avg_per_day)
  else:
      print_options('Error: invalid function: {}'.format(func))
