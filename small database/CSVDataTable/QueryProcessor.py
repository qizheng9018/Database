class QueryProcessor:

    def __init__(self, tables, constraints=None):
        self.table = tables
        self.con = constraints
        pass

    # Query if of the form:
    # { "table_name": "some name", "template": {...}, "fields": [] }
    def find_by_query(self, q):
        table = self.table[q["table_name"]]
        table.load()
        if "operation_name" in q.keys():
            if q["operation_name"] == "find_by_template":
                return table.find_by_template(q["template"], q["fields"])
            elif q["operation_name"] == "find_by_primary_key":
                return table.find_by_primary_key(q["template"], q["fields"])
        else:
            print(q["template"])
            print(q["fields"])
            return table.find_by_template(q["template"], q["fields"])
        pass

    # t_name is table name
    # Row is row to insert into table.
    def insert(self, q):
        table_s = self.table[self.con["source_table_name"]]
        table_s.load()
        table_t = self.table[self.con["target_table_name"]]
        table_t.load()
        s_a = self.con["source_attribute"]
        t_a = self.con["target_attribute"]
        t = table_t.find_by_template({t_a:q["template"][t_a]}, fields=[t_a])
        #s = table_s.find_by_template(q["template"][s_a], fields=[s_a])
        if q["template"][s_a] in t:
            insert_row = q["template"]
            table_s.insert(insert_row)
        else:
            return "Target table cannot be matched"
        pass

    # Same for delete.
    # tmpl is the template to delete.
    def delete(self, q):
        table_s = self.table[self.con["source_table_name"]]
        table_s.load()
        table_t = self.table[self.con["target_table_name"]]
        table_t.load()
        s_a = self.con["source_attribute"]
        t_a = self.con["target_attribute"]
        s = table_s.find_by_template({s_a:q["template"][s_a]}, fields=[s_a])
        if s == "Nothing match":
            return "Source table cannot be matched"
        else:
            delete_row = q["template"]
            table_t.delete(delete_row)
        pass
