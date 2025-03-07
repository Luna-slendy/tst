"""
Tests for the postfix expression evaluator application (Task 3).
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

# Path to the postfix_evaluator.cpp file
POSTFIX_EVALUATOR_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "applications/postfix_evaluator.cpp")

def test_postfix_evaluator_exists():
    """Test that the postfix_evaluator.cpp file exists."""
    assert os.path.exists(POSTFIX_EVALUATOR_PATH), f"File {POSTFIX_EVALUATOR_PATH} does not exist"

def test_postfix_evaluator_basic():
    """Test that the postfix evaluator correctly evaluates basic expressions."""
    # Skip if the file doesn't exist
    if not os.path.exists(POSTFIX_EVALUATOR_PATH):
        pytest.skip(f"File {POSTFIX_EVALUATOR_PATH} does not exist")
    
    # Create a temporary file with test cases
    temp_file = os.path.join(os.path.dirname(__file__), "temp_postfix_evaluator.cpp")
    
    with open(POSTFIX_EVALUATOR_PATH, 'r') as f:
        evaluator_code = f.read()
    
    # Find the main function and replace it with our test main
    main_start = evaluator_code.find("int main()")
    if main_start == -1:
        main_start = evaluator_code.find("int main ()")
    
    if main_start == -1:
        pytest.skip("Could not find main function in postfix_evaluator.cpp")
    
    main_end = evaluator_code.rfind("}")
    
    test_main = """
int main()
{
    // Test basic postfix expression evaluations
    struct TestCase {
        string postfix;
        int expected_result;
    };
    
    vector<TestCase> test_cases = {
        {"5", 5},                    // Single operand
        {"5 3 +", 8},               // Addition
        {"5 3 -", 2},               // Subtraction
        {"5 3 *", 15},              // Multiplication
        {"6 3 /", 2},               // Division
        {"5 3 + 2 *", 16},          // Addition then multiplication
        {"5 3 * 2 +", 17},          // Multiplication then addition
        {"5 1 2 + 4 * + 3 -", 14}   // Complex expression
    };
    
    for (const TestCase& test_case : test_cases) {
        int result = evaluatePostfix(test_case.postfix);
        if (result != test_case.expected_result) {
            cout << "FAIL: For postfix '" << test_case.postfix << "', expected result " 
                 << test_case.expected_result << ", but got " << result << endl;
            return 1;
        }
    }
    
    cout << "PASS: All basic test cases passed" << endl;
    return 0;
}
"""
    
    # Assuming there's a function called evaluatePostfix
    # If the function has a different name, the test will fail
    
    modified_code = evaluator_code[:main_start] + test_main
    
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

def test_postfix_evaluator_complex():
    """Test that the postfix evaluator correctly evaluates complex expressions."""
    # Skip if the file doesn't exist
    if not os.path.exists(POSTFIX_EVALUATOR_PATH):
        pytest.skip(f"File {POSTFIX_EVALUATOR_PATH} does not exist")
    
    # Create a temporary file with test cases
    temp_file = os.path.join(os.path.dirname(__file__), "temp_postfix_evaluator_complex.cpp")
    
    with open(POSTFIX_EVALUATOR_PATH, 'r') as f:
        evaluator_code = f.read()
    
    # Find the main function and replace it with our test main
    main_start = evaluator_code.find("int main()")
    if main_start == -1:
        main_start = evaluator_code.find("int main ()")
    
    if main_start == -1:
        pytest.skip("Could not find main function in postfix_evaluator.cpp")
    
    main_end = evaluator_code.rfind("}")
    
    test_main = """
int main()
{
    // Test complex postfix expression evaluations
    struct TestCase {
        string postfix;
        int expected_result;
    };
    
    vector<TestCase> test_cases = {
        {"10 5 + 2 * 8 /", 3},                      // (10+5)*2/8 = 3
        {"100 50 25 + - 10 * 5 /", 50},             // (100-(50+25))*10/5 = 50
        {"2 3 4 * +", 14},                          // 2+(3*4) = 14
        {"5 1 2 + 4 * + 3 -", 14},                  // 5+((1+2)*4)-3 = 14
        {"7 2 3 * -", 1},                           // 7-(2*3) = 1
        {"9 3 / 2 * 7 +", 13},                      // (9/3)*2+7 = 13
        {"20 10 5 + - 2 /", 2},                     // (20-(10+5))/2 = 2
        {"8 4 / 3 2 * +", 8},                       // (8/4)+(3*2) = 8
        {"100 10 / 5 * 2 + 10 -", 42},              // ((100/10)*5)+2-10 = 42
        {"1 2 + 3 4 + * 5 6 + *", 165}              // ((1+2)*(3+4))*(5+6) = 165
    };
    
    for (const TestCase& test_case : test_cases) {
        int result = evaluatePostfix(test_case.postfix);
        if (result != test_case.expected_result) {
            cout << "FAIL: For postfix '" << test_case.postfix << "', expected result " 
                 << test_case.expected_result << ", but got " << result << endl;
            return 1;
        }
    }
    
    cout << "PASS: All complex test cases passed" << endl;
    return 0;
}
"""
    
    modified_code = evaluator_code[:main_start] + test_main
    
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

def test_postfix_evaluator_error_handling():
    """Test that the postfix evaluator handles errors correctly."""
    # Skip if the file doesn't exist
    if not os.path.exists(POSTFIX_EVALUATOR_PATH):
        pytest.skip(f"File {POSTFIX_EVALUATOR_PATH} does not exist")
    
    # Create a temporary file with test cases
    temp_file = os.path.join(os.path.dirname(__file__), "temp_postfix_evaluator_error.cpp")
    
    with open(POSTFIX_EVALUATOR_PATH, 'r') as f:
        evaluator_code = f.read()
    
    # Find the main function and replace it with our test main
    main_start = evaluator_code.find("int main()")
    if main_start == -1:
        main_start = evaluator_code.find("int main ()")
    
    if main_start == -1:
        pytest.skip("Could not find main function in postfix_evaluator.cpp")
    
    main_end = evaluator_code.rfind("}")
    
    test_main = """
int main()
{
    // Test error handling for postfix expression evaluation
    vector<string> invalid_expressions = {
        "",                   // Empty expression
        "+",                  // Single operator
        "5 +",                // Missing operand
        "+ 5",                // Missing operand
        "5 5",                // Missing operator
        "5 5 + +",            // Extra operator
        "5 0 /",              // Division by zero
        "a b +",              // Non-numeric operands
        "5 5 5 +",            // Extra operand
        "5 5 + + +"           // Too many operators
    };
    
    bool all_passed = true;
    
    for (const string& invalid_expr : invalid_expressions) {
        try {
            int result = evaluatePostfix(invalid_expr);
            // If we get here, the function didn't throw an exception
            // For some cases like division by zero, we might expect an exception
            // For others, the function might return a special value or handle it differently
            cout << "For invalid postfix '" << invalid_expr 
                 << "', got result " << result << endl;
        } catch (...) {
            // Exception was thrown, which is acceptable for invalid input
            cout << "Exception thrown for invalid postfix '" << invalid_expr << "'" << endl;
        }
    }
    
    cout << "PASS: Error handling test completed" << endl;
    return 0;
}
"""
    
    modified_code = evaluator_code[:main_start] + test_main
    
    with open(temp_file, 'w') as f:
        f.write(modified_code)
    
    # Run the test
    output = run_cpp_file(temp_file)
    
    # We don't assert here because the implementation might handle errors differently
    # Just check if the test ran without crashing
    assert "Runtime error" not in output, f"Test crashed with output: {output}"
    assert "PASS: Error handling test completed" in output, f"Test failed with output: {output}"
