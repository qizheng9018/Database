import csv
import pymysql
class RDBTable:
    # t_name: The "Name" of the collection.
    # t_file: The name of the CSV file. The class looks in the data_dir for the file.
    def __init__(self, t_name, t_file, key_columns):
        # Your code goes here
        self.table = t_name
        self.file = t_file
        self.key = key_columns
        self.cursor = None
        self.cnx = None
        pass
    
    def templateToWhereClause(self):
        s = ""
        t = self.t
        for (k,v) in t.items():
            if s != "":
                s += " AND "
            s += k + "='" + v + "'"
        
        if s != "":
            s = " WHERE " + s;
        return s
    
    # Pretty print the CSVTable and its attributes.
    def __str__(self):
        # Your code goes here.
        # Optional
        pass
    
    # loads the data from the file into the class instance data.
    # You decide how to store and represent the rows from the file.
    def load(self):
        # Your code goes here
        self.cnx = pymysql.connect(host='localhost',
                                   user='root',
                                   password='gfiato',
                                   db='Lahman2017',
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)
        self.cursor=self.cnx.cursor()
        pass
    
    # Obvious
    def save(self):
        self.cnx.close()
        pass
    
    # The input is:
    # t: The template to match. The result is a list of rows
    # whose attribute/value pairs exactly match the template.
    # fields: A subset of the fields to include for each result.
    # Raises an exception if the template or list of fields contains
    # a column/attribute name not in the file.
    def find_by_template(self, t, fields=None):
        # Your code goes here
        self.t = t
        w = RDBTable.templateToWhereClause(self)
        if fields != None:
            a = "SELECT "
            for i in fields:
                a = a + i + ", "
            q = a[:-2] + " FROM " + self.table + w + ";"
        else:
            q = "SELECT * FROM " + self.table + w + ";"
        print ("Query = ", q)
        self.cursor.execute(q);
        r = self.cursor.fetchall()
        #print("Query result = ", r)
        return r
    

    def find_by_primary_key(self, t, fields=None):
        key = {}
        for i in range(len(self.key)):
            key[self.key[i]] = t[i]
        self.t = key
        w = RDBTable.templateToWhereClause(self)
        if fields != None:
            a = "SELECT "
            for i in fields:
                a = a + i + ", "
            q = a[:-2] + " FROM " + self.table + w + ";"
        else:
            q = "SELECT * FROM " + self.table + w + ";"
        print ("Query = ", q)
        self.cursor.execute(q);
        r = self.cursor.fetchall()
        return r

    # Inserts the row into the table.
    # Raises on duplicate key or invalid columns.
    def insert(self, r):
        #         # Your code goes here
        q = "DESCRIBE " + self.table +";"
        self.cursor.execute(q);
        k = self.cursor.fetchall()
        columns = []
        for i in k:
            columns.append(i["Field"])
        for i in r.keys():
            if i not in columns:
                return "Invalid columns"
        a = RDBTable.find_by_template(self,r)
        #print(a)
        if len(a) > 0:
            return "Duplicate"
        q1 = "INSERT INTO " + self.table + " ("
        q2 = " VALUES ("
        for key, value in r.items():
            q1 = q1 + key + ", "
            q2 = q2 + "'" + value + "', "
        q1 = q1[:-2] + ")"
        q2 = q2[:-2] + ");"
        q_all = q1 + q2
        print(q_all)
        self.cursor.execute(q_all);
        r = self.cursor.fetchall()
        qt = "SELECT * FROM People WHERE playerID='dff1';"
        self.cursor.execute(qt);
        k = self.cursor.fetchall()
        k = self.cursor.close
        #print(k)
        self.cnx.commit()
        return "Successfully insert the row"


    # t: A template.
    # Deletes all rows matching the template.
    def delete(self, t):
        # Your code goes here.
        a = RDBTable.find_by_template(self,t)
        if len(a) == 0:
            return "Nothing Match"
        self.t = t
        w = RDBTable.templateToWhereClause(self)
        q = "DELETE FROM " + self.table + " " + w + ";"
        self.cursor.execute(q);
        self.cnx.commit()
        return "Successfully delete the data"
        pass


