import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path

from controller_adaptive import MAX_CYCLES, calculate_green_duration, choose_next_road
from controller_flat import (
    calculate_green_duration as flat_calculate_green_duration,
    choose_next_road as flat_choose_next_road,
)
from scenario_config import ACTIVE_SCENARIO, SCENARIOS

LOG_DIR = Path("logs")

def simulation_timestamp():
    return datetime.now(timezone(timedelta(hours=7))).strftime("%Y%m%d%H%M%S")


CSV_PATH = LOG_DIR / f"traffic_wait_comparison._{simulation_timestamp()}.csv"
MD_PATH = LOG_DIR / f"traffic_wait_summary._{simulation_timestamp()}.md"


def make_update_traffic(arrival_rates, departure_rate, road_order):
    def update_traffic(traffic, green_road, green_duration):
        departure = departure_rate * green_duration

        for road in road_order:
            arrival = arrival_rates.get(road, 0) * green_duration

            if road == green_road:
                traffic[road] = max(0, traffic[road] - departure)

            traffic[road] = max(0, round(traffic[road] + arrival))

        return traffic

    return update_traffic


def cycle_wait_time(traffic, green_road, green_duration, current_index, duration_fn, road_selector, road_order):
    """Estimate each road's wait until its next green phase using the fixed rotation."""
    wait_by_road = {road: 0 for road in road_order}
    total_wait = 0

    future_sequence = []
    for offset in range(len(road_order)):
        road = road_selector(current_index + offset)
        future_sequence.append((road, duration_fn(traffic[road])))

    for road in road_order:
        if road == green_road:
            wait_by_road[road] = 0
            continue

        wait = 0
        for next_road, duration in future_sequence:
            if next_road == road:
                break
            wait += duration

        wait_by_road[road] = wait
        total_wait += wait

    return wait_by_road, total_wait


def simulate_strategy(name, traffic_dict, duration_fn, road_selector, update_fn, road_order, scenario_name):
    traffic = traffic_dict.copy()
    current_index = 0
    rows = []
    total_wait_all_cycles = 0
    road_totals = {road: 0 for road in road_order}
    for cycle in range(1, MAX_CYCLES + 1):
        green_road = road_selector(current_index)
        green_duration = duration_fn(traffic[green_road])

        wait_by_road, total_wait = cycle_wait_time(
            traffic,
            green_road,
            green_duration,
            current_index,
            duration_fn,
            road_selector,
            road_order,
        )
        total_wait_all_cycles += total_wait

        for road in road_order:
            road_totals[road] += wait_by_road[road]

        row = {
            "scenario": scenario_name,
            "strategy": name,
            "cycle": cycle,
            "green_road": green_road,
            "green_duration_seconds": green_duration,
            "total_wait_this_cycle_seconds": total_wait,
        }

        for road in road_order:
            row[f"{road}_before"] = traffic[road]
            row[f"{road}_wait_seconds"] = wait_by_road[road]
            row[f"{road}_total_wait_seconds"] = road_totals[road]

        rows.append(row)

        traffic = update_fn(traffic, green_road, green_duration)
        current_index += 1

    summary_row = {
        "scenario": scenario_name,
        "strategy": name,
        "cycle": "TOTAL",
        "green_road": "",
        "green_duration_seconds": "",
        "total_wait_this_cycle_seconds": total_wait_all_cycles,
    }

    for road in road_order:
        summary_row[f"{road}_before"] = ""
        summary_row[f"{road}_wait_seconds"] = ""
        summary_row[f"{road}_total_wait_seconds"] = road_totals[road]

    rows.append(summary_row)
    return rows


def write_csv(rows, road_order):
    fieldnames = [
        "scenario",
        "strategy",
        "cycle",
        "green_road",
        "green_duration_seconds",
        "total_wait_this_cycle_seconds",
    ]

    for road in road_order:
        fieldnames.extend([f"{road}_before", f"{road}_wait_seconds", f"{road}_total_wait_seconds"])

    with CSV_PATH.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def format_seconds(value):
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.1f}"


def average_wait_for_strategy(strategy_averages, strategy, road):
    stats = strategy_averages.get(strategy, {}).get(road, {})
    total = stats.get("total", 0)
    count = stats.get("count", 0)
    return total / count if count else 0


def write_markdown(rows, scenario_map):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    markdown = []
    markdown.append("# Traffic Wait Comparison Summary")
    markdown.append("")
    markdown.append(f"Simulation timestamp: {timestamp}")
    markdown.append("")
    markdown.append("## Method")
    markdown.append("- Fixed signal order follows the configured road list")
    markdown.append("- Adaptive strategy adjusts green duration using traffic count")
    markdown.append("- Flat strategy uses a constant 30-second green duration")
    markdown.append("- Per-road wait is the average wait while that road is red before its next green phase")
    markdown.append("")

    for scenario_name in scenario_map:
        scenario = scenario_map[scenario_name]
        road_order = scenario["roads"]
        scenario_rows = [row for row in rows if row.get("scenario") == scenario_name]
        strategy_totals = {}
        strategy_averages = {}

        for row in scenario_rows:
            if row["cycle"] == "TOTAL":
                strategy_totals[row["strategy"]] = {"total_wait": row["total_wait_this_cycle_seconds"]}
                for road in road_order:
                    strategy_totals[row["strategy"]][f"{road}_total"] = row[f"{road}_total_wait_seconds"]
                continue

            strategy = row["strategy"]
            strategy_averages.setdefault(strategy, {road: {"total": 0, "count": 0} for road in road_order})

            for road in road_order:
                wait = row[f"{road}_wait_seconds"]
                if wait > 0:
                    strategy_averages[strategy][road]["total"] += wait
                    strategy_averages[strategy][road]["count"] += 1

        adaptive_total = strategy_totals.get("adaptive", {}).get("total_wait", 0)
        flat_total = strategy_totals.get("flat_30s", {}).get("total_wait", 0)
        road_text = " -> ".join(road_order)
        initial_traffic_text = ", ".join(f"{road}={scenario['initial_traffic'][road]}" for road in road_order)
        arrival_rate_text = ", ".join(f"{road}={scenario['arrival_rates'].get(road, 0)}" for road in road_order)

        markdown.append(f"## Scenario: {scenario_name}")
        markdown.append(f"- Road order: {road_text}")
        markdown.append(f"- Initial traffic: {initial_traffic_text}")
        markdown.append(f"- Arrival rates: {arrival_rate_text}")
        markdown.append(f"- Adaptive total wait: {adaptive_total}s")
        markdown.append(f"- Flat 30s total wait: {flat_total}s")
        markdown.append(f"- Difference: {flat_total - adaptive_total}s")
        markdown.append("")

        for strategy in ["adaptive", "flat_30s"]:
            title = "Adaptive" if strategy == "adaptive" else "Flat 30s"
            markdown.append(f"### {title} average red-light wait per road")
            for road in road_order:
                avg = average_wait_for_strategy(strategy_averages, strategy, road)
                markdown.append(f"- {road}: {format_seconds(avg)}s")
            markdown.append("")

        for row in scenario_rows:
            if row["cycle"] == "TOTAL":
                strategy = row["strategy"]
                markdown.append(f"### {strategy} total")
                markdown.append(f"- Total wait: {row['total_wait_this_cycle_seconds']}s")
                for road in road_order:
                    avg = average_wait_for_strategy(strategy_averages, strategy, road)
                    markdown.append(f"- {road} average wait while red: {format_seconds(avg)}s")
                markdown.append("")

    markdown.append("## CSV Output")
    markdown.append(f"- File: [{CSV_PATH.name}]({CSV_PATH})")
    markdown.append("")

    MD_PATH.write_text("\n".join(markdown), encoding="utf-8")


def main():
    LOG_DIR.mkdir(exist_ok=True)

    timestamp = simulation_timestamp()
    global CSV_PATH, MD_PATH
    CSV_PATH = LOG_DIR / f"traffic_wait_comparison._{timestamp}.csv"
    MD_PATH = LOG_DIR / f"traffic_wait_summary._{timestamp}.md"

    all_rows = []

    for scenario_name, scenario in SCENARIOS.items():
        road_order = scenario["roads"]
        traffic_config = scenario["initial_traffic"]
        arrival_rates = scenario["arrival_rates"]
        departure_rate = scenario["departure_rate"]

        adaptive_update = make_update_traffic(arrival_rates, departure_rate, road_order)
        flat_update = make_update_traffic(arrival_rates, departure_rate, road_order)

        adaptive_rows = simulate_strategy(
            "adaptive",
            traffic_config.copy(),
            calculate_green_duration,
            choose_next_road,
            adaptive_update,
            road_order,
            scenario_name,
        )

        flat_rows = simulate_strategy(
            "flat_30s",
            traffic_config.copy(),
            flat_calculate_green_duration,
            flat_choose_next_road,
            flat_update,
            road_order,
            scenario_name,
        )

        all_rows.extend(adaptive_rows)
        all_rows.extend(flat_rows)

    write_csv(all_rows, SCENARIOS[ACTIVE_SCENARIO]["roads"])
    write_markdown(all_rows, SCENARIOS)

    print(f"Saved comparison CSV to: {CSV_PATH}")
    print(f"Saved summary markdown to: {MD_PATH}")
    print(f"Scenarios included: {', '.join(SCENARIOS.keys())}")
    print()

    for row in all_rows:
        if row["cycle"] == "TOTAL":
            print(f"{row['scenario']} | {row['strategy']}: total_wait={row['total_wait_this_cycle_seconds']}s")


if __name__ == "__main__":
    main()
