from itertools import combinations

def comb_exames(Exames):
    return combinations(Exames,2)


def distances(time_slots):
    return [i for i in range(time_slots)]


def distance_param_cost(distances_list,max_distance_penality):

    dist_param = dict()

    for dist in distances_list:

        if dist > max_distance_penality:

            dist_param[dist] = max_distance_penality

        else:

            dist_param[dist] = dist

    return dist_param


def distance_2(dist_penality):

    return [i for i in range(1,dist_penality+1)]

def get_solution(m):

    solution = {}

    for v in m.getVars():
        if 'Distance' not in v.VarName:
            if v.X >= 0.5:
                solution[v.VarName.split('[')[1].split(',')[0]] = int(
                    v.VarName.split('[')[1].split(',')[1].split(']')[0])
    return solution


def get_objective(solution, Conflict_Dictionary, n_students,objVal):

    exames = list(solution.keys())

    combinations = comb_exames(exames)

    obj = 0

    for i,j in combinations:

        if Conflict_Dictionary[(i,j)] > 0:

            dist = abs(solution[i]-solution[j])

            penality = 0

            if dist <= 5:

                penality = 2**(5-dist)

            else:

                penality = 0

            obj += (Conflict_Dictionary[(i,j)]/n_students)*penality

    if round(obj,3) !=  round(objVal,3):

        return False

    return True

def is_feasible(solution, Conflict_Dictionary, ex_list ):

    exames = list(solution.keys())

    no_conflict = True

    one_timeslot = False

    if len(exames) == len(ex_list):

        one_timeslot = True

    combinations = comb_exames(exames)

    for i,j in combinations:

        if Conflict_Dictionary[(i, j)] > 0:

            if solution[i] == solution[j]:

                no_conflict = False

    return no_conflict and one_timeslot









