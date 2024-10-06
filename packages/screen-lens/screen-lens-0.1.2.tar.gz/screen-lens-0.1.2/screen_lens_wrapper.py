import subprocess
import pkg_resources
import os

def run_shell_script():
    script_path = pkg_resources.resource_filename(__name__, 'bin/screen_lens.sh')
    subprocess.call(['bash', script_path])
