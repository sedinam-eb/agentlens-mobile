import os
import sys
import json
import time
from typing import List, Dict, Any

# Ensure server module imports resolve cleanly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from server.agent.core import PolarisAgent
from server.eval.engine import PolarisRubricEngine

BENCHMARKS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "benchmarks"))

def load_all_tasks() -> List[Dict[str, Any]]:
    """Discovers and parses all benchmark task configurations."""
    tasks = []
    if not os.path.exists(BENCHMARKS_DIR):
        print(f"[-] Error: Benchmarks directory not found at {BENCHMARKS_DIR}")
        return tasks

    for task_folder in sorted(os.listdir(BENCHMARKS_DIR)):
        task_json_path = os.path.join(BENCHMARKS_DIR, task_folder, "task.json")
        if os.path.isfile(task_json_path):
            with open(task_json_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                config["folder_name"] = task_folder
                tasks.append(config)
    return tasks

def print_leaderboard(results: List[Dict[str, Any]]):
    """Outputs a clean, formatted Markdown/ASCII leaderboard summary."""
    print("\n" + "=" * 80)
    print("                    POLARIS AGENT EVALUATION LEADERBOARD                    ")
    print("=" * 80)
    
    header = f"{'TASK ID':<30} | {'STATUS':<8} | {'SCORE':<8} | {'STEPS':<8} | {'TIME(s)':<8}"
    print(header)
    print("-" * 80)

    total_score = 0.0
    passed_count = 0

    for res in results:
        status_str = "PASSED" if res["passed"] else "FAILED"
        score_str = f"{res['composite_score']:.4f}"
        steps_str = f"{res['trajectory_depth']}/{res['max_budget']}"
        time_str = f"{res['execution_time_sec']:.2f}"
        
        print(f"{res['task_id']:<30} | {status_str:<8} | {score_str:<8} | {steps_str:<8} | {time_str:<8}")
        
        total_score += res["composite_score"]
        if res["passed"]:
            passed_count += 1

    avg_score = total_score / len(results) if results else 0.0
    pass_rate = (passed_count / len(results) * 100) if results else 0.0

    print("-" * 80)
    print(f"SUMMARY: Benchmark Pass Rate: {pass_rate:.1f}% ({passed_count}/{len(results)}) | Mean Polaris Score: {avg_score:.4f}")
    print("=" * 80 + "\n")

def run_benchmark_suite():
    tasks = load_all_tasks()
    if not tasks:
        print("[-] No benchmark tasks discovered. Exiting.")
        return

    print(f"[+] Discovered {len(tasks)} benchmark tasks in {BENCHMARKS_DIR}")
    results = []

    for task in tasks:
        task_id = task["id"]
        folder_name = task["folder_name"]
        starter_path = os.path.join(BENCHMARKS_DIR, folder_name, "starter")

        print(f"\n[>] Running Benchmark: {task_id}")
        print(f"    Prompt: {task['prompt'][:90]}...")
        
        start_time = time.time()
        
        # 1. Instantiate & Run Agent Loop
        agent = PolarisAgent(
            workspace_path=starter_path,
            task_prompt=task["prompt"],
            max_steps=task.get("max_steps", 12)
        )
        trajectory = agent.run()
        
        # 2. Run Gradle Unit Tests
        test_results = agent.tools.run_gradle_tests()
        passed = test_results.get("passed", False)
        
        elapsed_time = time.time() - start_time

        # 3. Calculate Polaris Composite Rubric Score
        eval_metrics = PolarisRubricEngine.calculate_score(
            passed=passed,
            trajectory=trajectory,
            task_config=task
        )
        
        eval_metrics["passed"] = passed
        eval_metrics["execution_time_sec"] = elapsed_time
        results.append(eval_metrics)

        print(f"    [+] Task Finished in {elapsed_time:.2f}s | Passed: {passed} | Composite Score: {eval_metrics['composite_score']}")

    # 4. Print Unified Summary Leaderboard
    print_leaderboard(results)

if __name__ == "__main__":
    run_benchmark_suite()
