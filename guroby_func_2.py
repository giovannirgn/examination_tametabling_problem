import gurobipy as gp
from gurobipy import GRB,quicksum
from load_instances import read_instance_students, read_instance_slot
from utils import  distance_2, comb_exames,get_solution,get_objective,is_feasible
from path import path_instances


def model2(Exames, Timeslots, Distances, Conflict_Dictionary,Number_of_Students,instance):

    env = gp.Env(empty=True)

    env.start()

    env.setParam("TimeLimit",100)

    m = gp.Model("The Examination Timetabling Problem", env=env)

    # X variables: 1 if the exam e is scheduled in the jth time slot
    #              0 otherwise

    x = m.addVars(((e,j) for e in Exames for j in Timeslots),
                    lb =0,
                    ub = 1,
                    vtype= GRB.BINARY,
                    name= f"Exam_Timeslot_Variable")

    len_exames_timeslot_var = len(x)
    print(f'lenght of Exam_Timeslot_Variable {len_exames_timeslot_var}')

    # Y variables. 1 if the exam e is scheduled in the jth timeslot and the exam k is scheduled in the timeslot j + d
    #              0 otherwise

    y = m.addVars(
                    ((e, k, d)     for e,k in comb_exames(Exames) if Conflict_Dictionary[e, k] > 0
                                   for d in Distances),
                    lb=0,
                    ub=1,
                    vtype=GRB.BINARY,
                    name=f"Exams_Timeslot_Distance_Variable")

    len_exames_distance_var = len(y)
    print(f'lenght of Exam_Distance_Variable {len_exames_distance_var}')

    print("Setting Objective")

    m.setObjective(
                    quicksum((y[e,k,d] * (2 ** (5 - d)) * Conflict_Dictionary[e, k])/ Number_of_Students for e, k in comb_exames(Exames) if Conflict_Dictionary[e, k] > 0
                                                                                                         for d in Distances),
                                                                                                         GRB.MINIMIZE)

    print("Setting At_most_in_one_Timeslot_Constraints")

    m.addConstrs(
                   (quicksum(x[e, j] for j in Timeslots) == 1 for e in Exames),f"At_most_in_one_Timeslot_Constraints")

    m.addConstrs(
                   (x[e, j] + x[k, j] <= 1 for e, k in comb_exames(Exames) if Conflict_Dictionary[e, k] > 0
                                           for j in Timeslots),
                                           "Conflicting_Exames_Timeslot_Constraints")

    print('Setting Linking X and Y Constraints')

    m.addConstrs(
                    (x[e, j] + x[k, j + d] + x[e, j + d] + x[k, j] <= 1 + y[e, k, d] for e, k in comb_exames(Exames) if Conflict_Dictionary[e, k] > 0
                                                                                     for j in Timeslots
                                                                                     for d in Distances if j + d <= max(Timeslots)),
                                                                                     'Linking_x-y_Constraints_Family_1')

    print('Optimizing.....')

    m.optimize()

    print('Writing Solutions')

    m.write(f"solutions/Exames timetable scheduling_Problem_{instance}.lp")
    m.write(f"solutions/Exames timetable scheduling_Solution_{instance}.sol")

    return m


def solve2(instance):

    Exam_list, Student_list, Conflict_Dictionary, n_exams, \
    n_students, enrollements, density = read_instance_students(path_instances, f'{instance}.stu')

    Timeslots, Timeslots_list = read_instance_slot(path_instances, f'{instance}.slo')

    Distances_list = distance_2(5)

    m = model2(Exam_list, Timeslots_list, Distances_list, Conflict_Dictionary, n_students,instance)

    return n_exams, n_students, enrollements, Timeslots, density, m.objVal,m, Conflict_Dictionary, n_students, Exam_list

def write_result2(instance):

    n_exams, n_students, enrollements, Timeslots, density, objVal,m, Conflict_Dictionary, n_students, ex_list = solve2(instance)

    print("Check")

    sol = get_solution(m)

    obj_ok = get_objective(sol, Conflict_Dictionary, n_students, objVal)

    feas_ok = is_feasible(sol, Conflict_Dictionary, ex_list)

    print("The objective value is correct?", obj_ok)
    print('The solution is feasible?',feas_ok)

    with open('results.txt', 'a') as f:

        f.write('\n')
        f.write(f'{instance},{n_exams},{n_students},{enrollements},{Timeslots},{density},{objVal}')

    return



