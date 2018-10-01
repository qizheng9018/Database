#!/usr/bin/python3.6.5
# -*- coding: utf-8 -*-
import csv
import json
import collections

class CSVTable:
    # t_name: The "Name" of the collection.
    # t_file: The name of the CSV file. The class looks in the data_dir for the file.
    def __init__(self, t_name, t_file, key_columns):
        # Your code goes here
        self.table = t_name
        self.file = t_file
        self.key_c = key_columns
        self.L = []
        self.data_dir = "/Users/zhengqi/Downloads/database/hw1/Data/"        
        pass

    
    # Pretty print the CSVTable and its attributes.
    def __str__(self):
        # Your code goes here.
        # Optional    
        pass

    # loads the data from the file into the class instance data.
    # You decide how to store and represent the rows from the file.
    def load(self):     
        # Your code goes here
        with open(self.data_dir + self.file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.L.append(row)
        pass
    
    # Obvious
    def save(self):
        with open(self.data_dir + self.file, 'w') as f:
            w = csv.writer(f)
            fieldnames = self.L[0].keys()
            w.writerow(fieldnames)
            for row in self.L:
                w.writerow(row.values())
        pass
    
    # The input is:
    # t: The template to match. The result is a list of rows
    # whose attribute/value pairs exactly match the template.
    # fields: A subset of the fields to include for each result.
    # Raises an exception if the template or list of fields contains
    # a column/attribute name not in the file.
    def find_by_template(self, t, fields=None):
        # Your code goes here
        result = []
        length = len(self.L)
        l = len(t)
        if l == 0:
            return None
        for i in range(length):
            count = 0
            for j in t.keys():
#                print(j)
#                print(t[j])
#                print(self.L[i])
#                print(self.L[i][j])
                if self.L[i][j] != t[j]:
                    break
                else:
                    count += 1
            if count == l:
                if fields == None:
                    result.append(self.L[i])
                else:
                    dic = {}
                    for j in fields:
                        dic[j] = self.L[i][j]
                    result.append(dic)
        if len(result) > 0:
            return result
        else:
            return "Nothing match"
        pass
    
    def find_by_primary_key(self, t, fields=None):
        length = len(self.L)
        l = len(t)
        for i in range(length):
            count = 0
            for j in range(len(self.key_c)):
                if self.L[i][self.key_c[j]] != t[j]:
                    break
                else:
                    count += 1
            if count == l:
                if fields == None:
                    return self.L[i]
                else:
                    dic = {}
                    for j in range(len(fields)):
                        dic[fields[j]] = self.L[i][fields[j]]
                    return dic
        return "Nothing match"
        pass
    
    # Inserts the row into the table. 
    # Raises on duplicate key or invalid columns.
    def insert(self, r):
#         # Your code goes here
        for i in r.keys():
            if i not in self.L[0].keys():
                return "Invalid columns"
        for i in range(len(self.L)):
            count = 0
            for j in r.keys():
                if self.L[i][j] == r[j]:
                    count += 1
            if count == len(sorted(r.keys())):
                return "Duplicated row"
        k = collections.OrderedDict()
        for i in self.L[0].keys():
            k[i] = None
        for key, value in r.items():
            k[key] = value
        self.L.append(k)
        return "Successfully insert the row"
        pass
  
    # t: A template.
    # Deletes all rows matching the template.
    def delete(self, t):
        # Your code goes here.
        result = []
        length = len(self.L)
        l = len(t)
        if l == 0:
            return None
        flag = -1
        while True:
            flag += 1
            count = 0
            for j in t.keys():
                if self.L[flag][j] != t[j]:
                    break
                else:
                    count += 1
            if count == l:
                print(flag)
                result.append(self.L[flag])
                self.L.pop(flag) 
                flag -= 1
            if flag == len(self.L)-1:
                break
        if len(result)>0:
            return result
        else:
            return "Nothing match"
        pass
