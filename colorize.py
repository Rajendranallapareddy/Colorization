import cv2
import numpy as np
import os

def colorize_image(image_path):
    # Load the pre-trained model
    prototxt = 'model/colorization_deploy_v2.prototxt'
    model = 'model/colorization_release_v2.caffemodel'
    pts = 'model/pts_in_hull.npy'

    net = cv2.dnn.readNetFromCaffe(prototxt, model)
    pts = np.load(pts)

    # Load the cluster centers as 1x1 convolution kernel
    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = pts.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [pts.astype(np.float32)]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, np.float32)]

    # Load the input image in grayscale
    img = cv2.imread(image_path)
    scaled = img.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

    # Resize the L channel to network's input size
    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    # Predict the ab channels
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))

    # Resize the ab channels to original image size
    ab = cv2.resize(ab, (img.shape[1], img.shape[0]))

    # Combine with original L channel
    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

    # Convert back to BGR
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = (255.0 * colorized).astype("uint8")

    # Save the output image
    colorized_image_path = os.path.join('uploads', 'colorized_' + os.path.basename(image_path))
    cv2.imwrite(colorized_image_path, colorized)

    return colorized_image_path
