#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: dharm7
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "las-vegas_nevada.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE

mapping = {"St": "Street", "St.": "Street", "street": "Street", "AVE": "Avenue",
            "Ave": "Avenue", "Ave.": "Avenue", "Avene": "Avenue", "Avene.": "Avenue",
            "Rd": "Road", "Rd.": "Road", "Pkwy": "Parkway", 'Pkwy.': "Parkway",
            "Ln": "Lane", "Ln.": "Lane", "lane": "Lane",
            "Hwy": "Highway", "Hwy.": "Highway", "HWY": "Highway",
            "Expwy": "Expressway", "Expwy.": "Expressway",
            "Dr": "Drive", "Dr.": "Drive", "Blvd": "Boulevard", "Blvd.": "Boulevard", "N.": "North"}


def audit_street_type(street_types, street_name):
    """this function audit street name type"""
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    """this function if an attribute includes a street"""
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    """this function return all street name types"""
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping):
    """this function update street name and make street name to be consistent"""
    name = name.replace(",", "")
    for word in name.split(" "):
        if word in mapping.keys():
            name = name.replace(word, mapping[word])

    return name


def output():
    """This function print updated street name"""
    st_types = audit(OSMFILE)
    #assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "El Camino Rd":
                assert better_name == "El Camino Road"
            if name == "Thomas Ryan Blvd":
                assert better_name == "Thomas Ryan Boulevard"
    print "Pass"
def test():
    """This function is test sample dataset only"""
    st_types = audit("sample.osm")
    assert len(st_types) == 0
    pprint.pprint(dict(st_types))

if __name__ == '__main__':
    #test()
    output()