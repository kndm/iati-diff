import xml.etree.ElementTree as ET
import requests, shutil, os
from lxml import etree
from xmldiff import main, formatting


tree = ET.parse('activity-list(2).xml')
root = tree.getroot()

elemList = []
count = 0

current_identifier = ''
recording = False

for elem in tree.iter():
	print(elem.tag)
	if elem.tag == 'iati-identifier':
		if current_identifier != elem.text and current_identifier is not '':
			if file:
				file.close()

		recording = True
		current_identifier = elem.text
		new_data = ET.Element('iati-activity')
		new_data_identifier = ET.SubElement(new_data, 'iati-identifier')
		new_data_identifier.text = current_identifier

	if recording == True:
		current_child = ET.SubElement(new_data, elem.tag)
		current_child.text = elem.text
		new_data.append(current_child)
		with open(current_identifier + '.xml', 'wb') as file:
			print(new_data)
			file.write(ET.tostring(new_data))

	count = count+1
	print(count)
