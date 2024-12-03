import pm4py
import pm4py.algo.evaluation.simplicity.algorithm as evaluate_simplicity
import pm4py.algo.evaluation.generalization.variants.token_based as evaluate_generalization

def evaluate_petri_net(log, net, initial_marking, final_marking ,verbose = False):
    fitness        = pm4py.fitness_token_based_replay(log, net, initial_marking, final_marking)
    simplicity     = evaluate_simplicity.apply(net)
    generalization = evaluate_generalization.apply(log, net, initial_marking, final_marking)
    
    if verbose:
        print("Fitness: ", fitness)
        print("Simplicity: ", simplicity)
        print("Generalization: ", generalization)

    return fitness['log_fitness'], simplicity, generalization