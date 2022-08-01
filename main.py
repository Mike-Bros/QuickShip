# Author: Michael Bros
# Student_ID: 002706681

from datetime import datetime
from services.RouteService import RouteService


def simulate_day():
    """Simulates the day of deliveries using the route_service to manage the trucks and routes

    """
    # Startup RouteService and load trucks with seed data for trip 1
    route_service = RouteService()

    # Load trucks with seed data for trip 1
    route_service.load_trip(1)
    # Use RouteService to help optimize the route for trip 1 using permutation and weight analysis
    route_service.optimize_truck_packages_greedy("truck_1")
    route_service.optimize_truck_packages_greedy("truck_2")

    # Start the day 8:00AM, change status of trucks that are on route
    route_service.start_route("truck_1")
    route_service.start_route("truck_2")

    # Load trucks with seed data for trip 2
    route_service.load_trip(2)
    # Use RouteService to help optimize the route for trip 2 using permutation and weight analysis
    route_service.optimize_truck_packages_greedy("truck_1")
    route_service.optimize_truck_packages_greedy("truck_2")

    # Start route for trip 2 with start_time being the trucks last recorded time
    # or delayed_time if the truck arrived back at the HUB before they can leave with the packages needed
    delayed_time = datetime(2022, 1, 1, 10, 20)
    if delayed_time > route_service.truck_1.last_time:
        route_service.start_route("truck_1", delayed_time)
    else:
        route_service.start_route("truck_1", route_service.truck_1.last_time)
    delayed_time = datetime(2022, 1, 1, 9, 5)
    if delayed_time > route_service.truck_2.last_time:
        route_service.start_route("truck_2", delayed_time)
    else:
        route_service.start_route("truck_2", route_service.truck_2.last_time)

    all_delivered_packages = route_service.truck_1.delivered_packages + route_service.truck_2.delivered_packages
    # Now that simulation day has finished we refresh the package_service table for efficient lookups
    route_service.package_service.refresh_package_table(all_delivered_packages)
    # Print hash table representation after it has been updated
    route_service.package_service.package_hash.print_table()
    # Print concise package info for all delivered packages, check if there are any packages delivered late
    problem_packages = []
    for i in range(1, len(all_delivered_packages) + 1):
        package = route_service.package_service.get_package_by_id(i)
        package.print()
        if package.delivery_status != "Delivered On Time":
            problem_packages.append(package)

    # Check if problem packages were found in the previous step
    if len(problem_packages) > 0:
        print("Problem package(s) found....")
        for package in problem_packages:
            package.print()
        raise Exception(
            "Problem package(s) were found, this means delivery status was not Delivered On Time at the end of the day")
    else:
        print("All packages delivered and on time, no problem packages found!")

    # Check to see if there are any packages that have not yet been delivered
    if len(all_delivered_packages) < 40:
        raise Exception("Not all packages delivered, only have " + str(len(all_delivered_packages)) + " delivered")
    else:
        print("All 40 packages have been delivered as expected!")

    # Check that all packages were delivered on time

    # Check that both trucks did not exceed the 140-mile total distance limit
    total_distance = route_service.truck_1.total_mileage + route_service.truck_2.total_mileage
    if total_distance > 140:
        raise Exception(
            "Total distance for both trucks exceeded 140 miles. Total Distance: " + str(round(total_distance, 2)))
    else:
        print("All packages have been delivered in under 140 miles! Trucks combined total mileage: " + str(
            round(total_distance, 2)))

    # Check that 3, 18, 36, 38 where delivered on truck 2
    only_truck_2 = [3, 18, 36, 38]
    for package in route_service.truck_2.delivered_packages:
        if only_truck_2.__contains__(package.id):
            only_truck_2.remove(package.id)
    if len(only_truck_2) > 0:
        raise Exception("Packages [3, 18, 36, 38] must all be delivered on truck 2")
    else:
        print("Packages [3, 18, 36, 38] were all delivered on truck 2")

    # Check that 3, 18, 36, 38 where delivered together
    together = [13, 14, 15, 16, 19, 20]
    seed_1 = set(together).issubset(route_service.t1_trip_1_seed)
    seed_2 = set(together).issubset(route_service.t1_trip_2_seed)
    seed_3 = set(together).issubset(route_service.t2_trip_1_seed)
    seed_4 = set(together).issubset(route_service.t2_trip_2_seed)
    if seed_1 or seed_2 or seed_3 or seed_4:
        print("Packages [13, 14, 15, 16, 19, 20] were all delivered together!")
    else:
        raise Exception("Packages [13, 14, 15, 16, 19, 20] must all be delivered together")


if __name__ == '__main__':
    simulate_day()
