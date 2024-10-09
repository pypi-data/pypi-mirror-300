import numpy as np
import cv2 as cv
from skimage import img_as_ubyte
from skimage import feature


def remove_small_contours(contours, min_length=4):
    filtered_contours = []
    for contour in contours:
        # Přetypování na NumPy pole s typem np.int32
        contour_np = np.array(contour, dtype=np.int32)

        # Ověření, že kontura není prázdná, a kontrola délky
        if len(contour_np) > 0:
            if cv.arcLength(contour_np, True) >= min_length:
                filtered_contours.append(contour_np)
    return filtered_contours
def compute_hu_moments(contour):
    moments = cv.moments(contour)
    hu_moments = cv.HuMoments(moments).flatten()
    return hu_moments

def find_intersection(img_binary, filtered_contours, contours, hierarchy, edges, inner_contours):
    result_mask = np.zeros_like(img_binary, dtype=np.uint8)

    for contour in filtered_contours:
        filled_contour = cv.fillPoly(np.zeros_like(img_binary), [contour], 1)

        intersection = filled_contour & edges

        if np.any(intersection):
            result_mask = result_mask | filled_contour

    if inner_contours:
        inner_contours_mask = np.zeros_like(img_binary, dtype=np.uint8)
        for i in range(len(contours)):
            if hierarchy[0, i, 3] != -1:
                inner_filled_contour = cv.fillPoly(np.zeros_like(img_binary), [contours[i]], 1)

                inner_contours_mask = cv.bitwise_or(inner_filled_contour, inner_contours_mask)

        inner_contours_mask = Dilation(Erosion(inner_contours_mask, 3, 1), 3, 1)

        return np.clip(result_mask, 0, 1), np.clip(inner_contours_mask, 0, 1)

    return np.clip(result_mask, 0, 1), None


def create_binary_mask(img_gray, threshold, dilation_size, erosion_size=None):
    img_binary = img_as_ubyte(img_gray > threshold)
    img_binary = np.invert(img_binary)
    if erosion_size is not None:
        img_binary = Erosion(img_binary, erosion_size, 1)
    img_binary = Dilation(img_binary, dilation_size, 1)
    return img_binary


def calculate_canny_edges(img_gray, std_k, sigma):
    mean = np.mean(img_gray)
    std = np.std(img_gray)
    low_threshold = mean - std_k * std / 2
    high_threshold = mean + std_k * std / 2
    edges = feature.canny(img_gray, sigma=sigma, low_threshold=low_threshold, high_threshold=high_threshold)
    return edges


def laplacian_of_gaussian(image, std_k, sigma):
    image = cv.bitwise_not(image)

    blurred_image = cv.GaussianBlur(image, (0, 0), sigmaX=sigma, sigmaY=sigma)

    laplacian = cv.Laplacian(blurred_image, cv.CV_64F)

    # Apply threshold to focus on significant edges
    laplacian_abs = np.abs(laplacian)
    mean = np.mean(laplacian_abs)
    std = np.std(laplacian_abs)
    threshold = mean + std_k * std

    laplacian_thresholded = np.where(laplacian_abs > threshold, laplacian, 0)

    zc_image = np.zeros_like(laplacian_thresholded)

    sign_change_horizontal = np.diff(np.sign(laplacian_thresholded), axis=1)
    sign_change_vertical = np.diff(np.sign(laplacian_thresholded), axis=0)

    zc_image[:, 1:][sign_change_horizontal != 0] = 255
    zc_image[1:, :][sign_change_vertical != 0] = 255

    return zc_image.astype(np.uint8)


def filter_contours(contours, min_area):
    filtered_contours = []

    for contour in contours:
        if cv.contourArea(contour) >= min_area:
            filtered_contours.append(contour)

    return filtered_contours


def filter_contours_on_frame(contours, img_shape, min_area, detect_corrupted):
    height, width = img_shape
    min_area = min_area * height * width
    filtered_contours = []

    if detect_corrupted:
        total_outer_area = sum(cv.contourArea(contour) for contour in contours)

        for contour in contours:
            touches_top = np.any(contour[:, :, 1] == 0)
            touches_bottom = np.any(contour[:, :, 1] == height - 1)
            touches_left = np.any(contour[:, :, 0] == 0)
            touches_right = np.any(contour[:, :, 0] == width - 1)
            num_edges_touched = sum([touches_top, touches_bottom, touches_left, touches_right])

            contour_area = cv.contourArea(contour)
            if num_edges_touched > 0 or contour_area < min_area:
                # Check if the contour's area is large enough to return an empty list immediately
                if contour_area > 0.75 * total_outer_area:
                    return [], np.empty((0, 4), int)
            else:
                filtered_contours.append(contour)
    else:
        return contours

    return filtered_contours


def check_window_size(window_size):
    return window_size + 1 if window_size % 2 == 0 else window_size


def findContours(img_binary, inner_contours):
    if inner_contours:
        contours, hierarchy = cv.findContours(img_binary, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    else:
        contours, hierarchy = cv.findContours(img_binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    return contours, hierarchy


def Dilation(img, dilation_size=3, iterations=1, dilation_shape=cv.MORPH_ELLIPSE):
    element = cv.getStructuringElement(dilation_shape, (2 * dilation_size + 1, 2 * dilation_size + 1),
                                       (dilation_size, dilation_size))
    img_final = cv.dilate(img, element, iterations=iterations)

    return img_final


def Erosion(img, erosion_size=3, iterations=1, erosion_shape=cv.MORPH_ELLIPSE):
    element = cv.getStructuringElement(erosion_shape, (2 * erosion_size + 1, 2 * erosion_size + 1),
                                       (erosion_size, erosion_size))
    img_final = cv.erode(img, element, iterations=iterations)

    return img_final
