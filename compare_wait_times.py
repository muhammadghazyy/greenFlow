import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path

from controller_adaptive import (
    MAX_CYCLES,
    ROAD_ORDER,
    initial_traffic,
    calculate_green_duration,
    choose_next_road,
    update_traffic,
)
from controller_flat import (
    initial_traffic as flat_initial_traffic,
    calculate_green_duration as flat_calculate_green_duration,
    choose_next_road as flat_choose_next_road,
    update_traffic as flat_update_traffic,
)

LOG_DIR = Path("logs")


def simulation_timestamp():
    return datetime.now(timezone(timedelta(hours=7))).strftime("%Y%m%d%H%M%S")


CSV_PATH = LOG_DIR / f"traffic_wait_comparison._{simulation_timestamp()}.csv"
MD_PATH = LOG_DIR / f"traffic_wait_summary._{simulation_timestamp()}.md"


def cycle_wait_time(traffic, green_road, green_duration, current_index, duration_fn, road_selector):
    """Estimate each road's wait until its next green phase using the fixed rotation."""
    wait_by_road = {road: 0 for road in ROAD_ORDER}
    total_wait = 0

    future_sequence = []
    for offset in range(len(ROAD_ORDER)):
        road = road_selector(current_index + offset)
        future_sequence.append((road, duration_fn(traffic[road])))

    for road in ROAD_ORDER:
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


def simulate_strategy(name, traffic_dict, duration_fn, road_selector, update_fn):
    traffic = traffic_dict.copy()
    current_index = 0
    rows = []
    total_wait_all_cycles = 0
    road_totals = {road: 0 for road in ROAD_ORDER}

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
        )
        total_wait_all_cycles += total_wait

        for road in ROAD_ORDER:
            road_totals[road] += wait_by_road[road]

        row = {
            "strategy": name,
            "cycle": cycle,
            "green_road": green_road,
            "green_duration_seconds": green_duration,
            "total_wait_this_cycle_seconds": total_wait,
            "A_before": traffic["A"],
            "B_before": traffic["B"],
            "C_before": traffic["C"],
            "A_wait_seconds": wait_by_road["A"],
            "B_wait_seconds": wait_by_road["B"],
            "C_wait_seconds": wait_by_road["C"],
            "A_total_wait_seconds": road_totals["A"],
            "B_total_wait_seconds": road_totals["B"],
            "C_total_wait_seconds": road_totals["C"],
        }
        rows.append(row)

        traffic = update_fn(traffic, green_road, green_duration)
        current_index += 1

    summary_row = {
        "strategy": name,
        "cycle": "TOTAL",
        "green_road": "",
        "green_duration_seconds": "",
        "total_wait_this_cycle_seconds": total_wait_all_cycles,
        "A_before": "",
        "B_before": "",
        "C_before": "",
        "A_wait_seconds": "",
        "B_wait_seconds": "",
        "C_wait_seconds": "",
        "A_total_wait_seconds": road_totals["A"],
        "B_total_wait_seconds": road_totals["B"],
        "C_total_wait_seconds": road_totals["C"],
    }
    rows.append(summary_row)
    return rows


def write_csv(rows):
    fieldnames = [
        "strategy",
        "cycle",
        "green_road",
        "green_duration_seconds",
        "total_wait_this_cycle_seconds",
        "A_before",
        "B_before",
        "C_before",
        "A_wait_seconds",
        "B_wait_seconds",
        "C_wait_seconds",
        "A_total_wait_seconds",
        "B_total_wait_seconds",
        "C_total_wait_seconds",
    ]

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


def write_markdown(rows):
    strategy_totals = {}
    strategy_averages = {}

    for row in rows:
        if row["cycle"] == "TOTAL":
            strategy_totals[row["strategy"]] = {
                "total_wait": row["total_wait_this_cycle_seconds"],
                "A_total": row["A_total_wait_seconds"],
                "B_total": row["B_total_wait_seconds"],
                "C_total": row["C_total_wait_seconds"],
            }
            continue

        strategy = row["strategy"]
        strategy_averages.setdefault(strategy, {road: {"total": 0, "count": 0} for road in ROAD_ORDER})

        for road in ROAD_ORDER:
            wait = row[f"{road}_wait_seconds"]
            if wait > 0:
                strategy_averages[strategy][road]["total"] += wait
                strategy_averages[strategy][road]["count"] += 1

    adaptive_total = strategy_totals.get("adaptive", {}).get("total_wait", 0)
    flat_total = strategy_totals.get("flat_30s", {}).get("total_wait", 0)

    adaptive_a_avg = average_wait_for_strategy(strategy_averages, "adaptive", "A")
    adaptive_b_avg = average_wait_for_strategy(strategy_averages, "adaptive", "B")
    adaptive_c_avg = average_wait_for_strategy(strategy_averages, "adaptive", "C")
    flat_a_avg = average_wait_for_strategy(strategy_averages, "flat_30s", "A")
    flat_b_avg = average_wait_for_strategy(strategy_averages, "flat_30s", "B")
    flat_c_avg = average_wait_for_strategy(strategy_averages, "flat_30s", "C")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    markdown = []
    markdown.append("# Traffic Wait Comparison Summary")
    markdown.append("")
    markdown.append(f"Simulation timestamp: {timestamp}")
    markdown.append("")
    markdown.append("## Method")
    markdown.append("- Fixed A -> B -> C signal order")
    markdown.append("- Adaptive strategy adjusts green duration using traffic count")
    markdown.append("- Flat strategy uses a constant 30-second green duration")
    markdown.append("- Per-road wait is the average wait while that road is red before its next green phase")
    markdown.append("")
    markdown.append("## Result Summary")
    markdown.append("")
    markdown.append(f"- Adaptive total wait: {adaptive_total}s")
    markdown.append(f"- Flat 30s total wait: {flat_total}s")
    markdown.append(f"- Difference: {flat_total - adaptive_total}s")
    markdown.append("")
    markdown.append("### Adaptive average red-light wait per road")
    markdown.append(f"- A: {format_seconds(adaptive_a_avg)}s")
    markdown.append(f"- B: {format_seconds(adaptive_b_avg)}s")
    markdown.append(f"- C: {format_seconds(adaptive_c_avg)}s")
    markdown.append("")
    markdown.append("### Flat 30s average red-light wait per road")
    markdown.append(f"- A: {format_seconds(flat_a_avg)}s")
    markdown.append(f"- B: {format_seconds(flat_b_avg)}s")
    markdown.append(f"- C: {format_seconds(flat_c_avg)}s")
    markdown.append("")
    markdown.append("## CSV Output")
    markdown.append(f"- File: [{CSV_PATH.name}]({CSV_PATH})")
    markdown.append("")
    markdown.append("## Detailed Results")
    markdown.append("")

    for row in rows:
        if row["cycle"] == "TOTAL":
            strategy = row["strategy"]
            markdown.append(f"### {strategy} total")
            markdown.append(f"- Total wait: {row['total_wait_this_cycle_seconds']}s")
            markdown.append(f"- A average wait while red: {format_seconds(average_wait_for_strategy(strategy_averages, strategy, 'A'))}s")
            markdown.append(f"- B average wait while red: {format_seconds(average_wait_for_strategy(strategy_averages, strategy, 'B'))}s")
            markdown.append(f"- C average wait while red: {format_seconds(average_wait_for_strategy(strategy_averages, strategy, 'C'))}s")
            markdown.append("")

    MD_PATH.write_text("\n".join(markdown), encoding="utf-8")


def main():
    LOG_DIR.mkdir(exist_ok=True)

    timestamp = simulation_timestamp()
    global CSV_PATH, MD_PATH
    CSV_PATH = LOG_DIR / f"traffic_wait_comparison._{timestamp}.csv"
    MD_PATH = LOG_DIR / f"traffic_wait_summary._{timestamp}.md"

    adaptive_rows = simulate_strategy(
        "adaptive",
        initial_traffic.copy(),
        calculate_green_duration,
        choose_next_road,
        update_traffic,
    )

    flat_rows = simulate_strategy(
        "flat_30s",
        flat_initial_traffic.copy(),
        flat_calculate_green_duration,
        flat_choose_next_road,
        flat_update_traffic,
    )

    all_rows = adaptive_rows + flat_rows
    write_csv(all_rows)
    write_markdown(all_rows)

    print(f"Saved comparison CSV to: {CSV_PATH}")
    print(f"Saved summary markdown to: {MD_PATH}")
    print()

    for row in all_rows:
        if row["cycle"] == "TOTAL":
            print(f"{row['strategy']}: total_wait={row['total_wait_this_cycle_seconds']}s")


if __name__ == "__main__":
    main()
