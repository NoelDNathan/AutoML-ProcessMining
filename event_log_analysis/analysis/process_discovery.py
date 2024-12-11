import pm4py
from pm4py import fitness_token_based_replay
from pm4py.visualization.petri_net import visualizer as pn_visualizer
import pm4py.algo.evaluation.simplicity.algorithm as evaluate_simplicity
import pm4py.algo.evaluation.generalization.variants.token_based as evaluate_generalization
from event_log_analysis.utils.save_utils import SaveUtils

class ProcessDiscovery:
    """Class for process discovery and evaluation."""

    def __init__(self, log):
        self.log = log
        self.results = []  # To store evaluation results
        self.summary = ""  # To store text-based results for summary saving

    def run_all_miners_and_evaluate(self):
        miners = {
            "Alpha Miner": pm4py.discover_petri_net_alpha,
            "Heuristic Miner": pm4py.discover_petri_net_heuristics,
            "Inductive Miner": pm4py.discover_petri_net_inductive
        }
        # Header for CSV
        csv_header = ["Algorithm", "Fitness", "Simplicity", "Generalization"]

        print("Algorithm           | Fitness   | Simplicity | Generalization")
        self.summary += "Algorithm           | Fitness   | Simplicity | Generalization\n"

        for name, miner in miners.items():
            print(f"\n--- {name} ---")
            self.summary += f"\n--- {name} ---\n"
            net, im, fm = miner(self.log)
            gviz = pn_visualizer.apply(net, im, fm)
            pn_visualizer.view(gviz)

            # Evaluation
            fitness = fitness_token_based_replay(self.log, net, im, fm)["log_fitness"]
            simplicity = evaluate_simplicity.apply(net)
            generalization = evaluate_generalization.apply(self.log, net, im, fm)
            print(f"{name:18} | {fitness:.4f}   | {simplicity:.4f}     | {generalization:.4f}")
            self.summary += f"{name:18} | {fitness:.4f}   | {simplicity:.4f}     | {generalization:.4f}\n"

            self.results.append([name, fitness, simplicity, generalization])
        # Save results
        SaveUtils.save_csv("process_discovery_results.csv", self.results, csv_header)
        SaveUtils.save_summary("process_discovery_summary.txt", self.summary)