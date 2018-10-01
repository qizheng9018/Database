import RDBTable
import QueryProcessor
import json

# Make some tables
people = RDBTable.RDBTable("People", "People.csv", ["playerID"])
batting = RDBTable.RDBTable("Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"])
appearances = RDBTable.RDBTable("Appearances", "Appearances.csv", ['playerID', 'yearID', 'teamID'])

tables = { "People": people, "Batting": batting, "Appearances": appearances}

# A constraint
c1 = { "target_table": "People", "target_attribute": "playerID", "source_table": "Batting",
       "source_attribute": "playerID"}

processor = QueryProcessor.QueryProcessor(tables, [c1])
try:
    tmp = { "table_name": "People", "operation_name": "find_by_template", "template": {"nameLast" : "Ferguson", "nameFirst": "Donald"}, \
            "fields": ['playerID', 'nameLast', 'nameFirst', 'birthCity']}
    rr = processor.find_by_query(tmp)
    print("Query = ", tmp)
    print("Result = \n", json.dumps(rr, indent=2))
except Exception as e:
    print("Got exception = ", str(e))

tmp = { "table_name": "Batting", "template": {"playerID" : "willite01"},
"fields": ['G', 'AB', 'H', 'yearID']}
rr = processor.find_by_query(tmp)
print("Query = ", tmp)
print("Result = \n", json.dumps(rr, indent=2))

#try:
#    tmp = { "table_name": "Batting", "template": {"playerID" : "willite01"},
#        "fields": ['G', 'AB', 'H', 'yearID']}
#    rr = processor.find_by_query(tmp)
#    print("Query = ", tmp)
#    print("Result = \n", json.dumps(rr, indent=2))
#except Exception as e:
#    print("Got exception = ", str(e))

