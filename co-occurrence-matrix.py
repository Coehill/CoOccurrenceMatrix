import pandas as pd
import numpy as np
from collections import defaultdict
from collections import OrderedDict

'''
===================================
	Coursework Collection
===================================

The image collection, containing 10,000 images annotated using 100 tags, is stored in 3 databse tables and is presented in 2 different formats:
- MySQL database, entire database (mysql folder)
- 3 Comma seperated files, 1 for each table (csv folder)

===================================
			Tables
===================================
- photos (id int,width int,height int,title string,uploaded datetime)
- photos_tags (photoid int, tag string)
- tags (tag string, num_photos int)

If there are any issues, please contact p.mcparlane.1@research.gla.ac.uk
'''


'''
df = pd.DataFrame({'TFD' : ['AA', 'SL', 'BB', 'D0', 'Dk', 'FF'],
                    'Snack' : ['1', '0', '1', '1', '0', '0'],
                    'Trans' : ['1', '1', '1', '0', '0', '1'],
                    'Dop' : ['1', '0', '1', '0', '1', '1']}).set_index('TFD')

print(df)
df_asint = df.astype(int)
coocc = df_asint.T.dot(df_asint)

print(coocc)
'''
    
'''
There will be two arrays to begin with:
    1) photoIDArray: This will contain image names in the form of photoid's
    2) tagStringArray: This will contain tag names in the form of tag strings
    

'''
# Stores photo ID's, parallel to tagStringArray
# NOTE: photoIDArray will contain duplicates
photoIDArray =      []
# Stores tag strings, parallel to photoIDArray
# NOTE: tagStringArray will contain duplicates
tagStringArray =    []
# Initialize the dictionary of the form (key:[value1, value2, ...]) = (int photoid:[tag1, tag3, tag9, ...])
id_tag_dictionary = defaultdict(list)

# Import photos_tags.csv into a list
import csv
with open("coursework-image-collection/csv/photos_tags.csv") as f:
    reader = csv.reader(f, delimiter=",")
    d = list(reader)

# Populate photoIDArray, tagStringArray and id_tag_dictionary
for element in d:
    photoIDArray.append(element[0])
    tagStringArray.append(element[1])
    # Append the tag string in the current element to the dictionary at that photo id
    id_tag_dictionary[int(element[0])].append(element[1])

# Initialize the dictionary which will represent the panda dataframes, of the form:
# (key:[value1, value2, ...]) = (tag string: [1, 0, 0, 1, etc]) where (1,0) represent
# whether the photo at that location contains the tag key
dataFrameDict = defaultdict(list)
# dataFrameDictionary = OrderedDict


# The first item in the dictionary will be Image_Key_2815: [image id 1, image id 2, image id 3, ...]
for photoid in id_tag_dictionary:
    dataFrameDict['Image_Key_2815'].append(int(photoid))
    

# iterate over all tags in tagStringArray
# It's converted to a set to remove duplicates, then back to a list again
for tag in list(set(tagStringArray)):
    
    # iterate over all image id's
    for imageid in dataFrameDict['Image_Key_2815']:
        
        # if the current tag pertains to the current image id, then append 1
        # to dataFrameDictionary at that tag
        if (tag in id_tag_dictionary[imageid]):
            dataFrameDict[tag].append(1)
        
        # Otherwise, append 0 to dataFrameDictionary at that tag
        else:
            dataFrameDict[tag].append(0)
            

# Now that the dataFrameDictionary has been created, it's time to create an actual Panda DataFrame

# Create an ordered dictionary from dataFrameDict, where Image_Key_2815 is at the start
dataFrameDictOrdered = OrderedDict(dataFrameDict)
dataFrameDictOrdered.move_to_end('Image_Key_2815', last=False)

df = pd.DataFrame(dataFrameDictOrdered).set_index('Image_Key_2815')
df_asint = df.astype(int)
co_occurrence_matrix = df_asint.T.dot(df_asint)

# Set the co-occurrence values of 'X' with 'X' to be 0
np.fill_diagonal(co_occurrence_matrix.values, 0)

# export data frame to csv
co_occurrence_matrix.to_csv('output.csv', sep=',', encoding='utf-8')