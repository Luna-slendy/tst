# Stack Data Structure Mastery

This repository contains a series of tasks designed to help you master the stack data structure in C++. You are provided with a basic implementation of a stack in `stack.cpp` as your starting point.

## What is a Stack?

A stack is a linear data structure that follows the Last-In-First-Out (LIFO) principle. Think of it like a stack of plates - you can only add or remove plates from the top of the stack.

The basic operations of a stack are:
- **Push**: Add an element to the top of the stack
- **Pop**: Remove the top element from the stack
- **Peek/Top**: View the top element without removing it
- **isEmpty**: Check if the stack is empty
- **Size**: Get the number of elements in the stack

## Tasks

Complete the following tasks to master stacks. Each task builds on the previous ones, gradually increasing in complexity.

### Task 1: Understanding the Basics
1. Study the provided `stack.cpp` file
2. Document each method of the `Stack` class with comments explaining what it does
3. Trace through the execution of the `main()` function by hand, writing down the state of the stack after each operation
4. Modify the `main()` function to demonstrate all the stack operations in a clear, organized way

**Example Test Cases:**
```cpp
// Test isEmpty on empty stack
Stack stack;
if (!stack.isEmpty()) {
    cout << "FAIL: New stack should be empty" << endl;
}

// Test push and peek
stack.push(42);
if (stack.peek() != 42) {
    cout << "FAIL: peek should return 42" << endl;
}

// Test size after push
if (stack.size() != 1) {
    cout << "FAIL: Stack should have size 1 after one push" << endl;
}

// Test pop
int popped = stack.pop();
if (popped != 42) {
    cout << "FAIL: pop should return 42" << endl;
}

// Test LIFO behavior
for (int i = 0; i < 10; i++) {
    stack.push(i);
}
for (int i = 9; i >= 0; i--) {
    int value = stack.pop();
    if (value != i) {
        cout << "FAIL: Expected " << i << " but got " << value << endl;
    }
}
```

### Task 2: Stack Implementation Variations
1. Create a new file `array_stack.cpp` that implements a stack using a fixed-size array instead of a vector
2. Implement proper error handling for stack overflow (when pushing to a full stack) and underflow (when popping from an empty stack)
3. Create a new file `linked_list_stack.cpp` that implements a stack using a linked list
4. Compare the advantages and disadvantages of each implementation in a comment section

**Array Stack Requirements:**
- Implement a class named `ArrayStack` with the following methods:
  - `bool isEmpty()`: Returns true if the stack is empty
  - `int size()`: Returns the number of elements in the stack
  - `void push(int value)`: Adds an element to the top of the stack
  - `int peek()`: Returns the top element without removing it
  - `int pop()`: Removes and returns the top element
- Handle stack overflow: When pushing to a full stack, either throw an exception or print an error message
- Handle stack underflow: When popping from an empty stack, either throw an exception or print an error message

**Linked List Stack Requirements:**
- Implement a class named `LinkedListStack` with the same methods as above
- Create a proper node structure for the linked list
- Ensure proper memory management (no memory leaks)

**Example Test Cases:**
```cpp
// Basic operations test
ArrayStack stack;
stack.push(42);
if (stack.peek() != 42) {
    cout << "FAIL: peek should return 42" << endl;
}

// Test overflow (for array-based stack)
try {
    // Push more elements than the capacity
    for (int i = 0; i < 10000; i++) {
        stack.push(i);
    }
} catch (...) {
    cout << "PASS: Stack overflow detected" << endl;
}

// Test underflow
try {
    // Pop from an empty stack
    ArrayStack emptyStack;
    int value = emptyStack.pop();
} catch (...) {
    cout << "PASS: Stack underflow detected" << endl;
}
```


### Task 3: Stack Applications
Implement the following classic stack applications:

1. **Balanced Parentheses Checker** (`parentheses_checker.cpp`)
   - Write a function that checks if a string has balanced parentheses using a stack
   - Support multiple types of brackets: (), [], {}
   - Function signature: `bool isBalanced(const string& expression)`

   **Example Test Cases:**
   ```cpp
   // Balanced cases
   vector<string> balanced_cases = {
       "()",
       "[]",
       "{}",
       "([]{})",
       "{[()]}",
       "((()))",
       "({[]})",
       "",  // Empty string is balanced
       "a(b)c[d]e{f}g"  // With other characters
   };
   
   // Unbalanced cases
   vector<string> unbalanced_cases = {
       "(",
       ")",
       "(]",
       "([)]",
       "(()",
       "([{",
       "}])"
   };
   ```

2. **Infix to Postfix Converter** (`infix_to_postfix.cpp`)
   - Convert infix expressions (e.g., "A+B*C") to postfix notation (e.g., "ABC*+") using a stack
   - Support operators +, -, *, /, ^ with proper precedence
   - Function signature: `string infixToPostfix(const string& infix)`

   **Example Test Cases:**
   ```cpp
   // Basic conversions
   "A+B" -> "AB+"
   "A-B" -> "AB-"
   "A*B" -> "AB*"
   "A/B" -> "AB/"
   "A^B" -> "AB^"
   "A+B*C" -> "ABC*+"  // Operator precedence
   "A*(B+C)" -> "ABC+*"  // Parentheses
   "(A+B)*C" -> "AB+C*"  // Parentheses
   
   // Complex expressions
   "(A+B)*(C-D)" -> "AB+CD-*"
   "A^B^C" -> "ABC^^"  // Right-associative
   "((A+B)*C-(D/E))+F" -> "AB+C*DE/-F+"
   ```

3. **Postfix Expression Evaluator** (`postfix_evaluator.cpp`)
   - Evaluate postfix expressions using a stack
   - Support integer operands and operators +, -, *, /
   - Function signature: `int evaluatePostfix(const string& postfix)`

   **Example Test Cases:**
   ```cpp
   "5" -> 5  // Single operand
   "5 3 +" -> 8  // Addition
   "5 3 -" -> 2  // Subtraction
   "5 3 *" -> 15  // Multiplication
   "6 3 /" -> 2  // Division
   "5 3 + 2 *" -> 16  // Addition then multiplication
   "5 1 2 + 4 * + 3 -" -> 14  // Complex expression: 5+((1+2)*4)-3
   ```

### Task 4: Advanced Stack Problems
Solve these more challenging stack problems:

1. **Next Greater Element** (`next_greater_element.cpp`)
   - Given an array, find the next greater element for each element
   - Use a stack for an efficient O(n) solution
   - Function signature: `vector<int> nextGreaterElements(const vector<int>& arr)`
   - For each element, find the first greater element that appears to its right
   - If no greater element exists, use -1

   **Example Test Cases:**
   ```cpp
   // Input -> Expected Output
   {4, 5, 2, 25} -> {5, 25, 25, -1}
   {13, 7, 6, 12} -> {-1, 12, 12, -1}
   {1, 2, 3, 4} -> {2, 3, 4, -1}
   {4, 3, 2, 1} -> {-1, -1, -1, -1}
   ```

2. **Min Stack** (`min_stack.cpp`)
   - Design a stack that supports push, pop, top, and retrieving the minimum element in constant time
   - Class requirements:
     - `void push(int val)`: Pushes element val onto the stack
     - `void pop()`: Removes the element on top of the stack
     - `int top()`: Gets the top element of the stack
     - `int getMin()`: Retrieves the minimum element in the stack
   - All operations must be O(1) time complexity

   **Example Test Cases:**
   ```cpp
   MinStack minStack;
   minStack.push(-2);
   minStack.push(0);
   minStack.push(-3);
   minStack.getMin(); // return -3
   minStack.pop();
   minStack.top();    // return 0
   minStack.getMin(); // return -2
   ```

3. **Stack Sort** (`stack_sort.cpp`)
   - Sort a stack using only stack operations (push, pop, peek) and temporary variables
   - You may use one additional stack for temporary storage
   - Function signature: `void sortStack(Stack& s)`
   - The stack should be sorted in ascending order (smallest element on top)

   **Example Test Cases:**
   ```cpp
   // Input stack (top to bottom): 34, 3, 31, 98, 92, 23
   // Expected output (top to bottom): 3, 23, 31, 34, 92, 98
   
   // Input stack (top to bottom): 3, 5, 1, 4, 2
   // Expected output (top to bottom): 1, 2, 3, 4, 5
   ```

### Task 5: Stack in Real-World Applications
Choose one of the following projects:

1. **Simple Calculator** (`calculator.cpp`)
   - Implement a command-line calculator that evaluates expressions
   - Support parentheses and basic arithmetic operations
   - Handle input expressions like "3 + 4 * (2 - 1)"
   - Support operators: +, -, *, /, and parentheses
   - Properly handle operator precedence

   **Example Test Cases:**
   ```
   Input: "3+4"
   Output: 7
   
   Input: "3+4*2"
   Output: 11
   
   Input: "(3+4)*2"
   Output: 14
   
   Input: "3+4*(2-1)/2"
   Output: 5
   ```

2. **Undo/Redo Functionality** (`text_editor.cpp`)
   - Implement a simple text editor with undo/redo functionality using two stacks
   - Support the following operations:
     - `void write(string text)`: Add text
     - `void delete_last(int n)`: Delete the last n characters
     - `void undo()`: Undo the last operation
     - `void redo()`: Redo the last undone operation
     - `string get_text()`: Get the current text

   **Example Test Cases:**
   ```cpp
   TextEditor editor;
   editor.write("Hello");  // Text: "Hello"
   editor.write(" World");  // Text: "Hello World"
   editor.delete_last(6);  // Text: "Hello"
   editor.undo();  // Text: "Hello World" (undo the delete)
   editor.undo();  // Text: "Hello" (undo the write)
   editor.redo();  // Text: "Hello World" (redo the write)
   ```

3. **Maze Solver** (`maze_solver.cpp`)
   - Solve a maze using a stack-based depth-first search algorithm
   - Visualize the solution path
   - The maze should be represented as a 2D grid where:
     - '0' represents an open cell
     - '1' represents a wall
     - 'S' represents the start position
     - 'E' represents the end position
   - Function signature: `vector<pair<int, int>> solveMaze(vector<vector<char>>& maze)`
   - Return the path from start to end as a sequence of (row, column) coordinates

   **Example Test Cases:**
   ```cpp
   // Example maze:
   // S 0 1 1
   // 1 0 0 1
   // 1 1 0 1
   // 1 1 0 E
   
   vector<vector<char>> maze = {
       {'S', '0', '1', '1'},
       {'1', '0', '0', '1'},
       {'1', '1', '0', '1'},
       {'1', '1', '0', 'E'}
   };
   
   // Expected path coordinates (row, col):
   // (0,0) -> (0,1) -> (1,1) -> (1,2) -> (2,2) -> (3,2) -> (3,3)
   ```

## Folder Structure

Your repository should be organized as follows:

```
Stacks-master/
├── README.md                   # This file with tasks and instructions
├── stack.cpp                   # Original stack implementation (provided)
├── implementations/            # Different stack implementations
│   ├── array_stack.cpp        # Array-based stack implementation
│   └── linked_list_stack.cpp  # Linked list-based stack implementation
├── applications/              # Stack applications
│   ├── parentheses_checker.cpp  # Balanced parentheses checker
│   ├── infix_to_postfix.cpp     # Infix to postfix converter
│   └── postfix_evaluator.cpp    # Postfix expression evaluator
├── advanced/                  # Advanced stack problems
│   ├── next_greater_element.cpp # Next greater element finder
│   ├── min_stack.cpp            # Min stack implementation
│   └── stack_sort.cpp           # Stack sorting algorithm
└── projects/                  # Real-world applications
    ├── calculator.cpp           # Simple calculator
    ├── text_editor.cpp          # Text editor with undo/redo
    └── maze_solver.cpp          # Maze solver using stack
```

## Testing Your Code

We've provided pytest files to help you test your implementations. These tests will verify that your code works correctly for the specified requirements and edge cases.

**How to run the tests:**
```bash
# Install pytest if you don't have it already
pip install pytest

# Run all tests
python -m pytest tests/

# Run tests for a specific task
python -m pytest tests/test_basic_stack.py
```

**Note:** The tests will compile and run your C++ code, so make sure your code compiles without errors before running the tests.

## Submission Guidelines

For each task:
1. Create a separate .cpp file as specified in the folder structure above
2. Include detailed comments explaining your code
3. Add test cases to demonstrate the functionality
4. Ensure your code compiles without warnings and runs correctly
5. Make sure your code passes all the provided tests

## Evaluation Criteria

Your solutions will be evaluated based on:
1. Correctness: Does your code work as expected?
2. Code quality: Is your code well-organized, readable, and properly commented?
3. Efficiency: Does your solution use appropriate algorithms and data structures?
4. Completeness: Have you implemented all required features?

## Resources

Here are some helpful resources for learning more about stacks:
- [GeeksforGeeks - Stack Data Structure](https://www.geeksforgeeks.org/stack-data-structure/)
- [CPlusPlus.com - std::stack](http://www.cplusplus.com/reference/stack/stack/)
- [Stack Overflow - Common Stack Questions](https://stackoverflow.com/questions/tagged/stack+c%2B%2B)

Good luck, and happy coding!
