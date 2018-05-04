"""
This program is an implementation of Page Rank Algorithm using Random Surfer Model.
beta = 0.85
Original Matrix is :
0 1 0 0 0 0
0 0 1 1 1 0
0 1 0 1 1 0
0 1 1 0 1 0
0 1 1 1 0 1
0 0 0 0 0 0
"""
import sys
import numpy as np

# Function that reads the input file and creates the original matrix
def file_open(file_path,matrix,n):
	with open(file_path,"r") as f:
		for l in f:
			line = l.split(" ")
			line[-1]=line[-1].strip("\n")
			line = list(map(int,line))
			matrix.append(line)
			n=n+1
	matrix = np.array(matrix)
	return matrix,n

#Function that calculate the weights for each edge based on the outlink link	
def weights_cal(matrix):
	for row in matrix:
		count=0
		for col in row:
			if col==1:
				count=count+1
		
		if count == 0:
			t1 =0
		else:
			t1 = round(1/count,4)
			#t1 = 1/count
		weights.append(t1)
	return weights

#Function that creates transpose of matrix and multiplies it with the wiehgts	
def matrix_transpose(matrix,weights):
	matrix = matrix.transpose() 
	M = matrix * weights
	return np.round(M,4)
	#return M
def v_cal(v,N):
	for i in range(N):
		v.append(1/N)
	return np.round(v,4)
	#return v

#Function that determines the convergence of rank
def compare_array(M,v,iteration_no,v_new):
	if np.array_equal(v,v_new):
		return v_new, iteration_no
	else:
		v = np.round(v_new,4)
		#v = v_new
		temp = np.matmul(M,v_new) + second_term 
		v_new =np.round(temp,4)
		#v_new =temp
		iteration_no =iteration_no +1
		return compare_array(M,v,iteration_no,v_new)
#Main function which gives call to all the above functions and takes command line input		
if __name__ == "__main__":
	matrix =[]
	weights=[]
	v=[]
	v_new=[]
	matrix
	iteration_no = 0
	n=0
	file_path = sys.argv[1]
	matrix1,N= file_open(file_path,matrix,n)
	print("Originial Matrix: ")
	print(matrix1)
	weights1=weights_cal(matrix1)
	print("Weights based on number of outlink: ", weights1)
	M = matrix_transpose(matrix1,weights1)
	print("M: ")
	print(M)
	M = M * 0.85
	v1=v_cal(v,N)
	print("Initial Rank Matrix Ri: ", v1)
	second_term = [((1-0.85)/4)]*N
	second_term = np.round(second_term,4)
	v_new = np.matmul(M,v1) + second_term
	v_new = np.round(v_new,4)
	final_v, iter_no = compare_array(M,v1,iteration_no,v_new)
	print("Final Convergence Matrix: ", final_v)
	print("Total iterations : ",iter_no)