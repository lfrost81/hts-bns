import pprint
import pandas as pd
import numpy as np
import csv


def json_link_pairwise(forward_dict, delimiter=',', ofp=None):
    result = []

    for k, v in forward_dict.items():
        for k2, v2 in v.items():
            line = delimiter.join([k, k2, str(v2)])
            result.append(line)
            if ofp is not None:
                ofp.write(line + '\n')

    return result


def csv_link_pairwise(fp, delimiter=',', ofp=None):
    result = []

    df = pd.read_csv(fp, index_col=0, header=0)
    df = df.fillna(0)
    for k, v in df.items():
        for k2, v2 in v.items():
            if v2 != 0:
                line = delimiter.join([k2, k, str(v2)])
                result.append(line)

                if ofp is not None:
                    ofp.write(line + '\n')

    return result


def load_and_choice_merchant_pairwise(fp, delimiter=',', ofp=None):
    result = []

    reader = csv.reader(fp, delimiter='\t')
    choices = {}
    for row in reader:
        if len(row) == 2:
            choices[row[0]] = row[1].split(',')

    # keys = np.random.choice(list(choices.keys()), n_choice)
    # choices = {k: choices[k] for k in keys}

    for k, v in choices.items():
        for attr in v:
            line = delimiter.join([k, attr, str(1)])
            result.append(line)
            if ofp is not None:
                ofp.write(line + '\n')

    return result

if __name__ == '__main__':
    d = {
        '아리따움': {
            '미니스톱': 100,
            '미스터피자': 200
        },

        '미니스톱': {
            '아리따움': 1,
            '미스터피자': 2
        },
    }

    # with open('./sample/test.csv', 'w') as ofp:
    #     pprint.pprint(json_link_pairwise(d, '\t', ofp))

    with open('../data/src-store-to-store.csv') as fp:
        with open('../data/store_to_store.csv', 'w') as ofp:
            pprint.pprint(csv_link_pairwise(fp, delimiter=',', ofp=ofp))

    with open('../data/src-store-to-topic.txt') as fp:
        with open('../data/shop_to_topic.csv', 'w') as ofp:
            pprint.pprint(load_and_choice_merchant_pairwise(fp, delimiter=',', ofp=ofp))
