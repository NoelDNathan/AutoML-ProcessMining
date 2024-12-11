from log_loader import LogLoader
from analysis.log_analyzer import LogAnalyzer
from analysis.process_discovery import ProcessDiscovery

# --------------------------- CONFIGURATION ---------------------------
FILE_PATH = "data/PermitLog.xes.gz"
STYLE = "ggplot"

def main():
    # Load the log file
    log = LogLoader.load_log(FILE_PATH)

    # Log Analysis
    print("\n--- Event Log Analysis ---")
    analyzer = LogAnalyzer(log, style=STYLE)
    print("\n--- Start and End Activities ---")
    print("\n--- Case Length vs Throughput Analysis ---")
    analyzer.analyze_case_length_vs_throughput()

    print("\n--- Top Activity Pairs ---")
    analyzer.analyze_activity_pairs()
    analyzer.analyze_start_end_activities()
    print("\n--- Variants Analysis ---")
    analyzer.analyze_variants()
    print("\n--- Frequencies Analysis ---")
    analyzer.analyze_activity_frequencies(limit=10)
    print("\n--- Case Lengths Analysis")
    analyzer.analyze_case_lengths()
    print("\n--- Throughput Time Analysis ---")
    analyzer.analyze_throughput_time()
    print("\n--- Activity Boxplot ---")
    analyzer.analyze_activity_boxplot()
    print("\n--- Start End Activities Analysis ---")
    analyzer.analyze_start_end_activities()
    print("\n--- Case Length vs Throughput Analysis ---")
    analyzer.analyze_case_length_vs_throughput()

    print("\n--- Top Activity Pairs ---")
    analyzer.analyze_activity_pairs()
    # Save the final summary
    analyzer.save_summary()
    print("\n--- Analysis Complete! Results saved to the 'results' folder. ---")
    print("\n--- Complete Analysis Summary Saved! ---")

    # Process Discovery and Evaluation
    print("\n--- Process Model Discovery and Evaluation ---")
    discovery = ProcessDiscovery(log)
    discovery.run_all_miners_and_evaluate()

if __name__ == "__main__":
    main()
