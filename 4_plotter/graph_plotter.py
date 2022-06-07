# need to run guideline_parser.py first
#n Read its output csv here as input

import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '..')

from S4_score_analyser.score_calculator import get_total_score

#---------------------------------------------------------------------------------------------------------------------------
def main():
    file_with_final_scores = './../3_Guideline_parser/output_data/final_output_with_density.csv'
    input_df = pd.read_csv(file_with_final_scores)
    output_dataset = pd.DataFrame(columns=['saved_file','total_score', 'comment_density'])
    output_dataset = get_total_score(input_df, output_dataset)
    
    draw_graph(output_dataset)
    
    return output_dataset


#---------------------------------------------------------------------------------------------------------------------------

# def get_total_score(input_df, output_df):
#     new_saved_files = []
#     new_total_scores = []
#     new_comment_density = []
    
#     for index, row in input_df.iterrows():
#         new_saved_files.append(row['saved_file'])
#         new_comment_density.append(row['comment_density'])
        
#         # Calculatig the sum of the scores of one row
#         total = 0 + row['marks_of_rule_1'] + row['marks_of_rule_2'] + row['marks_of_rule_3'] + row['marks_of_rule_8'] + row['marks_of_rule_12']
#         new_total_scores.append(total)
        
    
#     output_df['saved_file'] = new_saved_files
#     output_df['total_score'] = new_total_scores
#     output_df['comment_density'] = new_comment_density
    
#     return output_df

#---------------------------------------------------------------------------------------------------------------------------
def draw_graph(dataset):
    dataset = dataset.sort_values('comment_density')
    # dataset.plot(x ='comment_density', y='total_score', kind = 'hist')
    plt.hist(dataset.total_score)
    plt.show()
    return 0

#---------------------------------------------------------------------------------------------------------------------------



#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
if __name__=="__main__":
    fout = main()
