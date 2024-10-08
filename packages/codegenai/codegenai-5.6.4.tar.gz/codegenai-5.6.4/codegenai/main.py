from codegenai.aids import *
from codegenai.cn import *
from codegenai.special import *
import os
import shutil
import subprocess


available = {'-1  ' : "AIDS & CN (Folder)",
             'AIDS' : "",
             '0   ' : "All",
             '1   ' : "Breadth First Search",
             '2   ' : "Depth First Search",
             '3   ' : "Uniform Cost Search",
             '4   ' : "Depth Limited Search", 
             '5   ' : "Iterative Deepening Search(IDDFS)", 
             '6   ' : "A*", 
             '7   ' : "Iterative Deepening A*", 
             '8   ' : "Simplified Memory Bounded A*",
             '9   ' : "Genetic Algorithm", 
             '10  ' : "Simulated Annealing",
             '11  ' : "Solving Sudoku(Simulated Annealing)",
             '12  ' : "Alpha-Beta Pruning",
             '13  ' : "Map Coloring(Constraint Satisfaction Problem)",
             '14  ' : "House Allocation(Constraint Satisfaction Problem)",
             '    ' : "",
             'CN  ' : "",
             '15  ' : "Chat Application",
             '16  ' : "File Transfer",
             '17  ' : "RMI(Remote Method Invocation)",
             '18  ' : "Wired Network TCL Script",
             '19  ' : "Wired Network AWK File",
             '20  ' : "Wireless Network TCL Script",
             '21  ' : "Wireless Network AWK File"}

file_path = { 'code'        : 'All.ipynb',
              'bfs'         : 'BFS.ipynb',
              'dfs'         : 'DFS.ipynb',
              'ucs'         : 'UCS.ipynb',
              'dls'         : 'DLS.ipynb',
              'ids'         : 'IDS.ipynb',
              'astar'       : 'Astar.ipynb',
              'idastar'     : 'IDAstar.ipynb',
              'smastar'     : 'SMAstar.ipynb',
              'genetic'     : 'Genetic.ipynb',
              'sa'          : 'Simulated Annealing.ipynb',
              'sudoku'      : 'Sudoku.ipynb',
              'alphabeta'   : 'AlphaBetaPruning.ipynb',
              'csp_map'     : 'CSP Map Coloring.ipynb',
              'csp_house'   : 'CSP House Allocation.ipynb'}

def display(name = "", open = False):
    try:
        name = str(name)
        if   name in ['1']      :   print(bfs);         get_file(['bfs'], open)
        elif name in ['2']      :   print(dfs);         get_file(['dfs'], open)
        elif name in ['3']      :   print(ucs);         get_file(['ucs'], open)
        elif name in ['4']      :   print(dls);         get_file(['dls'], open)
        elif name in ['5']      :   print(ids);         get_file(['ids'], open)
        elif name in ['6']      :   print(astar);       get_file(['astar'], open)
        elif name in ['7']      :   print(idastar);     get_file(['idastar'], open)
        elif name in ['8']      :   print(smastar);     get_file(['smastar'], open)
        elif name in ['9']      :   print(genetic);     get_file(['genetic'], open)
        elif name in ['10']     :   print(sa);          get_file(['sa'], open)
        elif name in ['11']     :   print(sudoku);      get_file(['sudoku'], open)
        elif name in ['12']     :   print(alphabeta);   get_file(['alphabeta'], open)
        elif name in ['13']     :   print(csp_map);     get_file(['csp_map'], open)
        elif name in ['14']     :   print(csp_house);   get_file(['csp_house'], open)
        elif name in ['15']     :   print(chat)
        elif name in ['16']     :   print(file_transfer)
        elif name in ['17']     :   print(rmi)
        elif name in ['18']     :   print(wired_tcl)
        elif name in ['19']     :   print(wired_awk)
        elif name in ['20']     :   print(wireless_tcl)
        elif name in ['21']     :   print(wireless_awk)
        elif name in ['','0']   :   print(code);        get_file(['code'], open)
        elif name in ['-1']     :   get_folder(loc = True)
        else:
            for k, v in available.items():
                sep = " : " if v else ""
                print(k,v,sep = sep)
    except:
        pass

def get_file(files = [], open = False):
    if files[0] == "*":
        files = file_path.keys()
    for file in files:
        src = os.path.realpath(__file__)[:-7]+"\\data\\"+file_path[file]
        src = src.replace("\\\\","\\")
        try:
            dest = os.getcwd()+"\\ᵗᑋᵃᐢᵏ ᵞᵒᵘ "+file_path[file]
            shutil.copy(src, dest)
            if open:
                subprocess.Popen(f"jupyter notebook {dest}")
        except:
            try:
                dest = os.path.expanduser('~')+"\\Downloads\\ᵗᑋᵃᐢᵏ ᵞᵒᵘ "+file_path[file]
                shutil.copy(src, dest)
            except:
                pass

def get_folder(loc = False, i = 0, j = 0):
    src = os.path.realpath(__file__)[:-7]+"\\data\\AIDS  &  CN"
    src = src.replace("\\\\","\\")
    try:
        dest = os.path.expanduser('~')+"\\Downloads\\ᵗᑋᵃᐢᵏ ᵞᵒᵘ AIDS  &  CN"+(f" ({i})" if i != 0 else "")
        shutil.copytree(src, dest, symlinks=False,
                        copy_function = shutil.copy2,
                        ignore=shutil.ignore_patterns('.ipynb_checkpoints', '__init__.py', '__pycache__'),
                        ignore_dangling_symlinks=False, 
                        dirs_exist_ok=False)
        if loc:
            print("Path:",dest.replace("\\\\","\\"))
    except FileExistsError:
        get_folder(loc, i + 1, j)
    except:
        try:
            dest = os.getcwd()+"\\ᵗᑋᵃᐢᵏ ᵞᵒᵘ AIDS  &  CN"+(f" ({j})" if j != 0 else "")
            shutil.copytree(src, dest, symlinks=False,
                            copy_function = shutil.copy2,
                            ignore=shutil.ignore_patterns('.ipynb_checkpoints', '__init__.py', '__pycache__'),
                            ignore_dangling_symlinks=False, 
                            dirs_exist_ok=False)
            if loc:
                print("Path:",dest.replace("\\\\","\\"))
        except FileExistsError:
            get_folder(loc, i, j + 1)
        except Exception as e:
            print(e)
                    
def ghost(key = None, what = ""):
    if key and isinstance(key,str) and key == pwd:
        available = {'101  or  sudoku   ' : "Solving Sudoku(Loading Bar)"}
        try:
            if isinstance(what,str):
                what =  what.lower()
            if what in ["sudoku", 101]   :   print(sudoku_lb)
            else:
                print("Invalid Value! Refer Below Table")
                for k, v in available.items():
                    print(k,v,sep = " : ")
        except:
            pass