import time
import json


def define_all_possible_combinations(actions, argent_initial):
    res = []
    cur_comb0 = []
    func_recursive(res, cur_comb0, actions, argent_initial)

    print(len(res))
    return res


def func_recursive(res, previous_comb, actions, argent_initial):
    # Loop on each action
    index_beg = previous_comb[-1] + 1 if len(previous_comb) > 0 else 1
    for index in range(index_beg, 25):
        # Build possible combination
        cur_comb = list(previous_comb)
        cur_comb.append(index)

        # If combination is not too expensive
        if compute_combination_cost(cur_comb, actions) <= argent_initial:
            # Add combination in result
            res.append(cur_comb)

            # Loop for second action
            func_recursive(res, cur_comb, actions, argent_initial)


def compute_combination_cost(comb, actions):
    comb_cost = 0
    for action in comb:
        current_action = actions[action]
        cost_for_one_action = current_action['Cost']
        comb_cost += cost_for_one_action
    return comb_cost


def compute_combination_benefit(comb, actions):
    comb_benefit = 0
    for action in comb:
        current_action = actions[action]
        benefice_for_one_action = (current_action['Cost'] * current_action['Benefice']) / 100
        comb_benefit += benefice_for_one_action
    return comb_benefit


if __name__ == '__main__':

    with open('data.json') as mon_fichier:
        actions_json = json.load(mon_fichier)

    actions = {int(k): actions_json[k] for k in actions_json}

    argent_initial = 500

    # Define all possible combination
    start = time.time()
    possible_combination = define_all_possible_combinations(actions, argent_initial)

    # Compute the benefit af each combination
    combination_benefits = []
    for combinaison in possible_combination:
        benefit = compute_combination_benefit(combinaison, actions)
        combination_benefits.append((combinaison, benefit))
    best_comb_and_benefit = max(combination_benefits, key=lambda x: x[1])

    # Define the best combination with highest benefit
    best_comb = best_comb_and_benefit[0]
    best_benefit = best_comb_and_benefit[1]
    print("La meilleure combinaison d'action est : " + str(best_comb) + " avec un benefice de : " + str(best_benefit))
    end = time.time()
    print("The time of execution of above program is :", end - start)
