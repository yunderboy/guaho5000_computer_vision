# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2


def midpoint(pt_a, pt_b):
    return ((pt_a[0] + pt_b[0]) * 0.5, (pt_a[1] + pt_b[1]) * 0.5)


def detect_object_size(img_path, obj_width):

    # load the image, convert it to greyscale, and blur it slightly
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # sort the contours from left-to-right and initialize the
    # 'pixels per metric' calibration variable
    (cnts, _) = contours.sort_contours(cnts)
    pixels_per_metric = None

    # loop over the contours individually
    for c in cnts:
        # if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 100:
            continue

        # compute the rotated bounding box of the contour
        orig = image.copy()
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        # order the points in the contour such that they appear
        # in top-left, top-right, bottom-right, and bottom-left
        # order, then draw the outline of the rotated bounding
        # box
        box = perspective.order_points(box)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

        # loop over the original points and draw them
        for (x, y) in box:
            cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

        # unpack the ordered bounding box, then compute the midpoint
        # between the top-left and top-right coordinates, followed by
        # the midpoint between bottom-left and bottom-right coordinates
        (tl, tr, br, bl) = box
        (tltr_x, tltr_y) = midpoint(tl, tr)
        (blbr_x, blbr_y) = midpoint(bl, br)

        # compute the midpoint between the top-left and top-right points,
        # followed by the midpoint between the top-righ and bottom-right
        (tlbl_x, tlbl_y) = midpoint(tl, bl)
        (trbr_x, trbr_y) = midpoint(tr, br)

        # draw the midpoints on the image
        cv2.circle(orig, (int(tltr_x), int(tltr_y)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(blbr_x), int(blbr_y)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(tlbl_x), int(tlbl_y)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(trbr_x), int(trbr_y)), 5, (255, 0, 0), -1)

        # draw lines between the midpoints
        cv2.line(orig, (int(tltr_x), int(tltr_y)), (int(blbr_x), int(blbr_y)),
                 (255, 0, 255), 2)
        cv2.line(orig, (int(tlbl_x), int(tlbl_y)), (int(trbr_x), int(trbr_y)),
                 (255, 0, 255), 2)

        # compute the Euclidean distance between the midpoints
        d_a = dist.euclidean((tltr_x, tltr_y), (blbr_x, blbr_y))
        d_b = dist.euclidean((tlbl_x, tlbl_y), (trbr_x, trbr_y))

        # if the pixels per metric has not been initialized, then
        # compute it as the ratio of pixels to supplied metric
        # (in this case, inches)
        if pixels_per_metric is None:
            pixels_per_metric = d_b / obj_width

        # compute the size of the object
        dim_a = d_a / pixels_per_metric
        dim_b = d_b / pixels_per_metric

        # draw the object sizes on the image
        cv2.putText(orig, "{:.1f}mm".format(dim_a),
                    (int(tltr_x - 15), int(tltr_y - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (255, 255, 255), 2)
        cv2.putText(orig, "{:.1f}mm".format(dim_b),
                    (int(trbr_x + 10), int(trbr_y)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (255, 255, 255), 2)

        # show the output image
        cv2.imshow("Image", orig)
        cv2.waitKey(0)

    return

if __name__ == '__main__':
    detect_object_size('./images/plate_test.png', 22.25)