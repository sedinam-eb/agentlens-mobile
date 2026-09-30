AgentLens Mobile 📱🤖
Python 3.11+
Gemini 1.5 Pro
Evaluation Framework
License: MIT
AgentLens Mobile is an open-source evaluation harness and benchmark suite designed to evaluate, trajectory-track, and benchmark autonomous LLM coding agents on long-horizon software engineering tasks within Android/Kotlin and React Native codebases.
Built explicitly to bridge the gap between simple code generation and complex, multi-file architectural refactoring, AgentLens Mobile provides deterministic grading, step-by-step agent trajectory observability, and real-time mobile execution telemetry via a native Android dashboard.
🌟 Key Highlights & Engineering Features
￼ Long-Horizon Multi-File Task Suite: A benchmark dataset of complex mobile software engineering challenges (e.g., state migration, asynchronous memory leak fixes, SQLite database migrations, and concurrency refactoring).
￼ Deterministic Multi-Dimensional Rubrics: Automated sandboxed graders evaluate submissions using weighted metrics: functional correctness (￼), step efficiency, token context footprint, and code quality linting.
￼ Agent Trajectory & Telemetry Logging: Real-time capture of agent reasoning loops, tool-calling steps, diff patches, and tool-call latency using Gemini 1.5 Pro tool-calling capabilities.
￼ Mobile Real-Time Control Panel: A Jetpack Compose companion app streaming live tool executions, token usage, and automated evaluation scorecards over WebSockets.
📐 Architecture & System Topology
📊 Evaluation Methodology & Scoring Rubrics
AgentLens evaluates agents beyond binary pass/fail mechanics by applying a multi-dimensional weighted rubric for every benchmark run:
Where:
￼ ￼: Deterministic pass/fail state of isolated unit/integration test suites.
￼ ￼: Penalizes unnecessary execution loops and tool redundancy.
￼ ￼: Measures static code analysis results, lint warnings, and runtime memory leak regression.
📁 Repository Structure
🚀 Quickstart Guide
Prerequisites
￼ Python 3.11+
￼ JDK 17+ (for Android/Gradle evaluations)
￼ Docker (optional, for isolated sandbox execution)
￼ Gemini API Key
1. Installation
2. Environment Setup
3. Run a Benchmark Evaluation
To execute an autonomous agent on ⁠task_01_viewmodel_migration⁠ and evaluate performance:
4. Expected Output
🎯 Alignment with DeepMind Polaris Objectives
This repository was specifically constructed to address key research challenges emphasized by Google DeepMind's Polaris team:
1. In-Depth Benchmark Construction: Demonstrates how to write realistic multi-file coding problems with rigorous constraints rather than toy competitive programming problems.
2. Deterministic Evaluation: Implements isolated execution environments to prevent evaluation flakiness and verify solution correctness.
3. Agent Trajectory Analysis: Collects detailed step-by-step logs to analyze agent failures during long-horizon software engineering workflows.
📜 License
Distributed under the MIT License. See ⁠LICENSE⁠ for more information.