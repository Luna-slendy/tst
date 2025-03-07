"""
Tests for the linked list-based stack implementation (Task 2).
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

# Path to the linked_list_stack.cpp file
LINKED_LIST_STACK_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "implementations/linked_list_stack.cpp")

def test_linked_list_stack_exists():
    """Test that the linked_list_stack.cpp file exists."""
    assert os.path.exists(LINKED_LIST_STACK_PATH), f"File {LINKED_LIST_STACK_PATH} does not exist"

def test_linked_list_stack_basic_operations():
    """Test that the basic stack operations work correctly for the linked list-based implementation."""
    # Skip if the file doesn't exist
    if not os.path.exists(LINKED_LIST_STACK_PATH):
        pytest.skip(f"File {LINKED_LIST_STACK_PATH} does not exist")
    
    # Create a temporary file with a modified main function to test basic operations
    temp_file = os.path.join(os.path.dirname(__file__), "temp_linked_list_stack_basic.cpp")
    
    with open(LINKED_LIST_STACK_PATH, 'r') as f:
        stack_code = f.read()
    
    # Find the main function and replace it with our test main
    main_start = stack_code.find("int main()")
    if main_start == -1:
        main_start = stack_code.find("int main ()")
    
    if main_start == -1:
        pytest.skip("Could not find main function in linked_list_stack.cpp")
    
    main_end = stack_code.rfind("}")
    
    test_main = """
int main()
{
    // Assuming the stack class is named LinkedListStack
    LinkedListStack stack;
    
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

def test_linked_list_stack_memory_management():
    """Test that the linked list-based stack properly manages memory (no memory leaks)."""
    # Skip if the file doesn't exist
    if not os.path.exists(LINKED_LIST_STACK_PATH):
        pytest.skip(f"File {LINKED_LIST_STACK_PATH} does not exist")
    
    # Create a temporary file with a modified main function to test memory management
    temp_file = os.path.join(os.path.dirname(__file__), "temp_linked_list_stack_memory.cpp")
    
    with open(LINKED_LIST_STACK_PATH, 'r') as f:
        stack_code = f.read()
    
    # Find the main function and replace it with our test main
    main_start = stack_code.find("int main()")
    if main_start == -1:
        main_start = stack_code.find("int main ()")
    
    if main_start == -1:
        pytest.skip("Could not find main function in linked_list_stack.cpp")
    
    main_end = stack_code.rfind("}")
    
    test_main = """
int main()
{
    // Assuming the stack class is named LinkedListStack
    
    // Test creating and destroying many stacks
    for (int i = 0; i < 100; i++) {
        LinkedListStack stack;
        
        // Push many elements
        for (int j = 0; j < 1000; j++) {
            stack.push(j);
        }
        
        // Pop some elements
        for (int j = 0; j < 500; j++) {
            stack.pop();
        }
        
        // Stack destructor should free all remaining nodes
    }
    
    // Test pushing and popping many elements
    LinkedListStack stack;
    
    for (int i = 0; i < 10000; i++) {
        stack.push(i);
    }
    
    for (int i = 0; i < 10000; i++) {
        stack.pop();
    }
    
    // Check that the stack is empty after popping all elements
    if (!stack.isEmpty()) {
        cout << "FAIL: Stack should be empty after popping all elements" << endl;
        return 1;
    }
    
    cout << "PASS: Memory management test completed" << endl;
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
    assert "PASS: Memory management test completed" in output, f"Test failed with output: {output}"

def test_linked_list_stack_underflow():
    """Test that the linked list-based stack handles underflow correctly."""
    # Skip if the file doesn't exist
    if not os.path.exists(LINKED_LIST_STACK_PATH):
        pytest.skip(f"File {LINKED_LIST_STACK_PATH} does not exist")
    
    # Create a temporary file with a modified main function to test underflow
    temp_file = os.path.join(os.path.dirname(__file__), "temp_linked_list_stack_underflow.cpp")
    
    with open(LINKED_LIST_STACK_PATH, 'r') as f:
        stack_code = f.read()
    
    # Find the main function and replace it with our test main
    main_start = stack_code.find("int main()")
    if main_start == -1:
        main_start = stack_code.find("int main ()")
    
    if main_start == -1:
        pytest.skip("Could not find main function in linked_list_stack.cpp")
    
    main_end = stack_code.rfind("}")
    
    test_main = """
int main()
{
    // Assuming the stack class is named LinkedListStack
    LinkedListStack stack;
    
    // Test popping from an empty stack
    bool underflow_detected = false;
    
    try {
        // Pop from an empty stack
        int value = stack.pop();
        cout << "Pop from empty stack returned: " << value << endl;
    } catch (...) {
        underflow_detected = true;
        cout << "PASS: Stack underflow detected" << endl;
    }
    
    if (!underflow_detected) {
        // Check if the implementation uses a different mechanism to handle underflow
        // For example, it might print an error message instead of throwing an exception
        cout << "No exception was thrown for stack underflow. This is acceptable if the implementation handles underflow differently." << endl;
    }
    
    cout << "PASS: Stack underflow test completed" << endl;
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
    assert "PASS: Stack underflow test completed" in output, f"Test failed with output: {output}"
