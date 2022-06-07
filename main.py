from models.Package import Package
from models.Truck import Truck

if __name__ == '__main__':
    p1 = Package(1, "1948 Circle", "Savage", "MN", 55811, "EOD", 3, "This is a special note")
    p2 = Package(2, "300 State St", "Prior Lake", "MN", 55821, "EOD", 2,)
    p3 = Package(3, "600 E 900 South", "Holladay", "MN", 53765, "10:30 AM", 2,)
    #p1.print()

    t1 = Truck()
    t1.load_package(p1)
    t1.load_package(p2)
    t1.load_package(p3)
    t1.load_package(p3)
    t1.load_package(p3)
    t1.load_package(p3)
    t1.load_package(p3)
    t1.load_package(p3)
    t1.load_package(p3)
    t1.load_package(p3)
    t1.load_package(p3)
    t1.load_package(p3)
    t1.load_package(p3)
    t1.load_package(p3)
    t1.load_package(p3)
    t1.load_package(p3)
    t1.print()

