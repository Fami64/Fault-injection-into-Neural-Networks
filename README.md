# Fault-injection-into-Neural-Networks

Code for fault injection into neural networks with reconfigurable fault rates.

To inject faults into a certain network follow these steps:
1. Extract weight matrix for each layer e.g. 

2. Run following command to inject x% faults into an N bit each layer:

%python NN_fault_Injection.py <layer1_weight_matrix_filename> .... <layern_weight_matrix_filename>  <quantization fault-rate

3. The program creates two sets of files for each layer with "defectmap" and "faulty" prefixes that respectively include the generated defect map for each layer and the faulty weights.

# Example:

The directory contains two files "testlayer1.txt" and "testlayer2.txt" each of which includes a weight matrix for one of the two layers of the target 12-bit quantized NN. The following command injects 0.01 faults into these layers:

%python NN_fault_Injection.py testlayer1.txt testlayer2.txt 12 0.01

The program generates two defectmaps "defectmap_0.01_layer1.txt" and "defectmap_0.01_layer2.txt" as well as two faulty weight faults "faulty_layer1.txt" and "faulty_0.01_layer2.txt". All the generated files are also included in the repository.


