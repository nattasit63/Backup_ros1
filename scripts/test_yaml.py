#!/usr/bin/env python3
import yaml
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# a_yaml_file = open("map.yaml")

# parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
# print(parsed_yaml_file["image"])

with open('map.yaml','r') as f:
    yml_dict = yaml.safe_load(f)
image_file = yml_dict.get('image')
print(image_file)

# im = Image.open(str(image_file))
img = mpimg.imread(image_file)
imgplot = plt.imshow(img)
plt.show()
