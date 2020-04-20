def bubble_sort(values):
    if isinstance(values, list) == True:
        values_to_sort = values.copy()
    else:
        values_to_sort = values

    exit_loop = False
    length = len(values_to_sort)
    while exit_loop == False:
        swapped = False
        for loop_counter in range (1, length):
            if values_to_sort[loop_counter - 1] > values_to_sort[loop_counter]:
                temp = values_to_sort[loop_counter]
                values_to_sort[loop_counter] = values_to_sort[loop_counter -1]
                values_to_sort[loop_counter -1] = temp
                swapped = True
        if swapped == False:
            exit_loop = True
    return values_to_sort
