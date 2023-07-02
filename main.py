from load_instances import read_instance_students, read_instance_slot
from gouroby_func import model
from utils import distances, distance_param_cost
from path import path_instances


Exam_list, Student_list, Conflict_Dictionary, n_exams,\
n_students, enrollements, density = read_instance_students(path_instances, 'instance01.stu')

Timeslots, Timeslots_list = read_instance_slot(path_instances, 'instance01.slo')

Distances_list = distances(Timeslots)

Distance_Parameters = distance_param_cost(Distances_list,Timeslots)

m = model(Exam_list, Timeslots_list, Distances_list, Distance_Parameters, Conflict_Dictionary, n_students)






