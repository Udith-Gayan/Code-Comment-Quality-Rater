import re

def calculate_comment_density(dataset, output_dataset):
    
    dataset_grouped_by_source = dict(tuple(dataset.groupby(['saved_file'])))
    
    comment_density_list = []
    
    for key_source in dataset_grouped_by_source:
      one_source_set = dataset_grouped_by_source[key_source]
      #First record is only used for calculation
      first_record = one_source_set.iloc[0]
      full_source_code = first_record['full_source_code']
      total_lines_count_in_file = get_line_count(full_source_code)
      total_comment_line_count = 0
      
      #looping the group to get comment text in each record
      for i in range(len(one_source_set)):
          comment_text = one_source_set.iloc[i]['comment_text']
          comment_line_count = get_line_count(comment_text)
          total_comment_line_count = total_comment_line_count + comment_line_count
      
        
      print('total lines = ', total_lines_count_in_file)    #print
      print('total comment lines = ', total_comment_line_count)    #print
      
      
      comment_density_percentage = (total_comment_line_count / total_lines_count_in_file) * 100.00
      comment_density_list.append(comment_density_percentage)
      print('total density = ', comment_density_percentage)    #print
      
    output_dataset['comment_density'] = comment_density_list

    return output_dataset


def get_line_count(inputText):
    text_lines = inputText.splitlines()
    line_count = 0
    #For each line
    for line in text_lines:
        # Remove spaces on two ends strip
        string_value = line.strip()
        # Remove special character except { ( )} and alpha-mumeric character
        string_value = re.sub(r'[^A-Za-z0-9(){}]', '', string_value)
        
        # if still not empty, count++
        if len(string_value) > 0 :
            line_count += 1
    
    return line_count