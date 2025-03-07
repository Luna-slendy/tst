"""
Tests for the basic stack implementation (Task 1).
"""
import subprocess
import os
import sys
import pytest

# Helper function to compile and run a C++ file
def run_cpp_file(file_path):
    # Get the directory containing the file
    file_dir = os.path.dirname(file_path)
    # Get the file name without extension
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    # Compile the file
    compile_result = subprocess.run(
        ["g++", "-o", os.path.join(file_dir, file_name), file_path],
        capture_output=True,
        text=True
    )
    if compile_result.returncode != 0:
        return f"Compilation error: {compile_result.stderr}"
    
    # Run the compiled file
    run_result = subprocess.run(
        [os.path.join(file_dir, file_name)],
        capture_output=True,
        text=True
    )
    
    # Clean up the compiled file
    try:
        os.remove(os.path.join(file_dir, file_name))
    except:
        pass
    
    if run_result.returncode != 0:
        return f"Runtime error: {run_result.stderr}"
    
    return run_result.stdout

# Path to the stack.cpp file
STACK_CPP_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "stack.cpp")

def test_stack_basic_operations():
    """Test that the basic stack operations work correctly."""
    # Create a temporary file with a modified main function to test basic operations
    temp_file = os.path.join(os.path.dirname(__file__), "temp_stack_basic.cpp")
    
    with open(STACK_CPP_PATH, 'r') as f:
        stack_code = f.read()
    
    # Replace the main function with our test main
    main_start = stack_code.find("int main()")
    main_end = stack_code.rfind("}")
    
    test_main = """
int main()
{
    Stack stack;
    
    // Test isEmpty on empty stack
    if (!stack.isEmpty()) {
        cout << "FAIL: New stack should be empty" << endl;
        return 1;
    }
    
    // Test size on empty stack
    if (stack.size() != 0) {
        cout << "FAIL: New stack should have size 0" << endl;
        return 1;
    }
    
    // Test push and peek
    stack.push(42);
    if (stack.peek() != 42) {
        cout << "FAIL: peek should return 42" << endl;
        return 1;
    }
    
    // Test isEmpty after push
    if (stack.isEmpty()) {
        cout << "FAIL: Stack should not be empty after push" << endl;
        return 1;
    }
    
    // Test size after push
    if (stack.size() != 1) {
        cout << "FAIL: Stack should have size 1 after one push" << endl;
        return 1;
    }
    
    // Test pop
    int popped = stack.pop();
    if (popped != 42) {
        cout << "FAIL: pop should return 42" << endl;
        return 1;
    }
    
    // Test isEmpty after pop
    if (!stack.isEmpty()) {
        cout << "FAIL: Stack should be empty after popping all elements" << endl;
        return 1;
    }
    
    // Test multiple pushes
    for (int i = 0; i < 10; i++) {
        stack.push(i);
    }
    
    // Test size after multiple pushes
    if (stack.size() != 10) {
        cout << "FAIL: Stack should have size 10 after 10 pushes" << endl;
        return 1;
    }
    
    // Test LIFO behavior
    for (int i = 9; i >= 0; i--) {
        int value = stack.pop();
        if (value != i) {
            cout << "FAIL: Expected " << i << " but got " << value << endl;
            return 1;
        }
    }
    
    cout << "PASS: All basic stack operations work correctly" << endl;
    return 0;
}
"""
    
    modified_code = stack_code[:main_start] + test_main
    
    with open(temp_file, 'w') as f:
        f.write(modified_code)
    
    # Run the test
    output = run_cpp_file(temp_file)
    
    # Clean up
    try:
        os.remove(temp_file)
    except:
        pass
    
    # Check the output
    assert "PASS: All basic stack operations work correctly" in output, f"Test failed with output: {output}"

def test_stack_edge_cases():
    """Test edge cases for the stack implementation."""
    # Create a temporary file with a modified main function to test edge cases
    temp_file = os.path.join(os.path.dirname(__file__), "temp_stack_edge.cpp")
    
    with open(STACK_CPP_PATH, 'r') as f:
        stack_code = f.read()
    
    # Replace the main function with our test main
    main_start = stack_code.find("int main()")
    main_end = stack_code.rfind("}")
    
    test_main = """
int main()
{
    Stack stack;
    
    // Test peek on empty stack (should crash or return garbage, but we're just checking if it compiles)
    try {
        int value = stack.peek();
        cout << "Peek on empty stack returned: " << value << endl;
    } catch (...) {
        cout << "Peek on empty stack threw an exception" << endl;
    }
    
    // Test pop on empty stack (should crash or return garbage, but we're just checking if it compiles)
    try {
        int value = stack.pop();
        cout << "Pop on empty stack returned: " << value << endl;
    } catch (...) {
        cout << "Pop on empty stack threw an exception" << endl;
    }
    
    // Test large number of elements
    const int NUM_ELEMENTS = 10000;
    for (int i = 0; i < NUM_ELEMENTS; i++) {
        stack.push(i);
    }
    
    if (stack.size() != NUM_ELEMENTS) {
        cout << "FAIL: Stack should have size " << NUM_ELEMENTS << " after " << NUM_ELEMENTS << " pushes" << endl;
        return 1;
    }
    
    // Test popping all elements
    for (int i = 0; i < NUM_ELEMENTS; i++) {
        stack.pop();
    }
    
    if (!stack.isEmpty()) {
        cout << "FAIL: Stack should be empty after popping all elements" << endl;
        return 1;
    }
    
    cout << "PASS: Stack edge cases handled correctly" << endl;
    return 0;
}
"""
    
    modified_code = stack_code[:main_start] + test_main
    
    with open(temp_file, 'w') as f:
        f.write(modified_code)
    
    # Run the test
    output = run_cpp_file(temp_file)
    
    # Clean up
    try:
        os.remove(temp_file)
    except:
        pass
    
    # Check the output
    assert "PASS: Stack edge cases handled correctly" in output, f"Test failed with output: {output}"
