import sys
import random
import copy
import math
import numpy as np

def setKthBit(n, k):
    return ((1 << k) | n)

def resetKthBit(n, k):
    return (~(1 << k) & n)

def getKthBit(n, k):
    if n & (1 << k):
        return 1
    else:
        return 0

def generate_faulty_weights(matrix_height, matrix_width, total_cells, fault_rate, weight_matrix, layer_file,quantization_bits):
    faulty_weight_matrix = copy.deepcopy(weight_matrix)
    defect_map = [[0] * (matrix_width * quantization_bits) for x in range(matrix_height)]
    stuckat_one_cells = []
    stuckat_zero_cells = []
    all_bits = quantization_bits * total_cells
    stuckat_cells = random.sample(range(0, all_bits - 1), int(fault_rate * all_bits))
    random.shuffle(stuckat_cells)
    stuckat_one_cells.extend(stuckat_cells[0: int(math.floor(0.8 * fault_rate * all_bits))])
    stuckat_zero_cells.extend(stuckat_cells[int(math.floor(0.8 * fault_rate * all_bits)):])


    # intitialize defect_map with 2
    # Later put 1 for stuck-at-1 and 0 for stuck-at-0 and 2 for clean cells
    for i in range(0, matrix_height):
        for j in range(0, quantization_bits * matrix_width):
            defect_map[i][j] = 2

    for x in stuckat_one_cells:
        rowAddress = x / (matrix_width * quantization_bits)
        columnAddress = x % (matrix_width * quantization_bits)
        defect_map[int(rowAddress)][columnAddress] = 1

    for x in stuckat_zero_cells:
        rowAddress = x / (matrix_width * quantization_bits)
        columnAddress = x % (matrix_width * quantization_bits)
        defect_map[int(rowAddress)][columnAddress] = 0

    for i in range(0, matrix_height):
        for j in range(0, matrix_width):
            for k in range(0, quantization_bits):
                this_weight = faulty_weight_matrix[i][j]
                if defect_map[i][j * quantization_bits + k] == 1:
                    if (getKthBit(this_weight, quantization_bits - k - 1) == 0):
                        this_weight = setKthBit(this_weight, quantization_bits - k - 1)

                elif defect_map[i][j * quantization_bits + k] == 0:
                    if (getKthBit(this_weight, quantization_bits - k - 1) == 1):
                        this_weight = resetKthBit(this_weight, quantization_bits - k - 1)

            faulty_weight_matrix[i][j] = this_weight

    return defect_map, faulty_weight_matrix

################## main function ################
total_arg = len(sys.argv)
fault_rate = float(sys.argv[total_arg-1])
quantization_bits = int(sys.argv[total_arg-2])


for i in range(1 , total_arg-2):
    layer_file =  sys.argv[i]
    weight_matrix = []

    with open(layer_file) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        for line in content:
            all_elem = line.split(',')
            all_elem_int = []
            for x in all_elem:
                if x != '':
                    all_elem_int.append(int(x))
            weight_matrix.append(all_elem_int)

    matrix_height = len(weight_matrix)
    matrix_width = len(weight_matrix[0])
    total_cells = matrix_height * matrix_width

    defect_map, faulty_weight_matrix = generate_faulty_weights(matrix_height, matrix_width, total_cells, fault_rate, weight_matrix, layer_file,quantization_bits)
    # Print the defect map
    filename = "defectmap" + "_" + str(fault_rate) + "_" + layer_file
    with open(filename, 'w') as outf:
        for i in range(0, matrix_height):
            for j in range(0, quantization_bits * matrix_width):
                outf.write(str(defect_map[i][j]) + ",")
            outf.write('\n')

    # Print the faulty weights
    filename = "faulty" + "_" + str(fault_rate) + "_" +  layer_file
    with open(filename, 'w') as outf:
        for i in range(0, matrix_height):
            for j in range(0, matrix_width):
                outf.write(str(faulty_weight_matrix[i][j]) + ",")
            outf.write('\n')

