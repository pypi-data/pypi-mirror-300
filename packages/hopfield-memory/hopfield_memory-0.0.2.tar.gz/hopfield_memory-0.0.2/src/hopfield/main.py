# -*- coding: utf-8 -*-
"""
Hopfield.ipynb
Original file is located at
    https://colab.research.google.com/drive/1YWYdjbddQZJUtcpn7BoGAQWOnQDiBTT9?usp=sharing
"""
import numpy as np
import matplotlib.pyplot as plt
import math
from PIL import Image, ImageFilter
import requests
from io import BytesIO

# Function to display an image
def plot_state(image, title="Image", pixel=32):
    plt.imshow(image.reshape((pixel, pixel)), cmap='gray')
    plt.title(title)
    plt.show()


# Function to load an image from a URL and convert it to a binary 32x32 image
from PIL import Image
import numpy as np
from io import BytesIO
import requests


def preprocess_image(image):
    return np.where(image.flatten() > 0.5, 1, -1)

def load_and_preprocess_image(image_source, pixel=32, url=False):
    
    # Load the image based on the source type
    if url:
        # Load image from URL
        response = requests.get(image_source)
        img = Image.open(BytesIO(response.content))
    elif isinstance(image_source, str):
        # Load image from a file path
        img = Image.open(image_source)
    elif isinstance(image_source, Image.Image):
        # If the input is already a PIL Image object
        img = image_source
    else:
        raise ValueError("Invalid image source. Provide a URL, file path, or PIL Image object.")
    
    # Convert the original image to a binary format
    img = img.convert('L')  # Convert to grayscale
    img = img.resize((pixel, pixel))  # Resize to 32x32
    img_array = np.asarray(img) / 255.0  # Normalize pixel values to [0, 1]
    binary_image = np.where(img_array > 0.3, 1, -1)  # Convert to binary: 1 or -1
    return binary_image

class HopfieldNetwork:
    def __init__(self, resolution=32*32):
        self.num_neurons = resolution
        self.weights = np.zeros((resolution, resolution))

    # Hebbian learning
    def train(self, patterns, url=False):
        """
        Train hopfield network with images from a URL, file path, or PIL Image object.
        
        Parameters:
        - patterns: List containing URLs (str), file path (str), or PIL Image objects
        - url: Boolean flag indicating if the source is a URL (default: False)
        """
        pixel = int(math.sqrt(self.num_neurons))
        for pattern in patterns:
            image = load_and_preprocess_image(pattern, pixel=pixel, url=url)
            image_flattened = preprocess_image(image)
            self.weights += np.outer(image_flattened, image_flattened)
        np.fill_diagonal(self.weights, 0)  # No self-connections
        self.weights /= len(image_flattened)

    def retrieve(self, pattern, max_iterations=100, url=False):
        """
        Retrieve trained images by providing blurred or noisy images to the Hopfield network

        Parameters:
        - pattern: Blurred/Noisy image URL (str), file path (str), or PIL Image object
        - max_iterations: number of max steps before stopping the network (default: 500)
        - url: Boolean flag indicating if the source is a URL (default: False)
        """
        pixel = int(math.sqrt(self.num_neurons))
        image = load_and_preprocess_image(pattern, url=url, pixel=pixel)
        image_flattened = preprocess_image(image)
        state = image_flattened.copy()
        for _ in range(max_iterations):
            for i in range(self.num_neurons):
                update = np.dot(self.weights[i], state)
                state[i] = 1 if update >= 0 else -1
        return state


