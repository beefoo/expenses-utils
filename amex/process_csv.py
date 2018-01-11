# -*- coding: utf-8 -*-

import argparse
import csv
import os
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="transactions/transactions_2017-10.csv", help="Path to CSV file with transactions")
parser.add_argument('-vendor', dest="VENDOR_FILE", default="vendors.csv", help="Path to vendor file")

args = parser.parse_args()

INPUT_FILE = args.INPUT_FILE
VENDOR_FILE = args.VENDOR_FILE
OUTPUT_FILE = INPUT_FILE.replace(".csv", "_processed.csv")

HEADINGS = ["Date", "Payer", "Description", "Vendor", "Category", "Amount"]

def parseNumber(string):
    try:
        num = float(string)
        return num
    except ValueError:
        return string

def parseNumbers(arr):
    for i, item in enumerate(arr):
        for key in item:
            arr[i][key] = parseNumber(item[key])
    return arr

def readCSV(filename):
    rows = []
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            rows = parseNumbers(rows)
    return rows

def getTransaction(row, vendors):
    t = False

    vendorString = row[2].lower()
    vendor = False
    for v in vendors:
        match = v["Match"].lower()
        if vendorString.startswith(match):
            vendor = v
            break

    if vendor:
        t = vendor.copy()
        t["Date"] = row[0].split(" ")[0]
        t["Amount"] = float(row[7])

    return t

vendors = readCSV(VENDOR_FILE)
vHeadings = [h for h in vendors[0]]
for h in vHeadings:
    if h != "Match" and h not in HEADINGS:
        HEADINGS.append(h)

transactions = []
with open(INPUT_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=",")
    for row in rows:
        t = getTransaction(row, vendors)
        if t:
            transactions.append(t)

with open(OUTPUT_FILE, 'w') as f:
    w = csv.writer(f)
    # w.writerow(HEADINGS)
    for t in transactions:
        row = []
        for h in HEADINGS:
            row.append(t[h])
        w.writerow(row)
    print "Wrote %s rows to %s" % (len(transactions), OUTPUT_FILE)
