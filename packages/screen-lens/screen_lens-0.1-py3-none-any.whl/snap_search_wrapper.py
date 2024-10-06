import subprocess
import os

def run_shell_script():
    script_path = os.path.join(os.path.dirname(__file__), 'snap_search.sh')
    subprocess.call(['bash', script_path])
