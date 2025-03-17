import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

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
            self.center, self.radius = args
            return

        # If 3 points are passed individually:
        elif len(args) == 3: 
            a, b, c = args
        else:
            raise ValueError("Circle requires Point and radius, a list of 3 Points, or 3 individual Points.")

        z1 = complex(a.x, a.y)
        z2 = complex(b.x, b.y)
        z3 = complex(c.x, c.y)
        if (z1 == z2) or (z2 == z3) or (z3 == z1):
            # 2 or 3 points are duplicates, draw a circle which includes them
            self.center = Point.midpoint(a, b)
            self.radius = a.distance_to(self.center)
            if not c.is_in_circle(self):
                self.center = Point.midpoint(a, c)
                self.radius = a.distance_to(self.center) 
            return

        w = (z3 - z1)/(z2 - z1)
      
        # You should change 0 to a small tolerance for floating point comparisons
        if abs(w.imag) <= 0:
            # TODO: This is ok too, just draw a circle with the 2 furthest points on the circumference.
            self.center = Point.midpoint(a, b)
            self.radius = a.distance_to(self.center)
            if not c.is_in_circle(self):
                self.center = Point.midpoint(a, c)
                self.radius = a.distance_to(self.center) 
            return
            
        center = (z2 - z1)*(w - abs(w)**2)/(2j*w.imag) + z1  # Simplified denominator
        
        self.radius = abs(z1 - center)
        self.center = Point(center.real, center.imag)

    def __repr__(self):
        return f"{self.center}, {self.radius}"

    def copy(self):
        return Circle(self.center, self.radius)
    
    def scale(self, factor):
        self.radius = self.radius * factor

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
                    for i in range(len(boundary)):
                        boundary_copy = boundary.copy()
                        boundary_copy[i] = p
                        circle = Circle(boundary_copy)

                        # if this circle contains the boundary point which was replaced, it's valid
                        if boundary[i].is_in_circle(circle):
                            candidate_circles.append(circle.copy())
                            break
    
                    # This can maybe go away once the algorithm is tested
                    if len(candidate_circles) == 0:
                        raise Exception('no candidate circles found!')

                    for c in candidate_circles:
                        if c.radius < circle.radius:
                            circle = c
        return circle

class FingerConfig:
    def __init__(self, config):
        self.thumb_length = config.get('thumb_length')
        self.index_length = config.get('index_length')
        self.middle_length = config.get('middle_length')
        self.ring_length = config.get('ring_length')  # Fixed typo
        self.pinky_length = config.get('pinky_length')  # Fixed typo

class FingerCounter:
    def __init__(self, config):
        base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
        options = vision.HandLandmarkerOptions(base_options=base_options,
                                            num_hands=2)
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.config = FingerConfig(config)

    def infer(self, image, show = False) -> list[list[list[float]]]:
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        result = self.detector.detect(mp_image)

        if show:
            annotated_image = show(mp_image.numpy_view(), result)
            cv2.imshow('test', cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        keypoints = []
        if len(result.hand_landmarks) == 0:
            return None

        for landmarks in result.hand_landmarks:
            landmarks_list = []

            for landmark in landmarks:
                landmarks_list.append([landmark.x, landmark.y])
            keypoints.append(landmarks_list)

        return keypoints

    def count_fingers(self, image, show = False):
        results = self.infer(image, show)
        if results is None:
            return None

        count = 0
        for r in results:
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
        palm_points = FingerCounter.get_palm_points_from_keypoints(points)
        return Circle.Welzl(palm_points)
    
    def get_palm_points_from_keypoints(points):
        wrist = Point(points[0][0], points[0][1])
        thumb_knuckle = Point(points[1][0], points[1][1])
        index_knuckle = Point(points[5][0], points[5][1])
        middle_knuckle = Point(points[9][0], points[9][1])
        ring_knuckle = Point(points[13][0], points[13][1])
        pinky_knuckle = Point(points[17][0], points[17][1])

        return [wrist, thumb_knuckle, index_knuckle, middle_knuckle, ring_knuckle, pinky_knuckle]
    
    def get_fingertip_points_from_keypoints(points):
        thumb_tip = Point(points[4][0], points[4][1])
        index_tip = Point(points[8][0], points[8][1])
        middle_tip = Point(points[12][0], points[12][1])
        ring_tip = Point(points[16][0], points[16][1])
        pinky_tip = Point(points[20][0], points[20][1])

        return [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]
    
    def test(self):
        cap = cv2.VideoCapture(0)  # Open default webcam

        while(1):
            ret, frame = cap.read()
            count = self.count_fingers(frame, False)
            if count is not None:
                print(count)

        cap.release()