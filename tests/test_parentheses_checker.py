"""
Tests for the parentheses checker application (Task 3).
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

# Path to the parentheses_checker.cpp file
PARENTHESES_CHECKER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "applications/parentheses_checker.cpp")

def test_parentheses_checker_exists():
    """Test that the parentheses_checker.cpp file exists."""
    assert os.path.exists(PARENTHESES_CHECKER_PATH), f"File {PARENTHESES_CHECKER_PATH} does not exist"

def test_parentheses_checker_balanced():
    """Test that the parentheses checker correctly identifies balanced parentheses."""
    # Skip if the file doesn't exist
    if not os.path.exists(PARENTHESES_CHECKER_PATH):
        pytest.skip(f"File {PARENTHESES_CHECKER_PATH} does not exist")
    
    # Create a temporary file with test cases
    temp_file = os.path.join(os.path.dirname(__file__), "temp_parentheses_checker.cpp")
    
    with open(PARENTHESES_CHECKER_PATH, 'r') as f:
        checker_code = f.read()
    
    # Find the main function and replace it with our test main
    main_start = checker_code.find("int main()")
    if main_start == -1:
        main_start = checker_code.find("int main ()")
    
    if main_start == -1:
        pytest.skip("Could not find main function in parentheses_checker.cpp")
    
    main_end = checker_code.rfind("}")
    
    test_main = """
int main()
{
    // Test balanced parentheses
    vector<string> balanced_cases = {
        "()",
        "[]",
        "{}",
        "([]{})",
        "{[()]}",
        "((()))",
        "({[]})",
        "",  // Empty string is balanced
        "a(b)c[d]e{f}g",  // With other characters
        "if (x > 0) { return [x, y]; }"  // Code-like example
    };
    
    for (const string& test_case : balanced_cases) {
        if (!isBalanced(test_case)) {
            cout << "FAIL: '" << test_case << "' should be balanced" << endl;
            return 1;
        }
    }
    
    cout << "PASS: All balanced test cases passed" << endl;
    return 0;
}
"""
    
    # Assuming there's a function called isBalanced
    # If the function has a different name, the test will fail
    
    modified_code = checker_code[:main_start] + test_main
    
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
    assert "PASS: All balanced test cases passed" in output, f"Test failed with output: {output}"

def test_parentheses_checker_unbalanced():
    """Test that the parentheses checker correctly identifies unbalanced parentheses."""
    # Skip if the file doesn't exist
    if not os.path.exists(PARENTHESES_CHECKER_PATH):
        pytest.skip(f"File {PARENTHESES_CHECKER_PATH} does not exist")
    
    # Create a temporary file with test cases
    temp_file = os.path.join(os.path.dirname(__file__), "temp_parentheses_checker_unbalanced.cpp")
    
    with open(PARENTHESES_CHECKER_PATH, 'r') as f:
        checker_code = f.read()
    
    # Find the main function and replace it with our test main
    main_start = checker_code.find("int main()")
    if main_start == -1:
        main_start = checker_code.find("int main ()")
    
    if main_start == -1:
        pytest.skip("Could not find main function in parentheses_checker.cpp")
    
    main_end = checker_code.rfind("}")
    
    test_main = """
int main()
{
    // Test unbalanced parentheses
    vector<string> unbalanced_cases = {
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        "(]",
        "[}",
        "{)",
        "([)]",
        "(()",
        "([{",
        "}])",
        "({)}",
        "if (x > 0 { return [x, y]; }"  // Missing closing parenthesis
    };
    
    for (const string& test_case : unbalanced_cases) {
        if (isBalanced(test_case)) {
            cout << "FAIL: '" << test_case << "' should be unbalanced" << endl;
            return 1;
        }
    }
    
    cout << "PASS: All unbalanced test cases passed" << endl;
    return 0;
}
"""
    
    modified_code = checker_code[:main_start] + test_main
    
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
    assert "PASS: All unbalanced test cases passed" in output, f"Test failed with output: {output}"

def test_parentheses_checker_edge_cases():
    """Test that the parentheses checker handles edge cases correctly."""
    # Skip if the file doesn't exist
    if not os.path.exists(PARENTHESES_CHECKER_PATH):
        pytest.skip(f"File {PARENTHESES_CHECKER_PATH} does not exist")
    
    # Create a temporary file with test cases
    temp_file = os.path.join(os.path.dirname(__file__), "temp_parentheses_checker_edge.cpp")
    
    with open(PARENTHESES_CHECKER_PATH, 'r') as f:
        checker_code = f.read()
    
    # Find the main function and replace it with our test main
    main_start = checker_code.find("int main()")
    if main_start == -1:
        main_start = checker_code.find("int main ()")
    
    if main_start == -1:
        pytest.skip("Could not find main function in parentheses_checker.cpp")
    
    main_end = checker_code.rfind("}")
    
    test_main = """
int main()
{
    // Test edge cases
    
    // Very long string with balanced parentheses
    string long_balanced = "";
    for (int i = 0; i < 1000; i++) {
        long_balanced += "({[]})";
    }
    
    if (!isBalanced(long_balanced)) {
        cout << "FAIL: Long balanced string should be balanced" << endl;
        return 1;
    }
    
    // Very long string with unbalanced parentheses (missing one closing bracket at the end)
    string long_unbalanced = long_balanced + "(";
    
    if (isBalanced(long_unbalanced)) {
        cout << "FAIL: Long unbalanced string should be unbalanced" << endl;
        return 1;
    }
    
    // String with only non-bracket characters
    string no_brackets = "abcdefghijklmnopqrstuvwxyz";
    
    if (!isBalanced(no_brackets)) {
        cout << "FAIL: String with no brackets should be balanced" << endl;
        return 1;
    }
    
    cout << "PASS: All edge cases passed" << endl;
    return 0;
}
"""
    
    modified_code = checker_code[:main_start] + test_main
    
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
