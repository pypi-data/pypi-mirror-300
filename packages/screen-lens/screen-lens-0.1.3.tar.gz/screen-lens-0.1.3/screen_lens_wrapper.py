import subprocess
import pkg_resources
import os

def run_shell_script():
    script_path = pkg_resources.resource_filename('screen_lens', 'bin/screen_lens.sh')
    if not os.path.exists(script_path):
        print('Error: script not found at {script_path}')
        exit(1)
    subprocess.call([script_path])
