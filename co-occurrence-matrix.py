import pandas as pd
import numpy as np
import math
import csv
from collections import defaultdict
from collections import OrderedDict
import string
    
co_occurrence_matrix = None
co_occurrence_matrix_pop_sig = None

def main():
    
    global co_occurrence_matrix
    global co_occurrence_matrix_pop_sig
    
    banner()
    
    print("Generating co-occurrence matrix...  ", end="")
    
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
    
    co_occurrence_matrix_pop_sig = co_occurrence_matrix.copy()
    
    # Import tags.csv into a dictionary of tag : count
    d = {}
    with open("coursework-image-collection/csv/tags.csv") as f:
        for line in f:
           (key, val) = line.split(',')
           d[key] = val
    
    i = len(set(photoIDArray)) # compute i for the IDF formula
    photoIdArray = None # no longer needed
    
    # compute and apply IDF score for all tags
    for tag in set(tagStringArray):
        ix = int(d[tag])
        idf = math.log(i/ix)
        co_occurrence_matrix_pop_sig.loc[tag, :] = co_occurrence_matrix_pop_sig.loc[tag, :] * idf
        co_occurrence_matrix_pop_sig[tag] = co_occurrence_matrix_pop_sig[tag] * idf
    tagStringArray = None #  no longer needed
    
    print("complete")
    
    export()
    
    tag_options()
        
    
''' Print the top 5 tags which occur with water, people and london '''
def recommend(com):
    
    flag = True
    
    while(flag):
    
        choice = input("\nWould you like to (a) choose a tag for recommendation, (b) use (water, people, london), or (q) quit?  (a/b/q)  ").lower()
        
        if (choice == 'a') | (choice == '(a)'):
            choice = input('Enter a tag to receive recommendations or type \'q\' to quit.  ').lower()
            if (choice == 'q') | (choice == 'quit'):
                flag = false
            else:
                print('\n' +  choice + ': \n')
                print(com.loc[choice].nlargest(5))
        elif (choice == 'b') | (choice == '(b)'):
            print("\nWater: \n")
            print(com.loc['water'].nlargest(5))
            print("\nPeople: \n")
            print(com.loc['people'].nlargest(5))
            print("\nLondon: \n")
            print(com.loc['london'].nlargest(5))
        elif (choice == 'q') | (choice == '(q)'):
            flag = False
        else:
            flag = True

    
def banner():
    print(" _______ _______ _______ _____    _______              \n" + 
        "|   |   |     __|   _   |  |  |  |_     _|.---.-.-----.\n" + 
"|       |__     |       |__    |   |   |  |  _  |  _  |\n" + 
"|__|_|__|_______|___|___|  |__|    |___|  |___._|___  |\n" + 
"                                                |_____|\n" + 
" ______                                                    __         __   __              \n" + 
"|   __ \.-----.----.-----.--------.--------.-----.-----.--|  |.---.-.|  |_|__|.-----.-----.\n" + 
"|      <|  -__|  __|  _  |        |        |  -__|     |  _  ||  _  ||   _|  ||  _  |     |\n" + 
"|___|__||_____|____|_____|__|__|__|__|__|__|_____|__|__|_____||___._||____|__||_____|__|__|\n" + 
"                                                                                           \n" + 
" _______               __                  \n" + 
"|     __|.--.--.-----.|  |_.-----.--------.\n" + 
"|__     ||  |  |__ --||   _|  -__|        |\n" + 
"|_______||___  |_____||____|_____|__|__|__|\n" + 
"         |_____|  ")
    
    
def export():
    global co_occurrence_matrix
    
    choice = input('Would you like to export the co-occurrence matrix to a .csv file? (y/n)  ')
    
    if (choice.lower() == 'y') | (choice.lower() == 'yes'):
        
        # export data frame to csv
        co_occurrence_matrix.to_csv('output.csv', sep=',', encoding='utf-8')
        print("The co-occurrence matrix has been outputted \"output.csv\"\n")
        
        
def tag_options():
    global co_occurrence_matrix
    global co_occurrence_matrix_pop_sig
    
    choice = input('Would you like tag recommendations based on their popularity and significance? (y/n)  ')
    if (choice.lower() == 'y') | (choice.lower() == 'yes'):
        print('Recommending tags based on popularity and significance.')
        recommend(co_occurrence_matrix_pop_sig)
    else:
        print('Recommending tags NOT based on popularity and significance.')
        recommend(co_occurrence_matrix)
    
    
main()