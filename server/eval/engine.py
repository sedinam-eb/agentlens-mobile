import subprocess
import time
from typing import Dict, Any

class EvalEngine:
    def __init__(self, workspace_path: str, task_config: Dict[str, Any]):
        self.workspace = workspace_path
        self.config = task_config

    def evaluate_submission(self, trajectory_data: list) -> Dict[str, Any]:
        start_time = time.time()
        
        # 1. Run automated build & test suite inside workspace
        test_result = subprocess.run(
            ["./gradlew", "test"],
            cwd=self.workspace,
            capture_output=True,
            text=True
        )
        
        passed = test_result.returncode == 0
        execution_time = time.time() - start_time
        
        # 2. Compute Multi-dimensional Rubric
        num_steps = len(trajectory_data)
        correctness_score = 1.0 if passed else 0.0
        step_efficiency_score = max(0.0, 1.0 - (num_steps / self.config["max_steps"]))
        
        final_score = (
            (correctness_score * self.config["eval_criteria"]["correctness_weight"]) +
            (step_efficiency_score * self.config["eval_criteria"]["efficiency_weight"])
        )

        return {
            "task_id": self.config["id"],
            "passed": passed,
            "final_score": round(final_score, 4),
            "trajectory_length": num_steps,
            "execution_time_sec": round(execution_time, 2)
        }
