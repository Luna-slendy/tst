"""
Tests for the next greater element problem (Task 4).
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

# Path to the next_greater_element.cpp file
NEXT_GREATER_ELEMENT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "advanced/next_greater_element.cpp")

def test_next_greater_element_exists():
    """Test that the next_greater_element.cpp file exists."""
    assert os.path.exists(NEXT_GREATER_ELEMENT_PATH), f"File {NEXT_GREATER_ELEMENT_PATH} does not exist"

def test_next_greater_element_basic():
    """Test that the next greater element function works correctly for basic cases."""
    # Skip if the file doesn't exist
    if not os.path.exists(NEXT_GREATER_ELEMENT_PATH):
        pytest.skip(f"File {NEXT_GREATER_ELEMENT_PATH} does not exist")
    
    # Create a temporary file with test cases
    temp_file = os.path.join(os.path.dirname(__file__), "temp_next_greater_element.cpp")
    
    with open(NEXT_GREATER_ELEMENT_PATH, 'r') as f:
        nge_code = f.read()
    
    # Find the main function and replace it with our test main
    main_start = nge_code.find("int main()")
    if main_start == -1:
        main_start = nge_code.find("int main ()")
    
    if main_start == -1:
        pytest.skip("Could not find main function in next_greater_element.cpp")
    
    main_end = nge_code.rfind("}")
    
    test_main = """
int main()
{
    // Test basic next greater element cases
    struct TestCase {
        vector<int> input;
        vector<int> expected_output;
    };
    
    vector<TestCase> test_cases = {
        {{4, 5, 2, 25}, {5, 25, 25, -1}},
        {{13, 7, 6, 12}, {-1, 12, 12, -1}},
        {{1, 2, 3, 4}, {2, 3, 4, -1}},
        {{4, 3, 2, 1}, {-1, -1, -1, -1}}
    };
    
    for (const TestCase& test_case : test_cases) {
        vector<int> result = nextGreaterElements(test_case.input);
        
        if (result.size() != test_case.expected_output.size()) {
            cout << "FAIL: Output size mismatch for input [";
            for (size_t i = 0; i < test_case.input.size(); i++) {
                cout << test_case.input[i];
                if (i < test_case.input.size() - 1) cout << ", ";
            }
            cout << "]" << endl;
            return 1;
        }
        
        for (size_t i = 0; i < result.size(); i++) {
            if (result[i] != test_case.expected_output[i]) {
                cout << "FAIL: For input [";
                for (size_t j = 0; j < test_case.input.size(); j++) {
                    cout << test_case.input[j];
                    if (j < test_case.input.size() - 1) cout << ", ";
                }
                cout << "], expected output [";
                for (size_t j = 0; j < test_case.expected_output.size(); j++) {
                    cout << test_case.expected_output[j];
                    if (j < test_case.expected_output.size() - 1) cout << ", ";
                }
                cout << "], but got [";
                for (size_t j = 0; j < result.size(); j++) {
                    cout << result[j];
                    if (j < result.size() - 1) cout << ", ";
                }
                cout << "]" << endl;
                return 1;
            }
        }
    }
    
    cout << "PASS: All basic test cases passed" << endl;
    return 0;
}
"""
    
    # Assuming there's a function called nextGreaterElements
    # If the function has a different name, the test will fail
    
    modified_code = nge_code[:main_start] + test_main
    
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

def test_next_greater_element_edge_cases():
    """Test that the next greater element function handles edge cases correctly."""
    # Skip if the file doesn't exist
    if not os.path.exists(NEXT_GREATER_ELEMENT_PATH):
        pytest.skip(f"File {NEXT_GREATER_ELEMENT_PATH} does not exist")
    
    # Create a temporary file with test cases
    temp_file = os.path.join(os.path.dirname(__file__), "temp_next_greater_element_edge.cpp")
    
    with open(NEXT_GREATER_ELEMENT_PATH, 'r') as f:
        nge_code = f.read()
    
    # Find the main function and replace it with our test main
    main_start = nge_code.find("int main()")
    if main_start == -1:
        main_start = nge_code.find("int main ()")
    
    if main_start == -1:
        pytest.skip("Could not find main function in next_greater_element.cpp")
    
    main_end = nge_code.rfind("}")
    
    test_main = """
int main()
{
    // Test edge cases for next greater element
    struct TestCase {
        vector<int> input;
        vector<int> expected_output;
    };
    
    vector<TestCase> test_cases = {
        {{}, {}},                                // Empty array
        {{1}, {-1}},                             // Single element
        {{1, 1, 1, 1}, {-1, -1, -1, -1}},        // All elements are the same
        {{INT_MAX}, {-1}},                       // Maximum integer value
        {{INT_MIN}, {-1}},                       // Minimum integer value
        {{5, 4, 3, 2, 1, 6}, {6, 6, 6, 6, 6, -1}},  // Decreasing then increasing
        {{1, 2, 3, 4, 3, 2, 1}, {2, 3, 4, -1, -1, -1, -1}}  // Increasing then decreasing
    };
    
    for (const TestCase& test_case : test_cases) {
        vector<int> result = nextGreaterElements(test_case.input);
        
        if (result.size() != test_case.expected_output.size()) {
            cout << "FAIL: Output size mismatch for input [";
            for (size_t i = 0; i < test_case.input.size(); i++) {
                cout << test_case.input[i];
                if (i < test_case.input.size() - 1) cout << ", ";
            }
            cout << "]" << endl;
            return 1;
        }
        
        for (size_t i = 0; i < result.size(); i++) {
            if (result[i] != test_case.expected_output[i]) {
                cout << "FAIL: For input [";
                for (size_t j = 0; j < test_case.input.size(); j++) {
                    cout << test_case.input[j];
                    if (j < test_case.input.size() - 1) cout << ", ";
                }
                cout << "], expected output [";
                for (size_t j = 0; j < test_case.expected_output.size(); j++) {
                    cout << test_case.expected_output[j];
                    if (j < test_case.expected_output.size() - 1) cout << ", ";
                }
                cout << "], but got [";
                for (size_t j = 0; j < result.size(); j++) {
                    cout << result[j];
                    if (j < result.size() - 1) cout << ", ";
                }
                cout << "]" << endl;
                return 1;
            }
        }
    }
    
    cout << "PASS: All edge cases passed" << endl;
    return 0;
}
"""
    
    modified_code = nge_code[:main_start] + test_main
    
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

def test_next_greater_element_performance():
    """Test the performance of the next greater element function."""
    # Skip if the file doesn't exist
    if not os.path.exists(NEXT_GREATER_ELEMENT_PATH):
        pytest.skip(f"File {NEXT_GREATER_ELEMENT_PATH} does not exist")
    
    # Create a temporary file with a performance test
    temp_file = os.path.join(os.path.dirname(__file__), "temp_next_greater_element_perf.cpp")
    
    with open(NEXT_GREATER_ELEMENT_PATH, 'r') as f:
        nge_code = f.read()
    
    # Find the main function and replace it with our test main
    main_start = nge_code.find("int main()")
    if main_start == -1:
        main_start = nge_code.find("int main ()")
    
    if main_start == -1:
        pytest.skip("Could not find main function in next_greater_element.cpp")
    
    main_end = nge_code.rfind("}")
    
    test_main = """
int main()
{
    // Test performance with a large array
    const int SIZE = 10000;
    vector<int> large_array(SIZE);
    
    // Fill the array with random values
    srand(time(NULL));
    for (int i = 0; i < SIZE; i++) {
        large_array[i] = rand() % 1000000;
    }
    
    // Measure the time it takes to find the next greater elements
    clock_t start = clock();
    vector<int> result = nextGreaterElements(large_array);
    clock_t end = clock();
    
    double cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    
    // Check that the result has the correct size
    if (result.size() != SIZE) {
        cout << "FAIL: Output size mismatch for large array" << endl;
        return 1;
    }
    
    cout << "PASS: Performance test completed in " << cpu_time_used << " seconds" << endl;
    
    // The function should run in O(n) time, so it should be relatively fast
    // even for large arrays. We don't set a specific time limit, but we check
    // that it completes.
    
    return 0;
}
"""
    
    modified_code = nge_code[:main_start] + test_main
    
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
    assert "PASS: Performance test completed" in output, f"Test failed with output: {output}"
