#!/usr/bin/env python
# coding: utf-8
from .main_view import MainView

import datetime


class TableView(MainView):
    def __init__(self):
        print('Construct Table')
        
    def display(self, datas):
        if(len(datas) > 0):
            datas_keys = datas[0].keys()

            row_format ="{:<20}" * (len(datas_keys))
            print(row_format.format(*datas_keys))
            for data in datas:
                list_values = list(data.values())
                list_values_format = []
                for i in list_values:
                    if i is None:
                        list_values_format.append("None")
                    elif isinstance(i, datetime.datetime):
                        list_values_format.append(i.strftime('%Y-%m-%d'))
                    else:
                        list_values_format.append(i)
                print(row_format.format(*list_values_format))
        else:
            print("No player create...")
