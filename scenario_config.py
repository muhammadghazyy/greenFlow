import json
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name("traffic_scenarios.json")


def _load_config():
    with CONFIG_PATH.open(encoding="utf-8") as config_file:
        return json.load(config_file)


_CONFIG = _load_config()
SCENARIOS = _CONFIG["scenarios"]
ACTIVE_SCENARIO = _CONFIG["active_scenario"]


def get_scenario(name=ACTIVE_SCENARIO):
    scenario = SCENARIOS[name].copy()
    scenario["roads"] = scenario["roads"].copy()
    scenario["initial_traffic"] = scenario["initial_traffic"].copy()
    scenario["arrival_rates"] = scenario["arrival_rates"].copy()
    return scenario
