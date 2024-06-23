import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_bias_metric(df):
    # Calculate the average WER for each Model and Style combination
    average_wer = df.groupby(['Model', 'Style'])['WER'].mean().reset_index()
    average_wer.rename(columns={'WER': 'Average_WER'}, inplace=True)

    # Merge this average WER back into the original DataFrame
    df = pd.merge(df, average_wer, on=['Model', 'Style'])

    # Calculate the adjusted WER
    df['Bias_Average'] = -np.log(df['WER'] / df['Average_WER'])

    return df

def plot_bias_metrics():
    data_path = "bias_metric_results.csv"  # Update the path if necessary
    bias_df = pd.read_csv(data_path)
    bias_df['Total_Bias_Error'] = bias_df.drop('Model', axis=1).sum(axis=1)
    bias_df = bias_df[['Model', 'Total_Bias_Error']]
    sns.set_palette("colorblind")  # Use a colorblind-friendly palette
    fig = plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x='Model', y='Total_Bias_Error', data=bias_df)
    plt.title('Total Sum of Bias Errors Per Model')
    plt.xlabel('Model')
    plt.ylabel('Total Bias Error')
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Save the figure as a PNG file
    fig.savefig("bias_metric_sum_metrics_plot.png")

if __name__ == "__main__":
    # Load the WER data
    wer_df = pd.read_csv('wer_results.csv')
    
    # Calculate the bias metrics
    bias_df = calculate_bias_metric(wer_df)

    bias_df['Group_Style'] = bias_df['Group'] + '-' + bias_df['Style']
    
    # Reshape the DataFrame to match the specified CSV structure
    # Assuming 'Group' in your structure refers to the model applied to various scenarios
    bias_metrics_pivot = bias_df.pivot_table(index='Model', columns='Group_Style', values='Bias_Average', aggfunc='sum')

    bias_metrics_pivot = bias_metrics_pivot.round(2)

    bias_metrics_pivot.reset_index(inplace=True)
    # Save the bias metrics to a CSV file
    bias_metrics_pivot.to_csv('bias_metric_results.csv', index=False)
    

    # Plot the bias metrics
    plot_bias_metrics()