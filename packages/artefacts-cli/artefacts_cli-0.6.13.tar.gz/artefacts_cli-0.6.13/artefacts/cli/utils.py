import subprocess
import sys


def run_and_save_logs(
    args, output_path, shell=False, executable=None, env=None, cwd=None
):
    """
    Run a command and save stdout and stderr to a file in output_path

    Note: explicitly list used named params instead of using **kwargs to avoid typing issue: https://github.com/microsoft/pyright/issues/455#issuecomment-780076232
    """
    output_file = open(output_path, "wb")
    proc = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,  # Capture stdout
        stderr=subprocess.PIPE,  # Capture stderr
        shell=shell,
        executable=executable,
        env=env,
        cwd=cwd,
    )
    # write test-process stdout and stderr into file and stdout
    if proc.stdout:
        for line in proc.stdout:
            decoded_line = line.decode()
            sys.stdout.write(decoded_line)
            output_file.write(line)
    if proc.stderr:
        for line in proc.stderr:
            decoded_line = line.decode()
            sys.stderr.write(decoded_line)
            output_file.write(line)
    proc.wait()
    return proc.returncode
