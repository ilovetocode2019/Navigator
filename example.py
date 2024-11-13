import navigator

def main():
    query = input("Enter a starting location: ")
    start = navigator.search_location(query)

    query = input("Enter a destination: ")
    end = navigator.search_location(query)

    print(f"\nFinding the shortest route from {start} to {end}..")

    route = navigator.find_route(start, end)
    print(route)

if __name__ == "__main__":
    main()
