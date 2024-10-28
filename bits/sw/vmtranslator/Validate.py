import re

# Define the valid command patterns
valid_commands = [
    r"\s*push constant \d+\s*",        # Matches 'push constant XXX' where XXX is a number
    r"\s*label [\w.]+\s*",             # Matches 'label XXX' where XXX is any word or contains a dot
    r"\s*if-goto [\w.]+\s*",           # Matches 'if-goto XXX' where XXX is any word or contains a dot
    r"\s*goto [\w.]+\s*",              # Matches 'goto XXX' where XXX is any word or contains a dot
    r"\s*push temp [0-7]\s*",          # Matches 'push temp 0 to 7'
    r"\s*pop temp [0-7]\s*",           # Matches 'pop temp 0 to 7'
    r"\s*push argument \d+\s*",        # Matches 'push argument XXX' where XXX is a number
    r"push local \d+",           # Matches 'push local X' where X is a number
    r"pop local \d+",            # Matches 'pop local X' where X is a number
    r"\s*add\s*",                      # Matches 'add'
    r"\s*sub\s*",                      # Matches 'sub'
    r"\s*neg\s*",                      # Matches 'neg'
    r"\s*not\s*",                      # Matches 'not'
    r"\s*and\s*",                      # Matches 'and'
    r"\s*or\s*",                       # Matches 'or'
    r"\s*eq\s*",                       # Matches 'eq'
    r"\s*gt\s*",                       # Matches 'gt'
    r"\s*lt\s*",                       # Matches 'lt'
    r"\s*function [\w.]+ \d+\s*",      # Matches 'function STRING XXX' where STRING can contain letters, digits, underscores, or dots, and XXX is a number
    r"\s*call [\w.]+ \d+\s*",          # Matches 'call STRING XXX' where STRING can contain letters, digits, underscores, or dots, and XXX is a number
    r"\s*return\s*",                   # Matches 'return'
]

def strip_comments(line):
    """Strip comments starting with '//' from the line."""
    return line.split('//')[0].strip()

def is_valid_command(command):
    """Check if the command matches one of the valid patterns or is an empty line."""
    if command.strip() == "":  # Accept empty lines
        return True
    for pattern in valid_commands:
        if re.fullmatch(pattern, command):
            return True
    return False

def validate_file(file_path):
    """Validate the file to ensure all commands are valid, ignoring comments."""
    return_count = 0
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            # Strip comments before validating the command
            stripped_line = strip_comments(line)
            if not is_valid_command(stripped_line):
                return False, f"Invalid command at line {line_number}: {line.strip()}"

            if stripped_line == "return":
                return_count += 1
                if return_count > 1:
                    return False, f"Multiple 'return' commands found; only one is allowed (line {line_number})."

    return True, ""
