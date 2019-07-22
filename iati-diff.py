
import requests, shutil, os, sys
import logging
from lxml import etree as ET
from xmldiff import main as diffile
from xmldiff import formatting

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

path_activities = "./activities/"
path_differences = "./differences/"
path_datastore = "./datastore/"


def main():
	recording = False
	parser = ET.XMLParser(remove_blank_text=True)
	tree = ET.parse(sys.argv[1], parser=parser)
	root = tree.getroot()
	current_identifier = ''

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
			current_child = ET.SubElement(new_data, elem.tag, attrib = elem.attrib)
			current_child.text = elem.text
			logging.debug("Old data is: {}".format(ET.tostring(new_data)))
			#new_data.append(current_child)
			logging.debug("New data is: {}".format(ET.tostring(new_data)))
			if new_data:
				with open(path_activities + current_identifier + '.xml', 'wb') as file:
					file.write(ET.tostring(new_data, pretty_print=True))


	fileList = os.listdir(path_activities)

	elemList = [str(element).replace(".xml", "") for element in fileList]

	logging.debug("Element List is: {}".format(elemList)) 

	first = None

	formatter = formatting.DiffFormatter(normalize=formatting.WS_BOTH, pretty_print=True)

	newf=""

	for filename in elemList:
		datastore_xml_url = 'http://datastore.iatistandard.org/api/1/access/activity.xml?iati-identifier=' + str(filename)
		response = requests.get(datastore_xml_url)
		with open(path_datastore + filename + '.xml', 'wb') as file:
			file.write(response.content)

		with open(path_differences + filename + '.csv', 'w') as diff_file:
			for line in diffile.diff_files(path_datastore + filename + '.xml' , path_activities + filename + '.xml', formatter=formatter):
				diff_file.write(line)


		with open(path_differences + filename + '.csv', 'r') as f:
			for line in f:
				if "move" not in line.strip():
					line_stripped = line.strip()+ ', ' +filename+';\n'
					line_replace_inner_bracket = line_stripped.replace('[', '')
					line_replace_outer_bracket = line_replace_inner_bracket.replace(']', '')
					newf += line_replace_outer_bracket
			f.close()


	with open('differences.csv', 'w') as f_2:	
			f_2.write(newf)
			f.close()





def createFolders():
	if not os.path.exists(path_activities):
		os.makedirs(path_activities)

	if not os.path.exists(path_datastore):
		os.makedirs(path_datastore)

	if not os.path.exists(path_differences):
		os.makedirs(path_differences)


def deleteFolders():

	if os.path.exists(path_activities):
		shutil.rmtree(path_activities)

	if os.path.exists(path_datastore):
		shutil.rmtree(path_datastore)

	if os.path.exists(path_differences):
		shutil.rmtree(path_differences)

def remove_newlines(fname):
    flist = open(fname).readlines()
    return [s.rstrip('\n') for s in flist]


if __name__ == '__main__':
	createFolders()
	main()