"""
Tests for the infix to postfix converter application (Task 3).
"""
import subprocess
import os
import sys
import pytest

# Helper function to compile and run a C++ file
def run_cpp_file(file_path, input_data=None):
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
    if input_data:
        run_result = subprocess.run(
            [os.path.join(file_dir, file_name)],
            input=input_data,
            capture_output=True,
            text=True
        )
    else:
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

# Path to the infix_to_postfix.cpp file
INFIX_TO_POSTFIX_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "applications/infix_to_postfix.cpp")

def test_infix_to_postfix_exists():
    """Test that the infix_to_postfix.cpp file exists."""
    assert os.path.exists(INFIX_TO_POSTFIX_PATH), f"File {INFIX_TO_POSTFIX_PATH} does not exist"

def test_infix_to_postfix_basic():
    """Test that the infix to postfix converter correctly converts basic expressions."""
    # Skip if the file doesn't exist
    if not os.path.exists(INFIX_TO_POSTFIX_PATH):
        pytest.skip(f"File {INFIX_TO_POSTFIX_PATH} does not exist")
    
    # Create a temporary file with test cases
    temp_file = os.path.join(os.path.dirname(__file__), "temp_infix_to_postfix.cpp")
    
    with open(INFIX_TO_POSTFIX_PATH, 'r') as f:
        converter_code = f.read()
    
    # Find the main function and replace it with our test main
    main_start = converter_code.find("int main()")
    if main_start == -1:
        main_start = converter_code.find("int main ()")
    
    if main_start == -1:
        pytest.skip("Could not find main function in infix_to_postfix.cpp")
    
    main_end = converter_code.rfind("}")
    
    test_main = """
int main()
{
    // Test basic infix to postfix conversions
    struct TestCase {
        string infix;
        string expected_postfix;
    };
    
    vector<TestCase> test_cases = {
        {"A+B", "AB+"},
        {"A-B", "AB-"},
        {"A*B", "AB*"},
        {"A/B", "AB/"},
        {"A^B", "AB^"},
        {"A+B*C", "ABC*+"},
        {"A*B+C", "AB*C+"},
        {"A*(B+C)", "ABC+*"},
        {"(A+B)*C", "AB+C*"},
        {"A+B+C", "AB+C+"},
        {"A*B*C", "AB*C*"}
    };
    
    for (const TestCase& test_case : test_cases) {
        string result = infixToPostfix(test_case.infix);
        if (result != test_case.expected_postfix) {
            cout << "FAIL: For infix '" << test_case.infix << "', expected postfix '" 
                 << test_case.expected_postfix << "', but got '" << result << "'" << endl;
            return 1;
        }
    }
    
    cout << "PASS: All basic test cases passed" << endl;
    return 0;
}
"""
    
    # Assuming there's a function called infixToPostfix
    # If the function has a different name, the test will fail
    
    modified_code = converter_code[:main_start] + test_main
    
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
    assert "PASS: All basic test cases passed" in output, f"Test failed with output: {output}"

def test_infix_to_postfix_complex():
    """Test that the infix to postfix converter correctly converts complex expressions."""
    # Skip if the file doesn't exist
    if not os.path.exists(INFIX_TO_POSTFIX_PATH):
        pytest.skip(f"File {INFIX_TO_POSTFIX_PATH} does not exist")
    
    # Create a temporary file with test cases
    temp_file = os.path.join(os.path.dirname(__file__), "temp_infix_to_postfix_complex.cpp")
    
    with open(INFIX_TO_POSTFIX_PATH, 'r') as f:
        converter_code = f.read()
    
    # Find the main function and replace it with our test main
    main_start = converter_code.find("int main()")
    if main_start == -1:
        main_start = converter_code.find("int main ()")
    
    if main_start == -1:
        pytest.skip("Could not find main function in infix_to_postfix.cpp")
    
    main_end = converter_code.rfind("}")
    
    test_main = """
int main()
{
    // Test complex infix to postfix conversions
    struct TestCase {
        string infix;
        string expected_postfix;
    };
    
    vector<TestCase> test_cases = {
        {"(A+B)*(C-D)", "AB+CD-*"},
        {"A+B*C+D", "ABC*+D+"},
        {"(A+B)*(C+D)", "AB+CD+*"},
        {"A*B+C*D", "AB*CD*+"},
        {"A+B+C+D", "AB+C+D+"},
        {"A*B*C*D", "AB*C*D*"},
        {"A^B^C", "ABC^^"},  // Right-associative
        {"(A+B)*C-(D/E)", "AB+C*DE/-"},
        {"A*(B+C*D)+E", "ABCD*+*E+"},
        {"((A+B)*C-(D/E))+F", "AB+C*DE/-F+"}
    };
    
    for (const TestCase& test_case : test_cases) {
        string result = infixToPostfix(test_case.infix);
        if (result != test_case.expected_postfix) {
            cout << "FAIL: For infix '" << test_case.infix << "', expected postfix '" 
                 << test_case.expected_postfix << "', but got '" << result << "'" << endl;
            return 1;
        }
    }
    
    cout << "PASS: All complex test cases passed" << endl;
    return 0;
}
"""
    
    modified_code = converter_code[:main_start] + test_main
    
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
    assert "PASS: All complex test cases passed" in output, f"Test failed with output: {output}"

def test_infix_to_postfix_edge_cases():
    """Test that the infix to postfix converter handles edge cases correctly."""
    # Skip if the file doesn't exist
    if not os.path.exists(INFIX_TO_POSTFIX_PATH):
        pytest.skip(f"File {INFIX_TO_POSTFIX_PATH} does not exist")
    
    # Create a temporary file with test cases
    temp_file = os.path.join(os.path.dirname(__file__), "temp_infix_to_postfix_edge.cpp")
    
    with open(INFIX_TO_POSTFIX_PATH, 'r') as f:
        converter_code = f.read()
    
    # Find the main function and replace it with our test main
    main_start = converter_code.find("int main()")
    if main_start == -1:
        main_start = converter_code.find("int main ()")
    
    if main_start == -1:
        pytest.skip("Could not find main function in infix_to_postfix.cpp")
    
    main_end = converter_code.rfind("}")
    
    test_main = """
int main()
{
    // Test edge cases for infix to postfix conversion
    struct TestCase {
        string infix;
        string expected_postfix;
    };
    
    vector<TestCase> test_cases = {
        {"A", "A"},  // Single operand
        {"", ""},    // Empty string
        {"(A)", "A"},  // Redundant parentheses
        {"((((A))))", "A"},  // Multiple redundant parentheses
        {"A+B+C+D+E+F+G+H+I+J", "AB+C+D+E+F+G+H+I+J+"},  // Many operands
        {"A*(B*(C*(D*(E*(F*(G*(H*(I*J))))))))", "ABCDEFGHIJ********"},  // Deeply nested
        {"A^B^C^D^E", "ABCDE^^^^"}  // Multiple exponentiation (right-associative)
    };
    
    for (const TestCase& test_case : test_cases) {
        string result = infixToPostfix(test_case.infix);
        if (result != test_case.expected_postfix) {
            cout << "FAIL: For infix '" << test_case.infix << "', expected postfix '" 
                 << test_case.expected_postfix << "', but got '" << result << "'" << endl;
            return 1;
        }
    }
    
    cout << "PASS: All edge cases passed" << endl;
    return 0;
}
"""
    
    modified_code = converter_code[:main_start] + test_main
    
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
    assert "PASS: All edge cases passed" in output, f"Test failed with output: {output}"

def test_infix_to_postfix_error_handling():
    """Test that the infix to postfix converter handles errors correctly."""
    # Skip if the file doesn't exist
    if not os.path.exists(INFIX_TO_POSTFIX_PATH):
        pytest.skip(f"File {INFIX_TO_POSTFIX_PATH} does not exist")
    
    # Create a temporary file with test cases
    temp_file = os.path.join(os.path.dirname(__file__), "temp_infix_to_postfix_error.cpp")
    
    with open(INFIX_TO_POSTFIX_PATH, 'r') as f:
        converter_code = f.read()
    
    # Find the main function and replace it with our test main
    main_start = converter_code.find("int main()")
    if main_start == -1:
        main_start = converter_code.find("int main ()")
    
    if main_start == -1:
        pytest.skip("Could not find main function in infix_to_postfix.cpp")
    
    main_end = converter_code.rfind("}")
    
    test_main = """
int main()
{
    // Test error handling for infix to postfix conversion
    vector<string> invalid_expressions = {
        "A+",        // Missing operand
        "+A",        // Missing operand
        "A++B",      // Invalid operator sequence
        "A(B+C)",    // Missing operator
        "(A+B)C",    // Missing operator
        "(A+B",      // Unbalanced parentheses
        "A+B)",      // Unbalanced parentheses
        "A+B**C",    // Invalid operator sequence
        "A*/B",      // Invalid operator sequence
        "A B"        // Invalid spacing
    };
    
    bool all_passed = true;
    
    for (const string& invalid_expr : invalid_expressions) {
        try {
            string result = infixToPostfix(invalid_expr);
            // If we get here, the function didn't throw an exception
            // Check if the result is empty or has some error indicator
            if (!result.empty() && result.find("ERROR") == string::npos) {
                cout << "FAIL: For invalid infix '" << invalid_expr 
                     << "', expected an error but got '" << result << "'" << endl;
                all_passed = false;
            }
        } catch (...) {
            // Exception was thrown, which is acceptable for invalid input
        }
    }
    
    if (all_passed) {
        cout << "PASS: All error handling tests passed" << endl;
        return 0;
    } else {
        return 1;
    }
}
"""
    
    modified_code = converter_code[:main_start] + test_main
    
    with open(temp_file, 'w') as f:
        f.write(modified_code)
    
    # Run the test
    output = run_cpp_file(temp_file)
    
    # We don't assert here because the implementation might handle errors differently
    # Just check if the test ran without crashing
    assert "Runtime error" not in output, f"Test crashed with output: {output}"
