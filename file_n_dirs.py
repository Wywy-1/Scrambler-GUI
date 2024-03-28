from sys import exit
from pathlib import Path
from dates import get_time

def mk_dir(path: str) -> str:
    """Makes a directory when given the desired full path (i.e., with
    the desired directory's name), returns the path of the new directory:
    - Handles FilesExistsError by printing to terminal and continuing,
    - Handles FileNotFoundError by finding the first existing directory in
    the path it is passed and making the desired directory there (if it
    already exists then prints to terminal and continues);
    - Handles all other errors by printing to terminal and exiting."""

    try:
        path.mkdir()

    except FileExistsError:
        '''If directory exists, creates a new directory inside of the existing directory,
        names it after the date, and sets this as the directory to create the exam
        and answer key.'''
        #path = Path(str(path)+"_"+get_time())      # Makes a new sibling directory with the old name AND the date
        path = path / get_time()                    # Makes a new directory names after the date with existing dir the parent
        path.mkdir()

    except FileNotFoundError:       # Exception is thrown when path specifices directories that don't exist
        print("Sorry, this path mentions folders that don't exist:, {}\n".format(path))
        new_dir = path.name         # Get the name of the desired directory

        path = find_existing_dir_in_path(1,path)    # path now reflects only existing directories
        print("So, I will just try and put {} here:\n{}\n".format(new_dir,path.name))
        path2 = path / new_dir      # Append desired directory name to path
        path = path2    #TODO is this redundant? could we just say, path = path / new_dir
        
        try:
            path.mkdir()           # Makes desired directory in last existing directory of initial 'path' variable

        except FileExistsError:
            '''If directory exists, creates a new directory inside of the existing directory,
            names it after the date, and sets this as the directory to create the exam
            and answer key.'''
            #path = Path(str(path)+"_"+get_time())      # Makes a new sibling directory with the old name AND the date
            path = path / get_time()                    # Makes a new directory names after the date with existing dir the parent
            path.mkdir()   

        except Exception as err:
            print("Unexpected error,\n\n{}, {}\n".format(err,type(err)))
            exit()

    except Exception as err:
        print("Unexpected error,\n\n{}, {}\n".format(err,type(err)))
        exit()
    
    return path
    
 
def find_existing_dir_in_path(count: int, path: str) -> str:
    """Searches through each parent in a path, returns the first
    parent that exists, and "." if no parent exists. 
    Input:   
        - int (initialize to '1')
        - str"""

    if path.is_dir():   # Ends when the path variable only has existing directories
        count = 16

    if count < 16:       # Ends when either; has looped 8 times, or finds an existing directory
        count += 1
        path = find_existing_dir_in_path(count,path.parent)

    return path


def rename_file(path: Path) -> Path:
    """Renames a file if there is already a file
    with that name in it's parent directory. Takes a path (with 
    file name) and returns a new path, the new name is 
    the old name plus the date and time, extension maintained
    at the end of the new name.
    - E.g., .../test.txt -> .../test, Mar-04,2024,13:53:21.txt"""

    if path.exists():
        parent = path.parent
        old_suff = path.suffix
        new_name = path.stem + ", " + get_time() + old_suff
        path = parent / new_name
    
    return path
