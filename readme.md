

# Event Log Analysis and Process Discovery

## Overview
This project provides an end-to-end solution for analyzing event logs and discovering process models. The tool utilizes the **PM4Py** library for event log analysis, process discovery, and evaluation. All results, including plots and metrics, are saved automatically for easy reporting and further analysis.

---
## Ultimate Goal
Our ultimate goal is to **develop a system that automates the selection and tuning of process discovery algorithms**. The system should:
- Perform **detailed exploratory data analysis (EDA)** on event log datasets to uncover insights about the process flows, case variations, and bottlenecks.

- Automatically select the best algorithm for a given event log dataset.
- Optimize hyperparameter settings to improve model quality.
- Use automated optimization techniques to ensure the highest performance of discovered process models.

---
## Features

### Event Log Analysis
1. **Start and End Activities Analysis**:
   - Visualizes the most frequent starting and ending activities.
2. **Variant Analysis**:
   - Identifies and visualizes the top 10 most frequent process variants.
3. **Activity Frequency Analysis**:
   - Plots the top 10 most frequent activities in the log.
4. **Case Length Distribution**:
   - Analyzes and visualizes the distribution of case lengths (number of events per case).
5. **Throughput Time Analysis**:
   - Calculates and visualizes the duration (in days) for all cases.
6. **Case Length vs Throughput Correlation**:
   - Identifies relationships between case lengths and their throughput times.
7. **Activity Pair Analysis**:
   - Analyzes the most frequent pairs of consecutive activities.

### Process Discovery and Evaluation
- Implements three process discovery algorithms:
  - **Alpha Miner**
  - **Heuristic Miner**
  - **Inductive Miner**
- Evaluates each model using:
  - **Fitness**: Measures how well the model explains the log.
  - **Simplicity**: Evaluates the complexity of the discovered model.
  - **Generalization**: Measures how well the model generalizes to unseen traces.

---

## Output
Results are saved automatically in the `results` folder:
- **Plots**: High-quality PNG files (e.g., `start_activities.png`, `top_variants.png`).
- **Metrics**:
  - CSV files (e.g., `process_discovery_results.csv`, `start_activities.csv`).
  - Summaries in text format (e.g., `process_discovery_summary.txt`, `summary.txt`).

---

## Folder Structure
```
event_log_analysis/
│── requirements.txt              # libraries needed to start the project
├── main.py                       # Main entry point
├── log_loader.py                 # Log loading logic
├── analysis/
│   ├── log_analyzer.py           # Event log analysis module
│   ├── process_discovery.py      # Process discovery and evaluation
│
├── utils/
│   ├── plot_utils.py             # Utilities for plotting
│   └── save_utils.py             # Utilities for saving plots and results
│
├── data/
│   └── PermitLog.xes             # Input XES log file
│
└── results/
    ├── plots/                    # Saved plots
    ├── process_discovery_results.csv
    ├── process_discovery_summary.txt
    ├── start_activities.csv
    └── summary.txt
├── notebooks/
│   └── EDA.ipynb ## Complete Analysis for XES log files

```

---

## Installation

### Prerequisites
- Python 3.8+
- PM4Py Library
- Matplotlib and Seaborn

### Install Dependencies
Run the following commands to install all required libraries:
```bash
pip install -r requirements.txt
conda install python-graphviz
```

---

## How to Run
1. Place your XES log file in the `data` folder (e.g., `PermitLog.xes`).
2. Update the `FILE_PATH` in `main.py` if needed.
3. Run the main script:
   ```bash
   python main.py
   ```

---

## Results
After execution, results will be stored in the `results` folder. Check the following:
1. **Plots**: High-quality visualizations.
2. **Summaries**: Text-based insights and CSV outputs.
3. **Metrics**: Evaluation of process models for Fitness, Simplicity, and Generalization.

---


## Acknowledgement 
This project is developed as part of the **Explainable Automated Machine Learning** course at the **University of Tartu** under the supervision of [Prof. Radwa ElShawi](https://github.com/RadwaElShawi).

---

## Authors
- [Ahmed Wael](https://github.com/ahmedwael19)  
- [Mohamed Maher](https://github.com/mmaher22)  
- [Noel Nathan](https://github.com/NoelDNathan)  

---