import tempfile
from pathlib import Path

def create_test_file(content: str) -> Path:
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    path = Path(tmp_file.name)
    tmp_file.write(content.encode("utf-8"))
    tmp_file.close()
    return path
