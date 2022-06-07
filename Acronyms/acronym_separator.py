import pandas as pd
import numpy as np
import string
import os

#--------------------------------------------------------------------------------------------------
def main():
    input_file = "D:\Educational\Academic\FYP Research\INTERIM\CODES\Acronyms\Acronyms_with_meaning.txt"
    output_file_path = "D:\Educational\Academic\FYP Research\INTERIM\CODES\Acronyms"
    
    df, output_file = acronym_classifier(input_file, output_file_path)
    
    return 0

#--------------------------------------------------------------------------------------------------

def acronym_classifier(input_file, output_file_path):
    
    if not os.path.exists(input_file):
        print("Input file path does not exist.")
        return -1
    
    # Using readlines()
    file1 = open(input_file, 'r', encoding='Latin1')
    Lines = file1.readlines()
    
    column_list, new_dictionary = get_new_dataframe()
    
    for line in Lines:
        line = line.strip()
        
        acronym = line.split('\t\t')[0]
        acronym = acronym.split('\s\s')[0]
        acronym = acronym.split('\t')[0]
        acronym = acronym.split('\s')[0]
        
        
        first_letter = acronym.upper()[0]
        if column_list.count(first_letter) > 0:
            the_tuple = new_dictionary[first_letter]
            the_tuple = the_tuple + (acronym,)
            new_dictionary[first_letter] = the_tuple
        else:
            the_tuple = new_dictionary['other']
            the_tuple = the_tuple + (acronym,)
            new_dictionary['other'] = the_tuple
    
    new_dictionary = remove_dictionary_duplicates(new_dictionary)
    df, output_file = save_dictionary_to_dataframe(new_dictionary, output_file_path)
    
    return df, output_file
        
#--------------------------------------------------------------------------------------------------

def remove_dictionary_duplicates(my_dictinary):
    
    for key, val in my_dictinary.items():
        the_tuple = my_dictinary[key]
        the_tuple = tuple(set(the_tuple))
        my_dictinary[key] = the_tuple
        
    return my_dictinary

#--------------------------------------------------------------------------------------------------

def get_new_dataframe():
    column_names = list(string.ascii_uppercase)
    column_names.append('other')
    
    
    my_dic = dict()
    for name in column_names:
        new_tuple = ()
        my_dic[name] = new_tuple
        
    
    return column_names, my_dic

#--------------------------------------------------------------------------------------------------

def save_dictionary_to_dataframe(my_dictionary, output_file_path):
    df = pd.concat([pd.DataFrame(v, columns=[k]) for k, v in my_dictionary.items()], axis=1)
    output_file = output_file_path+'\\acronym_table.csv'
    df.to_csv(output_file)
    return df, output_file



#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------



if __name__=="__main__":
    fout = main()


