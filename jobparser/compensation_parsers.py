import re
import numpy as np


def compensation_parser(item):
    item['compensation_min'] = np.nan
    item['compensation_max'] = np.nan
    item['compensation_currency'] = np.nan

    if (item['compensation'] == np.nan) or (item['compensation'] == 'з/п не указана'):
        return item

    compensation_tt = str(item['compensation'])
    compensation_tt = compensation_tt.replace(u'\xa0', ' ')

    fr = re.search('(на руки)', compensation_tt)  # drop 'на руки'
    if fr:
        compensation_tt = compensation_tt.replace(fr[0], '')

    numbers = '[\d+\s]*\d+'  # pattern for number values

    fr = re.search(f'^[\s]*от {numbers}', compensation_tt)  # 'от 30 000'
    if fr:
        item['compensation_min'] = float(fr[0][3:].replace(' ', ''))
        compensation_tt = compensation_tt.replace(fr[0], '')

    fr = re.search(f'^[\s]*{numbers}[\s]*[\-—]+', compensation_tt)  # '30 000-'
    if fr:
        item['compensation_min'] = float(fr[0][:-1].replace(' ', ''))
        compensation_tt = compensation_tt.replace(fr[0], '-')

    fr = re.search(f'^[\s]*до {numbers}', compensation_tt)  # 'до 30 000'
    if fr:
        item['compensation_max'] = float(fr[0][3:].replace(' ', ''))
        compensation_tt = compensation_tt.replace(fr[0], '')

    fr = re.search(f'^[\s]*[\-—]+[\s]*{numbers}', compensation_tt)  # '-30 000'
    if fr:
        item['compensation_max'] = float(fr[0][1:].replace(' ', ''))
        compensation_tt = compensation_tt.replace(fr[0], '')

    fr = re.search(f'^[\s]*{numbers}', compensation_tt)  # '30 000'
    if fr:
        item['compensation_max'] = float(fr[0].replace(' ', ''))
        item['compensation_min'] = float(fr[0].replace(' ', ''))
        compensation_tt = compensation_tt.replace(fr[0], '')

    item['compensation_currency'] = compensation_tt  # the rest to the currency

    return item
