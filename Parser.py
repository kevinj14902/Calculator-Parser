class TokenType:
    INT = 'INT'  # Integers
    ADD = 'ADD'  # Addition
    SUB = 'SUB'  # Subtraction
    MULT = 'MULT'  # Multiplication
    DIV = 'DIV'  # Division
    LEFTP = 'LEFTP'  # Left Parenthesis
    RIGHTP = 'RIGHTP'  # Right Parenthesis
    MOD = 'MOD'  # Modulus

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return f"<{self.type}, {self.value}>"
        return f"<{self.type}>"

class Node:
    def __init__(self, label=None, value=None, value_type=None):
        self.label = label
        self.value = value
        self.value_type = value_type
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    # Prints abstract syntax tree to the output file
    def print_tree_tofile(self, depth=0):
        indent = "  " * depth
        result = ''
        if self.label == "NUMBER":
            result += f"{self.value}\n"
        else:
            result += f"{indent}{self.label}\n"
        for child in self.children:
            result += child.print_tree_tofile(depth + 1)
        return result

class Parser:
    def __init__(self, input):
        self.input = input
        self.array = [line.strip() for line in self.input]
        self.array2 = []
        self.position = 0
        self.consecutive_op = False

        # Tokenize input
        for string in self.array:
            token = self.string_to_token(string)
            if token[1] == '':
                self.array2.append(Token(token[0]))
            else:
                if token[0] == TokenType.INT:
                    if self.is_invalid_number(token[1]):
                        with open('output.txt', 'a') as out:
                            # Error type 3 for invalid numbers such as 012345
                            out.write(f"Error type 3: Invalid number at '{token[1]}' \n")
                        continue
                self.array2.append(Token(token[0], token[1]))
        self.current_token = None

    # Checks if a number starts with 0 and has no decimal point
    def is_invalid_number(self, value):
        if value.isdigit() and value.startswith('0') and len(value) > 1:
            return True
        try:
            float(value)
            return False
        except ValueError:
            return True

    def string_to_token(self, string):
        index = 1
        result = ''
        result2 = ''
        while string[index] != ',' and string[index] != '>':
            result += string[index]
            index += 1
        if index < len(string) - 2:
            index += 1
            while string[index] != '>':
                result2 += string[index]
                index += 1
        return [result, result2]

    def get_next_token(self):
        if self.position < len(self.array2):
            self.current_token = self.array2[self.position]
            self.position += 1
            # Check for consecutive operators
            if self.current_token.type in [TokenType.ADD, TokenType.SUB, TokenType.MULT, TokenType.DIV, TokenType.MOD]:
                if self.consecutive_op:
                    raise Exception(f"Error type 1: Consecutive operators detected: {self.current_token.type}")
                self.consecutive_op = True
            else:
                self.consecutive_op = False

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.get_next_token()
        else:
            raise Exception(f"Expected token {token_type}, got {self.current_token}")

    def parse(self):
        self.get_next_token()
        return self.expr()

    # Checks if numbers are int or float for compatibility
    def validate_type_compatibility(self, left_node, right_node):
        if left_node.value_type == "int" and right_node.value_type == "float":
            raise Exception(f"Error type 4: Cannot add/subtract integer {left_node.value} with floating point {right_node.value}")
        if left_node.value_type == "float" and right_node.value_type == "int":
            raise Exception(f"Error type 4: Cannot add/subtract floating point {left_node.value} with integer {right_node.value}")

    # Parse expressions (+, -)
    def expr(self):
        node = self.term()
        while self.current_token.type in (TokenType.ADD, TokenType.SUB):
            if self.current_token.type == TokenType.ADD:
                op_symbol = '+' 
            else:
                op_symbol = '-'
            op_node = Node(label=op_symbol)
            op_node.add_child(node)
            self.eat(self.current_token.type)
            right_node = self.term()
            # Check for compatibility
            self.validate_type_compatibility(node, right_node)
            op_node.add_child(right_node)
            node = op_node
        return node

    # Parse terms (*, /, %)
    def term(self):
        node = self.factor()
        while self.current_token.type in (TokenType.MULT, TokenType.DIV, TokenType.MOD):
            if self.current_token.type == TokenType.MULT:
                op_symbol = '*' 
            if self.current_token.type == TokenType.DIV:
                op_symbol = '/' 
            if self.current_token.type == TokenType.MOD:
                op_symbol = '%'
            op_node = Node(label=op_symbol)
            op_node.add_child(node)
            self.eat(self.current_token.type)
            op_node.add_child(self.factor())
            node = op_node
        return node

    # Parse factors (numbers or parentheses)
    def factor(self):
        if self.current_token.type == TokenType.INT:
            value = self.current_token.value
            # Checks for int or float
            if '.' in value:
                value_type = "float"
            else:
                value_type = "int"
            leaf_node = Node(label="NUMBER", value=value, value_type=value_type)
            self.eat(self.current_token.type)
            return leaf_node
        elif self.current_token.type == TokenType.LEFTP:
            self.eat(TokenType.LEFTP)
            node = self.expr()
            self.eat(TokenType.RIGHTP)
            return node
        else:
            raise Exception(f"Unexpected token {self.current_token.type} in factor")

# Main method
if __name__ == "__main__":
    input = open('input.txt', 'r')
    parser = Parser(input)
    try:
        tree = parser.parse()
        with open('output.txt', 'a') as out:
            out.write(tree.print_tree_tofile())
    except Exception as e:
        with open('output.txt', 'a') as out:
            out.write(f"{str(e)}\n")
