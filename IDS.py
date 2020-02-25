#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''Note: please read comments for more clarification.'''


# Deepening Limited Search as DLS
def DLS(problem,limit):
    return recDLS(problem.INITIAL_STATE(),problem,limit)

# Iterative Deepening Search as IDS
def IDS(problem):
    for depth in range(1,50):# instead of infinite, taking 50
        result=DLS(problem,depth)
        if result == 1:
            return "Result found"
        elif result == -1:
            return "Failed to find Result\n"
        else:
            print("\n\ncut_off_occurred @ depth =",depth)


# In[2]:


#finding blank's location
def findBlankPosition(array):
    for i in range(3):
        for j in range(3):
            if array[i][j]==0:
                return i,j
            

# creating child node for particular action
def childNode(problem,node,array_loc):
    i,j=array_loc
    if i<0 or j<0 or j>2 or i>2:#for avoiding out of bound case
        return None
    else:
        iB,jB,= findBlankPosition(node)
        node[iB][jB]=node[i][j]; node[i][j]=0
        return node


# Recursive DLS as recDLS
'''NOTE: using direct 2D-array (as node) instead of node.state (in IDS)'''
def recDLS(node,problem,limit,cut_off=0,failure=-1):
    if problem.GOAL_TEST(node):
        print("\n\nWow! finally, You have done your Job :)\n\nYour solution is:\n ",node)
        return 1 #solution(node) 
    elif limit == 0:
        return cut_off
    else:
        cut_off_occurred = False
        for action_loc in problem.ACTIONS(node): 
            child = deepcopy(childNode(problem,node,action_loc))
#             print("\nchild_Node",child)
            if child:# to avoid node!=None, i.e. childNode's response as None
                result = recDLS(child,problem,limit-1)
                if result == cut_off:
                    cut_off_occurred = True
                elif result != failure: #result found 
                    return result
            
        if cut_off_occurred:#no solution found till this limit
            return cut_off
        else: #no solution found 
            print("\n:( very bad, Failure")
            return failure


# In[3]:


#class for problem object
class n_puzzle:# n=8
    
    def __init__(self):
        self.node=[[0,0,0],[0,0,0],[0,0,0]]
#         self.goal=[[1,2,3],[4,5,6],[7,8,0]]
        self.goal=[[0,1,2],[3,4,5],[6,7,8]]
        
    def ACTIONS(self,arr): #find 0 and take actions
        self.node=arr
        i,j=findBlankPosition(self.node)
        return [[i,j-1],[i,j+1],[i-1,j],[i+1,j]] #sending all four, boundry will check there only 
         
    def GOAL_TEST(self,arr):
        self.node=arr
        if self.node == self.goal:
            return True
        else:
            return False
        
    def INITIAL_STATE(self):
        array= [ [[0,2,1],[3,4,5],[6,7,8]], [[1,2,3],[4,5,6],[0,7,8]], [[8,0,2],[4,3,1],[7,6,5]], [[1,2,0],[3,4,5],[6,7,8]], [[8,1,2],[4,3,5],[7,6,0]], [[5,6,7],[8,3,4],[1,2,0]] ] 
#         array[4] result after 11 iterations (time 0:0:07.35, 1-11.6)
#         array[5] result after 15 iterations (time 0:4:57.39 ,1-15.4)
        #self.node=array[np.random.randint(0,6)]#for generating random index between 0 to 5 (but it changes every depth)
        self.node= array[4]
        print("\nStarting state is:",self.node)
        return self.node


# In[4]:


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


# In[5]:


import numpy as np
from copy import deepcopy
if __name__=="__main__":
    
    print("\nstarted executin............")
    problem = n_puzzle() #object
    print("\nIDS result: ",IDS(problem))
#     RandomArray()






