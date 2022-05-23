import numpy as np

def AdaptiveFilter(image, image_gray):

    filter = np.array([(1, 1, 1, 1, 1), (1, 1, 1, 1, 1), (1, 1, 1, 1, 1), (1, 1, 1, 1, 1), (1, 1, 1, 1, 1)]) * (1 / 25)

    img_shape = image.shape
    filter_shape = filter.shape

    # add padding to maintain size after filtering
    row = img_shape[0] + filter_shape[0] - 1
    col = img_shape[1] + filter_shape[1] - 1
    new_img_arr = np.zeros((row, col))

    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            new_img_arr[i + int((filter_shape[0] - 1) / 2), j + int((filter_shape[1] - 1) / 2)] = image_gray[i, j]

    local_var = np.zeros((img_shape[0], img_shape[1]))
    local_mean = np.zeros((img_shape[0], img_shape[1]))

    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            temp = new_img_arr[i:i + filter_shape[0], j:j + filter_shape[1]]
            local_mean[i, j] = np.mean(temp)
            local_var[i, j] = np.mean(temp ** 2) - (local_mean[i, j] ** 2)

    noise_var = np.sum(local_var) // len(local_var)

    local_var = np.maximum(noise_var, local_var)

    image_gray = np.subtract(image_gray, np.multiply(np.divide(noise_var, local_var), np.subtract(image_gray, local_mean)))
    image_gray = image_gray.astype(np.uint8)

    return image_gray