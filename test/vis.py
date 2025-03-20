import cv2
import numpy as np

# Annotate image with landmarks
def annotate_image(image_path, landmarks):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    height, width = image.shape[:2]  # Get image dimensions

    # Iterate through each set of coordinates in the landmarks
    for landmark_set in landmarks:
        for coords in landmark_set:
            x, y = int(coords[0] * width), int(coords[1] * height)
            cv2.circle(image, (x, y), radius=5, color=(0, 255, 0), thickness=-1)

    cv2.imshow('Annotated Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = 'black.jpg'       # Path to your image

    landmarks = [[
        [ 4.96419817e-01,  6.76409245e-01,  2.70172022e-05],
        [ 5.27356267e-01,  6.22745097e-01,  1.63881164e-02],
        [ 5.39986372e-01,  5.88243067e-01,  2.11258717e-02],
        [ 5.37679493e-01,  5.53249896e-01,  2.27675550e-02],
        [ 5.36505997e-01,  5.18429935e-01,  1.58824995e-02],
        [ 5.25904953e-01,  5.35612226e-01,  1.25245005e-03],
        [ 5.30406773e-01,  4.48966801e-01, -4.20776336e-03],
        [ 5.29075265e-01,  4.39178377e-01, -4.08343691e-03],
        [ 5.18490314e-01,  4.57334518e-01,  4.80341027e-03],
        [ 5.07147193e-01,  5.21879733e-01, -5.66312764e-03],
        [ 5.07794142e-01,  4.17332530e-01, -7.02968333e-04],
        [ 5.10344863e-01,  4.09513235e-01,  7.09563401e-03],
        [ 5.05904913e-01,  4.30430710e-01,  1.50430463e-02],
        [ 4.86105651e-01,  5.10734677e-01, -1.12741329e-02],
        [ 4.85288471e-01,  4.32510018e-01, -7.92713370e-03],
        [ 4.88134742e-01,  4.33807105e-01, -1.13558415e-02],
        [ 4.84531254e-01,  4.55191106e-01, -1.35519728e-02],
        [ 4.61524218e-01,  5.02443910e-01, -1.62559655e-02],
        [ 4.59132850e-01,  4.33067560e-01, -1.45911472e-02],
        [ 4.66821164e-01,  4.28921729e-01, -1.66506041e-02],
        [ 4.69354630e-01,  4.44151938e-01, -1.52661698e-02],]]
    annotate_image(image_path, landmarks)
