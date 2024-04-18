from scipy import misc
from PIL import Image
import imageio
import os
import numpy as np
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def extract_bayer_channels(raw):

    # Reshape the input bayer image
    ch_B  = raw[1::2, 1::2]
    ch_Gb = raw[0::2, 1::2]
    ch_R  = raw[0::2, 0::2]
    ch_Gr = raw[1::2, 0::2]

    RAW_combined = np.dstack((ch_B, ch_Gb, ch_R, ch_Gr))
    RAW_norm = RAW_combined.astype(np.float32) / (4 * 255)

    return RAW_norm



def load_training_batch(dataset_dir, TRAIN_SIZE, PATCH_WIDTH, PATCH_HEIGHT, DSLR_SCALE=1):

    train_directory_dslr = dataset_dir + '/train/canon/'
    train_directory_phone = dataset_dir + '/train/huawei_raw/'

    # NUM_TRAINING_IMAGES = 46839
    NUM_TRAINING_IMAGES = len([name for name in os.listdir(train_directory_phone)
                               if os.path.isfile(os.path.join(train_directory_phone, name))])

    TRAIN_IMAGES = np.random.choice(np.arange(0, NUM_TRAINING_IMAGES), TRAIN_SIZE, replace=False)

    train_data = np.zeros((TRAIN_SIZE, PATCH_WIDTH, PATCH_HEIGHT, 4))
    train_answ = np.zeros((TRAIN_SIZE, int(PATCH_WIDTH * DSLR_SCALE), int(PATCH_HEIGHT * DSLR_SCALE), 3))

    i = 0
    for img in TRAIN_IMAGES:

        I = np.asarray(imageio.imread((train_directory_phone + str(img) + '.png')))
        I = extract_bayer_channels(I)
        train_data[i, :] = I

        I = np.asarray(Image.open(train_directory_dslr + str(img) + '.jpg'))
        I = np.float32(np.reshape(I, [1, int(PATCH_WIDTH*DSLR_SCALE), int(PATCH_HEIGHT * DSLR_SCALE), 3])) / 255
        train_answ[i, :] = I

        i += 1

    return train_data, train_answ


def load_testing_data(dataset_dir, PATCH_WIDTH, PATCH_HEIGHT, DSLR_SCALE=1):

    test_directory_dslr = dataset_dir + '/test/canon/'
    test_directory_phone = dataset_dir + '/test/huawei_raw/'
    print(test_directory_dslr, "\n", test_directory_phone)
    NUM_TESTING_IMAGES = len([name for name in os.listdir(test_directory_phone) if os.path.isfile(os.path.join(test_directory_phone, name))])

    raw_imgs = np.zeros((NUM_TESTING_IMAGES, PATCH_WIDTH, PATCH_HEIGHT, 4))
    canon_imgs = np.zeros((NUM_TESTING_IMAGES, int(PATCH_WIDTH * DSLR_SCALE), int(PATCH_HEIGHT * DSLR_SCALE), 3))

    i = 0
    for img in range(NUM_TESTING_IMAGES):

        I = np.asarray(imageio.imread((test_directory_phone + str(img) + '.png')))
        I = extract_bayer_channels(I)
        raw_imgs[i, :] = I

        I = np.asarray(Image.open(test_directory_dslr + str(img) + '.jpg'))
        I = np.float32(np.reshape(I, [1, PATCH_WIDTH2, PATCH_HEIGHT2, 3])) / 255

        canon_imgs[i, :] = I

        i += 1
    return raw_imgs, canon_imgs


def load_testing_inp(dataset_dir, PATCH_WIDTH, PATCH_HEIGHT,s=0):

    test_directory_phone = dataset_dir

    NUM_TESTING_IMAGES = len([name for name in os.listdir(test_directory_phone) if os.path.isfile(os.path.join(test_directory_phone, name)) and not name.startswith('.')])
    # print([name for name in os.listdir(test_directory_phone) if os.path.isfile(os.path.join(test_directory_phone, name)) and not name.startswith('.')])
    # print(NUM_TESTING_IMAGES)
    raw_imgs = np.zeros((NUM_TESTING_IMAGES, PATCH_WIDTH, PATCH_HEIGHT, 4))
    
    i = 0
    for img in range(NUM_TESTING_IMAGES):
        I = np.asarray(imageio.imread((test_directory_phone + str((img+s)) + '.png')))
        I = extract_bayer_channels(I)
        print(I.shape)
        raw_imgs[i, :] = I

        i += 1
    return raw_imgs
