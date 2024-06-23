# How-to-measure-bias-in-automatic-speech-recognition-systems

## Overview
This repository contains the implementation and results of an extensive analysis of bias metrics in Automatic Speech Recognition (ASR) systems. The project aims to explore various bias metrics that do not rely on a reference group, providing insights into the fairness and performance disparities across different demographic groups.

## Repository Structure
- `average.py`: Script to calculate G2Average metric.
- `sum_of_groups.py`: Script to calculate Sum of Group Error Differences metric
- `bias_metric.py`: Script to caluclate my bias metric.
- `config.json`: Configuration file with parameters for the scripts.
- `diff_baseline.py`, `rel_baseline.py`: Scripts for setting baseline measures for different bias metrics.
- `wer_calculate.py`: Script to calculate Word Error Rates (WER).
- CSV Files: Contain raw data and results from the metrics calculations.
- PNG Files: Visualization plots generated from the analysis.
- asr_output: Error rates per demographic group

## Results
- `average_metric_results.csv`: Results from average metrics calculations.
- `bias_metric_results.csv`: Detailed results from bias metrics.
- `relative_data.csv`, `diff_data.csv`: Processed data files for relative and differential metrics.


### Running the Scripts
1. Run the metric calculation scripts to generate new data:
   ```bash
   python wer_calculate.py
   python bias_metric.py
   ```
2. See the results in corresponding CSV files and plots in corresponding PNG files


## Contact
For any queries regarding this project, please contact [t.lezovicova@student.tudelft.nl].
