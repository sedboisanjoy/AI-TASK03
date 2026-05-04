# ---------------------------------------------------------
# Q2: Blocks World Problem - Absolute Simplest Approach
# Uses Breadth-First Search (BFS) to find the shortest path 
# to stack the blocks correctly.
# ---------------------------------------------------------
from collections import deque

# State representation: A tuple of 3 stacks (tuples). 
# Top of the stack is the right-most item.
start_state = (('A', 'B'), ('C',), ())
goal_state = (('C', 'B', 'A'), (), ())

def get_possible_moves(state):
    moves = []
    # Try picking the top block from each stack...
    for i in range(len(state)):
        if not state[i]: continue  # Stack is empty
        
        block = state[i][-1]  # Top block
        
        # ...and place it on every other stack
        for j in range(len(state)):
            if i == j: continue
        
            new_state = list(state)
            new_state[i] = state[i][:-1]       # Remove from old stack
            new_state[j] = state[j] + (block,) # Add to new stack
            moves.append(tuple(new_state))
            
    return moves

def solve(start, goal):
    # Queue stores: (current_board_state, path_taken_so_far)
    queue = deque([(start, [])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        if current == goal:
            # Return full path including current state
            return path + [current]
            
        for next_state in get_possible_moves(current):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [current]))
                
    return None

if __name__ == "__main__":
    print("Solving Blocks World...")
    print("="*60)
    
    solution = solve(start_state, goal_state)
    
    if solution:
        # Calculate moves correctly
        total_states = len(solution)
        number_of_moves = total_states - 1  # Because step 0 is start
        
        print(f"\n✅ SOLUTION FOUND!")
        print(f"{'='*60}")
        print(f"Total states in path: {total_states}")
        print(f"Total moves required: {number_of_moves}")
        print(f"{'='*60}\n")
        
        # Print each step
        for step, state in enumerate(solution):
            # Show what move number this is
            if step == 0:
                print(f"START (Move 0): {state}")
            else:
                print(f"After Move {step}: {state}")
        
        print(f"\n{'='*60}")
        print(f"SUMMARY: Reached goal in {number_of_moves} move(s)!")
        print(f"{'='*60}")
        
        # Print visual representation
        print("\n📊 VISUAL REPRESENTATION:\n")
        for step, state in enumerate(solution):
            print(f"Step {step}:")
            stacks = [list(stack) for stack in state]
            for i, stack in enumerate(stacks):
                if stack:
                    print(f"  Stack {i}: {stack}")
                else:
                    print(f"  Stack {i}: empty")
            print()
            
    else:
        print("\n❌ No solution found!")
