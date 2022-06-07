# Need to run repo_miner_1.py  first 


import pandas as pd
import numpy as np
import re


    
    
    
#======================================================================================================
def main():
    dataset1 = pd.read_csv('./../1_Repo_miner/repo_miner_output_datasets/url_with_extracted_comments.csv')
    indexNamesToRemove = dataset1[ pd.isna(dataset1['comment_text'])].index
    dataset1 = dataset1.drop(indexNamesToRemove,inplace=False).reset_index(drop=True)
    
    dataset1 = attach_ending_line_numbers_and_comment_line_count(dataset1)
    dataset1 = attach_main_comment_category(dataset1)
    dataset1 = attach_consecutive_marker_number(dataset1)
    dataset1 = mark_codeInlined_comments(dataset1)
    
    dataset1.to_csv('classified_output_datasets/categorized_comment_list_d2.csv', index=False)
    return dataset1
#======================================================================================================

#-------------------------------------------------------------------------------------------------------

# Calculate end line number and no of lines in comments
def attach_ending_line_numbers_and_comment_line_count(ds):
    noOfLines = []
    ending_line_numbers = []
    for i in range(0, len(ds)):
      c = ds.iloc[i]['comment_text']
      nLines = c.count('\n')
      ending_number = nLines + ds.iloc[i]['starting_line_number']
      noOfLines.append(nLines + 1)
      ending_line_numbers.append(ending_number)
    
    ds['ending_line_number'] = ending_line_numbers
    ds['line_count'] = noOfLines
    return ds

#------------------------------------------------------------------------------------------------------

# Note
# DOCC :    This includes all comments starting with /**
# MULTIC :  This includes all comments starting with /*      ( even a single line comment is catgorized as a MULTIC)
# SINGLEC :  This includes all comments starting with //

def attach_main_comment_category(ds):
    comment_categories = []   # DOCC, MULTIC, SINGLEC   
    for i in range(0, len(ds)):   
      sc = ds.iloc[i]['full_source_code']
      scLines = sc.splitlines()
    
      if ds.iloc[i]['is_multiLine']:   #For multile Comments
        for j in range(0, len(scLines)):
          if j+1 == ds.iloc[i]['starting_line_number']:
            rLine = scLines[j].strip()
            if rLine.startswith("/**"):           # for Doc comments
              comment_categories.append('DOCC')
            else:                                 # For /*     */ comments
              comment_categories.append('MULTIC')
    
      else:      #For single Comments
        comment_categories.append('SINGLEC')
    
    ds['comment_category'] = comment_categories
    return ds

#------------------------------------------------------------------------------------------------------

def attach_consecutive_marker_number(ds):
    consecutive_markers = []   # True or False
    marker = 1
    starting_line_numbers = ds['starting_line_number']
    for i in range(0,len(ds)-1):
      init_number = starting_line_numbers[i]
      if init_number+1 == starting_line_numbers[i+1]:
        consecutive_markers.append(marker)
      else:
        consecutive_markers.append(marker)
        marker = marker+1
    
    consecutive_markers.append(marker)   # Add marker for last row
    
    ds['consecutive_marker'] = consecutive_markers
    return ds

#------------------------------------------------------------------------------------------------------

def mark_codeInlined_comments(ds):
    is_inline_with_code_list = []
    for i in range(0, len(ds)):
      comment_category = ds.iloc[i]['comment_category']
      if ((comment_category == 'SINGLEC') | (comment_category == 'MULTIC')) & (1 == ds.iloc[i]['line_count']):
        starting_line_number = ds.iloc[i]['starting_line_number']
        sc = ds.iloc[i]['full_source_code']
        scLines = sc.splitlines()
        full_code_line = scLines[starting_line_number-1]
        subtitute_string = re.sub("//.*|/\\*(?s:.*?)\\*/|(\"(?:(?<!\\\\)(?:\\\\\\\\)*\\\\\"|[^\r\n\"])*\")", "$1", full_code_line)
        subtitute_string = subtitute_string.strip()
        
        if subtitute_string.startswith("$1"):
          is_inline_with_code_list.append(False)
          
        else:
          is_inline_with_code_list.append(True)
          
        
        
      else:
        is_inline_with_code_list.append(False)
    
    ds['is_inlined_with_code_line'] = is_inline_with_code_list
    return ds
#------------------------------------------------------------------------------------------------------


if __name__=="__main__":
    fout = main()




















