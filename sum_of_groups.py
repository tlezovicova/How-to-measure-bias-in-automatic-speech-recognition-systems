import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def calculate_bias_metric(df):
    # Calculate the average WER for each Model and Style combination
    average_wer = df.groupby(['Model', 'Style'])['WER'].mean().reset_index()
    average_wer.rename(columns={'WER': 'Average_WER'}, inplace=True)

    # Merge this average WER back into the original DataFrame
    df = pd.merge(df, average_wer, on=['Model', 'Style'])

    # Calculate the adjusted WER
    df['Bias_SumOfErrors'] = abs(1 - (df['WER'] / df['Average_WER']))

    return df

def plot_bias_metrics():
    data_path = "sum_of_group_metric_results.csv"  # Update the path if necessary
    bias_df = pd.read_csv(data_path)
    sns.set_context("talk")  # This sets a larger scale for all fonts
    sns.set_palette("colorblind")  # This sets the color palette for the plots

    # Set up the figure and axes
    fig, axs = plt.subplots(2, 1, figsize=(15, 15))
    
    # Plot DC-Rd metrics
    sns.barplot(x='Model', y='value', hue='variable', 
                data=pd.melt(bias_df, id_vars=['Model'], value_vars=['DC-Rd', 'DT-Rd', 'NnT-Rd', 'NnA-Rd', 'DOA-Rd']),
                ax=axs[0])
    axs[0].set_title('Sum of Groups Error - Rd')
    axs[0].set_xlabel('Models')
    axs[0].set_ylabel('Bias')
    axs[0].tick_params(axis='x', rotation=45)
    
# Plot DC-HMI metrics
    sns.barplot(x='Model', y='value', hue='variable', 
                data=pd.melt(bias_df, id_vars=['Model'], value_vars=['DC-HMI', 'DT-HMI', 'NnT-HMI', 'NnA-HMI', 'DOA-HMI']),
                ax=axs[1])
    axs[1].set_title('Sum of Groups Error - HMI')
    axs[1].set_xlabel('Models')
    axs[1].set_ylabel('Bias')
    axs[1].tick_params(axis='x', rotation=45)
    
    # Adjust layout
    plt.tight_layout()

    # Save the figure as a PNG file
    fig.savefig("sum_of_group_metrics_plot.png")

if __name__ == "__main__":
    # Set the color palette
    sns.set_palette("colorblind")
    
    # Load the WER data
    wer_df = pd.read_csv('wer_results.csv')

    bias_df = calculate_bias_metric(wer_df)

    bias_df['Group_Style'] = bias_df['Group'] + '-' + bias_df['Style']
    
    # Reshape the DataFrame to match the specified CSV structure
    # Assuming 'Group' in your structure refers to the model applied to various scenarios
    bias_metrics_pivot = bias_df.pivot_table(index='Model', columns='Group_Style', values='Bias_SumOfErrors', aggfunc='sum')

    bias_metrics_pivot = bias_metrics_pivot.round(2)

    bias_metrics_pivot.reset_index(inplace=True)
    
    # Save the bias metrics to a CSV file
    bias_metrics_pivot.to_csv('sum_of_group_metric_results.csv', index=False)

    sns.color_palette("colorblind")

    # Plot the bias metrics
    plot_bias_metrics()
