import csv

def create_distances_dict(file_name):
    distances = {}
    with open(file_name, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            from_loc = row['from']
            to_loc = row['to']
            distance = int(row['distance'])
            add_distance(distances, from_loc, to_loc, distance)
    return distances

def add_distance(distances, from_loc, to_loc, distance):
    distances[(from_loc, to_loc)] = distance
    distances[(to_loc, from_loc)] = distance

def calculate_route_distance(distances, stops_list):
    tot_dist = 0
    for i in range(len(stops_list) - 1):
        tot_dist += distances.get((stops_list[i].strip(), stops_list[i + 1].strip()), 0)
    return tot_dist

def find_intermediate_distances(distances, source, destination, stops):
    stops_list = stops.split(",")
    stops_list = [stop.strip() for stop in stops_list]

    direct_distance = distances.get((source, destination))
    if direct_distance:
        total_distance = calculate_route_distance(distances, [source, destination])
        return total_distance

    total_distance = 0
    for i in range(len(stops_list) - 1):
        sub_route = stops_list[i:i+2]
        sub_distance = calculate_route_distance(distances, sub_route)
        if sub_distance:
            total_distance += sub_distance

    return total_distance if total_distance > 0 else None

def main():
    distances = create_distances_dict('distances.csv')
    source = input("Enter your source: ").strip()
    destination = input("Enter your destination: ").strip()

    routes = [
        {"source": "Delhi", "destination": "Chennai", "stops": "Delhi, Bhopal, Hyderabad, Chennai"},
        {"source": "Bengaluru", "destination": "Bhopal", "stops": "Bengaluru, Hyderabad, Bhopal"}
    ]

    for route in routes:
        source = route['source']
        destination = route['destination']
        stops = route['stops']

        total_distance = find_intermediate_distances(distances, source, destination, stops)

        if total_distance is not None:
            print(f"Total Distance from {source} to {destination}: {total_distance} km")
        else:
            print(f"No valid route found between {source} and {destination}")

if __name__ == "__main__":
    main()