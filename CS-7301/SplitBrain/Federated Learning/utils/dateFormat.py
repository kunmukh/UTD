#!/usr/bin/env python3.6

# Kunal Mukherjee
# 4/3/20
# Federated Learning of Encoders and word2vec


# utility to convert date to a desired format
# format the date in correct order
def getDate(date):

    format_date = date.replace("-", "_")
    year, month, date = format_date.split("_")

    if len(month) < 2:
        month = '0' + month
    if len(date) < 2:
        date = '0' + date
    if len(year) < 2:
        year = '0' + year

    return month + "_" + date + "_" + year