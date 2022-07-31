# Author: Michael Bros
# Student_ID: 002706681

from datetime import datetime
from services.RouteService import RouteService

if __name__ == '__main__':
    # Startup RouteService and load trucks with seed data for trip 1
    route_service = RouteService()
    route_service.load_trip(1)

    # Use RouteService to help optimize the route for trip 1 using permutation and weight analysis
    route_service.optimize_truck_packages_greedy("truck_1")
    route_service.optimize_truck_packages_greedy("truck_2")

    # Start the day 8:00AM, change status of trucks that are on route
    route_service.start_route("truck_1")
    print(route_service.truck_1.last_time.strftime("%I:%M %p"))
    route_service.start_route("truck_2")
    print(route_service.truck_2.last_time.strftime("%I:%M %p"))

    # Load trucks with seed data for trip 2
    route_service.load_trip(2)

    # Start route for trip 2 with start_time being the trucks last recorded time
    # or delayed_time if the truck arrived back at the HUB before they can leave with the packages needed
    delayed_time = datetime(2022, 1, 1, 10, 20)
    if delayed_time > route_service.truck_1.last_time:
        route_service.start_route("truck_1", delayed_time)
    else:
        route_service.start_route("truck_1", route_service.truck_1.last_time)
    print(route_service.truck_1.last_time.strftime("%I:%M %p"))
    delayed_time = datetime(2022, 1, 1, 9, 5)
    if delayed_time > route_service.truck_2.last_time:
        route_service.start_route("truck_2", delayed_time)
    else:
        route_service.start_route("truck_2", route_service.truck_2.last_time)
    print(route_service.truck_2.last_time.strftime("%I:%M %p"))

    # Load trucks with seed data for trip 3
    route_service.load_trip(3)

    # Start route for trip 3 with start_time being the trucks last recorded time
    # at this point there are no more time constraints therefore no delay_time like trip 2
    route_service.start_route("truck_1", route_service.truck_1.last_time)
    print(route_service.truck_1.last_time.strftime("%I:%M %p"))
    route_service.start_route("truck_2", route_service.truck_2.last_time)
    print(route_service.truck_2.last_time.strftime("%I:%M %p"))

    # Check to see if there are any packages that have not yet been delivered
    all_delivered_packages = route_service.truck_1.delivered_packages + route_service.truck_2.delivered_packages
    if len(all_delivered_packages) < 40:
        raise Exception("Not all packages delivered, only have " + str(len(all_delivered_packages)) + " delivered")

    route_service.package_service.package_hash.print_table()

    # Now that simulation day has finished we refresh the package_service table for efficient lookups
    route_service.package_service.refresh_package_table(all_delivered_packages)
    for i in range(1, len(all_delivered_packages) + 1):
        route_service.package_service.get_package_by_id(i).print()
