import CSVTable
import json
import sys, os

def test1():
    
    csvt = CSVTable.CSVTable("People", "People.csv", ["playerID"])
    csvt.load()
#print("Table = ", csvt)


def test_template(test_name, table_name, table_file, key_columns, template, fields=None, show_rows=False):
    print("\n\n*******************************")
    print("Test name = ", test_name)
    print("Template = ", template)
    print("Fields = ", fields)
    
    try:
        csvt = CSVTable.CSVTable(table_name, table_file, key_columns)
        csvt.load()
        
        if not show_rows:
            print("Table name = ", csvt.table)
            print("Table file = ", csvt.file)
            print("Table keys = ", csvt.key_c)
        else:
            print(csvt)
        
        r = csvt.find_by_template(template, fields)
        print("Result table:")
        print(r)
    except ValueError as ve:
        print("Exception = ", ve)

def test_primary_key(test_name, table_name, table_file, key_columns, primary_key, fields=None, show_rows=False):
    print("\n\n*******************************")
    print("Test name = ", test_name)
    print("Template = ", primary_key)
    print("Fields = ", fields)
    
    try:
        csvt = CSVTable.CSVTable(table_name, table_file, key_columns)
        csvt.load()
        
        if not show_rows:
            print("Table name = ", csvt.table)
            print("Table file = ", csvt.file)
            print("Table keys = ", csvt.key_c)
        else:
            print(csvt)
        
        r = csvt.find_by_primary_key(primary_key, fields)
        print("Result table:")
        print(r)
    except ValueError as ve:
        print("Exception = ", ve)


def test_insert(test_name, table_name, table_file, key_columns, row, show_rows=False):
    print("\n\n*******************************")
    print("Test name = ", test_name)
    print("Row to insert = ", row)
    
    try:
        csvt = CSVTable.CSVTable(table_name, table_file, key_columns)
        csvt.load()
        
        if not show_rows:
            print("Table name = ", csvt.table)
            print("Table file = ", csvt.file)
            print("Table keys = ", csvt.key_c)
        else:
            print(csvt)
    
        r = csvt.insert(row)
        print("Result:")
        csvt.save()
        print(r)

    except ValueError as ve:
        print("Exception = ", ve)

def test_delete(test_name, table_name, table_file, key_columns, template, show_rows=False):
    print("\n\n*******************************")
    print("Test name = ", test_name)
    print("Row to insert = ", template)
    
    try:
        csvt = CSVTable.CSVTable(table_name, table_file, key_columns)
        csvt.load()
        
        if not show_rows:
            print("Table name = ", csvt.table)
            print("Table file = ", csvt.file)
            print("Table keys = ", csvt.key_c)
        else:
            print(csvt)
        
        r = csvt.delete(template)
        print("Result:")
        csvt.save()
        print(r)
    
    except ValueError as ve:
        print("Exception = ", ve)

test1()


def test_templates():
    test_template("Test1", "People", "People.csv", ["playerID"],
                  {"birthMonth": "9", "nameLast": "Williams"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                  False)

    test_template("Test2", "People", "People.csv", ["playerID"],
                  {"nameFirst": "Ted", "nameLast": "Williams"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                  False)
                  
    test_template("Test3", "People", "People.csv", ["canary"],
                  {"nameFirst": "Ted", "nameLast": "Williams"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                  False)
                  
    test_template("Test4", "Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"],
                  {"playerID": "willite01"}, ["playerID", "yearID", "teamID", "AB", "H", "HR"],
                  False)
                  
    test_template("Test5", "Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"],
                  {"playerID": "willite01"}, ["playerID", "yearID", "teamID", "AB", "H", "HR"],
                  False)
                  
    test_template("Test6", "Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"],
                  {"playerID": "willite01", "yearID": "1961"}, ["playerID", "yearID", "teamID", "AB", "H", "HR"],
                  False)
                  
    test_template("Test7", "Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"],
                  {"playerID": "willite01", "yearID": "1960"}, ["playerID", "yearID", "teamID", "AB", "H", "HR"],
                  False)

test_templates()

def test_primary_keys():
    test_primary_key("KeyTest1", "People", "People.csv", ["playerID"],
                     ["abernbi01"], ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                  False)
    test_primary_key("KeyTest2", "People", "People.csv", ["playerID"],
                                ["abernte02"], ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                                False)
    test_primary_key("KeyTest3", "People", "People.csv", ["birthCity"],
                                ["Orange"], ["nameLast", "nameFirst", "birthMonth", "birthYear","birthCity"],
                                False)
    test_primary_key("KeyTest4", "Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"],
                                ["willite01", "1960", "BOS", "1"], ["G", "R", "H", "AB"],
                                False)
    test_primary_key("KeyTest5", "Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"],
                                                 ["willite01", "BOS", "1961", "1"], ["G", "H", "R", "AB"],
                                                 False)
test_primary_keys()

def test_inserts():
    
    test_insert("Insert Test 1", "People", "People.csv", ["playerID"],
                {"playerID": "dff1", "nameLast": "Ferguson", "nameFirst": "Donald"},
                False)
        
    test_template("Find after insert 1", "People", "People.csv", ["playerID"],
                  {"nameLast": "Ferguson"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                  False)
                
    try:
        test_insert("Insert Test 2", "People", "People.csv", ["playerID"],
                    {"playerID": "dff1", "nameLast": "Ferguson", "nameFirst": "Donald"},
                    False)
                        
        raise ValueError("That insert should not have worked!")

    except ValueError as ve:
        print("OK. Did not insert duplicate key.")
    
    
    test_insert("Insert Test 3", "Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"],
                {"playerID": "dff1", "teamID": "BOS", "yearID": "2018", "stint": "1",
                "AB": "100", "H": "100"},
                False)
        
    test_template("Find after insert 3", "Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"],
                  {"playerID": "dff1"}, None,
                  False)
    test_insert("Insert Test 4", "People", "People.csv", ["playerID"],
            {"abcde": "dff1"},
            False)

test_inserts()

def test_deletes():
    
    test_template("(Delete)Find after insert 1", "People", "People.csv", ["playerID"],
                  {"nameLast": "Ferguson"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                  False)

    test_delete("Delete test 1", "People", "People.csv", ["playerID"],
                              {"playerID": "dff1", "nameLast": "Ferguson", "nameFirst": "Donald"},
                              False)
    test_template("Find after delete 1", "People", "People.csv", ["playerID"],
                                {"nameLast": "Ferguson"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                                False)
                
    try:
        test_delete("Delete Test 1", "People", "People.csv", ["playerID"],
                                {"playerID": "dff1", "nameLast": "Ferguson", "nameFirst": "Donald"},
                                False)
                        
        raise ValueError("That delete should not have worked!")

    except ValueError as ve:
        print("OK. Nothing to delete.")
    

test_deletes()
