import pandas as pd
import numpy as np
import math
import csv
from collections import defaultdict
from collections import OrderedDict
    
'''
There will be two arrays to begin with:
    1) photoIDArray: This will contain image names in the form of photoid's
    2) tagStringArray: This will contain tag names in the form of tag strings
    

'''
def main():
    
    photoIDArray = [] # NOTE: photoIDArray will contain duplicates
    tagStringArray = [] # NOTE: tagStringArray will contain duplicates
    # Initialize the dictionary of the form (key:[value1, value2, ...]) = (int photoid:[tag1, tag3, tag9, ...])
    id_tag_dictionary = defaultdict(list)
    # Initialize the dictionary which will represent the panda dataframes, of the form:
    # (key:[value1, value2, ...]) = (tag string: [1, 0, 0, 1, etc]) where (1,0) represent
    # whether the photo at that location contains the tag key
    dataFrameDict = defaultdict(list)
    
    # Import photos_tags.csv into a list
    with open("coursework-image-collection/csv/photos_tags.csv") as f:
        reader = csv.reader(f, delimiter=",")
        d = list(reader)
    
    # Populate photoIDArray, tagStringArray and id_tag_dictionary
    for element in d:
        photoIDArray.append(element[0])
        tagStringArray.append(element[1])
        # Append the tag string in the current element to the dictionary at that photo id
        id_tag_dictionary[int(element[0])].append(element[1])
        
    
    # The first item in the dictionary will be Image_Key_2815: [image id 1, image id 2, image id 3, ...]
    for photoid in id_tag_dictionary:
        dataFrameDict['Image_Key_2815'].append(int(photoid))
        
    
    # iterate over all tags in tagStringArray; set is to remove duplicates
    for tag in list(set(tagStringArray)):
        for imageid in dataFrameDict['Image_Key_2815']:
            # if the current tag pertains to the current image id, then append 1
            # to dataFrameDictionary at that tag
            if (tag in id_tag_dictionary[imageid]):
                dataFrameDict[tag].append(1)
            # Otherwise, append 0 to dataFrameDictionary at that tag
            else:
                dataFrameDict[tag].append(0)
                
    
    # Create an ordered dictionary from dataFrameDict, where Image_Key_2815 is at the start
    dataFrameDictOrdered = OrderedDict(dataFrameDict)
    dataFrameDictOrdered.move_to_end('Image_Key_2815', last=False)
    
    # Use dataFrameDictOrdered to create a co-occurrence matrix
    df = pd.DataFrame(dataFrameDictOrdered).set_index('Image_Key_2815')
    df_asint = df.astype(int)
    co_occurrence_matrix = df_asint.T.dot(df_asint)
    
    # Set the co-occurrence values of 'X' with 'X' to be 0
    np.fill_diagonal(co_occurrence_matrix.values, 0)
    
    # export data frame to csv
    co_occurrence_matrix.to_csv('output.csv', sep=',', encoding='utf-8')
    print("\nTask 1: The co-occurrence matrix has been generated and outputted to the file \"output.csv\"\n")
    
    # Find the top 5 tags for water, people and london
    print("Task 2: Compute the top 5 tags for Water, People and London.")
    print("\nWater: \n")
    print(co_occurrence_matrix.loc['water'].nlargest(5))
    print("\nPeople: \n")
    print(co_occurrence_matrix.loc['people'].nlargest(5))
    print("\nLondon: \n")
    print(co_occurrence_matrix.loc['london'].nlargest(5))
    
    
    # Import tags.csv into a dictionary of tag : count
    d = {}
    with open("coursework-image-collection/csv/tags.csv") as f:
        for line in f:
           (key, val) = line.split(',')
           d[key] = val
    
    i = len(set(photoIDArray)) # compute i for the IDF formula
    
    # compute and apply IDF score for all tags
    for tag in set(tagStringArray):
        ix = int(d[tag])
        idf = math.log(i/ix)
        co_occurrence_matrix.loc[tag, :] = co_occurrence_matrix.loc[tag, :] * idf
        co_occurrence_matrix[tag] = co_occurrence_matrix[tag] * idf
        
    # Find the top 5 tags for water, people and london after applying the IDF formula
    print("\nTask 3: Recommend tags for water, people and London based on their popularity and significance.")
    print("\nWater: \n")
    print(co_occurrence_matrix.loc['water'].nlargest(5))
    print("\nPeople: \n")
    print(co_occurrence_matrix.loc['people'].nlargest(5))
    print("\nLondon: \n")
    print(co_occurrence_matrix.loc['london'].nlargest(5))
    
main()