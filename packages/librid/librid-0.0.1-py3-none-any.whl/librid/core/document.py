from os import remove
from shutil import copy, move
from scriptforge import CreateScriptService

from core.state import opened_docs as od
from core.config import base_path, input_dir, output_dir


def create_doc(filename, doc_type):
    try:
        ui = CreateScriptService("UI") 
        doc = ui.CreateDocument(
            documenttype=doc_type,
            hidden=True)
            
        od[filename] = doc

    except Exception as e:
        print(f"Error: Can not create document: '{filename}'.\n\n{e}")
        raise

def open_doc(filename):
    try:
        ui = CreateScriptService("UI")
        doc = ui.OpenDocument(
            filename=f"{input_dir}{filename}",
            hidden=True)

        od[filename] = doc

    except Exception as e:
        print(f"Error: Can not open document: '{filename}'.\n\n{e}")
        raise

def save_doc(filename):
    try:
        od[filename].Save()
    except Exception as e:
        print(f"Error: Can not save document: '{filename}'.\n\n{e}")
        raise

def save_as_doc(old_filename, new_filename):
    try:
        od[old_filename].SaveAs(
            output_dir + new_filename,
            overwrite=True)
    except Exception as e:
        print(f"Error: Can not save document: '{new_filename}'.\n\n{e}")
        raise

def save_copy_as_doc(source, target):
    try:
        od[source].SaveCopyAs(
            output_dir + target,
            overwrite=True)
    except Exception as e:
        print(f"Error: Can not save-copy document: '{source}' -> '{target}'.\n\n{e}")
        raise

def close_doc(filename):
    try:
        od[filename].CloseDocument(saveask=False)
        del od[filename]
    except Exception as e:
        print(f"Error: Can not close document: '{filename}'.\n\n{e}")
        raise

def copy_doc(source, target):
    try:    
        copy(base_path + source, base_path + target)
    except Exception as e:
        print(f"Error: Can not copy document: '{source}'.\n\n{e}")
        raise

def move_doc(source, target):
    try:
        move(base_path + source, base_path + target)
    except Exception as e:
        print(f"Error: Can not move document: '{source}'.\n\n{e}")
        raise

def rm_doc(filepath):
    try:
        remove(base_path + filepath)
    except Exception as e:
        print(f"Error: Can not remove document: '{filepath}'.\n\n{e}")
        raise

# TEST
if __name__ == "__main__":
    ...