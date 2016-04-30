Go to the location where you have downloaded the code Example - 

cd C:\D_Drive\Coding\Compiler\BaSimPL

Then to run our code, we can use following variations - 

python BaSimPL_Execute.py [inputfile=filename.smpl] [debug=1] [outputfile=filename.bspl]

where all those present in the square brackets are optional.

We have provided 5 sample programs, to execute all of them use following command - 

python BaSimPL_Execute.py

This will execute all the sample program with debug mode off. 

To run sample programs with debug mode use this

Python BaSimPL_Execute.py debug=1

5 sample programs given are 
1. Factorial_Iterative
This program will calcuate the factorial of the given number. It is present in factorial_iterative.smpl. It will first print global variables. Then ask for user input. Then it will print read input and finally factorial of the given number. This uses iterative while loop for calculation.

python BaSimPL_Execute.py inputfile=factorial_iterative.smpl outputfile=factorial_iterative.bspl

2. Factorial_Recursive
This program will calcuate the factorial of the given number. It is present in factorial_recursive.smpl. It will first print global variables. Then ask for user input. Then it will print read input and finally factorial of the given number. This uses recursive function.

python BaSimPL_Execute.py inputfile=factorial_recursive.smpl outputfile=factorial_recursive.bspl

3. Hemachandra_Fibonacci
This program will calculate the fibonacci numbers. It will ask for user input. Based on the input given, that many number of fibonacci numbers will be generated. This is present in the file hemachandra_fibonacci.smpl

python BaSimPL_Execute.py inputfile=hemachandra_fibonacci.smpl outputfile=hemachandra_fibonacci.bspl

4. Sum_Of_N
This program will calculate the sum of n numbers. It will ask for user input which will be n. Based on the input, it will ask n input numbers. Once all inputs are given, it will generate the output sum of those n numbers. In this it uses stack variable. Program is found in the file sum_of_n.smpl

python BaSimPL_Execute.py inputfile=sum_of_n.smpl outputfile=sum_of_n.bspl

5. Avg_Max_Min_Sum
This program given 3 numbers, it will calculate the average of those numbers, maximum, minimum and sum of those numbers. It will ask for 3 numbers from the user. Once 3 numbers are given it will display average, maximum, minimum and sum of those 3 numbers. Program is found in the file multiple_parameters.smpl. To execute the program you can run the following command. It uses multiple function call, if else constructs and logical operations.

python BaSimPL_Execute.py inputfile=multiple_parameters.smpl outputfile=multiple_parameters.bspl

Also if you create your own program then use this syntax, for without debug mode.

python BaSimPL_Execute.py inputfile=your_file_name.smpl outputfile=your_file_name.bspl

for enabling debug mode

python BaSimPL_Execute.py inputfile=your_file_name.smpl outputfile=your_file_name.bspl debug=1




