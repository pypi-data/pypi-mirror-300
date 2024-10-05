import os

# Define the path to the file containing the verbs using absolute path
current_dir = os.path.dirname(os.path.abspath(__file__))  # Get current directory of this file
verb_file_path = os.path.join(current_dir, 'verbs.txt')   # Join directory with file name

# Function to load verbs from the file
def load_verbs():
    with open(verb_file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

# Fetch all verbs when imported
verbs = load_verbs()
