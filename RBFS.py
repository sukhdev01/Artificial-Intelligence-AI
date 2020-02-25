#!/usr/bin/env python
# coding: utf-8

# In[13]:


'''Note: please read comments for more clarification.'''


#class for performing actoins and simplicity of code
class Puzzle:
    goal=[1,2,3,4,5,6,7,8,0]
    heuristic=None
    f_value=None
    needs_hueristic=False
    num_of_instances=0
    #for generating parent, action, path_cost initially
    def __init__(self,state,parent,action,path_cost,needs_hueristic=False):
        self.parent=parent
        self.state=state
        self.action=action
        if parent:
            self.path_cost = parent.path_cost + path_cost
        else:
            self.path_cost = path_cost
        #if heuristic is needed then inly will calculate and update value
        if needs_hueristic:
            self.needs_hueristic=True
            self.find_heuristic_value()
            self.f_value=self.heuristic+self.path_cost
        Puzzle.num_of_instances+=1


    def find_actions(self,i,j): #when we find blank i.e zero and take actions top,down,left, right
        actions = ['top', 'down', 'left', 'right']
        #for avoiding out of bound case, remove from actions
        if i == 0:   
            actions.remove('top')
        elif i == 2:  
            actions.remove('down')
        if j == 0:
            actions.remove('left')
        elif j == 2:
            actions.remove('right')
        return actions
    
    def __str__(self):
        return str(self.state[0:3])+'\n'+str(self.state[3:6])+'\n'+str(self.state[6:9])

    def find_heuristic_value(self):#for calculating huristic value using man-hattan diatance
        self.heuristic=0
        for num in range(1,9):
            distance=abs(self.state.index(num) - self.goal.index(num))
            i=int(distance/3)
            j=int(distance%3)
            self.heuristic=self.heuristic+i+j 

    def goal_test(self):    
        if self.state == self.goal:     # for verifying with goal
            return True
        return False


    def generate_child(self): 
        children=[]
        x = self.state.index(0) #getting index and converting into 2D array of 3x3
        i = int(x / 3)
        j = int(x % 3)
        actions=self.find_actions(i,j) #getting all actions

        for action in actions:
            new_state = self.state.copy() #copy,for avoiding call by reference in array pointer
            if action is 'top':
                new_state[x], new_state[x-3] = new_state[x-3], new_state[x]
            elif action is 'down':
                new_state[x], new_state[x+3] = new_state[x+3], new_state[x]
            elif action is 'left':
                new_state[x], new_state[x-1] = new_state[x-1], new_state[x]
            elif action is 'right':
                new_state[x], new_state[x+1] = new_state[x+1], new_state[x]
            children.append(Puzzle(new_state,self,action,1,self.needs_hueristic))
        return children

    def solution(self): #for finding solution steps as top, down, left, right
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        return solution


# In[14]:


#code for Recursive Best First Search as RBFS
def recursiveBFS(initial_state):
    node=RBFS(Puzzle(state=initial_state, parent=None, action=None, path_cost=0, needs_hueristic=True), f_limit=maxsize)
    node=node[0]
    return node.solution()


#return both solution or failure  and new f_cost_limit
def RBFS(node,f_limit):
    
    successors=[]
    if node.goal_test():
        return node,None
    
    children=node.generate_child() #generating all the valid children node from parent node
    if not len(children):
        return None, maxsize
    
    count=-1
    for child in children:
        count+=1
        successors.append((child.f_value, count,child))
        
    while len(successors):
        successors.sort()
        best=successors[0][2] #for finding best node with f_value
        if best.f_value > f_limit:
            return None, best.f_value #in case of failure
        alternative=successors[1][0] #for finding 2nd minimum best node with f_value
        
        result,best.f_value=RBFS(best,min(f_limit,alternative))
        
        successors[0]=(best.f_value,successors[0][1],best)
        if result!=None:
            break
            
    return result,None


# In[15]:


from sys import maxsize
if __name__=="__main__":
    state=[1,2,3,5,6,7,8,0,4]
    RBFS = recursiveBFS(state)
    
    print("\nNote:- \nleft action :=> for going to new state by replacing zero with left number of zero.")
    print("\nright action :=> for going to new state by replacing zero with right number of zero.")
    print("\ntop action :=> for going to new state by replacing zero with top number of zero.")
    print("\ndown action :=> for going to new state by replacing zero with down number of zero.\n\n ")
    
    print("strated execution............ \n\nstarting state is: \n",[[1,2,3],[5,6,0],[7,8,4]])
    print("\nActions, that are taken, are following.......\n\n", RBFS)







