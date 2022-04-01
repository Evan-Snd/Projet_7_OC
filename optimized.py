import time
import csv
import statistics


# res = [[1],[2],[3],[5]]
def define_all_possible_combinations(actions, argent_initial, param):
    res = []
    cur_comb0 = []
    func_recursive(res, cur_comb0, actions, argent_initial, param)

    return res


def func_recursive(res, previous_comb, remaining_actions, remaining_money, param):
    res_found = False
    # Build possible combination
    # Recuperer la valeur max du benefice

    liste_index_best_benefice = find_best_benef_index(remaining_actions, remaining_money, param)

    actions_available = dict(remaining_actions)
    for index in liste_index_best_benefice:
        # Build possible combination
        cur_comb = list(previous_comb)
        cur_comb.append(index)
        del actions_available[index]
        # print("la combinaison actuel est : {}".format(cur_comb))

        # If combination is not too expensive
        if remaining_actions[index]['Cost'] <= remaining_money:
            found = func_recursive(res, cur_comb, actions_available, remaining_money - remaining_actions[index]['Cost'],
                                   param)

            if not found:
                res.append(cur_comb)
                res_found = True

    return res_found


def find_best_benef_index(dict_actions, remaining_money, param):
    liste_index_best_benefice = []

    max_cost = 0
    index_cost = 0
    for k in dict_actions:
        best_cost_action = dict_actions[k]['Cost']
        if best_cost_action > max_cost:
            max_cost = best_cost_action
            index_cost = k
    # print(index_cost)

    if index_cost != 0 and dict_actions[index_cost]['Cost'] < remaining_money:
        param = 1

    tmp_actions_available = {i: dict_actions[i] for i in dict_actions if dict_actions[i]['Cost'] <= remaining_money}

    n = min(param, len(tmp_actions_available))

    for y in range(n):
        max_benef = 0
        index_benef = 0
        for action in tmp_actions_available:
            benef_current = tmp_actions_available[action]['Benefice']
            if benef_current > max_benef:
                max_benef = benef_current
                index_benef = action
        liste_index_best_benefice.append(index_benef)
        tmp_actions_available.pop(index_benef)
    # print("    best index : {}".format(liste_index_best_benefice))
    return liste_index_best_benefice


def compute_combination_benefit(comb, actions):
    comb_benefit = 0
    for action in comb:
        current_action = actions[action]
        benefice_for_one_action = (current_action['Cost'] * current_action['Benefice']) / 100
        comb_benefit += benefice_for_one_action
    return comb_benefit


def compute_combinaison_name(comb, actions):
    list_name_actions = []
    for action in comb:
        current_name_action = actions[action]['name']
        list_name_actions.append(current_name_action)
    return list_name_actions


full_actions = {}
reader = csv.DictReader(open(r"C:\Users\sinda\OneDrive\Bureau\FormationPython\dataset2_Python+P7.csv"))
i = 0

for raw in reader:
    i += 1
    full_actions[i] = {'name': raw['name'], 'Cost': float(raw['price']), 'Benefice': float(raw['profit'])}

# print(len(full_actions))
actions_positive = {i: full_actions[i] for i in full_actions if float(full_actions[i]['Cost']) > 0}
rendement_dict = {int(k): actions_positive[k]['Benefice'] / actions_positive[k]['Cost'] for k in actions_positive}
moy_rendement = statistics.mean(list(rendement_dict[k] for k in rendement_dict))
actions = {i: full_actions[i] for i in actions_positive if rendement_dict[i] > moy_rendement / 10}
# print(len(actions))
# print(moy_rendement)

argent_initial = 500

parameter = 3

# Define all possible combination
start = time.time()
possible_combination = define_all_possible_combinations(actions, argent_initial, parameter)

# Compute the benefit af each combination
combination_benefits = []
for combinaison in possible_combination:
    benefit = compute_combination_benefit(combinaison, actions)
    combination_benefits.append((combinaison, benefit))
best_comb_and_benefit = max(combination_benefits, key=lambda x: x[1])

# Define the best combination with highest benefit
best_comb = best_comb_and_benefit[0]
best_benefit = best_comb_and_benefit[1]
best_comb_name = list(compute_combinaison_name(best_comb, actions))
print(
    "La meilleure combinaison d'action est : \n {} ".format(best_comb_name) + "\n\nAvec un benefice de : {}".format(
        best_benefit))
end = time.time()
print("The time of execution of above program is :", end - start)
from guppy import hpy
h = hpy()
print(h.heap())
