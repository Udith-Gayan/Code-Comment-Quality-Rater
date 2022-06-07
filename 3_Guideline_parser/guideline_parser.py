# need to run comment_classifier.py first
#n Read its output csv here as input

import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize

from Comment_density_calculation_3_1.Comment_density_calculator import calculate_comment_density

#================================================================================================

def main():
    classified_dataset = pd.read_csv("./../2_Comment_classifier/classified_output_datasets/categorized_comment_list_d2.csv")
    output_dataset = pd.DataFrame(columns=['saved_file','marks_of_rule_1'])       # Initialize output dataset
    output_dataset = run_rule_one(classified_dataset, output_dataset)
    output_dataset = run_rule_two(classified_dataset, output_dataset)
    output_dataset = run_rule_three(classified_dataset, output_dataset)
    output_dataset = run_rule_eight(classified_dataset, output_dataset)
    
    # Rule 12
    acronym_file = "D:\Educational\Academic\FYP Research\INTERIM\CODES\Acronyms\\acronym_table.csv"
    output_dataset = run_rule_twelve(classified_dataset, output_dataset, acronym_file)
    
    output_dataset = calculate_comment_density(classified_dataset, output_dataset)

    output_dataset.to_csv('output_data/final_output_with_density.csv', index=False)


    return output_dataset

#================================================================================================

#-------------------------------------------------------------------------------------------------------------

#Guide Line - 1
# (1/2) Comment blocks that introduce large sections of code and are more than 2 lines long should use /* */ (C) style .

def run_rule_one(dataset, output_dataset,allowed_score = 4.12):
    dataset_grouped_by_source = dict(tuple(dataset.groupby(['saved_file'])))

    saved_files = []
    marks_of_rule_1 = []
    for key_source in dataset_grouped_by_source:
      marks = 0.0
      one_source_set = dataset_grouped_by_source[key_source]
      for i in range(0,len(one_source_set)):
        theTupple = one_source_set.iloc[i]
        if (theTupple['comment_category'] == 'MULTIC') & (theTupple['line_count'] > 2):
            marks = marks + allowed_score
            
      
      
      
      
      # source_set_grouped_by_consecutive_marker = dict(tuple(one_source_set.groupby(['consecutive_marker'])))
      # for marker_key in source_set_grouped_by_consecutive_marker:
      #   if (len(source_set_grouped_by_consecutive_marker[marker_key]) <= 2) & any(source_set_grouped_by_consecutive_marker[marker_key]['comment_category'] == 'SINGLEC'):
      #     marks = marks + allowed_score
      saved_files.append(key_source)
      marks_of_rule_1.append(marks)
    
    output_dataset['saved_file'] = saved_files
    output_dataset['marks_of_rule_1'] = marks_of_rule_1
    
    output_dataset.to_csv('output_data/marks_with_Rule_1.csv', index=False)
    return output_dataset

#-------------------------------------------------------------------------------------------------------------
# Guide Line - 2
# 1. Comments within /* */ should use * on each line with the same space/tab rules as doc blocks.

def run_rule_two(dataset, output_dataset, allowed_score = 3.85):
    dataset_grouped_by_source = dict(tuple(dataset.groupby(['saved_file'])))

    saved_files = []
    marks_of_rule_2 = []
    
    for key_source in dataset_grouped_by_source:
      marks = 0
      one_source_set = dataset_grouped_by_source[key_source]
      source_set_grouped_by_comment_category = dict(tuple(one_source_set.groupby(['comment_category'])))
    
      for marker_key in source_set_grouped_by_comment_category:
        tupleList = source_set_grouped_by_comment_category[marker_key]
    
        if (marker_key == 'MULTIC') & any(source_set_grouped_by_comment_category[marker_key]['comment_category'] == 'MULTIC'):
          for index,eachTuple in tupleList.iterrows():   #tuples looping
           
            source_code_lines = eachTuple['full_source_code'].splitlines()
            starting_line_number = eachTuple['starting_line_number']
            ending_line_number = eachTuple['ending_line_number']
           
    
            line_count = eachTuple['line_count']
            comment_lines = []
    
            if line_count > 1:
             
              for i in range(0, len(source_code_lines)):
                k = i+1
                if (k >= starting_line_number) & (k <= ending_line_number):
                  # print(f'Comment Lne nummber: {k}')
                  
                  comment_lines.append(source_code_lines[i])
                
              
              tempo_score = 0
    
              first_line = comment_lines[0]
              first_indentation_pattern = []
              for eachletter in first_line:
                if eachletter in [' ', '\t','/', '*', ' ']:
                  first_indentation_pattern.append(eachletter)
                else:
                  break
              
              
              middle_lines_indentation_pattern = ""
              middle_lines_indentation_pattern = middle_lines_indentation_pattern.join(first_indentation_pattern)
              middle_lines_indentation_pattern = middle_lines_indentation_pattern.replace('/',' ')   # replace to check for next lines
              
    
              for i in range(0, len(comment_lines)):
                if i == 0:
                  continue
                if i == (len(comment_lines)-1):
                  break
                if comment_lines[i].startswith(middle_lines_indentation_pattern):
                  tempo_score = tempo_score + 1
    
              last_line_indentation_pattern = ''.join(first_indentation_pattern)
              star_position = last_line_indentation_pattern.find('*')
              last_line_indentation_pattern = "".join((last_line_indentation_pattern[:star_position-1]," ",last_line_indentation_pattern[star_position:]))
              last_line_indentation_pattern = "".join((last_line_indentation_pattern[:star_position+1],"/",last_line_indentation_pattern[star_position+2:]))
              last_line_indentation_pattern = last_line_indentation_pattern.rstrip()
             

              
    
              if (tempo_score == (len(comment_lines) - 2)):
                
                marks = marks + allowed_score
    
            else:  #if line count is 1
              
              marks = marks + allowed_score
     
      saved_files.append(key_source)
      marks_of_rule_2.append(marks)
    
    output_dataset['marks_of_rule_2'] = marks_of_rule_2
    output_dataset.to_csv('output_data/marks_with_Rule_1_2.csv', index=False)
    return output_dataset

#-------------------------------------------------------------------------------------------------------------

# Guideline 3
# Don’t use a blank line between comments and the code they refer to (no space underneath a comment block).
def run_rule_three(dataset, output_dataset, allowed_score = 3.70):
    dataset_grouped_by_source = dict(tuple(dataset.groupby(['saved_file'])))
    
    marks_of_rule_3 = []
    
    for key_source in dataset_grouped_by_source:
      marks = 0
      one_source_set_tuples = dataset_grouped_by_source[key_source]
    
      # ----------------------------------------------------------------------
      # Condition one ( For non-consecutive MULTIC and DOCC)
      for i in range(0,len(one_source_set_tuples)):
        theTupple = one_source_set_tuples.iloc[i]
    
        sourceCode = theTupple['full_source_code']
        scLines = sourceCode.splitlines()
    
        is_Inlined = theTupple['is_inlined_with_code_line']
        cType = theTupple['comment_category']
        lineCount = theTupple['line_count']
    
        startingLineNumber = theTupple['starting_line_number']
        endingLineNumber = theTupple['ending_line_number']
    
        nextComment_StartingLineNumber = -500
        is_nextComment_inlined = False
        if not i == (len(one_source_set_tuples) - 1):
          nextComment_StartingLineNumber = one_source_set_tuples.iloc[i+1]['starting_line_number']
          is_nextComment_inlined = one_source_set_tuples.iloc[i+1]['is_inlined_with_code_line']
    
        is_nextLine_also_a_comment_but_inlined = (((endingLineNumber+1) == nextComment_StartingLineNumber) and is_nextComment_inlined) or (not ((endingLineNumber+1) == nextComment_StartingLineNumber))  # check - next line is a code line or a space
        
        if (cType == 'DOCC' and is_nextLine_also_a_comment_but_inlined) or (cType == 'MULTIC' and lineCount > 1 and is_nextLine_also_a_comment_but_inlined) or (cType == 'MULTIC' and lineCount == 1 and not is_Inlined and is_nextLine_also_a_comment_but_inlined):
           nextLine = scLines[startingLineNumber].strip()
           if not nextLine == '':
             marks = marks + allowed_score
             
    
      
    
      # ----------------------------------------------------------------------
      # Checking SINGLEC Comments after grouping
      new_dataset_with_singlec_only = one_source_set_tuples
      indexes_with_other_two_types = new_dataset_with_singlec_only[(new_dataset_with_singlec_only['comment_category'] == 'MULTIC') | (new_dataset_with_singlec_only['comment_category'] == 'DOCC')].index
      new_dataset_with_singlec_only = new_dataset_with_singlec_only.drop(indexes_with_other_two_types, inplace = False ).reset_index(drop = True)
    
      dataset_group_by_consecutive_marker = dict(tuple(new_dataset_with_singlec_only.groupby(['consecutive_marker'])))
      
      ending_line_numbers = []   # This can be null if no single line comments available
      for marker_key in dataset_group_by_consecutive_marker:
        marked_tuples = dataset_group_by_consecutive_marker[marker_key]
        last_tuple = marked_tuples.iloc[-1]
        ending_line_numbers.append(last_tuple['ending_line_number'])
    
      for lc_ending_line_number in ending_line_numbers:
        last_record = one_source_set_tuples.query(f'ending_line_number == {lc_ending_line_number}').iloc[0]
        last_record_index = one_source_set_tuples.query(f'ending_line_number == {lc_ending_line_number}').index[0]
        next_record_index = last_record_index + 1
    
        ending_line_number = last_record['ending_line_number']
        
        sc = last_record['full_source_code']
        scLines = sc.splitlines()
        nextLine = scLines[ending_line_number]
        stripped_nextLine = nextLine.strip()
    
        # Checking if next line is a comment but inline
        nextLine_is_okay_to_proceed = True
        next_line_number = ending_line_number + 1
        if any(one_source_set_tuples.starting_line_number == next_line_number):
          next_record = one_source_set_tuples.query(f'starting_line_number == {next_line_number}').iloc[0]
          if next_record['is_inlined_with_code_line']:
            nextLine_is_okay_to_proceed = True
          else:
            nextLine_is_okay_to_proceed = False
        
        if nextLine_is_okay_to_proceed:
          if not stripped_nextLine == '':
            marks = marks + allowed_score
            # --
    
      
      marks_of_rule_3.append(marks)
    
    output_dataset['marks_of_rule_3'] = marks_of_rule_3
    output_dataset.to_csv('output_data/marks_with_Rule_1_2_3.csv', index=False)
    
    return output_dataset

#-------------------------------------------------------------------------------------------------------------

#Guideline 08
#Always have a space between // and the start of the comment text. 
def run_rule_eight(dataset, output_dataset, allowed_score = 4.01):
    dataset_grouped_by_source = dict(tuple(dataset.groupby(['saved_file'])))

    marks_of_rule_8 = []
    
    for key_source in dataset_grouped_by_source:
      marks = 0
      one_source_set_tuples = dataset_grouped_by_source[key_source]
    
      # ----------------------------------------------------------------------
      # Extract SINGLEC comments and check if it has a space after //
      for i in range(0,len(one_source_set_tuples)):
        theTupple = one_source_set_tuples.iloc[i]
    
        sourceCode = theTupple['full_source_code']
        scLines = sourceCode.splitlines()
    
        is_Inlined = theTupple['is_inlined_with_code_line']
        cType = theTupple['comment_category']
        startingLineNumber = theTupple['starting_line_number']
        
        if cType == 'SINGLEC':       # For SINGLEC comments only
            comment_text = scLines[startingLineNumber-1].strip()
            if not is_Inlined:       #For in_lined == false
                if comment_text[2] == ' ':
                    marks = marks + allowed_score
            else:                    # for in_lined == true comments
                # find the position of the second / and check for the next position whether it is a space
                second_dash_index = comment_text.find('/', comment_text.find('/') + 1)
                space_index = second_dash_index + 1
                if comment_text[space_index] == ' ':
                    marks = marks + allowed_score
            
      marks_of_rule_8.append(marks)
    
    output_dataset['marks_of_rule_8'] = marks_of_rule_8
    output_dataset.to_csv('output_data/marks_with_Rule_1_2_3_8.csv', index=False)
    return output_dataset




#-------------------------------------------------------------------------------------------------------------

# Guideline 12
# Capitalise all letters of acronyms such as HTML, XML, SQL, GMT, and UTC. 
def run_rule_twelve(dataset, output_dataset,acronym_file_path, allowed_score = 3.96):
    acronym_df = pd.read_csv(acronym_file_path)
    
    dataset_grouped_by_source = dict(tuple(dataset.groupby(['saved_file'])))
    marks_of_rule_12 = []
    
    for key_source in dataset_grouped_by_source:
        marks = 0
        one_source_set = dataset_grouped_by_source[key_source]
        #looping the group to get comment text in each record
        for i in range(len(one_source_set)):
            comment_text = one_source_set.iloc[i]['comment_text']
            text_lines = comment_text.splitlines()
            #looping each line in a comment
            for k in range(len(text_lines)):
                a_line = text_lines[k]
                #Tokenize the lines into words
                tokens = a_line.split()
                # For each token or word
                for token in tokens:
                    first_letter = token[0]
                    if first_letter.isalpha():
                        first_letter_upper = first_letter.upper()
                        if token.upper() in acronym_df[first_letter_upper].values and token.isupper():
                            # Give one mark
                            marks = marks + allowed_score
                    else: # Check 'OTHER' column
                        if token.upper() in acronym_df['other'].values and token.isupper():
                            marks = marks + allowed_score
        
        marks_of_rule_12.append(marks)
    output_dataset['marks_of_rule_12'] = marks_of_rule_12
    output_dataset.to_csv('output_data/marks_with_Rule_1_2_3_8_12.csv', index=False)
    return output_dataset



#-------------------------------------------------------------------------------------------------------------




#-------------------------------------------------------------------------------------------------------------



if __name__=="__main__":
    fout = main()
