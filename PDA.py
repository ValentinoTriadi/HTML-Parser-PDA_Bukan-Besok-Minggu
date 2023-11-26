# Let's write a Python script to convert the file into PlantUML code
# The format for every line will be: "{column 1} --> {column 4} : {column 2}, {column 3} / {column 5}"

file_path = 'PDA.txt'

def convert_to_plantuml(file_path):
    plantuml_code = "@startuml\n"
    
    with open(file_path, 'r') as file:
        for line in file:
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

# Convert the file and save the PlantUML code to a new file
plantuml_code = convert_to_plantuml(file_path)
output_file_path = 'PDA_converted_to_plantuml.txt'
with open(output_file_path, 'w') as output_file:
    output_file.write(plantuml_code)
