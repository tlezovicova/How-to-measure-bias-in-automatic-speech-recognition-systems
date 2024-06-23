import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_relative_metrics_seaborn():
    # Load the CSV data into a DataFrame
    data_path = "relative_data.csv"  # Update the path if necessary
    relative_data = pd.read_csv(data_path)
    
    sns.set_context("talk")  # This sets a larger scale for all fonts
    sns.set_palette("colorblind")  # This sets the color palette for the plots

    # Set up the figure and axes
    fig, axs = plt.subplots(2, 1, figsize=(15, 15))
    
    # Plot DC-Rd metrics
    sns.barplot(x='Relative', y='value', hue='variable', 
                data=pd.melt(relative_data, id_vars=['Relative'], value_vars=['DC-Rd', 'DT-Rd', 'NnT-Rd', 'NnA-Rd', 'DOA-Rd']),
                ax=axs[0])
    axs[0].set_title('G2min and G2norm - Rd')
    axs[0].set_xlabel('Demographic Groups')
    axs[0].set_ylabel('Bias')
    axs[0].tick_params(axis='x', rotation=45)
    
    # Plot DC-HMI metrics
    sns.barplot(x='Relative', y='value', hue='variable', 
                data=pd.melt(relative_data, id_vars=['Relative'], value_vars=['DC-HMI', 'DT-HMI', 'NnT-HMI', 'NnA-HMI', 'DOA-HMI']),
                ax=axs[1])
    axs[1].set_title('G2min and G2norm - HMI')
    axs[1].set_xlabel('Demographic Groups')
    axs[1].set_ylabel('Bias')
    axs[1].tick_params(axis='x', rotation=45)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure as a PNG file
    fig.savefig("relative_metrics_plot.png")

if __name__ == "__main__":
    plot_relative_metrics_seaborn()
