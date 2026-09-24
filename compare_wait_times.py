import csv
from datetime import datetime
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
CSV_PATH = LOG_DIR / "traffic_wait_comparison.csv"
MD_PATH = LOG_DIR / "traffic_wait_summary.md"


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


def write_markdown(rows):
    strategy_totals = {}

    for row in rows:
        if row["cycle"] != "TOTAL":
            continue

        strategy_totals[row["strategy"]] = {
            "total_wait": row["total_wait_this_cycle_seconds"],
            "A_total": row["A_total_wait_seconds"],
            "B_total": row["B_total_wait_seconds"],
            "C_total": row["C_total_wait_seconds"],
        }

    adaptive_total = strategy_totals.get("adaptive", {}).get("total_wait", 0)
    flat_total = strategy_totals.get("flat_30s", {}).get("total_wait", 0)
    adaptive_a = strategy_totals.get("adaptive", {}).get("A_total", 0)
    adaptive_b = strategy_totals.get("adaptive", {}).get("B_total", 0)
    adaptive_c = strategy_totals.get("adaptive", {}).get("C_total", 0)
    flat_a = strategy_totals.get("flat_30s", {}).get("A_total", 0)
    flat_b = strategy_totals.get("flat_30s", {}).get("B_total", 0)
    flat_c = strategy_totals.get("flat_30s", {}).get("C_total", 0)

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
    markdown.append("- Wait estimate is based on the time until each non-green road reaches its next green phase in the rotation")
    markdown.append("")
    markdown.append("## Result Summary")
    markdown.append("")
    markdown.append(f"- Adaptive total wait: {adaptive_total}s")
    markdown.append(f"- Flat 30s total wait: {flat_total}s")
    markdown.append(f"- Difference: {flat_total - adaptive_total}s")
    markdown.append("")
    markdown.append("### Adaptive road totals")
    markdown.append(f"- A: {adaptive_a}s")
    markdown.append(f"- B: {adaptive_b}s")
    markdown.append(f"- C: {adaptive_c}s")
    markdown.append("")
    markdown.append("### Flat 30s road totals")
    markdown.append(f"- A: {flat_a}s")
    markdown.append(f"- B: {flat_b}s")
    markdown.append(f"- C: {flat_c}s")
    markdown.append("")
    markdown.append("## CSV Output")
    markdown.append(f"- File: [{CSV_PATH.name}]({CSV_PATH})")
    markdown.append("")
    markdown.append("## Detailed Results")
    markdown.append("")

    for row in rows:
        if row["cycle"] == "TOTAL":
            markdown.append(f"### {row['strategy']} total")
            markdown.append(f"- Total wait: {row['total_wait_this_cycle_seconds']}s")
            markdown.append(f"- A total wait: {row['A_total_wait_seconds']}s")
            markdown.append(f"- B total wait: {row['B_total_wait_seconds']}s")
            markdown.append(f"- C total wait: {row['C_total_wait_seconds']}s")
            markdown.append("")

    MD_PATH.write_text("\n".join(markdown), encoding="utf-8")


def main():
    LOG_DIR.mkdir(exist_ok=True)

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
