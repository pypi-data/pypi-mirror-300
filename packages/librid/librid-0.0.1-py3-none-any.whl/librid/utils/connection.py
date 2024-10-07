from dotenv import load_dotenv
from os import getenv

from scriptforge import ScriptForge

load_dotenv()

def connect_liboffice():
    try:
        ScriptForge(
            hostname=getenv('LIBRE_HOST'),
            port=int(getenv('LIBRE_PORT')))
        print("LibreOffice connection is working.")
    except Exception as e:
        print(f"Error: Can not connect to LibreOffice service.\n\n{e}")
        raise

# TEST
if __name__ == "__main__":
    connect_liboffice()