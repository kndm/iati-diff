# iati-diff
Script made to spot differences between XML files IATI activities against the XML file provided by the Datastore on the same activity.

# Requirements
- Python 3
- pip 
All requirements can be currently found in the requirements.txt file and installed via pip with the following command:

<b>pip install -r requirements.txt</b>

# Running IATI-Diff

IATI-Diff can be run using the following command via command prompt: 

<b>python iati-diff.py filename</b>
  
  
  <c>Filename: XML file to be compared</c>
  
# Output

IATI-Diff produces a .csv file with the differences on each file that can be found in the /differences folder, each difference file is named after its IATI-identifier
