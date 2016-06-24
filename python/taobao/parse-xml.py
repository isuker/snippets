#!/usr/bin/python

from xml.dom import minidom

xml_file = "./xml_out.xml"

xmldoc = minidom.parse(xml_file)

#print xmldoc.toxml()

####################################
root = xmldoc.documentElement
print type(root)
print "nodeName: " , root.nodeName
print "nodeType: " , root.nodeType

child_nodes = root.childNodes
print type(child_nodes)
print child_nodes.length

for loop in range(0, child_nodes.length):

    node = child_nodes[loop]
    if node.nodeType == 1:
        print child_nodes[loop].nodeName
        print child_nodes[loop].nodeValue
    print "-----------------------------------------------"

message =root.getElementsByTagName('MESSAGE')
attr = message[0].attributes
print type(attr)
for (key, item) in attr.items():
    print key, " => ", item

parms = root.getElementsByTagName('IPARAMVALUE')
for i in range(0, parms.length):
    name = parms[i].getAttribute('NAME')
    print name

    # serach 'ObjectName'
    if name == 'ObjectName':
        nodes = parms[i].childNodes
        for loop in range(0, nodes.length):
            if nodes[loop].nodeType == 1:
                inst = nodes[loop]
                print inst.toxml()
    



