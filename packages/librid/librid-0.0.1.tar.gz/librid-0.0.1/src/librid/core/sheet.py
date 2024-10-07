from core.state import opened_docs as od


# TODO: optional target, if not added work with same file
def copy_sheet(
        source_file,
        source_sheet,
        target_file,
        target_sheet):
    try:
        od[target_file].CopySheet(
            od[source_file].Sheet(source_sheet),
            target_sheet)
    except Exception as e:
        print(
            f"Error: Can not copy {source_file}.{source_sheet} " + \
            f"to {target_file}.{target_sheet}.\n\n{e}")
        raise

def insert_sheet(filename, sheetname):
    try:
        od[filename].InsertSheet(sheetname)
    except Exception as e:
        print(f"Error: can not insert {sheetname} into {filename}.\n\n{e}")
        raise

# Q: what if I want to move sheet from another file?
def move_sheet(filename, source_sheet, target_sheet):
    try:
        od[filename].MoveSheet(source_sheet, target_sheet)
    except Exception as e:
        print(f"Error: can not move {source_sheet} to {target_sheet}.\n\n{e}")
        raise

def remove_sheet(filename, sheetname):
    try:
        od[filename].RemoveSheet(sheetname)
    except Exception as e:
        print(f"Error: can not remove {filename}.{sheetname}.\n\n{e}")
        raise

def rename_sheet(filename, old_sheetname, new_sheetname):
    try:
        od[filename].RenameSheet(old_sheetname, new_sheetname)
    except Exception as e:
        print(f"Error: can not rename {filename}.{old_sheetname} to {new_sheetname}.\n\n{e}")
        raise
