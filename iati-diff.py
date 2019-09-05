import requests, shutil, os, sys
import logging
import re
import xml.dom.minidom as prettifier
from lxml import etree as ET
from xmldiff import main as diffile
from xmldiff import formatting

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

path_activities = "./activities/"
path_differences = "./differences/"
path_datastore = "./datastore/"


def main():

	recording_flag = False
	activity_start_count = 0
	query = sys.argv[1] + '&format=xml'
	query_response = requests.get(query)

	with open('activity-list.xml', 'wb') as activity_query_file:
		activity_query_file.write(query_response.content)

	with open('activity-list-fix.xml', 'w') as new_activity_file:
		with open('activity-list.xml', 'r') as activity_file:
			for line in activity_file:
		   		if "<iati-activity" in line:
		   			activity_start_count = activity_start_count + 1
		   			if "iati-extra" in line:
		   				line = line.replace('<iati-activity', '<iati-activity xmlns:iati-extra="http://datastore.iatistandard.org/ns"')
		   		
		   			if activity_start_count > 1:
		   				line = '\n'


		   			recording_flag = True

	   			if recording_flag == True:
		   			if "</iati-activity" in line or "</iati-activities" in line:
		   				line = '\n'

		   			else:
		   				new_activity_file.write(line.strip()+"\n")
			new_activity_file.write('</iati-activity>')
				
	# LOAD XML AND XSL SCRIPT
	xml = ET.parse('activity-list-fix.xml')
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
	   	xml_ugly = prettifier.parseString(response.content)
	   	xml_pretty = xml_ugly.toprettyxml()
	   	file.write(xml_pretty.encode('utf-8'))

	   	recording_flag = False
	   	xlmns_namespaces = ""


	   with open(path_datastore + output_identifier.text + '.xml', 'r', encoding="utf-8") as raw_datastore:
	   	for line in raw_datastore:
	   		# TODO, TURN THIS INTO A FUNCTION FOR THE TAGS XMLNS FIX
	   		if "<iati-activity" in line:
	   			if "iati-extra" in line:
	   				line = line.replace('<iati-activity', '<iati-activity xmlns:iati-extra="http://datastore.iatistandard.org/ns"')


	   			recording_flag = True

   			if recording_flag == True:
	   			if "</iati-activity" in line:
	   				recording_flag = False
	   				newf+= "</iati-activity>"
	   			else:
	   				newf+= line.strip()+"\n"



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
	   	header = '''<!DOCTYPE html>
	   	<html>
	   	<head>
	   	<link rel="stylesheet" href="../style.css">
	   	</head>
	   	<body>\n'''
	   	footer = '''</body>
	   	</html>
	   	'''
	   	with open(path_differences + output_identifier.text + '.html', 'w', encoding="utf-8") as mockup_file_result:
	   		mockup_file_result.write(header)
	   		with open(path_differences + output_identifier.text + '.xml', 'r', encoding="utf-8") as mockup_file:
	   			for line in mockup_file:
	   				if 'xmlns:diff=""' in line:
	   					line = line.replace('xmlns:diff=""', '')
	   				if '<' in line:
	   					line = line.replace('<', '&lt;')
	   				if '>' in line:
	   					line = line.replace('>', '&gt;')
	   				if 'diff:insert' in line:
	   					counter = line.find('&gt;')
	   					if line[counter+4] != line[-1]:
	   						counter_closing = line.index('&lt;', counter)
	   						line = line[:counter+4] + '<div class="DiffInsert"><pre>' + line[counter+4:counter_closing] + '</pre></div>' + line[counter_closing:]
	   					line = line.replace('diff:insert=""', '')
	   				if 'diff:del' in line:
	   					counter = line.find('&gt;')
	   					if line[counter+4] != line[-1]:
	   						counter_closing = line.index('&lt;', counter)
	   						line = line[:counter+4] + '<div class="DiffDel"><pre>' + line[counter+4:counter_closing] + '</pre></div>' + line[counter_closing:]
	   					line = line.replace('diff:delete=""', '')
	   				if 'diff:add-attr' in line:
	   					# MAKE A LIST OF THE ATTRIBUTES IN ORDER TO SELECT THEM INDIVIDUALLY IN THE CSS LATER ON
	   					attribute_selector = re.search('add-attr=\"(.+?)\"', line).group(1)
	   					attribute_list = attribute_selector.split(";")
	   					for attribute in attribute_list:
	   						if str(attribute) in line:
	   							try:
	   								attribute_value = re.search(str(attribute) + '=\"(.+?)\"', line).group(1)
	   								line = re.sub('(diff:add-attr=\".+?\")','', line)
	   								line = line.replace(attribute, '<div class="DiffInsert"><pre>' + attribute)
	   								line = line.replace(attribute_value + '"', attribute_value + '"</pre></div>')
	   								
	   							except AttributeError:
	   								# It did not match the regex, likely because the attribute does not have any value and it is a value itself
	   								line = re.sub('(diff:add-attr=\".+?\")','', line)
	   								line = line.replace(attribute, '<div class="DiffInsert"><pre>' + attribute + '</pre></div>')

	   					#line = line.replace('diff:add-attr=', '<div class="DiffInsert"><pre>add-attr=')
	   					#line = line + '</pre></div>'
	   				mockup_file_result.write('<pre>' + line.strip()+'</pre>' + '\n')
	   		mockup_file_result.write(footer)




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

	if os.path.isfile('./activity-list-fix.xml'):
		os.remove('./activity-list-fix.xml')


if __name__ == '__main__':
	createFolders()
	main()
	'''deleteFolders() disabled for debugging purposes. This method cleans up files that we don't want users to see 
	but still are necessary for processing the differences.'''
	#deleteFolders()