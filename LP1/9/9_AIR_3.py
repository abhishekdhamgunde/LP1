# Implement goal stack planning for the following configurations from the blocks world
import sys
import copy
import heapq

filename = sys.argv

num_nodes_expanded = 0

# Opening input file for reading and reading the inputs

file = open(filename[1], "r")
line = file.readline()
num_blocks = int(line)
line = file.readline()
line = line.strip()
algorithm = line

line = file.readline()
line = file.readline()
line = line.strip() # Return a copy of the string with leading and trailing whitespace removed.
i_state = line

line = file.readline()
line = file.readline()
line = line.strip()
g_state = line


ll = i_state.split(") (")
ll[0] = ll[0][1:]
ll[len(ll)-1] = ll[len(ll)-1][:-1]


i_state = ll


state_size = num_blocks**2+3*num_blocks+1

s = []
g = []

"""
STATE DESCRIPTION

All the states have been stored in the form of a boolean array of size n^2+3*n+1
The first n^2 entries denote if any of the predicates on(1,1), on(1,2),....., on(n,n) are true in that state
The next n entries denote if any of the predicates ontable(1), ontable(2),...., ontable(n) are true in that state
The next n entries denote if any of the predicates clear(1), clear(2),...., clear(n) are true in that state
The next n entries denote if any of the predicates hold(1), hold(2),...., hold(n) are true in that state
The last entry denotes if predicate <empty> is true in that state or not 
"""

s = [0]*state_size
g = [0]*state_size

for i in range(len(ll)):                       # Populating the starting state array
    ele = ll[i]
    ele = ele.split(" ")
    if(ele[0] == "on"):
        num1 = int(ele[1])-1
        num2 = int(ele[2])-1
        s[num1*num_blocks+num2] = 1
    elif(ele[0] == "ontable"):
        num1 = int(ele[1])-1
        s[num_blocks*num_blocks+num1] = 1
    elif(ele[0] == "clear"):
        num1 = int(ele[1])-1
        s[num_blocks*num_blocks+num_blocks+num1] = 1
    elif(ele[0] == "hold"):
        num1 = int(ele[1])-1
        s[num_blocks*num_blocks+2*num_blocks+num1] = 1
    elif(ele[0] == "empty"):
        s[num_blocks*num_blocks+3*num_blocks] = 1


ll = []
ll = g_state.split(") (")
ll[0] = ll[0][1:]
ll[len(ll)-1] = ll[len(ll)-1][:-1]

g_state = ll


for i in range(len(ll)):                         # Populating the goal state array
    ele = ll[i]
    ele = ele.split(" ")
    if(ele[0] == "on"):
        num1 = int(ele[1])-1
        num2 = int(ele[2])-1
        g[num1*num_blocks+num2] = 1
    elif(ele[0] == "ontable"):
        num1 = int(ele[1])-1
        g[num_blocks*num_blocks+num1] = 1
    elif(ele[0] == "clear"):
        num1 = int(ele[1])-1
        g[num_blocks*num_blocks+num_blocks+num1] = 1
    elif(ele[0] == "hold"):
        num1 = int(ele[1])-1
        g[num_blocks*num_blocks+2*num_blocks+num1] = 1
    elif(ele[0] == "empty"):
        g[num_blocks*num_blocks+3*num_blocks] = 1


# print(s,g)
# Defined a stack for using in

class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."

    def __init__(self):
        self.list = []

    def push(self, item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0


"""
Function which returns true if the current state is a goal state(given in the file) 
or else returns false
"""


def isGoalState(state):
    if(len(state) != len(g)):
        return 0
    for i in range(len(g)):
        if(state[i] != g[i]):
            return 0
    return 1


def goalStackPlanning():
    # List of actions to take (initially empty)
    actions_to_take = []
    stack = Stack()                          # Stack initialized
    new = copy.deepcopy(g)
    # pushing the goal state onto the stack
    stack.push(new)
    cur_state = copy.deepcopy(s)
    p_cond = [0]*(num_blocks*num_blocks+3*num_blocks+1)

    # Pushing the predicates of the goal state individually onto the stack
    for i in range(num_blocks*num_blocks+3*num_blocks+1):
        if(new[i] == 1):
            stack.push(i+1)

    while(not stack.isEmpty()):            # While stack not empty
        ele = stack.pop()
        # if popped element is a conjunct goal
        if(type(ele) == list):
            passed = 1
            # Checking if all the predicates are individually true
            for i in range(num_blocks*num_blocks+3*num_blocks+1):
                if(ele[i] == 1 and cur_state[i] == 0):
                    passed = 0
                    break
            """
                        If the predicates are not true then pushing the conjunct goal
                        and the individual predicates on the stack again
                        """
            if(passed == 0):
                stack.push(ele)
                for i in range(num_blocks*num_blocks+3*num_blocks+1):
                    if(ele[i] == 1):
                        stack.push(i+1)
        # if popped element is a predicate
        elif(type(ele) == int):
            # if <empty> present in current state>
            if(cur_state[ele-1] == 0):
                act = []
                ano = ele-1
                # if predicate is on(x,y), selecting the relevant action to push on the stack
                if(ano < num_blocks*num_blocks):
                    a = ano/num_blocks
                    b = ano % num_blocks
                    act = "stack "+str(a+1)+" "+str(b+1)
                    stack.push(act)
                    precond = copy.deepcopy(p_cond)
                    precond[num_blocks*num_blocks+num_blocks+b] = 1
                    precond[int(num_blocks*num_blocks+2*num_blocks+a)] = 1
                    stack.push(precond)
                    stack.push(num_blocks*num_blocks+num_blocks+b+1)
                    stack.push(int(num_blocks*num_blocks+2*num_blocks+a)+1)

                # if predicate is Ontable(x), selecting the relevant action to push on the stack
                elif(ano < num_blocks*num_blocks+num_blocks):
                    a = ano-(num_blocks*num_blocks)
                    act = "release "+str(a+1)
                    stack.push(act)
                    precond = copy.deepcopy(p_cond)
                    precond[int(num_blocks*num_blocks+2*num_blocks+a)] = 1
                    stack.push(precond)
                    stack.push(int(num_blocks*num_blocks+2*num_blocks+a)+1)

                # if predicate is Clear(x), selecting the relevant action to push on the stack
                elif(ano < num_blocks*num_blocks+2*num_blocks):
                    holdblock = 0
                    b = ano-(num_blocks*num_blocks+num_blocks)
                    if(cur_state[num_blocks*num_blocks+2*num_blocks+b] == 1):
                        holdblock = 1
                    if(holdblock == 1):
                        a = ano-(num_blocks*num_blocks+num_blocks)
                        # Release block only
                        act = "release "+str(a+1)
                        stack.push(act)
                        precond = copy.deepcopy(p_cond)
                        precond[int(num_blocks*num_blocks+2*num_blocks+a)] = 1
                        stack.push(precond)
                        stack.push(int(num_blocks*num_blocks+2*num_blocks+a)+1)
                    else:
                        b = ano-(num_blocks*num_blocks+num_blocks)
                        a = -1
                        for i in range(num_blocks):
                            if(cur_state[i*num_blocks+b] == 1):
                                a = i
                                break
                        if(a != -1):
                            act = "unstack "+str(a+1)+" "+str(b+1)
                            stack.push(act)
                            precond = copy.deepcopy(p_cond)
                            precond[num_blocks*a+b] = 1
                            precond[num_blocks*num_blocks+3*num_blocks] = 1
                            precond[num_blocks*num_blocks+num_blocks+a] = 1
                            stack.push(precond)
                            stack.push(num_blocks*num_blocks+num_blocks+a+1)
                            stack.push(num_blocks*num_blocks+3*num_blocks+1)
                            stack.push(num_blocks*a+b+1)

                # if predicate is hold(x), selecting the relevant action to push on the stack
                elif(ano < num_blocks*num_blocks+3*num_blocks):
                    a = ano-(num_blocks*num_blocks+2*num_blocks)
                    ontable = 0
                    if(cur_state[num_blocks*num_blocks+a] == 1):
                        ontable = 1
                    if(ontable == 1):
                        act = "pick "+str(a+1)
                        stack.push(act)
                        precond = copy.deepcopy(p_cond)
                        precond[num_blocks*num_blocks+a] = 1
                        precond[num_blocks*num_blocks+num_blocks+a] = 1
                        precond[num_blocks*num_blocks+3*num_blocks] = 1
                        stack.push(precond)
                        stack.push(num_blocks*num_blocks+3*num_blocks+1)
                        stack.push(num_blocks*num_blocks+num_blocks+a+1)
                        stack.push(num_blocks*num_blocks+a+1)
                    else:
                        b = -1
                        for i in range(a*num_blocks, (a+1)*num_blocks):
                            if(cur_state[i] == 1):
                                b = i
                                break
                        if(b != -1):
                            b = b-a*num_blocks
                            act = "unstack "+str(a+1)+" "+str(b+1)
                            stack.push(act)
                            precond = copy.deepcopy(p_cond)
                            precond[num_blocks*a+b] = 1
                            precond[num_blocks*num_blocks+3*num_blocks] = 1
                            precond[num_blocks*num_blocks+num_blocks+a] = 1
                            stack.push(precond)
                            stack.push(num_blocks*num_blocks+num_blocks+a+1)
                            stack.push(num_blocks*num_blocks+3*num_blocks+1)
                            stack.push(num_blocks*a+b+1)
                            s
                else:
                    a = -1
                    for i in range(num_blocks*num_blocks+2*num_blocks, num_blocks*num_blocks+3*num_blocks):
                        if(cur_state[i] == 1):
                            a = i-num_blocks*num_blocks-2*num_blocks
                            break
                    if(a != -1):
                        act = "release "+str(a+1)
                        stack.push(act)
                        precond = copy.deepcopy(p_cond)
                        precond[int(num_blocks*num_blocks+2*num_blocks+a)] = 1
                        stack.push(precond)
                        stack.push(int(num_blocks*num_blocks+2*num_blocks+a)+1)

        # if popped element is an action, then applying the action to the current state and storing it
        elif(type(ele) == str):
            actions_to_take.append(ele)
            elements = ele.split(" ")
            if(elements[0] == "pick"):
                num = int(elements[1])
                cur_state[num_blocks*num_blocks+num -
                          1] = 0                  # Not ontable
                cur_state[num_blocks*num_blocks +
                          num_blocks+num-1] = 0       # Not Clear
                cur_state[num_blocks*num_blocks+2 *
                          num_blocks+num-1] = 1     # Hold Block
                cur_state[num_blocks*num_blocks+3 *
                          num_blocks] = 0           # Not empty
            elif(elements[0] == "unstack"):
                num1 = int(elements[1])
                num2 = int(elements[2])
                cur_state[num_blocks*num_blocks+2 *
                          num_blocks+num1-1] = 1     # Hold(A)
                cur_state[num_blocks*num_blocks +
                          num_blocks+num2-1] = 1       # Clear(B)
                # not on(A,B)
                cur_state[num_blocks*(num1-1)+num2-1] = 0
                cur_state[num_blocks*num_blocks+3 *
                          num_blocks] = 0            # not empty
                cur_state[num_blocks*num_blocks+num_blocks +
                          num1-1] = 0       # Not Clear(A)
            elif(elements[0] == "release"):
                num = int(elements[1])
                cur_state[num_blocks*num_blocks+num -
                          1] = 1                  # ontable
                cur_state[num_blocks*num_blocks +
                          num_blocks+num-1] = 1       # Clear
                cur_state[num_blocks*num_blocks+2 *
                          num_blocks+num-1] = 0     # Not Hold Block
                cur_state[num_blocks*num_blocks+3 *
                          num_blocks] = 1           # empty
            elif(elements[0] == "stack"):
                num1 = int(float(elements[1]))
                num2 = int(elements[2])
                cur_state[num_blocks*num_blocks+2 *
                          num_blocks+num1-1] = 0     # Not Hold(A)
                cur_state[num_blocks*num_blocks+num_blocks +
                          num2-1] = 0       # Not Clear(B)
                # on(A,B)
                cur_state[num_blocks*(num1-1)+num2-1] = 1
                cur_state[num_blocks*num_blocks+3 *
                          num_blocks] = 1            # empty
                cur_state[num_blocks*num_blocks +
                          num_blocks+num1-1] = 1       # Clear(A)

    # returning the final list of actions
    return actions_to_take


file.close()

file = open("output_"+filename[1], "w")

if(algorithm == "g"):  # Calling the Goal Stack Algorithm
    actions = goalStackPlanning()
    print("Goal Stack Planning used")
    print("Solution Length: ", len(actions))
    file.write(str(len(actions))+"\n")
    for i in range(len(actions)):
        print(actions[i]+"\n")
        file.write(actions[i]+"\n")

file.close()
