from pathlib import Path

def load_policies(policy_dir: str):
    policy_files = sorted(Path(policy_dir).glob("*.txt"))
    policies = {}
    original_policies = {}

    for file in policy_files:
        name = file.stem
        with file.open("r", encoding="utf-8-sig", errors="replace") as f:
            text = f.read()

        lines = [line.strip() for line in text.splitlines()]
        clean_lines = [line for line in lines if line]

        policies[name] = "\n".join(clean_lines)
        original_policies[name] = text

    return policies, original_policies
