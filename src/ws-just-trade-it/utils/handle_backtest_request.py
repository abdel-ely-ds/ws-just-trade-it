

def to_python_file(strategy_code: str):
    strategy_name = strategy_code[:strategy_code.index("[Strategy]")].split(" ")[-1].lower()
    with open(f"/custom_strategies/{strategy_name}.py", "w") as f:
        f.write(strategy_code)