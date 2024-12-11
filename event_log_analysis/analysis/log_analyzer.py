from matplotlib import pyplot as plt
from pm4py.statistics.start_activities.log.get import get_start_activities
from pm4py.statistics.end_activities.log.get import get_end_activities
from pm4py.statistics.traces.generic.log import case_statistics
from pm4py.algo.filtering.log.attributes import attributes_filter
from event_log_analysis.utils.plot_utils import PlotUtils
from event_log_analysis.utils.save_utils import SaveUtils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.util import sorting
import pandas as pd
class LogAnalyzer:
    """Class for event log analysis."""

    def __init__(self, log, style="ggplot"):
        self.log = log
        self.analysis_summary = ""
        self.csv_data = []
        plt.style.use(style)

    def analyze_start_end_activities(self):
        start_activities = get_start_activities(self.log)
        end_activities = get_end_activities(self.log)
        PlotUtils.plot_bar(start_activities, "Start Activities Distribution", "Activities", "Count", "lightblue")
        SaveUtils.save_plot("start_activities.png")
        # Save summary
        summary = f"Start Activities:\n{start_activities}\n\nEnd Activities:\n{end_activities}\n"
        self.analysis_summary += summary
        PlotUtils.plot_bar(end_activities, "End Activities Distribution", "Activities", "Count", "salmon")
        SaveUtils.save_plot("end_activities.png")
        # Save CSV
        data = [[k, v] for k, v in start_activities.items()]
        SaveUtils.save_csv("start_activities.csv", data, ["Activity", "Count"])
    def analyze_variants(self):
        variants = case_statistics.get_variant_statistics(self.log)
        top_variants = sorted(variants, key=lambda x: x['count'], reverse=True)[:10]
        # Extract variant names and counts
        variant_labels = [
            (str(v['variant'])[:30] + "...") if len(str(v['variant'])) > 30 else str(v['variant'])
            for v in top_variants
        ]
        variant_counts = [v['count'] for v in top_variants]
        PlotUtils.plot_horizontal_bar( variant_counts,variant_labels, "Top 10 Variants", "Cases")
        SaveUtils.save_plot("top_variants.png")

    def analyze_activity_frequencies(self, limit=10):
        activities = attributes_filter.get_attribute_values(self.log, "concept:name")
        PlotUtils.plot_bar(activities, "Top 10 Activity Frequencies", "Activities", "Frequency", "skyblue", limit)
        SaveUtils.save_plot("top_activity_frequencies.png")

    def analyze_case_lengths(self):
        case_lengths = [len(trace) for trace in self.log]
        avg_length = sum(case_lengths) / len(case_lengths)
        PlotUtils.plot_histogram(case_lengths, "Case Length Distribution", "Events per Case", "Cases")
        SaveUtils.save_plot("case_length_distribution.png")
        summary = f"Case Length Analysis:\nMin: {min(case_lengths)}, Max: {max(case_lengths)}, Avg: {avg_length:.2f}\n"
        self.analysis_summary += summary
        # Save CSV
        data = [[i, l] for i, l in enumerate(case_lengths)]
        SaveUtils.save_csv("case_lengths.csv", data, ["Case ID", "Length"])
    def analyze_throughput_time(self):
        """Analyze throughput time using case durations."""
        case_durations = case_statistics.get_all_case_durations(self.log, parameters={"time_unit": "days"})
        print(f"\nThroughput Time Analysis:")
        print(f"Min: {min(case_durations):.2f} days")
        print(f"Max: {max(case_durations):.2f} days")
        print(f"Avg: {sum(case_durations) / len(case_durations):.2f} days")

        # Plot the throughput time
        PlotUtils.plot_histogram(case_durations, "Throughput Time Distribution", "Days", "Cases")
        SaveUtils.save_plot("throughput_time_distribution.png")

    def analyze_activity_boxplot(self):
        activities = attributes_filter.get_attribute_values(self.log, "concept:name")
        PlotUtils.plot_boxplot(list(activities.values()), "Boxplot of Activity Frequencies")
        SaveUtils.save_plot("activity_frequency_boxplot.png")

    def analyze_case_length_vs_throughput(self):
        """Analyze case length vs throughput time."""
        # Step 1: Convert DataFrame to EventLog if needed
        if isinstance(self.log, pd.DataFrame):
            event_log = log_converter.apply(self.log, variant=log_converter.Variants.TO_EVENT_LOG)
        else:
            event_log = self.log

        # Step 2: Sort the log by timestamp
        sorted_log = sorting.sort_timestamp(event_log)

        # Step 3: Compute case lengths and durations
        case_lengths = []
        case_durations = []

        for trace in sorted_log:
            # Calculate case length
            case_lengths.append(len(trace))

            # Calculate duration (end time - start time)
            start_time = trace[0]['time:timestamp']
            end_time = trace[-1]['time:timestamp']
            duration = (end_time - start_time).total_seconds() / (60 * 60 * 24)  # Convert to days
            case_durations.append(duration)

    def analyze_activity_pairs(self):
        """Analyze and visualize bigram (consecutive activity) frequencies."""
        pairs = {}
        for trace in self.log:
            for i in range(len(trace) - 1):
                pair = (trace[i]['concept:name'], trace[i + 1]['concept:name'])
                pairs[pair] = pairs.get(pair, 0) + 1

        top_pairs = sorted(pairs.items(), key=lambda x: x[1], reverse=True)[:10]
        pair_names = [f"{p[0]} -> {p[1]}" for p, _ in top_pairs]
        counts = [count for _, count in top_pairs]

        PlotUtils.plot_horizontal_bar(counts, pair_names,  "Top 10 Activity Pairs", "Frequency")
        SaveUtils.save_plot("top_activity_pairs.png")
    def save_summary(self):
        """Save the accumulated analysis summary."""
        SaveUtils.save_summary("summary.txt", self.analysis_summary)