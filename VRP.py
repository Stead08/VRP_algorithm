import pprint
import random
from typing import List, Tuple
import matplotlib.pyplot as plt

Request = Tuple[Tuple[float, float], Tuple[float, float], Tuple[int, int], int]
TaxiBase = Tuple[float, float]

def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


def calculate_route_duration(route: List[int], requests: List[Request], base: TaxiBase) -> float:
    duration = 0
    prev_point = base

    for r_idx in route:
        request = requests[r_idx]
        origin, destination, desired_pickup_time, allowed_delay = request
        duration += calculate_distance(prev_point, origin)
        duration += calculate_distance(origin, destination)
        prev_point = destination

    duration += calculate_distance(prev_point, base)
    return duration


def sequential_vrp_algorithm(max_taxi: int, requests: List[Request], base: TaxiBase) -> List[List[int]]:
    if len(requests) == 0:
        return [[]]

    taxi_routes = []
    unassigned_requests = list(range(len(requests)))

    while unassigned_requests and len(taxi_routes) < max_taxi:
        new_route = [unassigned_requests.pop(0)]
        best_insertion = None
        min_duration_diff = float('inf')

        while len(new_route) < len(requests) // max_taxi:
            for r_idx in unassigned_requests:
                for i in range(len(new_route) + 1):
                    temp_route = new_route[:i] + [r_idx] + new_route[i:]
                    duration_diff = calculate_route_duration(temp_route, requests, base) - calculate_route_duration(
                        new_route, requests, base)
                    if duration_diff < min_duration_diff:
                        min_duration_diff = duration_diff
                        best_insertion = (r_idx, i)

            if best_insertion:
                r_idx, i = best_insertion
                unassigned_requests.remove(r_idx)
                new_route.insert(i, r_idx)
                best_insertion = None
                min_duration_diff = float('inf')
            else:
                break

        taxi_routes.append(new_route)

    if unassigned_requests:
        raise ValueError(
            f"Cannot satisfy all requests with {max_taxi} taxis. At least {len(taxi_routes) + 1} taxis needed.")
    return taxi_routes


def plot_taxi_routes(taxi_routes: List[List[int]], requests: List[Request], base: TaxiBase) -> None:
    plt.figure()

    for taxi_id, route in enumerate(taxi_routes):
        x = [base[0]]
        y = [base[1]]
        for r_idx in route:
            origin, destination, _, _ = requests[r_idx]
            x.extend([origin[0], destination[0]])
            y.extend([origin[1], destination[1]])
        x.append(base[0])
        y.append(base[1])
        plt.plot(x, y, marker='o', linestyle='-', markersize=5, label=f"Taxi {taxi_id + 1}")
    plt.legend()
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Taxi Routes")
    plt.grid()
    fig_filename = str(random.randint(100, 1000)) + ".png"
    # plt.savefig(fig_filename, format="png", dpi=300, )
    plt.show()


def generate_test_case(num_customers: int) -> List[Request]:
    requests = []
    for _ in range(num_customers):
        origin = (random.randint(0, 25), random.randint(0, 40))
        destination = (random.randint(0, 25), random.randint(0, 40))
        pickup_hour = random.randint(10, 18)
        pickup_minute = random.randint(0, 59)
        allowed_delay = random.randint(10, 15)
        stay_hour = random.randint(1, 3)
        requests.append((origin, destination, (pickup_hour, pickup_minute), allowed_delay))
        requests.append((destination, origin, (pickup_hour + stay_hour, pickup_minute), allowed_delay))
    return requests


def print_taxi_routes(taxi_routes: List[List[int]], requests: List[Request]) -> None:
    for taxi_idx, route in enumerate(taxi_routes):
        print(f"Taxi {taxi_idx + 1} route:")
        sorted_route = sorted(route, key=lambda x: requests[x][2])
        for req_idx in sorted_route:
            request = requests[req_idx]
            print(f"  From {request[0]} to {request[1]} at {request[2][0]}:{request[2][1]:02d} ")


def check_if_customers_return_home(taxi_routes: List[List[int]], requests: List[Request]) -> bool:
    for i in range(0, len(requests), 2):
        home, destination = requests[i][0], requests[i][1]
        found_home, found_destination = False, False
        for route in taxi_routes:
            if i in route:
                found_home = True
            if i + 1 in route:
                found_destination = True
            if found_home and found_destination:
                break
        if not found_home or not found_destination:
            return False
    return True


def main():
    num_customers = 18
    max_taxi = 3
    taxi_base = (10, 10)

    requests = generate_test_case(num_customers)
    taxi_routes = sequential_vrp_algorithm(max_taxi, requests, taxi_base)
    print_taxi_routes(taxi_routes, requests)
    plot_taxi_routes(taxi_routes, requests, taxi_base)
    pprint.pprint(requests)

    if check_if_customers_return_home(taxi_routes, requests):
        print("All customers have returned home.")
    else:
        print("Some customers did not return home.")


if __name__ == "__main__":
    main()
