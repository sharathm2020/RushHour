from rushhour import State, util, DEFAULT_STATE
from agent import Agent


#Main Function that calls all search methods, BFS, DFS or a_star(Default: BFS)
def main():    
    cmd = util.get_arg(1) or "a_star"
    stateString = util.get_arg(2) or DEFAULT_STATE
    state = State(stateString)
    agent = Agent(state)
    if cmd == "random":
        visited_nodes = agent.random_walk(state, 8)
        util.pprint(visited_nodes)
    elif cmd == "bfs":
        agent.bfs(state)
    elif cmd == "dfs":
        agent.dfs(state)
    elif cmd == "a_star":
        agent.a_star(state, temp_heuristic)

#Heuristic that calculates the number of cars blocking the 'x' cars in both the x and y plane
def temp_heuristic(state):
    exit_y = state.EXIT_Y
    num_of_blockage = 0
    x_pos = get_x_max_pos(state, exit_y)
    #Check each x position in the range of the max xpos and the state_size
    for x in range(x_pos + 1, state.SIZE):
        #Checks each x coordinate for row y for a car blocking the path
        if state.get(x, exit_y) not in (' ', 'x'):
            num_of_blockage += 1
            
            is_column_filled = True
            #Check to see if each column is filled with non-empty spaces
            for y in range(state.SIZE):
                if state.get(x, y) == ' ':
                    is_column_filled = False
                    break
            #if the column contains no empty spaces, assume multiple moves must be made to unblock that path
            if is_column_filled:
                num_of_blockage += 2
    
    return num_of_blockage


#Original basic heuristic - solved this board: 'abb   |a  c  |axxc  |   c e|dff  e|d ggge' in 156 iterations and only accounted for cars in the x position of each column
""" def temp_heuristic(state):
    exit_y = state.EXIT_Y
    num_of_blockage = 0
    x_pos = get_x_max_pos(state, exit_y)
    for x in range(x_pos + 1, state.SIZE):
        if state.get(x, exit_y) not in (' ', 'x'):
            num_of_blockage += 1
    return num_of_blockage """

#Function to calculate the right most x for each row
def get_x_max_pos(state, exit_y):
    x_pos = -1
    for x in range(state.SIZE):
        if state.get(x, exit_y) == 'x':
            x_pos = x
    return x_pos


if __name__ == '__main__':
    main()