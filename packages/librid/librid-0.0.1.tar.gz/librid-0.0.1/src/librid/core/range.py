from core.state import opened_docs as od


# range example: 'SheetnameX.A1:B2'
def clear_all(filename, range):
    try:
        od[filename].ClearAll(range)
    except Exception as e:
        print(f"Error: can not clear range {range} in {filename}.\n\n{e}")
        raise

def clear_formats(filename, range):
    try:
        od[filename].ClearFormats(range)
    except Exception as e:
        print(f"Error: can not clear formats in {range} in document {filename}.\n\n{e}")
        raise

def clear_values(filename, range):
    try:
        od[filename].ClearValues(range)
    except Exception as e:
        print(f"Error: can not clear values in {range} in document {filename}.\n\n{e}")
        raise

# TODO: optional target, if not added work with same file
def copy_to_cell(
        source_file,
        source_range,
        target_file,
        target_range):
    try:
        od[target_file].CopyToCell(
            od[source_file].Range(source_range),
            target_range)
    except Exception as e:
        print(
            f"Error: Can not copy {source_file}.{source_range} " + \
            f"to {target_file}.{target_range}.\n\n{e}")
        raise

def get_formula(filename, range):
    try:
        return od[filename].GetFormula(range)
    except Exception as e:
        print(f"Error: can not get formula(s) from {range} in {filename}.\n\n{e}")
        raise

def get_value(filename, range):
    try:
        return od[filename].GetValue(range)
    except Exception as e:
        print(f"Error: can not get value(s) from {range} in {filename}\n\n{e}.")
        raise

# Q: what if I want to move range from another file?
def move_range(filename, source_range, target_range):
    try:
        od[filename].MoveRange(source_range, target_range)
    except Exception as e:
        print(f"Error: can not move {source_range} to {target_range}\n\n{e}.")
        raise

# TODO: implement all 3 possible usecase
def set_formula(filename, range, formulas: list):
    try:
        od[filename].SetFormula(range, formulas)
    except Exception as e:
        print(f"Error: can no set {formulas} in {range}\n\n{e}.")
        raise

# TODO: implement all 3 possible usecase
def set_value(filename, range, values: list):
    try:
        od[filename].SetValue(range, values)
    except Exception as e:
        print(f"Error: can no set {values} in {range}\n\n{e}.")
        raise
