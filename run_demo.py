from orchestrator import Orchestrator


def main():
    orch = Orchestrator(max_attempts=2)
    objective = "Go to https://www.americanas.com.br/ and report the text of the first link."
    out = orch.run(objective, start_url="https://www.americanas.com.br/")
    print("Run result:\n", out)


if __name__ == "__main__":
    main()
