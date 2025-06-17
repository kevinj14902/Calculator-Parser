## Instructions

Place a text file with tokens in the same directory as parser. This text file will be the input. Run the parser and it should create
a new file called output.txt which contains the parse tree for the inputted tokens. Accepted tokens include addition, subtraction, multiplication, division, parenthesis, modulus and integers.

Inputs should follow this format  
`<INT,2>`  
`<ADD>`  
`<INT,5>`

Sample inputs are provided. To run each one, change the file name in the main function for example: input = open('input2.txt', 'r') will give the output for input2.txt. Input files 1, 2, and 3 are semantically correct. 4, 5, and 6 are semantically incorrect.

## Assumptions

I have assumed that the parser input takes single text files at a time and saves the output to an output text file.
I have assumed that error 4 (mismatched numerical types) doesn't apply to multiplication and division