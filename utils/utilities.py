import pm4py
import pm4py.algo.evaluation.simplicity.algorithm as evaluate_simplicity
import pm4py.algo.evaluation.generalization.variants.token_based as evaluate_generalization
from scipy.stats import wilcoxon
from IPython.display import clear_output
net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(log)
from pm4py.algo.filtering.log.start_activities import start_activities_filter
from pm4py.algo.filtering.log.end_activities import end_activities_filter


class Utilities:
    @staticmethod
    def mixed_score(log, model, verbose = False):
        (net, initial_marking, final_marking) = model
        fitness        = pm4py.fitness_token_based_replay(log, net, initial_marking, final_marking)
        simplicity     = evaluate_simplicity.apply(net)
        generalization = evaluate_generalization.apply(log, net, initial_marking, final_marking)    
        
        if verbose:
            print("Fitness: ", fitness)
            print("Simplicity: ", simplicity)
            print("Generalization: ", generalization)
        
        fitness_score = fitness['log_fitness']

        return (fitness_score + simplicity + generalization) / 3
    
    @staticmethod
    def fitness_score(log, model):
        (net, initial_marking, final_marking) = model
        fitness = pm4py.fitness_token_based_replay(log, net, initial_marking, final_marking)
        return fitness['log_fitness']

    @staticmethod
    def wilcoxon_signed_rank_test(log, baseline_model, 
                                    optimized_model, 
                                    eval_func_name,
                                    alpha = 0.05, 
                                    n = 300, 
                                    m = 100):

        if eval_func_name == "mixed":
            eval_func = Utilities.mixed_score
        elif eval_func_name == "fitness":
            eval_func = Utilities.fitness_score
        else:
            raise ValueError("Invalid evaluation function name. Please choose 'mixed_score' or 'fitness'")
                             
        baseline_scores = []
        optimized_scores = []


        option = 1

        if option == 1:
            block_size = n
            num_blocks = len(log) // block_size
            for i in range(num_blocks):
                sample = log.iloc[i*block_size:block_size*(i+1)]

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
                "There is no significant difference between the optimized pipeline and baseline.")

        return statistic, p_value

    @staticmethod
    def filter_log_by_start_and_end(log, start_activity, end_activity):
        """
        Filter a log to keep only traces that start with `start_activity` and end with `end_activity`.

        :param log: The input event log (PM4Py log object)
        :param start_activity: The required starting activity (string)
        :param end_activity: The required ending activity (string)
        :return: A filtered log with only the desired traces
        """
        # Filter traces that start with the specified activity
        log_start_filtered = start_activities_filter.apply(log, {start_activity})
        
        # Filter traces that end with the specified activity
        log_filtered = end_activities_filter.apply(log_start_filtered, {end_activity})
        
        return log_filtered


