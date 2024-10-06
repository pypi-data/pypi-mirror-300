import subprocess
import importlib.resources as pkg_resources
import os

def run_shell_script():
    # Locate the shell script using importlib.resources
    with pkg_resources.path('screen_lens.bin', 'screen_lens.sh') as script_path:
        script_path = str(script_path)

        if not os.path.exists(script_path):
            print(f"Error: Script not found at {script_path}")
            exit(1)

        # Execute the shell script
        subprocess.call([script_path])