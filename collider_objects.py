# RectangleCollider
# Creates a rectangle using a top left coordinate and a width and height
# Used for collision detection
class RectangleCollider:
    # Constructor
    def __init__(self, position_left, position_top, width, height):
        self.position_left = position_left
        self.position_top = position_top
        self.width = width
        self.height = height
    # Updating the rectangle's position
    def update(self, position_left, position_top):
        self.position_left = position_left
        self.position_top = position_top

# CircleCollider
# Creates a circle around a center with a radius
# Used for collision deteciton
class CircleCollider:
    # Constructor
    def __init__(self, position_x, position_y, radius):
        self.position_x = position_x
        self.position_y = position_y
        self.radius = radius
    # Updating the circle's position
    def update(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y