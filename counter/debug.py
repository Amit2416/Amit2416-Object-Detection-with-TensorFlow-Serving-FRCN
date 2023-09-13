import os

from PIL import ImageDraw, ImageFont


def draw(predictions, image, image_name):
    draw_image = ImageDraw.Draw(image, "RGBA")

    image_width, image_height = image.size

    font = ImageFont.truetype("counter/resources/arial.ttf", 20)
    i = 0
    for prediction in predictions:
        box = prediction.box
        draw_image.rectangle(
            [(box.xmin * image_width, box.ymin * image_height),
             (box.xmax * image_width, box.ymax * image_height)],
            outline='red')
        class_name = prediction.class_name
        draw_image.text(
            (box.xmin * image_width, box.ymin * image_height - font.getsize(class_name)[1]),
            f"{class_name}: {prediction.score}", font=font, fill='black')
        i += 1
    try:
        os.mkdir('tmp/debug')
    except OSError:
        pass
    image.save(f"tmp/debug/{image_name}", "JPEG")

"""
debug.py - Debugging and Visualization Utility for Machine Learning Models

This script provides functions for visualizing and debugging the predictions of
machine learning models, particularly for object detection or image classification tasks.

Functions:
    - draw(predictions, image, image_name):
        Draws bounding boxes and class labels on an input image based on the provided predictions.
        
        Arguments:
        - predictions (list): A list of prediction objects representing detected objects or classes.
        - image (PIL.Image.Image): The input image on which to draw the predictions.
        - image_name (str): The name of the image used when saving the result.

    Example Usage:
    ```
    from PIL import Image
    from debug import draw

    # Load image and predictions
    image = Image.open("input_image.jpg")
    predictions = [...]  # List of prediction objects

    # Visualize and save the image with predictions
    draw(predictions, image, "output_image.jpg")
    ```

File Structure:
    - This script assumes that it's part of a larger project with the following structure:
      ```
      project_root/
      ├── debug.py
      ├── counter/
      │   └── resources/
      │       └── arial.ttf
      └── tmp/
          └── debug/
      ```

    - The "counter/resources/arial.ttf" font file is used for drawing text on the images.
    - The resulting images with predictions are saved in the "tmp/debug/" directory.

This script is intended for debugging and visualizing the results of machine learning models, and the name "debug.py" reflects its purpose.
"""
