# iati-diff
Script made to spot differences between XML files IATI activities against the XML file provided by the Datastore on the same activity.

# Requirements
- Python 3
- pip 
All requirements can be currently found in the requirements.txt file and installed via pip with the following command:

<b>pip install -r requirements.txt</b>


# Files found in this repository

- iati-diff.py: Main script used to spot differences between IATI-activity files
- activity_style.xsl: XML Style Sheet file required for the input activity file to be split by iati-diff.py in order to generate the files to be compared 1:1 against the datastore.
- htmlformatter.xslt: Used for styling and customization of visualization of differences found in the output files.

# Running IATI-Diff

IATI-Diff can be run using the following command via command prompt: 

<b>python iati-diff.py "query_to_file"</b>
  
  
  <c>query_to_file: Query to the list of activities, enclosed by quotes. It is downloaded as a XML file to be compared by IATI-Diff.</c>
  
# Output and Visualization

IATI-Diff produces a XML file with the differences found on each activity compared to its datastore counterpart, as well as a HTML version for friendly visualization. The output files can be found in the /differences/ folder, named after its IATI-Identifier.

