#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''Note: please read comments for more clarification.'''


#finding blank's location in state
def findBlankPosition(array):
    for i in range(3):
        for j in range(3):
            if array[i][j] == 0:
                return i,j


#finding man-hattan distance 
def heuristicFun(arr,heuristic_value=0): #NOTE: goal must be numpy array for using np.where(list==element)
    Goal=np.array([[0,1,2],[3,4,5],[6,7,8]])
    for i in range(3):
        for j in range(3):
            x,y=np.where(Goal==arr[i][j])
            heuristic_value += abs(x[0]-i)+abs(y[0]-j)
    return heuristic_value
   
    
# creating child node for particular action
def childNode(problem,node,array_loc):
    i,j = array_loc
    if i<0 or j<0 or j>2 or i>2: #for avoiding out of bound case
        return None
    else:
        iB,jB = findBlankPosition(node.state)
        node.state[iB][jB] = node.state[i][j]
        node.state[i][j] = 0
        return node
    

#class for Node for containing g,f,h values and state list
class Node:
    def __init__(self):#need in f=g+h function
        self.g=0
        self.h=0
        self.f=0
        self.state=[[0,0,0],[0,0,0],[0,0,0]]


#class for normal functions
class puzzle:
    
    def __init__(self):  
        self.node=Node()
        self.goal=[[0,1,2],[3,4,5],[6,7,8]]
        
    def ACTIONS(self,arr): #find 0 and take actions as top,down,left,right
        self.node=arr
        i,j=findBlankPosition(self.node)
        return [[i-1,j],[i+1,j],[i,j-1],[i,j+1]] #sending all 4 case, boundry will be checked there itself
         
    def GOAL_TEST(self,node):
        self.node=node
        if self.node.state == self.goal: # for verifying with goal
            return True
        else:
            return False
        
    def INITIAL_STATE(self):
#         self.node.state=RandomArray()
        self.node.state =[[6,0,2],[4,7,3],[1,5,8]]
        self.node.h = heuristicFun(self.node.state)
        self.node.g = 0
        self.node.f = self.node.g + self.node.h  #using f(n) = g(n) + h(n)
        return self.node 


# In[2]:


#here, problem is object of puzzle class
def A_Star(problem,closedList,openList):

    if len(openList)==0:# when openList is empty
        print("\n\n\nFailed to find solution")
        return -1
    
    node=openList[0]
    for succ in openList: #finding mimnimun f_value node in openList
        if node.f > succ.f:
            node=succ
            
    openList.remove(openList[openList.index(node)]) # removing node from openList that has min. f value 
    closedList.append(node)#adding popped node to closedList
    print("\ncurrent node ",node.state)
    
    if problem.GOAL_TEST(node):#checking, whether node is goal or not ?
        print("\n\nWow! finally you have found the solution.\n\nThat is:\n",node.state)
        return node.f #SOLUTION found returning f_value 

    for action_loc in problem.ACTIONS(node.state):
        child=deepcopy(childNode(problem,node,action_loc))#deepcopy,for avoiding call by reference in array pointer
        if child:#checking, child is not None ?
            
            if child in openList:#for updating g of child ==>> child.g = min(child.g , node.g + 1)
                openList[openList.index(child)].g = min(child.g , node.g + 1) 
            elif (child not in closedList): # obviously, not in openList due to if condition
                child.g = node.g + 1
                child.h = heuristicFun(child.state)
                child.f = child.g + child.h   #using f(n) = g(n) + h(n)
                openList.append(child) #adding to openList after calculating f,g,h values
                
#             print("\nchild added to openSet ",child.state)
    return A_Star(problem,closedList,openList)
    
        


# In[3]:


#creating starting board 8-puzzle 
'''NOTE: But it can't be used due to unsolvable case might generate.'''
def RandomArray():
    arr=np.zeros([3,3],dtype=int)
    for i in range(3):    #generate random 2D array of size 3x3 with one number repeated (form 1 to 8)
        for j in range(3):
            k=0;x=np.random.randint(1,9)
            while(x in arr and k<100):
                x=np.random.randint(1,9);k+=1
            arr[i][j]=x
    
    dic={}    #for finding repeated number from that 2D array (It can't be done by predefined functions)
    for i in range(3): #creating dictionary for  keeping count 
        for j in range(3):
            x=arr[i][j]
            dic[x]=0 if x not in dic else 1
    for key, value in dic.items():  # finding that number
        if value==1:
            num=key
            break
    x,y=np.where(arr==num) #finding index of the number in the array 
    print(arr)
    print(x,y)
    arr[x[0]][x[1]]=0   # replacing that number with zero
    print("\nstarting Array:\n",arr)
    return [arr]     # finally, we got a random array with 0 to 8 number in 3x3 matrix


# In[4]:


#main function for starting execution 
import numpy as np
from copy import deepcopy
if __name__=="__main__":
 
    print("\nNOTE:- You might get 'maximum recursion depth exceeded' due to unsolvable 8-puzzle problem.")
    print("\nstarted execution............")
    problem = puzzle() #object for simplicity of code
    closedSet=[]  #visited states ,adding visited array for reducing space complexcity
        
    openSet=[problem.INITIAL_STATE()]#adding starting state in openList
    
    print("\nTotal f_value : ",A_Star(problem,closedSet,openSet))

