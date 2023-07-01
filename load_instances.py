def read_instance_students(file):
    ex = set()  # set of all exames
    stud = set()  # set of all students
    ex_stud = dict()  # dictonary : key exam value list of students enrolled

    raw_lines = open(file, 'r', encoding="utf-8").read().splitlines()

    for line in raw_lines:

        s_line = line.split(' ')[0]
        e_line = line.split(' ')[1]

        stud.add(s_line)  # add student to the set
        ex.add(e_line)  # add exam to the set

        if e_line not in ex_stud:

            ex_stud[e_line] = set()
            ex_stud[e_line].add(s_line)

        else:

            ex_stud[e_line].add(s_line)

    ex = sorted(ex)
    stud = sorted(stud)

    n = dict()  # dictionary with key each permutation of two exam and value the number of common students

    for ex1 in ex:

        for ex2 in ex:

            if ex1 != ex2:

                counter = 0

                st_ex1 = ex_stud[ex1]

                st_ex2 = ex_stud[ex2]

                for student in st_ex1:

                    if student in st_ex2:
                        counter += 1

                n[(ex1, ex2)] = counter

    enrollements = 0

    for exa in ex_stud:
        enrollements += len(ex_stud[exa])

    count_conflict = 0

    for pair in n:

        if n[pair] > 0:
            count_conflict += 1

    density = round(count_conflict / len(n), 2)

    return list(ex), list(stud), n, len(ex), len(stud), enrollements, density

def read_instance_slot(file):
    time_slots = int(open(file, 'r', encoding="utf-8").read().splitlines()[0])

    time_slots_list = [x for x in range(1, time_slots + 1)]

    return time_slots, time_slots_list