import os.path
from os import path
from datetime import datetime
import wget
import pandas as pd

from comment_parser import comment_parser
from comment_parser import parsers
# https://github.com/jeanralphaviles/comment_parser


#===========================================================================================================

def main():
    
    # test_java_file = 'repo_miner_input_datasets/java_commented_file_urls.csv'
    # ankiAndroid_url_file = 'repo_miner_input_datasets/Anki-Android.csv'
    # jitsi_url_file = 'repo_miner_input_datasets/jitsi.csv'
    # moshi_file = 'repo_miner_input_datasets/moshi.csv'
    # all_three_repos_files = 'repo_miner_input_datasets/all_three_repo_urls.csv'
    

    # This is online ur dataset
    # url_dataset = pd.read_csv(all_three_repos_files)
    # new_dataset = create_dataset_with_extracted_comments(url_dataset, False)
    
    test_files = 'repo_miner_input_datasets/Test/java_commented_local_file_paths.csv'
    #This is for local java files
    url_dataset = pd.read_csv(test_files)
    new_dataset = create_dataset_with_extracted_comments(url_dataset, True)
    
    return new_dataset
    

#===========================================================================================================


#------------------------------------------------------------------------------------

#Create github raw URL from a normal page URL
def get_raw_url(url):
  url = url.replace('github.com', 'raw.githubusercontent.com', 1)
  url = url.replace('/blob/', '/',1)
  return url;


#Read a file and return the content
def get_file_content(source_path):
  f = open(source_path, "r")
  file_content = f.read()
  return file_content

#------------------------------------------------------------------------------------

def get_full_comment_of_a_file(filePath):
    z = comment_parser.extract_comments(filePath, mime='text/x-java-source')
    return z
  
#------------------------------------------------------------------------------------

# This method is for downloading files from github
# Download each file as a java file and extract full comment detail list
def download_and_get_full_comment_list_of_a_file(url):
  """
  Attributes
  -----------
  url: str
     raw-url of a java file and the url must end with '.java' extension.
  
  Returns
  --------
  A list containing comment units(comment,line_number,isMultiline)
  """
  
  # This two lines should run only one time
  if path.exists('repo_miner_input_datasets/tempo_code_files') == False:
      os.mkdir('repo_miner_input_datasets/tempo_code_files')
  
  
  #Creating file name
  now_time =datetime.now()
  millisec = now_time.timestamp() * 10000
  millisec = str(millisec).split('.')[0]
  partial_name = url.split('/')[-1].split('.')[0]
  file_name = partial_name + millisec + '.java'

  #Download the file and save in colab location
  wget.download(url, f"repo_miner_input_datasets/tempo_code_files/{file_name}")

  saved_file = f"repo_miner_input_datasets/tempo_code_files/{file_name}"
  z = get_full_comment_of_a_file(saved_file)

  file_content = get_file_content(saved_file)
  
  return z, saved_file, file_content

#------------------------------------------------------------------------------------

def create_dataset_with_extracted_comments(dataset_with_urls_or_file_paths, is_local_path):
    repeated_saved_file = []
    repeated_saved_code = []
    comment_text_list = []
    comment_starting_line_number_list = []
    comment_is_multiLine = []

    # Create a new dataset with above details
    new_dataset_1 = pd.DataFrame(columns=['saved_file', 'full_source_code', 'comment_text','starting_line_number','is_multiLine'])

    
    # For each repo url 
    for url in dataset_with_urls_or_file_paths['url']:
        raw_path = get_raw_url(url) if not is_local_path else url
  
        # Local paths or not
        if not is_local_path:
            comment_list_of_a_file, saved_file, file_content = download_and_get_full_comment_list_of_a_file(raw_path)
        else:
            comment_list_of_a_file = get_full_comment_of_a_file(raw_path)
            saved_file = raw_path
            file_content = get_file_content(raw_path)
  
        # For each comment unit of a file
        for full_comment in comment_list_of_a_file:
            repeated_saved_file.append(raw_path)
            repeated_saved_code.append(file_content)
            # print('\n-------------------------------------\n')
            # print(full_comment)
            # print(str(full_comment.line_number).split(',')[-2])
    
            comment_text_list.append(full_comment)
            comment_starting_line_number_list.append(int(str(full_comment.line_number).split(',')[-2]))
            # print(bool(str(full_comment.line_number).split(',')[-1].split(')')[0]))
            comment_is_multiLine.append(eval(str(full_comment.line_number).split(',')[-1].split(')')[0]))

  
  
  
    new_dataset_1['saved_file'] = repeated_saved_file
    new_dataset_1['full_source_code'] = repeated_saved_code
    new_dataset_1['comment_text'] = comment_text_list
    new_dataset_1['starting_line_number'] = comment_starting_line_number_list
    new_dataset_1['is_multiLine'] = comment_is_multiLine

    print(len(comment_text_list))
    # print(new_dataset_1['is_multiLine'])
  
    # Save the dataset to a csv file
    new_dataset_1.to_csv(r'repo_miner_output_datasets/url_with_extracted_comments.csv', index=False, mode='w+')
    return new_dataset_1

  
#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

if __name__=="__main__":
    fout = main()



#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------