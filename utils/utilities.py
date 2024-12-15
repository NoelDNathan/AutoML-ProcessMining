import pm4py
import pm4py.algo.evaluation.simplicity.algorithm as evaluate_simplicity
from pm4py.algo.evaluation.generalization import algorithm as evaluate_generalization
import pm4py.algo.evaluation.generalization.variants.token_based as evaluate_generalization
from scipy.stats import wilcoxon
from IPython.display import clear_output
from pm4py.algo.filtering.log.start_activities import start_activities_filter
from pm4py.algo.filtering.log.end_activities import end_activities_filter
import sys
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay


sys.path.append("../")
path_metrics = "../results/metrics.csv"

import pandas as pd


class Utilities:
    @staticmethod
    def mixed_score(log, model, verbose=False):
        (net, initial_marking, final_marking) = model
        fitness = Utilities.fitness_score(log, model)
        simplicity = Utilities.simplicity_score(log, model)
        generalization = Utilities.generalization_score(log, model)

        if verbose:
            print("Fitness: ", fitness)
            print("Simplicity: ", simplicity)
            print("Generalization: ", generalization)


        return (fitness + simplicity + generalization) / 3

    @staticmethod
    def fitness_score(log, model):
        (net, initial_marking, final_marking) = model
        fitness_res = token_replay.apply(log, net, initial_marking, final_marking)
        
        if isinstance(fitness_res, list) and len(fitness_res) > 0:
            total_fitness = sum(res["trace_fitness"] for res in fitness_res if "trace_fitness" in res)
            num_traces = len(fitness_res)
            fitness = total_fitness / num_traces if num_traces > 0 else 0.0
        else:
            fitness = 0.0

        return fitness
    
    @staticmethod
    def generalization_score(log, model):
        (net, initial_marking, final_marking) = model
        return evaluate_generalization.apply(log, net, initial_marking, final_marking)
    
    def simplicity_score(log, model):
        (net, initial_marking, final_marking) = model
        return evaluate_simplicity.apply(net)



    @staticmethod
    def wilcoxon_signed_rank_test(
        log, baseline_model, optimized_model, eval_func_name, alpha=0.05, n=300, m=100
    ):

        if eval_func_name == "mixed":
            eval_func = Utilities.mixed_score
        elif eval_func_name == "fitness":
            eval_func = Utilities.fitness_score
        else:
            raise ValueError(
                "Invalid evaluation function name. Please choose 'mixed_score' or 'fitness'"
            )

        baseline_scores = []
        optimized_scores = []

        option = 1

        if option == 1:
            block_size = n
            num_blocks = len(log) // block_size
            for i in range(num_blocks):
                sample = log.iloc[i * block_size : block_size * (i + 1)]

                x = eval_func(sample, baseline_model)
                y = eval_func(sample, optimized_model)
                baseline_scores.append(x)
                optimized_scores.append(y)
                clear_output()

            if len(log) % block_size != 0:
                sample = log.iloc[num_blocks * block_size :]

                x = eval_func(sample, baseline_model)
                y = eval_func(sample, optimized_model)

                baseline_scores.append(x)
                optimized_scores.append(y)

        if option == 2:
            for i in range(m):
                sample = log.sample(n)
                baseline_scores.append(eval_func(sample, baseline_model))
                optimized_scores.append(eval_func(sample, optimized_model))
                clear_output()

        # Perform Wilcox signed-rank test to compare the losses
        statistic, p_value = wilcoxon(baseline_scores, optimized_scores)

        print("\nWilcoxon Signed-Rank Test (Log Loss):")
        print(f"Statistic: {statistic:.4f}, P-value: {p_value:.4f}")
        # Interpret the results
        if p_value < alpha:
            print("The optimized pipeline significantly beats the baseline.")
        else:
            print(
                "There is no significant difference between the optimized pipeline and baseline."
            )

        return statistic, p_value

    @staticmethod
    def evaluate_and_save(log, model, model_name, eval_func_name, cv=10):

        if eval_func_name == "mixed":
            eval_func = Utilities.mixed_score
        elif eval_func_name == "fitness":
            eval_func = Utilities.fitness_score
        else:
            raise ValueError(
                "Invalid evaluation function name. Please choose 'mixed_score' or 'fitness'"
            )

        scores = []
        block_size = len(log) // cv
        num_blocks = 10
        for i in range(num_blocks):
            if i == num_blocks - 1:
                block = log[i * block_size :]
            else:
                block = log[i * block_size : block_size * (i + 1)]
            scores.append(eval_func(block, model))
            clear_output()

        name = model_name + "_" + eval_func_name

        df = pd.read_csv(path_metrics)        
        if name in df.columns:
            df = df.drop(columns=[name])
        df[model_name + "_" + eval_func_name + "_scores"] = scores
        df.to_csv(path_metrics, index=False)

        return scores
