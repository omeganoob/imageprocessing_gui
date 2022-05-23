import numpy as np

def MaxFilter(image, image_gray):

    filter = np.array([(1, 1, 1, 1, 1), (1, 1, 1, 1, 1), (1, 1, 1, 1, 1), (1, 1, 1, 1, 1), (1, 1, 1, 1, 1)]) * (1/25)

    img_shape = image.shape
    filter_shape = filter.shape

    # add padding to maintain size after filtering
    row = img_shape[0] + filter_shape[0] - 1
    col = img_shape[1] + filter_shape[1] - 1
    new_img_arr = np.zeros((row, col))

    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            new_img_arr[i + int((filter_shape[0] - 1) / 2), j + int((filter_shape[1] - 1) / 2)] = image_gray[i, j]

    print(new_img_arr)

    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            temp = new_img_arr[i:i + filter_shape[0], j:j + filter_shape[1]]
            res = np.amax(temp)
            image_gray[i, j] = res
    
    return image_gray