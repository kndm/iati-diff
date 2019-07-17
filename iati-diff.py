
import requests, shutil, os, sys
import logging
from lxml import etree as ET
from xmldiff import main, formatting

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

tree = ET.parse(sys.argv[1])
root = tree.getroot()

current_identifier = ''
recording = False

for elem in tree.iter():
	logging.debug("Elem tag is: {} ".format(elem.tag))
	if elem.tag == 'iati-identifier':

		recording = True
		new_data = ET.Element('iati-activity')
		new_data_identifier = ET.SubElement(new_data, 'iati-identifier')

		logging.debug("Elem tag is iati-identifier")
		if current_identifier != elem.text and current_identifier is not '':
			logging.debug("Current identifier != elem.text and current_identifier is not empty: {} {}".format(elem.text, current_identifier))

		current_identifier = elem.text
		new_data_identifier.text = current_identifier




	if recording == True and elem.tag != 'iati-identifier':
		current_child = ET.SubElement(new_data, elem.tag)
		current_child.text = elem.text
		logging.debug("Old data is: {}".format(ET.tostring(new_data)))
		#new_data.append(current_child)
		logging.debug("New data is: {}".format(ET.tostring(new_data)))
		if new_data:
			with open('./activities/' + current_identifier + '.xml', 'wb') as file:
				file.write(ET.tostring(new_data, pretty_print=True))



