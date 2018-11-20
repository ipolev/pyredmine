#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from redminelib import Redmine

#Variables
worktime_file = './file-time.csv'

#remove file if exist
if os.path.isfile(worktime_file):
    os.remove(worktime_file)

redmine = Redmine('<url redmine>', key='<api key redmine>')

time_table = {}

#Get date worktime from api Redmine
for username in redmine.user.all():
#	print (username.login)
    user = username.id
#	print (username.mail)
    time_dates = redmine.time_entry.filter(from_date='2018-10-01', to_date='2018-10-30', user_id=user)
    for tdate in time_dates:
        tuser = tdate.user.name.encode('utf-8')
        tproject = tdate.project.name.encode('utf-8')
        tissue = tdate.issue.id
        issue_subject = redmine.issue.get(tissue).subject.encode('utf-8')
        thours = tdate.hours
        if not tuser in time_table:
             time_table[tuser] = {}
        if not tproject in time_table[tuser]:
             time_table[tuser][tproject] = {}
        if not tissue in time_table[tuser][tproject]:
             time_table[tuser][tproject][tissue] = {'name': issue_subject, 'time': thours}
        else:
             time_table[tuser][tproject][tissue]['time'] += thours

#Create templete file
file_table = open (worktime_file, 'w')
file_table.write('Пользователь' + ';' + 'Проект' + ';' + '№ Задачи' + ';' + 'Наименование Задачи' + ';' + 'Время,ч\n')

#Add date worktime to file
for key1 in time_table:
    file_table.write(str(key1) + ';\n')
    for key2 in time_table[key1]:
        file_table.write(';' + str(key2) + ';\n')
        for key3 in time_table[key1][key2]:
            file_table.write(';;' + str(key3) + ';\n')
            issue_name = time_table[key1][key2][key3]['name']
            issue_time = time_table[key1][key2][key3]['time']
            file_table.write(';;;' + str(issue_name) + ';' + str(issue_time) + '\n')

#Close file 
file_table.close()

#time_entries.export('csv', savepath='/home/admin2/', filename='time_entries.csv')