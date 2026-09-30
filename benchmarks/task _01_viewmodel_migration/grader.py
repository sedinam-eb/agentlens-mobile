import subprocess
import json
import os
from typing import Dict, Any

def run_evaluation(workspace_path: str) -> Dict[str, Any]:
    """Executes Gradle build & test suite and parses target task results."""
    try:
        result = subprocess.run(
            ["./gradlew", "test"],
            cwd=workspace_path,
            capture_output=True,
            text=True,
            timeout=120
        )
        passed = (result.returncode == 0)
        return {
            "passed": passed,
            "exit_code": result.returncode,
            "stdout": result.stdout[-1500:],
            "stderr": result.stderr[-1000:]
        }
    except Exception as e:
        return {"passed": False, "error": str(e)}

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), "starter")
    print(json.dumps(run_evaluation(path), indent=2))
