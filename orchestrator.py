from typing import Any, Dict, List
from Tools.perception import Perception, capture_perception
from Agents.planner import Planner
from executor import Executor
from reviewer import Reviewer


class Orchestrator:
    def __init__(self, max_attempts: int = 3):
        self.planner = Planner()
        self.executor = Executor()
        self.reviewer = Reviewer()
        self.max_attempts = max_attempts
        self.history: List[Dict[str, Any]] = []

    def run(self, objective: str, start_url: str | None = None) -> Dict[str, Any]:
        attempts = 0
        # initial perception
        perception = capture_perception(start_url) if start_url else capture_perception()

        while attempts < self.max_attempts:
            attempts += 1
            plan = self.planner.plan(perception, objective)

            exec_result = self.executor.execute_plan(plan)

            review = self.reviewer.review(exec_result, objective)

            self.history.append({
                "attempt": attempts,
                "plan": plan,
                "exec_result": exec_result,
                "review": review,
            })

            if review.get("success"):
                return {"status": "success", "result": review.get("result"), "history": self.history}

            # if failed, update perception from the last browser state and replan
            perception = Perception(dom=exec_result.get("dom", ""), screenshot=exec_result.get("screenshot"))

        return {"status": "failed", "history": self.history}


if __name__ == "__main__":
    orch = Orchestrator()
    out = orch.run("Get the text of the first link on the page.", start_url="https://example.com")
    print(out)
