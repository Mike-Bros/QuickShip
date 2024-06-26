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

    # Finished the simulation return route_service to main method to be used in UI
    return route_service


if __name__ == '__main__':
    route_service = None
    user_has_not_quit = True
    print("Welcome to QuickShip!")
    print("While the application is running input q anytime to quit")

    while user_has_not_quit:
        user_input = input(
            "Are you ready to simulate the day? Type y or yes to begin (this will ingest csv data and simulate full delivery day)\n")
        if user_input == 'q':
            user_has_not_quit = False
            break
        if user_input == 'y' or user_input == 'yes':
            route_service = simulate_day()
            if route_service is None:
                raise Exception("Simulation failed to return the route_service")
            break

    while user_has_not_quit:
        print("Now in mode selection, type the corresponding letter to enter a mode")
        print("Single Package Lookup - p" + "\t| Packages in Status Range - s")
        user_input = input()
        if user_input == 'q':
            print("Quitting program...")
            user_has_not_quit = False
        elif user_input == 'p':
            in_package_mode = True
            print("Now in package lookup mode, at anytime type b to return to mode selection")
            while in_package_mode:
                user_input = input("Enter package ID\n")
                if user_input == 'q':
                    print("Quitting program...")
                    in_package_mode = False
                    user_has_not_quit = False
                elif user_input == 'b':
                    in_package_mode = False
                else:
                    package = route_service.package_service.get_package_by_id(int(user_input))
                    package.print_verbose()
        elif user_input == 's':
            in_range_mode = True
            print("Now in packages status range mode, at anytime type b to return to mode selection")
            while in_range_mode:
                print("Input time format HHMM, IE: 0930 = 9:30am, 1400 = 2:00pm")
                print("You will need to specify a time range in the format HHMM:HHMM, EI: 0930-1400 = 9:30am-2:00pm")
                user_input = input("Enter time range\n")
                if user_input == 'q':
                    print("Quitting program...")
                    in_range_mode = False
                    user_has_not_quit = False
                elif user_input == 'b':
                    in_range_mode = False
                else:
                    start_time = user_input.split('-')[0]
                    start_hour = start_time[0:2]
                    start_min = start_time[2:]
                    start_time = datetime(2022, 1, 1, int(start_hour), int(start_min))

                    end_time = user_input.split('-')[1]
                    end_hour = end_time[0:2]
                    end_min = end_time[2:]
                    end_time = datetime(2022, 1, 1, int(end_hour), int(end_min))

                    route_service.package_service.print_status_check(start_time, end_time)
