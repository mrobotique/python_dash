import WazeRouteCalculator

from_address = '795 Sterling Lyon Parkway, Winnipeg'
to_address = '117 Kind Edward Street, Winnipeg'
region = 'NA'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
route.calc_route_info()
