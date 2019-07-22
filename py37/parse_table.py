# -*- coding: utf-8 -*-

import pandas as pd
import csv

url = 'http://hy.taojindi.com/scompany441117/'
tb = pd.read_html(url, encoding='utf-8')[0]
tb.to_csv(r'1.csv', mode='a', encoding='utf_8', header=1, index=0)