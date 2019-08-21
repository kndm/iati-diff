
import requests, shutil, os, sys
import logging
from lxml import etree as ET
from xmldiff import main as diffile
from xmldiff import formatting

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

path_activities = "./activities/"
path_differences = "./differences/"
path_datastore = "./datastore/"
datastore_xml_header = '''<result xmlns:iati-extra="http://datastore.iatistandard.org/ns">\n<ok>True</ok>
\n<iati-activities generated-datetime='2019-08-20T20:48:00.588612'>\n
<query>\n
<total-count>1</total-count>\n
<start>0</start>\n
<limit>50</limit>\n
</query>\n'''


def main():
	# LOAD XML AND XSL SCRIPT
	xml = ET.parse('activity-list(2).xml')
	xsl = ET.parse('activity_style.xsl')
	xslt_formatting = ET.parse('htmlformatter.xslt')
	transform = ET.XSLT(xsl)

	# LOOP THROUGH ALL NODE COUNTS AND PASS PARAMETER TO XSLT
	iati_count = len(xml.xpath('//iati-identifier'))
	formatter = formatting.XMLFormatter(normalize=formatting.WS_BOTH, pretty_print=True)
	for i in range(iati_count):
	   newf=""
	   newf2= ""
	   n = ET.XSLT.strparam(str(i+1))            
	   result = transform(xml, item_num=n)         # NAME OF XSL PARAMETER

	   # SAVE XML TO FILE
	   with open(path_activities + 'Output_{}.xml'.format(i+1), 'wb') as f:
	   	#f.write(header.encode('utf-8'))
	   	f.write(result)
	   
	   output_parser = ET.parse(path_activities + 'Output_{}.xml'.format(i+1))
	   output_root = output_parser.getroot()
	   output_identifier = output_root.find('iati-identifier')
	   datastore_xml_url = 'http://datastore.iatistandard.org/api/1/access/activity.xml?iati-identifier=' + output_identifier.text
	   response = requests.get(datastore_xml_url)

	   with open(path_datastore + output_identifier.text + '.xml', 'wb') as file:
	   	file.write(response.content)

	   	recording_flag = False
	   	xlmns_namespaces = ""


	   with open(path_datastore + output_identifier.text + '.xml', 'r', encoding="utf-8") as raw_datastore:
	   	for line in raw_datastore:
	   		if "<iati-activity" in line:
	   			if "xmlns:akvo" in line:
	   				xlmns_namespaces = ' xmlns:akvo="http://akvo.org/iati-activities"'

	   			recording_flag = True
	   			line = "<iati-activity" + xlmns_namespaces + ">"

   			if recording_flag == True:
	   			if "</iati-activity" in line:
	   				recording_flag = False
	   				newf+= "</iati-activity>"
	   			else:
	   				newf+= line.strip()+"\n"



			   			

	   	print('NEW F IS: ', newf)


	   with open(path_activities + 'Output_{}.xml'.format(i+1), 'r', encoding="utf-8") as raw_list:
	   	for line in raw_list:
	   		newf2+= line.strip() + '\n'

	   with open (path_datastore + 'formatted-' + output_identifier.text + '.xml', 'w', encoding="utf-8") as formatted_datastore:
	   	formatted_datastore.write(newf)

	   with open (path_activities + 'formatted-' + output_identifier.text + '.xml', 'w', encoding="utf-8") as formatted_list:
	   	formatted_list.write(newf2)


	   if not os.stat(path_datastore + 'formatted-' + output_identifier.text + '.xml').st_size == 0:
	   	with open(path_differences + output_identifier.text + '.xml', 'w', encoding="utf-8") as diff_file:
	   		result = diffile.diff_files(path_activities + 'formatted-' + output_identifier.text + '.xml', path_datastore + 'formatted-' + output_identifier.text + '.xml', formatter=formatter, diff_options={'F': 1, 'ratio_mode':'accurate'})
	   		if 'http://namespaces.shoobx.com/diff' in result:
	   			result = result.replace('http://namespaces.shoobx.com/diff', '')
	   		diff_file.write(result)




class HTMLFormatter(formatting.XMLFormatter):
	def render(self, result):
		transform = lxml.etree.XSLT(xslt_formatting)
		result = transform(result)
		return super(HTMLFormatter, self).render(result)


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


if __name__ == '__main__':
	createFolders()
	main()