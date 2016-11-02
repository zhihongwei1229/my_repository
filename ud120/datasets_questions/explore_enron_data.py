#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle
if True:
    #file = open("../final_project/final_project_dataset.pkl", "r")
    #str = file.read(100);
    #print(str)
    enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "rb"))
    #print(len(enron_data))
    #print(enron_data)
    #print(enron_data['GARLAND C KEVIN'])
    if False: #count poi people
        poi_count=0
        for x in enron_data:
            #print(enron_data[x]['poi'])
            if enron_data[x]['poi'] == True:
                poi_count = poi_count+1

        print(poi_count)

    if True:

        #print(enron_data['PRENTICE JAMES']['total_stock_value'])
        #print(enron_data['COLWELL WESLEY']['from_this_person_to_poi'])
        salary_info = 0
        poi_count = 0
        total_data_set = 0
        no_payment_info = 0
        #print(enron_data['SKILLING JEFFREY K']['total_payments'])
        #print(enron_data['LAY KENNETH L']['total_payments'])
        #print(enron_data['FASTOW ANDREW S']['total_payments'])
        #print(enron_data['FASTOW ANDREW S'])
        for x in enron_data:
            total_data_set += 1
            if enron_data[x]['poi'] == True:
                poi_count += 1
            if enron_data[x]['total_payments'] == 'NaN':
                no_payment_info += 1
            if (enron_data[x]['total_payments'] == 'NaN' and enron_data[x]['poi'] == True):
                salary_info += 1
        percent = salary_info / poi_count
        print(no_payment_info)
        print(total_data_set)


if False:
    line_count = 0
    name_list = open("../final_project/poi_names.txt", "r")
    with name_list as f:
        for line in f:
            if line.strip() != '':
                print(line)
                line_count += 1
    print(line_count)





