from detector import liteRT_detector
from . import finger_counter_config

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def distance_to(self, point):
        return ((self.x - point.x) ** 2.0 + (self.y - point.y)**2.0) ** 0.5
    
    def midpoint(a, b):
        return Point((a.x + b.x) / 2.0, (a.y + b.y) / 2.0)
    
    def is_in_circle(self, circle):
        return self.distance_to(circle.center) <= circle.radius

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
    
    def __repr__(self):
        return f"{self.center}, {self.radius}"
    
    def from_2_points(a, b):
        center = Point.midpoint(a, b)
        radius = center.distance_to(a)
        return Circle(center, radius)

class FingerCounter:
    def __init__(self, config):
        self.config = finger_counter_config.FingerCounterConfig(config)
        self.detector = liteRT_detector.LiteRT_Detector(self.config.min_confidence)

    def count_fingers(self, image):
        result = self.detector.detect(image)
        if result is None:
            return None

        count = 0
        for r in result:
            count = count + self.count_fingers_from_keypoints(r)

        return count
    
    def count_fingers_from_keypoints(self, points):
        palm_circle = FingerCounter.calculate_palm_circle(points)
        thumb, index, middle, ring, pinky = FingerCounter.get_fingertip_points_from_keypoints(points)
        count = 0
        if thumb.distance_to(palm_circle.center) >= palm_circle.radius * self.config.thumb_length:
            count = count + 1
        if index.distance_to(palm_circle.center) >= palm_circle.radius * self.config.index_length:
            count = count + 1
        if middle.distance_to(palm_circle.center) >= palm_circle.radius * self.config.middle_length:
            count = count + 1
        if ring.distance_to(palm_circle.center) >= palm_circle.radius * self.config.ring_length:
            count = count + 1
        if pinky.distance_to(palm_circle.center) >= palm_circle.radius * self.config.pinky_length:
            count = count + 1
        return count
    
    def calculate_palm_circle(points):
        wrist, middle_knuckle = FingerCounter.get_palm_points_from_keypoints(points)
        return Circle.from_2_points(wrist, middle_knuckle)
    
    def get_palm_points_from_keypoints(points):
        wrist = Point(points[0][0], points[0][1])
        middle_knuckle = Point(points[9][0], points[9][1])

        return [wrist, middle_knuckle]
    
    def get_fingertip_points_from_keypoints(points):
        thumb_tip = Point(points[4][0], points[4][1])
        index_tip = Point(points[8][0], points[8][1])
        middle_tip = Point(points[12][0], points[12][1])
        ring_tip = Point(points[16][0], points[16][1])
        pinky_tip = Point(points[20][0], points[20][1])

        return [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]