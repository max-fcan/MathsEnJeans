from dataclasses import dataclass
from typing import Optional

import math

@dataclass
class Point:
    name: str
    coordinates: tuple
    
    def exists(self) -> bool:
        if self.name in City._all_cities:
            return True
        else:
            return False

class City:
    _all_cities = []
    def __init__(self, point: Point) -> None:
        self.name = point.name
        self.coordinates = point.coordinates
        self._register()

    def _register(self) -> bool:
        if self.name:
            City._all_cities.append(self.name)
            return True
        else:
            raise NameError("City name is invalid")

    def distance(self, city: Point, not_city=False) -> Optional[float]:
        if not city.exists():
            if not not_city:
                print(f"City {self.name} doesnt exists")
                return
            else:
                print(f"warning: Point {self.name} in not a city")

        return math.dist(self.coordinates, city.coordinates)


class CityConfiguration:
    def __init__(self) -> None:
        self.cities: list[City]

    def measure_efficiency(self) -> float:
        # distances = [city.distance(i) for city in self.cities for i in self.cities if city != i]
        # return sum(distances)

c1 = City(Point('A', (0, 0)))
p2 = (Point('B', (1, 0)))
print(c1.name, c1.coordinates, c1.distance(p2, not_city=True))
