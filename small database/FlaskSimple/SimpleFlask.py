# Lahman.py

# Convert to/from web native JSON and Python/RDB types.
import json

# Include Flask packages
from flask import Flask
from flask import request
import copy

import SimpleBO

# The main program that executes. This call creates an instance of a
# class and the constructor starts the runtime.
app = Flask(__name__)

def parse_and_print_args():
    fields = None
    in_args = None
    if request.args is not None:
        in_args = dict(copy.copy(request.args))
        fields = copy.copy(in_args.get('fields', None))
        offset = copy.copy(in_args.get('offset', None))
        limit = copy.copy(in_args.get('limit', None))
        #print(fields)
        if fields:
            del(in_args['fields'])
        if offset:
            del(in_args['offset'])
        else:
            offset = ["0"]
        if limit:
            del(in_args['limit'])
        else:
            limit = ["10"]

    try:
#        print("*************")
#        print(request)
        if request.data:
            body = json.loads(request.data)
        #print(body)
        else:
            body = None
    except Exception as e:
        print("Got exception = ", e)
        body = None
    print("Request.args : ", json.dumps(in_args))
    return in_args, fields, offset, limit, body

def pigination(result, offset, limit):
    re = {}
    re["data"] = result
    cur = {}
    next = {}
    #print(offset[0])
    #print(type(offset[0]))
    n = int(offset[0])+10
    cur["current"] =request.url[21:]
    if "offset" in cur["current"]:
        count = -1
        for i in range(100):
            if request.url[count] == "o":
                break
            count -= 1
        next["next"] =request.url[21:count] + "offset=" + str(n) + "&limit=10"
    else:
        if "?" in cur["current"]:
            next["next"] =request.url[21:] + "&offset=" + str(n) + "&limit=10"
        else:
            next["next"] =request.url[21:] + "?offset=" + str(n) + "&limit=10"
    #print(next["next"])
    link = [cur, next]
    re["links"] = link
    #print(re)
    re = str(re).replace("'", "\"")
    re = str(re).replace("None", "\"null_block\"")
    print(re)
    re = json.loads(re)
    return re

@app.route('/api/<resource>', methods=['GET', 'POST'])
def get_resource(resource):
    in_args, fields, offset, limit, body = parse_and_print_args()
    if request.method == 'GET':
        #/localhost:5000/api/people?nameLast=Smith&fields=nameLast,playerID
        result = SimpleBO.find_by_template(resource, in_args, offset, limit, fields)
        re = pigination(result, offset, limit)
        return json.dumps(re), 200, {"content-type": "application/json; charset: utf-8"}
    elif request.method == 'POST':
#        print(resource)
#        print(body)
        result = SimpleBO.insert(resource, body)
        return "Successfully insert"
#        return json.dumps(result), 200, \
#            {"content-type": "application/json; charset: utf-8"}
#print(result)
    else:
        return "Method " + request.method + " on resource " + resource + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

@app.route('/api/<resource>/<primary_key>', methods=['GET', 'PUT', 'DELETE'])
def get_resource_primary_key(resource, primary_key):
    in_args, fields, offset, limit, body = parse_and_print_args()
    if request.method == 'GET':
        #127.0.0.1:5000/api/people/willite01?offset=0&limit=10
        result = SimpleBO.find_by_primary_key(primary_key, resource, in_args, offset, limit, fields)
        re = pigination(result, offset, limit)
        return json.dumps(re), 200, {"content-type": "application/json; charset: utf-8"}
    elif request.method == 'PUT':
        result = SimpleBO.update_by_primary_key(primary_key, resource, body)
        return json.dumps(result), 200, {"content-type": "application/json; charset: utf-8"}
    elif request.method == 'DELETE':
        result = SimpleBO.delete_by_primary_key(primary_key, resource)
        return json.dumps(result), 200, {"content-type": "application/json; charset: utf-8"}
    else:
        return "Method " + request.method + " on resource " + resource + \
            " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

@app.route('/api/<resource>/<primary_key>/<related_resource>', methods=['GET', 'POST'])
def get_resource_resource1(resource, primary_key, related_resource):
    in_args, fields, offset, limit, body = parse_and_print_args()
    if request.method == 'GET':
        result = SimpleBO.find_by_primary_key_r(primary_key, resource, related_resource, in_args, offset, limit, fields)
        re = pigination(result, offset, limit)
        return json.dumps(re), 200, {"content-type": "application/json; charset: utf-8"}
    elif request.method == 'POST':
        result = SimpleBO.insert_by_primary_key_r(resource, related_resource, body, primary_key)
        return json.dumps(result), 200, \
                {"content-type": "application/json; charset: utf-8"}
    else:
        return "Method " + request.method + " on resource " + resource + \
            " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

@app.route('/api/teammates/<playerid>', methods=['GET'])
def get_teammates(playerid):
    in_args, fields, offset, limit, body = parse_and_print_args()
    if request.method == 'GET':
        result = SimpleBO.teammates(playerid, offset, limit, fields=None)
#        print(result)
        re = pigination(result, offset, limit)
        return json.dumps(re), 200, {"content-type": "application/json; charset: utf-8"}
    else:
        return "Method " + request.method + " on resource " + resource + \
            " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

@app.route('/api/people/<playerid>/career_stats', methods=['GET'])
def get_career_stats(playerid):
    in_args, fields, offset, limit, body = parse_and_print_args()
    if request.method == 'GET':
        result = SimpleBO.stats(playerid, offset, limit, fields=None)
        re = pigination(result, offset, limit)
        return json.dumps(re), 200, {"content-type": "application/json; charset: utf-8"}

    else:
        return "Method " + request.method + " on resource " + resource + \
            " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

@app.route('/api/<roster>', methods=['GET'])
def get_roster(roster):
    in_args, fields, offset, limit, body = parse_and_print_args()
    if request.method == 'GET':
        result = SimpleBO.roster(in_args, offset, limit, fields=None)
        re = pigination(result, offset, limit)
        return json.dumps(re), 200, {"content-type": "application/json; charset: utf-8"}
    else:
        return "Method " + request.method + " on resource " + resource + \
            " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

if __name__ == '__main__':
    app.run()

