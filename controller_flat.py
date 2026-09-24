ARRIVAL_RATE_A = 0.5
ARRIVAL_RATE_B = ARRIVAL_RATE_A * 0.25
ARRIVAL_RATE_C = ARRIVAL_RATE_B * 0.5
DEPARTURE_RATE = 2.0
MAX_CYCLES = 10
ROAD_ORDER = ["A", "B", "C"]

initial_traffic = {
    "A": 36,
    "B": 3,
    "C": 6,
}

def calculate_green_duration(vehicle_count):
    # min_green = 5
    # max_green = 40
    # seconds_per_vehicle = 2

    # green = min_green + (vehicle_count * seconds_per_vehicle)

    return 30

def choose_next_road(current_index):
    """Return the next road in the fixed A -> B -> C rotation."""
    return ROAD_ORDER[current_index % len(ROAD_ORDER)]

def update_traffic(traffic, green_road, green_duration):
    """Apply simple arrival and departure changes for one green phase."""
    departure = DEPARTURE_RATE * green_duration

    arrival_rates = {
        "A": ARRIVAL_RATE_A,
        "B": ARRIVAL_RATE_B,
        "C": ARRIVAL_RATE_C,
    }

    for road in ROAD_ORDER:
        arrival = arrival_rates[road] * green_duration

        if road == green_road:
            traffic[road] = max(0, traffic[road] - departure)

        traffic[road] = max(0, round(traffic[road] + arrival))

    return traffic


def simulate_cycles():
    """Run a fixed number of cycles in round-robin order."""
    traffic = initial_traffic.copy()
    current_index = 0

    for cycle in range(1, MAX_CYCLES + 1):
        green_road = choose_next_road(current_index)
        green_duration = calculate_green_duration(traffic[green_road])

        print(f"--- Cycle {cycle} ---\n")
        print("Traffic before:")
        for road in ROAD_ORDER:
            print(f"{road} = {traffic[road]}")

        states = {road: "RED" for road in ROAD_ORDER}
        states[green_road] = "GREEN"

        print("\nDecision:")
        for road in ROAD_ORDER:
            print(f"{road} = {states[road]}")

        print(f"\nGreen duration: {green_duration} seconds")

        traffic = update_traffic(traffic, green_road, green_duration)

        print("\nTraffic after:")
        for road in ROAD_ORDER:
            print(f"{road} = {traffic[road]}")
        print()

        current_index += 1

def main():
    simulate_cycles()

if __name__ == "__main__":
    main()
