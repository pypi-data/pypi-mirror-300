import subprocess
import sys

def run_script(script_name):
    try:
        result = subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("""
How to run: python maincode.py -1 | -2 | -3

-1: Identify water bridges in RNA–protein complexes.
    - For this, ensure that the output files from HBPLUS are placed in the current directory.

-2: Analyze the output of option -1 and identify the topology of the water bridges, such as A1-w-N1, A1-w-N2, and others.

-3: Provide nomenclature for the A1-w-N1 topology only.
""")

        sys.exit(1)

    arg = sys.argv[1]

    if arg == '-1':
        run_script('1_Identification of water bridges.py')
    elif arg == '-2':
        run_script('2_Topological classification of water bridges.py')
    elif arg == '-3':
        run_script('3_Nomenclature of A1-w-N1 waterbridges.py')
    else:
        print("Please enter a valid argument; -1, -2, or -3.")
        sys.exit(1)
