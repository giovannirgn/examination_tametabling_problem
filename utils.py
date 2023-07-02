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