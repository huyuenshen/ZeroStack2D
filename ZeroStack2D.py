#!/usr/bin/python3
"""
ZeroStack2D Interpreter
A 2D stack-based esolang interpreter, implemented in Python 3.

This interpreter executes ZeroStack2D programs, which are 2D grids of instructions
that manipulate a stack and control the instruction pointer direction.
"""

import sys, argparse
args=argparse.ArgumentParser(description="""
ZeroStack2D Interpreter
A 2D stack-based esolang interpreter, implemented in Python 3.

This interpreter executes ZeroStack2D programs, which are 2D grids of instructions
that manipulate a stack and control the instruction pointer direction.
""")

args.add_argument("input_file")

class Element():
    """
    Represents a single node in the linked-list stack.
    Each node holds a data value and a reference to the next node.
    """
    def __init__(self, data):
        self.data = data  # The value stored in this node
        self.next = None  # Reference to the next node in the stack

class Stack:
    """
    Implements a stack using a singly linked list for O(1) push/pop operations.
    The head of the list is the top of the stack.
    """
    def __init__(self):
        self.head = None  # The top of the stack is initially empty

    def __bool__(self):
        """
        Allows checking if the stack is empty using 'if stack:'.
        Returns True if the stack is not empty, False otherwise.
        """
        return self.head is not None
    
    def push(self, data):
        """
        Pushes a new element onto the top of the stack.
        Creates a new node and makes it the new head.
        """
        new_node = Element(data)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        """
        Removes and returns the top element of the stack.
        If the stack is empty, returns 0 to avoid errors.
        """
        if not self:
            return 0
        data = self.head.data
        self.head = self.head.next  # Move the head to the next node
        return data

    def swap(self):
        """
        Swaps the top two elements of the stack.
        If the stack has less than two elements, it pushes 0s to make the operation safe.
        """
        if not self:
            self.push(0)
        a = self.pop()
        b = self.pop() if self else 0
        self.push(a)
        self.push(b)

    def add(self, b):
        """
        Adds a value 'b' to the top element of the stack.
        Pops the top element, adds 'b' to it, and pushes the result back.
        """
        a = self.pop()
        self.push(b + a)

# --- Main Execution Loop ---

# Read the program file from command line argument
try:
    with open((x:=args.parse_args().input_file),"r") as f:
        # Read the program as a list of lines (the 2D grid)
        pr = f.readlines()
        program=[]
        for i in pr:
            program.append(list(i))
except IndexError:
    # Exit if no filename is provided
    sys.exit(0)
# Initialize the execution state
stack = Stack()  # The main data stack
x = 0            # X-coordinate of the instruction pointer (IP)
y = 0            # Y-coordinate of the instruction pointer (IP)
d = 0            # Direction of the IP: 0->right, 1->up, 2->left, 3->down
# Main execution loop

while True:
    # Get the current instruction from the 2D grid
    try:
        cmd = program[y][x]
    except IndexError:
        cmd=" "
    # --- Direction Control Instructions ---
    if cmd == ">":
        d = 0  # Set direction to right
    elif cmd == "<":
        d = 2  # Set direction to left
    elif cmd == "^":
        d = 1  # Set direction to up
    elif cmd == "v":
        d = 3  # Set direction to down

    # --- Stack Manipulation Instructions ---
    elif cmd in "!0":
        stack.push(0)  # Push a 0 onto the stack
    elif cmd == "+":
        stack.add(1)   # Increment the top stack element by 1
    elif cmd == "-":
        stack.add(-1)  # Decrement the top stack element by 1
    elif cmd == ":":
        # Duplicate the top stack element
        k = stack.pop()
        stack.push(k)
        stack.push(k)
    elif cmd in "\\/":
        stack.swap()    # Swap the top two stack elements

    # --- Input/Output Instructions ---
    elif cmd == "?":
        # Read a character from input and push its ASCII value
        stack.push(ord(input()))
    elif cmd == "~":
        # Read an integer from input and push it
        stack.push(int(input()))
    elif cmd == "$":
        stack.pop()     # Discard the top stack element
    elif cmd == ".":
        # Pop and print the top stack element as a number
        print(stack.pop())
    elif cmd == ",":
        # Pop and print the top stack element as a character
        print(chr(stack.pop()), end='')

    # --- Conditional Branching Instructions ---
    elif cmd == "|":
        """
        Vertical branch:
        - Pop the top element. If non-zero, set direction to up (1).
        - If zero, set direction to down (3).
        - Push the popped element back onto the stack.
        - If stack is empty, default to down (3).
        """
        if stack:
            a = stack.pop()
            if a:
                d = 1
            else:
                d = 3
            stack.push(a)
        else:
            d = 3

    elif cmd == "_":
        """
        Horizontal branch:
        - Pop the second element from the top. If non-zero, set direction to right (0).
        - If zero, set direction to left (2).
        - Push the popped element back onto the stack.
        - If stack is empty, default to left (2).
        """
        if stack:
            a = stack.pop()
            a = stack.pop()
            if a:
                d = 0
            else:
                d = 2
            stack.push(a)
        else:
            d = 2

    # --- Termination Instruction ---
    elif cmd == "@":
        sys.exit(0)  # Exit the main loop and terminate the program

    # --- Move the Instruction Pointer ---
    if d == 0:
        x += 1  # Move right
    elif d == 1:
        y -= 1  # Move up
    elif d == 2:
        x -= 1  # Move left
    elif d == 3:
        y += 1  # Move down