import re

def convert_to_plantuml(file_path):
    plantuml_code = "@startuml\n"
    
    with open(file_path, 'r') as file:
        for line in file.readlines()[2:]:
            parts = line.split()
            # Ensure the line has enough parts to avoid index errors
            if len(parts) >= 5:
                from_state = parts[0]
                input_symbol = parts[1]
                stack_symbol = parts[2]
                to_state = parts[3]
                push_symbol = parts[4]
                plantuml_code += f"\"{from_state}\" --> \"{to_state}\" : \"{input_symbol}, {stack_symbol} / {push_symbol}\"\n"

    plantuml_code += "@enduml"
    return plantuml_code

def find_unreachable_states(plantuml_code):
    # Extracting states and transitions from PlantUML code
    transitions = re.findall(r'"([^"]+)" --> "([^"]+)"', plantuml_code)
    states = set([transition[0] for transition in transitions] + [transition[1] for transition in transitions])

    # Building a graph of the state transitions
    graph = {state: [] for state in states}
    for start, end in transitions:
        graph[start].append(end)

    # Assuming the first state is the initial state
    initial_state = transitions[0][0] if transitions else None
    if not initial_state:
        return "No initial state found"

    # Traversing the graph to find accessible states
    accessible_states = set()
    def traverse(state):
        if state in accessible_states:
            return
        accessible_states.add(state)
        for next_state in graph[state]:
            traverse(next_state)

    traverse(initial_state)

    # Finding and returning unreachable states
    unreachable_states = states - accessible_states
    return unreachable_states if unreachable_states else "All states are reachable"
import re

def print_all_states(plantuml_code):
    # Extracting states and transitions from PlantUML code
    transitions = re.findall(r'"([^"]+)" --> "([^"]+)"', plantuml_code)
    states = set([transition[0] for transition in transitions] + [transition[1] for transition in transitions])

    # Printing all states in one line separated by space
    print(" ".join(states))




file_path = 'PDA.txt'
# Print all states
# Convert the file and save the PlantUML code to a new file
plantuml_code = convert_to_plantuml(file_path)
output_file_path = 'PDA_converted_to_plantuml.txt'
with open(output_file_path, 'w') as output_file:
    output_file.write(plantuml_code)


print_all_states(plantuml_code)
print("\n")
# Finding unreachable states
unreachable_states = find_unreachable_states(plantuml_code)
print("Unreachable States:", unreachable_states)