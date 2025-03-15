from ultralytics import YOLO

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance_to(self, point):
        return ((self.x - point.x) ** 2.0 + (self.y - point.y)**2.0) ** 0.5
    
    def midpoint(a, b):
        return Point((a.x + b.x) / 2.0, (a.y + b.y) / 2.0)
    
    def is_in_circle(self, circle):
        return self.distance_to(circle.center) <= circle.radius
    
# Scott (https://math.stackexchange.com/users/740203/scott), Get the equation of a circle when given 3 points,
# URL (version: 2023-02-21): https://math.stackexchange.com/q/3503338   
class Circle:
    def __init__(self, *args):
        # If the input is a list of 3 points:
        if len(args) == 1 and isinstance(args[0], list) and len(args[0]) == 3:
            # Unpack the list of points into a, b, and c
            a, b, c = args[0]

        # If center and radius are given:
        elif len(args) == 2:
            self.center = args[0]
            self.radius = args[1]
            return
        
        # If 3 points are passed individually:
        elif len(args) == 3: 
            a, b, c = args
        else:
            raise ValueError("You must provide either a center and radius, a list of 3 points, or 3 individual points.")
        
        z1 = complex(a.x, a.y)
        z2 = complex(b.x, b.y)
        z3 = complex(c.x, c.y)
        if (z1 == z2) or (z2 == z3) or (z3 == z1):
            # TODO: Some points are duplicates, this is ok. Need to handle this appropriately
            raise ValueError(f"Duplicate points: {a}, {b}, {c}")
            
        w = (z3 - z1)/(z2 - z1)
        
        # You should change 0 to a small tolerance for floating point comparisons
        if abs(w.imag) <= 0:
            # TODO: This is ok too, just draw a circle with the 2 furthest points on the circumference.
            raise ValueError(f"Points are collinear: {a}, {b}, {c}")
            
        center = (z2 - z1)*(w - abs(w)**2)/(2j*w.imag) + z1  # Simplified denominator
        
        self.radius = abs(z1 - center)
        self.center = Point(center.real, center.imag)

    def copy(self):
        return Circle(self.center, self.radius)

    
class FingerCounter:
    def __init__(self):
        try:
            self.model = YOLO('hands-pose.onnx') # Adds deps on onnx, onnxruntime
        except FileNotFoundError:
            model = YOLO('hands-pose.pt')
            model.export(format='onnx')
            self.model = YOLO('hands-pose.onnx')

    def count_fingers(self, image):
        results = self.model(image)

        # print(keypoints[0].xy)
        # results[0].show()

        count = 0
        for r in results:
            keypoints = r.keypoints

    def get_fingers_from_keypoints(keypoints):
        points = FingerCounter.format_keypoints(keypoints)
        return

    def calculate_palm_region(points):
        wrist = points[0]
        thumb_knuckle = points[1]
        index_knuckle = points[5]
        middle_knuckle = points[9]
        ring_knuckle = points[13]
        pinky_knuckle = points[17]

        palm_points = [wrist, thumb_knuckle, index_knuckle, middle_knuckle, ring_knuckle, pinky_knuckle]
        return
    
    def Welzl(points):
        match len(points):
            case 0:
                return None
            case 1:
                return Circle(points[0], 0)
            case 2:
                center = Point.midpoint(points[0], points[1])
                radius = center.distance_to(points[0])
                return Circle(center, radius)
            case 3:
                circle = Circle(points)
            case _:
                boundary = points[:3]
                circle = Circle(boundary)

                # for all additional points, check if they are already in the circle
                for p in points[3:]:
                    if p.is_in_circle(circle):
                        continue

                    # if not, find the smallest circle which encloses this point and all the old boundary points
                    candidate_circles = []
                    for i in len(boundary):
                        boundary_copy = boundary.copy()
                        boundary_copy[i] = p
                        circle = Circle(boundary_copy)

                        # if this circle contains the boundary point which was replaced, it's valid
                        if boundary[i].is_in_circle(circle):
                            candidate_circles.append(circle.copy())
                            break
                    
                    # This can maybe go away once the algorithm is tested
                    if len(candidate_circles == 0):
                        raise Exception('no candidate circles found!')

                    for c in candidate_circles:
                        if c.radius < circle.radius:
                            circle = c
        return circle
    
    def format_keypoints(keypoints):
        return keypoints.xy().squeeze().tolist()


p1 = Point(1, 1)
p2 = Point(2, 1)
p3 = Point(3, 1)
p4 = Point(4, 1)
p5 = Point(5, 1)
p6 = Point(6, 1)
p7 = Point(7, 1)
points = [p1, p2, p3, p4, p5, p6, p7]

circle = FingerCounter.Welzl(points)
print(circle)