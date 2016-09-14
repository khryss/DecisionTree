from pprint import pprint
from math import log
import collections



rows = []
rows.append({"id":"1",  "outlook":"sunny",    "humidity":"high",   "wind":"week",   "degrees":"05-10", "decision":True})
rows.append({"id":"2",  "outlook":"overcast", "humidity":"normal", "wind":"strong", "degrees":"10-15", "decision":False})
rows.append({"id":"3",  "outlook":"overcast", "humidity":"high",   "wind":"week",   "degrees":"20-25", "decision":True})
rows.append({"id":"4",  "outlook":"rain",     "humidity":"high",   "wind":"strong", "degrees":"20-25", "decision":False})
rows.append({"id":"5",  "outlook":"rain",     "humidity":"normal", "wind":"week",   "degrees":"20-25", "decision":False})
rows.append({"id":"6",  "outlook":"rain",     "humidity":"normal", "wind":"week",   "degrees":"15-20", "decision":False})
rows.append({"id":"7",  "outlook":"overcast", "humidity":"normal", "wind":"week",   "degrees":"10-15", "decision":False})
rows.append({"id":"8",  "outlook":"overcast", "humidity":"normal", "wind":"week",   "degrees":"15-20", "decision":True})
rows.append({"id":"9",  "outlook":"sunny",    "humidity":"high",   "wind":"strong", "degrees":"05-10", "decision":True})
rows.append({"id":"10", "outlook":"rain",     "humidity":"normal", "wind":"week",   "degrees":"20-25", "decision":False})


def process_data(rows):
    print "\nProcessing data..."
    raw_atts = rows[0].keys()
    raw_atts.remove("id")
    raw_atts.remove("decision")
    attributes = raw_atts

    result = []
    for att in attributes:
        values = {}
        for row in rows:
            if not values.get(row[att]):
                values[row[att]] = [0, 0]
            values[row[att]][row['decision']] += 1

        att_tuple = (att, values)
        result.append(att_tuple)

    order_by_entropia(result)

    return result


def entropia(no, yes):
    no = float(no)
    yes = float(yes)
    total = no + yes

    try:
        elem_no = -(no/total)*log(no/total, 2)
    except ValueError:
        elem_no = 0
    try:
        elem_yes = -(yes/total)*log(yes/total, 2)
    except ValueError:
        elem_yes = 0
    result = elem_no + elem_yes

    return result


def compute_attribute_entropia(attribute):
    att_opts = attribute[1]

    total = 0
    att_decisions = [0, 0]

    for opt in att_opts.values():
        total += sum(opt)
        att_decisions[False] += opt[0]
        att_decisions[True] += opt[1]

    result = entropia(*att_decisions)

    for att_name, opt in att_opts.items():
        no = float(opt[0])
        yes = float(opt[1])
        result -= ((no+yes)/total)*entropia(no, yes)
    return result


def order_by_entropia(attributes):
    print "\nOrdering attributes..."
    for att in attributes:
        print att, 'Gain:', compute_attribute_entropia(att)
    attributes.sort(key=compute_attribute_entropia, reverse=True)
    print
    print attributes



class Node(object):
    def __init__(self,
                 value,
                 children_att=None,
                 decisions=[0, 0],
                 level=0):
        self.value = value
        self.children_att = children_att
        self.children = {}
        self.decisions = decisions
        self.level = level

    def add_attribute(self, attribute):
        # This method is called on root for all attributs.
        # It searches for the first no-child node to put the attribute.
        att_name, att_opts = attribute

        # find the first no-child node to put the attribute
        nodes_to_visit = [self]
        curr_node = nodes_to_visit.pop(0)
        while curr_node.children:
            nodes_to_visit += curr_node.children.values()
            curr_node = nodes_to_visit.pop(0)

        curr_node.children_att = att_name
        for opt_name, opt_decisions in att_opts.items():
            curr_node.children[opt_name] = Node(value=opt_name,
                                                decisions=opt_decisions,
                                                level=curr_node.level+1)

    def show(self):
        print "| "*self.level,
        print self
        for c in self.children.values():
            c.show()

    def __repr__(self):
        return "<%s" % self.value + str(self.decisions) + " %s" % self.children_att +">"


def create_tree():
    print "\nCreating tree..."

    root = Node(value='root')
    for attr in attributes:
        root.add_attribute(attr)

    return root


def predict(root, row):
    print "\nPredicting..."
    curr_node = root

    while True:
        print curr_node
        if not curr_node.children:
            return '{0!s}/{1!s}'.format(*curr_node.decisions)

        child = curr_node.children[row[curr_node.children_att]]

        # check for purity
        if 0 in child.decisions:
            print child
            return not child.decisions.index(0)

        curr_node = child



attributes = process_data(rows)
root = create_tree()
root.show()

print predict(root, {"outlook":"sunny",    "humidity":"high",   "wind":"strong", "degrees":"05-10"})
print predict(root, {"outlook":"sunny",    "humidity":"normal", "wind":"strong", "degrees":"10-15"})
print predict(root, {"outlook":"overcast", "humidity":"high",   "wind":"week",   "degrees":"15-20"})
