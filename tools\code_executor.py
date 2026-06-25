import subprocess
import tempfile
import os
from typing import Optional


def execute_python(code: str, timeout: int = 30) -> dict:
    """
    Execute Python code in a sandboxed subprocess.
    Returns stdout, stderr, and return code.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        tmp_path = f.name

    try:
        result = subprocess.run(
            ["python3", tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "success": result.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Execution timed out", "returncode": -1, "success": False}
    finally:
        os.unlink(tmp_path)
