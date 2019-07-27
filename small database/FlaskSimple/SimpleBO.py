import pymysql
import json

cnx = pymysql.connect(host='localhost',
                              user='dbuser',
                              password='dbuser',
                              db='lahman2017raw',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)


def run_q(q, args, fetch=False):
    cursor = cnx.cursor()
    cursor.execute(q, args)
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    cnx.commit()
    return result


def template_to_where_clause(t):
    s = ""

    if t is None:
        return s

    for (k, v) in t.items():
        if s != "":
            s += " AND "
        s += k + "='" + v[0] + "'"

    if s != "":
        s = "WHERE " + s;

    return s

def roster(in_args, offset, limit, fields=None):
    wc = template_to_where_clause(template)
#    print (in_args)
#    s1 = list(in_args.keys())
#    print(s1)
#    for i in s1:
#        print(i)
#    #CREATE VIEW roster AS
#    q = "select a.nameLast, a.nameFirst, b.playerID, b.teamID,  b.yearID, c.G_all, H as hits, AB as ABs, f.A, f.E\
#        from batting b\
#        join people a\
#        on a.playerID = b.playerID\
#        join appearances c\
#        on c.playerID = b.playerID and c.teamID  = b.teamID and c.yearID = b.yearID\
#        join fielding f\
#        on b.playerID = f.playerID and b.teamID= f.teamID and b.yearID = f.yearID\
#        where b.teamID= '" +s1[0]+ "' and b.yearID = '" +s1[1]+"'\
#        group by b.playerID;"
#    result = run_q(q, None, True)
#    re = ""
#    for i in result:
#        s1 = list(i.values())
#        #        for i in range(len(s1)):
#        #            s1[i] = "{:<12}".format(s1[1])
#        s1 = ",".join(str(j) for j in s1)
#        re += s1 + "\n"
    q = "select * from roster " + wc
    print(q)
    result = run_q(q, None, True)
    return result

def stats(playerID, offset, limit, fields=None):
    q = "select c.playerID, c.teamID, c.yearID, c.G_all, c.hits, c.ABs, f.A, f.E from\
        (select a.playerID, b.teamID, b.yearID, G_all, sum(H) as hits, sum(AB) as ABs from appearances a\
        join batting b\
        on a.playerID = b.playerID and a.teamID = b.teamID and a.yearID = b.yearID\
        where a.playerID = %s\
        group by a.playerID, b.teamID, b.yearID) c\
        join Fielding f\
        on c.playerID = f.playerID and c.teamID = f.teamID and c.yearID = f.yearID limit "+ limit[0]+ " offset " + offset[0]
    result = run_q(q, (playerID), True)
#    re = ""
#    for i in result:
#        s1 = list(i.values())
##        for i in range(len(s1)):
##            s1[i] = "{:<12}".format(s1[1])
#        s1 = ",    ".join(str(j) for j in s1)
#        re += s1 + "\n"
    return result

def teammates(playerID, offset, limit, fields=None):
    q = "select \
            a.playerID as playerID, b.playerID as ID, max(b.yearID), min(b.yearID), count(*) as c\
        from\
            batting a\
        join\
            batting b\
        on a.teamID = b.teamID and a.yearID = b.yearID\
        where\
            a.playerID = %s and a.playerID != b.playerID\
        group by b.playerID limit "+ limit[0]+ " offset " + offset[0]
    result = run_q(q, (playerID), True)
    print (result)
    print (type(result))
#    re = ""
#    for i in result:
#        s1 = list(i.values())
##        for i in range(len(s1)):
##            s1[i] = "{:<12}".format(s1[i])
#        s1 = ",    ".join(str(j) for j in s1)
#        re += s1 + "\n"
    return result

def get_primary_key(resource):
#    a = {"people":"playerID", "managers":"playerID", "appearances":"playerID", \
#        "batting":"playerID", "fielding":"playerID", "teams":"teamID"}
    q = "SHOW KEYS FROM " + resource + " WHERE Key_name = 'PRIMARY'"
    result = run_q(q, None, True)
    print(result)
    print(result[0])
    re = result[0]["Column_name"]
    print(re)
    return re

def insert_by_primary_key_r(resource, related_resource, body, primary_key):
    pk = get_primary_key(resource)
#    fk = get_foreign_key(related_resource)
    print(body)
    
    print(pk)
    body[pk] = primary_key
    try:
        keys = body.keys()                      # Get the key names. These map to column names.
        q = "INSERT into " + related_resource + " "     # Beginning of the insert statement.
        s1 = list(body.keys())
        s1 = ",".join(s1)
        q += "(" + s1 + ") "
        v = ["%s"] * len(keys)
        v = ",".join(v)
        q += "values(" + v + ");"
        print (q)
        params = tuple(body.values())
        result = run_q(q, params, False)
        return result

    except Exception as e:
        print("Exception  in insert, e = ", e)
        raise Exception("Boom! Original = ", e)


def find_by_primary_key_r(primary_key, resource, resource1, in_args, offset, limit, fields=None):
    pk = get_primary_key(resource)
#    fk = get_foreign_key(resource1)

    if fields:
        q = "select " + fields[0] + " from " + resource + " join " + resource1 + " using (" + pk\
            + ") where " + pk + "= %s" + " limit "+ limit[0]+ " offset " + offset[0]
    else:
        q = "select * from " + resource + " join " + resource1 + " using (" + pk\
            + ") where " + pk + "= %s" + " limit "+ limit[0]+ " offset " + offset[0]
    result = run_q(q, (primary_key), True)
    return result

def find_by_primary_key(primary_key, resource, in_args, offset, limit, fields=None):
    pk = get_primary_key(resource)
    if fields:
        q = "select " + fields[0] + " from " + resource + " where " + pk + "= %s" + " limit "+ limit[0]+ " offset " + offset[0]
    else:
        print("=======")
        print(pk)
        q = "select * from " + resource + " where " + pk + "= %s" + " limit "+ limit[0]+ " offset " + offset[0]
    result = run_q(q, (primary_key), True)
    return result

def delete_by_primary_key(primary_key, resource):
    pk = get_primary_key(resource)
    q = "DELETE FROM " + resource + " WHERE " + pk + "= %s"
    result = run_q(q, (primary_key), False)
    return result

def update_by_primary_key(primary_key, resource, body):
    pk = get_primary_key(resource)
    try:
        keys = body.keys()                      # Get the key names. These map to column names.
        q = "UPDATE " + resource + " SET "     # Beginning of the insert statement.
        for i in body.keys():
            q += i + "=%s, "
        q = q[:-2] + " where " + pk + "= '" + primary_key + "';"
        print (q)
        params = tuple(body.values())
        result = run_q(q, params, False)
        return result
    except Exception as e:
        print("Exception  in insert, e = ", e)
        raise Exception("Boom! Original = ", e)
    result = run_q(q, (primary_key), True)
    return result

def find_by_template(table, template, offset, limit, fields=None):
    wc = template_to_where_clause(template)
    if fields:
        q = "select " + fields[0] + " from " + table + " " + wc + " limit "+ limit[0]+ " offset " + offset[0]
    else:
        q = "select * from " + table + " " + wc + " limit "+ limit[0]+ " offset " + offset[0]
    print(q)
    result = run_q(q, None, True)
#    print(type(result))
    return result

def insert(resource, body):
    """
        :param resource: The name of the table underlying the resource.
        :param body: The body (row) data to insert in a dictionary.
        :return: None. Throws an exception is insert fails.
        """
    try:
        keys = body.keys()                      # Get the key names. These map to column names.
        q = "INSERT into " + resource + " "     # Beginning of the insert statement.
        
        # Will produce a list of the columns for the insert as a comma separated string,
        # e.g. playerID,nameLast,nameFirst,throws.
        s1 = list(body.keys())
        s1 = ",".join(s1)
        
        # Wrap with ( ... ) which is the insert statement format.
        q += "(" + s1 + ") "
        
        # If there are N keys/columns, there must also be N values.
        # This forms a string of the form %s,%s,%s,...,%s for each of the column values to to insert.
        v = ["%s"] * len(keys)
        v = ",".join(v)
        # Wrap the placeholders with values(...)
        q += "values(" + v + ");"
        print (q)
        # The values to insert into table are passed in the tuple, which gets inserted into
        # template in position of %s in order.
        params = tuple(body.values())
        # Submit the query template and parameters.
        # Insert does not return a result.
        result = run_q(q, params, False)
        return result
    except Exception as e:
        print("Exception  in insert, e = ", e)
        raise Exception("Boom! Original = ", e)




