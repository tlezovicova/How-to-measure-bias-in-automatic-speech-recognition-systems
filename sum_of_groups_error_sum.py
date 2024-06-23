import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_and_aggregate_data(filepath):
    # Load the CSV file
    bias_df = pd.read_csv(filepath)
    
    # Sum all errors for each model
    bias_df['Total_Bias_Error'] = bias_df.drop('Model', axis=1).sum(axis=1)
    return bias_df[['Model', 'Total_Bias_Error']]

def plot_total_bias_errors(aggregated_data):
    sns.set_palette("colorblind")  # Use a colorblind-friendly palette
    fig = plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x='Model', y='Total_Bias_Error', data=aggregated_data)
    plt.title('Total Sum of Bias Errors Per Model')
    plt.xlabel('Model')
    plt.ylabel('Total Bias Error')
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Save the figure as a PNG file
    fig.savefig("sum_of_group_sum_metrics_plot.png")

if __name__ == "__main__":
    # Specify the path to your CSV file
    filepath = 'sum_of_group_metric_results.csv'
    
    # Load and aggregate the data
    aggregated_data = load_and_aggregate_data(filepath)

    aggregated_data.to_csv('sum_of_group_sum_metric_results.csv', index=False)
    
    # Plot the total bias errors
    plot_total_bias_errors(aggregated_data)
