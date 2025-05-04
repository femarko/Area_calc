from math import pi

class Circle:
    def __init__(self, radius: float):
        self.params = {"radius": radius}

    def area(self) -> float:
        return self.params["radius"] ** 2 * pi


class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = {"width": width}
        self.height = {"height": height}

    def area(self) -> float:
        return self.width["width"] * self.height["height"]