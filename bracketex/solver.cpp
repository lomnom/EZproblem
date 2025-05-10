#include <iostream>
#include <stack>
typedef long long int ll;

using namespace std;

/*
Explanation: 
[Considered a recursive solution with seeking, its kinda complicated and could bug. Stack solution it is.]
0. Maintain a stack for open brackets, open_brackets.
1. Go through all characters from start to end.
   1. If bracket is opening, open_brackets.push(type)
   2. If bracket is closing, 
     1. If bracket is not same type as open_brackets.top(), invalid closing - return invalid
     2. Else, open_brackets.pop(), if possible else return invalid
2. At the end, if there is anything left on the stack, it means there are unclosed brackets. Return invalid.
3. If invalid was not returned yet, return valid.
*/

typedef uint8_t bracket_t;

// Bracket types
#define CURLY 0
#define SQUARE 1
#define ROUND 2

// Bracket state
typedef bool state_t;
#define OPEN true
#define CLOSE false

bracket_t bracket_type(char bracket){
	if (bracket == '}' || bracket == '{'){
		return CURLY;
	} else if (bracket == ']' || bracket == '['){
		return SQUARE;
	} else if (bracket == ')' || bracket == '('){
		return ROUND;
	}
}

state_t bracket_state(char bracket){
	if (bracket == '}' || bracket == ')' || bracket == ']'){
		return CLOSE;
	} else if (bracket == '{' || bracket == '(' || bracket == '['){
		return OPEN;
	}
}

int main(){
	cin.tie(0);
	cout.sync_with_stdio(false);

	stack<bracket_t> open_brackets;

	ll length;
	cin >> length;

	string brackets;
	cin >> brackets;

	for (ll index = 0; index < length; index++){
		char bracket = brackets[index];
		state_t state = bracket_state(bracket);
		bracket_t type = bracket_type(bracket);
		if (state == OPEN){
			open_brackets.push(type);
		} else if (state == CLOSE){
			if (open_brackets.empty()){
				cout << "Invalid\n";
				return 0;
			}

			bracket_t deepest_open = open_brackets.top();
			if (type != deepest_open){
				cout << "Invalid\n";
				return 0;
			} else {
				open_brackets.pop();
			}
		}
	}

	if (open_brackets.empty()){
		cout << "Valid\n";
	} else {
		cout << "Invalid\n";
	}

	return 0;
}