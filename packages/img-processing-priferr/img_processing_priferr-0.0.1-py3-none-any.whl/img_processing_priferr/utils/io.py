from skimage.io import imread, imsave

def read_image(path, is_grey = False):
  image = imread(path, as_grey = is_gray)
  return image

def save_image(image, path):
  imsave(path, image)
