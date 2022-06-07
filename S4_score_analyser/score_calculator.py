# need to run guideline_parser.py first
#n Read its output csv here as input

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing





#---------------------------------------------------------------------------------------------------------------------------
def main():
    file_with_final_scores = './../3_Guideline_parser/output_data/final_output_with_density.csv'
    input_df = pd.read_csv(file_with_final_scores)
    output_dataset = pd.DataFrame(columns=['saved_file','total_score', 'comment_density', 'rate'])
    output_dataset = get_total_score(input_df, output_dataset)
    output_dataset = get_score_density_rate(output_dataset, output_dataset)
    output_dataset = get_scaled_score_density_rate(output_dataset,'rate')
    graph = draw_graph(output_dataset)


    
    return output_dataset


#--------------------------------------------------------------------------------------------------------------------



def get_total_score(input_df, output_df):
    new_saved_files = []
    new_total_scores = []
    new_comment_density = []
    
    for index, row in input_df.iterrows():
        new_saved_files.append(row['saved_file'])
        new_comment_density.append(row['comment_density'])
        
        # Calculatig the sum of the scores of one row
        total = 0 + row['marks_of_rule_1'] + row['marks_of_rule_2'] + row['marks_of_rule_3'] + row['marks_of_rule_8'] + row['marks_of_rule_12']
        new_total_scores.append(total)
        
    
    output_df['saved_file'] = new_saved_files
    output_df['total_score'] = new_total_scores
    output_df['comment_density'] = new_comment_density
    
    return output_df


#--------------------------------------------------------------------------------------------------------------------

def get_score_density_rate(input_df, output_df):
    new_saved_files = []
    new_total_scores = []
    new_comment_density = []
    new_rates = []
    
    for index, row in input_df.iterrows():
        new_saved_files.append(row['saved_file'])
        new_comment_density.append(row['comment_density'])
        new_total_scores.append(row['total_score'])
        
        # Calculatig the sum of the scores of one row
        rate = row['total_score'] / row['comment_density']
        new_rates.append(rate)
    
    output_df['saved_file'] = new_saved_files
    output_df['total_score'] = new_total_scores
    output_df['comment_density'] = new_comment_density
    output_df['rate'] = new_rates
    
    return output_df

def draw_graph(input_df):
    rate_values = input_df['scaled_rate']
    print(rate_values)
    
    sm.qqplot(rate_values)
    plt.plot([-2, 1.5], [0, 1.5])

    plt.show()


    # #Histogram
    plt.figure(figsize=(16,5))
    plt.subplot(1,2,1)
    sns.distplot(rate_values)
    plt.show()
    

def get_scaled_score_density_rate(input_df,column_name):
    scaler = StandardScaler()
    input_df['scaled_rate'] = my_scaler(0,1,input_df['rate'].astype(float))
    return input_df

def my_scaler(min_scale_num,max_scale_num,var):
    return (max_scale_num - min_scale_num) * ( (var - min(var)) / (max(var) - min(var)) ) + min_scale_num

def dddd(input_df):
    model = sm.OLS(input_df.total_score, input_df.comment_density)
    results = model.fit()
    print(results.summary())
    return results.summary()


#---------------------------------------------------------------------------------------------------------------------

if __name__=="__main__":
    fout = main()

