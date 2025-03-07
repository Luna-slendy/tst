#include <iostream>
#include <vector>
using namespace std;
class Stack
{
    private:
        vector<int> data;
    public:
        bool isEmpty()
        {
            return data.empty();
        }
        int size()
        {
            return data.size();
        }
        void push(int value)
        {
            data.push_back(value);    
        }
        
        int peek()
        {
            return data.back();
        }  
        
        int pop()
        {
            int value_to_return = peek();
            data.pop_back();
            return value_to_return;
        };
};

int main()
{
    Stack stack;
    stack.push(10);
    cout << "peek into stack = " << stack.peek() << endl;
    for(int i = 0; i< 100; i++)
    {
        stack.push(i);
    }
    cout << "size of a stack - " << stack.size() << endl;
    cout << "peeking in stack = " << stack.peek() << endl;

    for(;stack.size();)
    {
        cout << "value from stack = " << stack.pop()  << endl;
    }
}