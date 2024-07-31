from collections import deque
import heapq
import random
import util

class Node:
    def __init__(self, state, parent = None, action = None, cost = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost


class Agent:
    def __init__(self, initial_state):
        self.initial_state = initial_state


    #Random Walk Method
    #Goal: Generate all the possible next states given the current state and a number of walks(n)

    def random_walk(self, state, n):
        ##initialize current node as well as visited node list
        current_node = Node(state)
        visitedNodes = [current_node.state]
        
        #iterate n-number of times, performing an action each time
        #generate a new random action and create a new state from that action
        #set the new current node to the current node with a new action,
        i = 0
        for i in range(n - 1):
            actions = current_node.state.actions()
            action = random.choice(actions)
            new_state = current_node.state.execute(action)
            current_node = Node(new_state, current_node, action)
            visitedNodes.append(new_state)

        return visitedNodes

    

    #Search Function containing BFS, DFS, and a_star search
    #Goal: Implement functionality for BFS, DFS and A_Star search that can properly process a given board and find the goal board as efficiently as possible

    def _search(self, state, type_of_search = 'bfs', heuristic = None):
        #Initialize new node with the passed state
        #BFS = Create Queue of unvisited nodes with starting node
        #DFS = Create Stack of unvisisted nodes with starting node
        #a_star = create new empty priority queue, add the current starting node into the not visited priority queue
        
        starting_node = Node(state)
        if type_of_search == 'bfs':
            notVisitedNodes = deque([starting_node])
        elif type_of_search == 'dfs':
            notVisitedNodes = [starting_node]
        else:
            notVisitedNodes = [(heuristic(state), starting_node)]

        visitedNodes = set()
        path_to_node = []
        iteration_count = 0
        
        #Created function for sorting by the first element of each tuple within the list, the first element being f(n)
        def get_sorted_key(node_tuples):
                return node_tuples[0]

        #Iterate over the queue/stack/priority queue of unvisited nodes
        #a_star = pop the smallest(smallest f(n)) element from the queue, 1 being the f(n) value
        #bfs = pop the element in the front of the queue
        #dfs - pop the element most recently added to the stack
        while notVisitedNodes:
            if type_of_search == 'a_star':
                notVisitedNodes.sort(key = get_sorted_key) #Sort by f(n)
                cur_node = notVisitedNodes.pop(0)[1]
            elif type_of_search == 'bfs':
                cur_node = notVisitedNodes.popleft()
            else:
                cur_node = notVisitedNodes.pop()
            
            
            #check to see if the current state is the goal state
            #if it is, add the state to the current node path list and reverse that list(Start -> Goal => Goal -> Start)
            #print the path to the node and the number of paths explored
            if cur_node.state.is_goal():
                iteration_count += 1
                path_to_node.append(cur_node.state)
                path_to_node.reverse()
                util.pprint(path_to_node)
                print(str(iteration_count))
                return cur_node
            
            #If the current state is not the goal state and is not found in the visitedNodes list, add the state to that list, and append it to the node path
            #create a new node and set it equal to the current nodes parent pointer
            if str(cur_node.state) not in visitedNodes:
                iteration_count += 1
                visitedNodes.add(str(cur_node.state))
                path_to_node.append(cur_node.state)
                new_Node = cur_node.parent


                #for each possible movement that can be made from the current node, create a new node with that action executed from the current state
                #check to see if the new state has already been visited, if not, add one to the new nodes cost, and create a new node object with the appropriate arguments
                #then append this new node to the current queue/stack/priority queue of unvisited nodes
                #for a_star, calculuate a new f(n) for the current state based on the heuristic, append to list of notVisitedNodes
                for action in cur_node.state.actions():
                    new_node_state = cur_node.state.execute(action)
                    if str(new_node_state) not in visitedNodes:
                        new_node_cost = cur_node.cost + 1
                        new_Node = Node(new_node_state, cur_node, action, new_node_cost)
                        
                        if type_of_search == 'a_star':
                            new_f_n = new_node_cost + (heuristic(new_node_state))
                            notVisitedNodes.append((new_f_n, new_Node))
                        else:
                            notVisitedNodes.append(new_Node)
    
            
    def bfs(self, state):
        return self._search(state, 'bfs')

    def dfs(self, state):
        return self._search(state, 'dfs')
    
    def a_star(self, state, heuristic):
        return self._search(state, 'a_star', heuristic)


