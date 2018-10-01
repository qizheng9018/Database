import numpy as np
import csv
import CSVTable
import json

L = []
with open("/Users/zhengqi/Downloads/database/hw1/Data/Batting.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if len(L) == 0:
            L.append(row["playerID"])
        elif row["playerID"] not in L:
            L.append(row["playerID"])
L = sorted(L)

people = CSVTable.CSVTable("People", "People.csv", ["playerID"])
people.load()
batting = CSVTable.CSVTable("Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"])
batting.load()

d = []
count = 0.0
for i in L:
    count += 1
    if count % 1000.0 == 0:
        print(count)
    t1 = [i]
    pp = people.find_by_primary_key(t1)
    t2 = {"playerID":i}
    fields =  ["yearID", "AB", "H"]
    if type(pp) != str:
        if i == pp["playerID"]:
            rr = batting.find_by_template(t2, fields)
            #print(rr)
            bat_sum = 0.0
            hit_sum = 0.0
            if int(rr[-1]["yearID"]) >= 1960:
                for j in rr:
                    bat_sum += float(j["AB"])
                    hit_sum += float(j["H"])
                if bat_sum > 200:
                    player = {}
                    player["first_name"] = pp["nameFirst"]
                    player["last_name"] = pp["nameLast"]
                    player["career_hits"] = hit_sum
                    player["career_at_bats"] = bat_sum
                    player["career_average"] = hit_sum/bat_sum
                    player["first_year"] = rr[0]["yearID"]
                    player["last_year"] = rr[-1]["yearID"]
                    d.append(player)
#print(d)
l = []
for i in d:
    l.append(i["career_average"])
k = np.argsort(l)
Top = []
for i in range(1,11):
    Top.append(d[k[len(k)-i]])
print(json.dumps(Top, indent=2))
