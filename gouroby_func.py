import gurobipy as gp
from gurobipy import GRB
from load_instances import read_instance_students, read_instance_slot
from utils import distances, distance_param_cost
from path import path_instances


def model(Exames, Timeslots, Distances, Distance_Parameters, Conflict_Dictionary,Number_of_Students):

    env = gp.Env(empty=True)

    env.start()

    #env.setParam("Presolve", 2)

    #env.setParam("MIPGap", 1e-4)

    env.setParam("TimeLimit", 5000
                 )

    m = gp.Model("The Examination Timetabling Problem", env = env)

    print("Setting Variables")

    # X variables: 1 if the exam e is scheduled in the jth time slot
    #              0 otherwise

    x = m.addVars(((e,j) for e in Exames for j in Timeslots),
                    lb =0,
                    ub = 1,
                    vtype= GRB.BINARY,
                    name= f"Exam_Timeslot_Variable")

    # Y variables. 1 if the exam e i scheduled in the jtj timeslot and the exam k is schetuled in the timeslot j + d
    #              0 otherwise


    y = m.addVars(
                    ((e, j, k, d) for e in Exames
                                  for k in Exames if k != e
                                  for j in Timeslots
                                  for d in Distances if j + d <= max(Timeslots)),
                    lb=0,
                    ub=1,
                    vtype=GRB.BINARY,
                    name=f"Exams_Timeslot_Distance_Variable")

    print("Setting Objective")

    m.setObjective(
                    sum((y[e, j, k, d] * (2 ** (5 - Distance_Parameters[d])) * Conflict_Dictionary[e, k])
                                                                                   / Number_of_Students
                    for e in Exames
                    for k in Exames if k != e
                    for j in Timeslots
                    for d in Distances if j + d <= max(Timeslots)),
                  GRB.MINIMIZE)

    print("Setting At_most_in_one_Timeslot_Constraints")

    m.addConstrs((sum(x[e, j] for j in Timeslots) == 1 for e in Exames),f"At_most_in_one_Timeslot_Constraints")

    print("Setting Conflicting_Exames_Timeslot_Constraints")

    m.addConstrs((x[e, j] + x[k, j] <= 1 for e in Exames
                                         for k in Exames if e != k
                                                         and Conflict_Dictionary[e, k] > 0
                                         for j in Timeslots),
                  "Conflicting_Exames_Timeslot_Constraints")

    print("Setting Linking X and Y Constraints")

    #  if y[e,j,k,d] = 1  ===> x[e,j] = 1 and x[k,j+d] = 1

    print('-----First Family')

    m.addConstrs((y[e, j, k, d] <= x[e, j] for e in Exames
                                           for k in Exames if e != k
                                           for j in Timeslots
                                           for d in Distances if j + d <= max(Timeslots)),
                  'Linking_x-y_Constraints_Family_1')

    print('-----Second Family')

    m.addConstrs((y[e,j,k,d] <= x[k,j+d]   for e in Exames
                                           for k in Exames if e != k
                                           for j in Timeslots
                                           for d in Distances if j + d <= max(Timeslots)),
                  'Linking_x-y_Constraints_Family_2')

    print('-----Third Family')

    m.addConstrs((y[e,j,k,d] >= x[e,j] + x[k,j+d] - 1   for e in Exames
                                                        for k in Exames if e != k
                                                        for j in Timeslots
                                                        for d in Distances if j + d <= max(Timeslots)),
                  'Linking_x-y_Constraints_Family_3')

    print('Optimizing.....')

    m.optimize()

    print('Writing Solutions')

    m.write("Exames timetable scheduling.lp")
    m.write("Exames timetable scheduling.sol")

    return m


def solve(instance):

    Exam_list, Student_list, Conflict_Dictionary, n_exams, \
    n_students, enrollements, density = read_instance_students(path_instances, f'{instance}.stu')

    Timeslots, Timeslots_list = read_instance_slot(path_instances, f'{instance}.slo')

    Distances_list = distances(Timeslots)

    Distance_Parameters = distance_param_cost(Distances_list, 5)

    m = model(Exam_list, Timeslots_list, Distances_list, Distance_Parameters, Conflict_Dictionary, n_students)

    return m