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
        } //checks if stack empty
        int size()
        {
            return data.size();
        } //returns size of a stack
        void push(int value)
        {
            data.push_back(value);    
        } // pushs value to the top of stack
        
        int peek()
        {
            return data.back();
        }   // show the top ellement of stack
        
        int pop()
        {
            int value_to_return = peek();
            data.pop_back();
            return value_to_return;
        }; //work like peek, but then deleting ellements
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