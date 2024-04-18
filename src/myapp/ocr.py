import cv2
import easyocr
import matplotlib.pyplot as plt
import os

# specify folder path
folder_path = ''

# instance text detector
reader = easyocr.Reader(['en'])

# process all images in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        # read image
        image_path = os.path.join(folder_path, filename)
        img = cv2.imread(image_path)

        # detect text on image
        text_ = reader.readtext(img)

        threshold = 0.25
        # draw bbox and text
        for t_, t in enumerate(text_):
            print(t)

            bbox, text, score = t

            if score > threshold:
                # Fix the rectangle coordinates
                cv2.rectangle(img, (int(bbox[0][0]), int(bbox[0][1])), (int(bbox[2][0]), int(bbox[2][1])), (0, 255, 0), 5)
                cv2.putText(img, text, (int(bbox[0][0]), int(bbox[0][1])), cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)

        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()
