"""Generate a sequential of relational vectors"""
import json
import numpy as np
import glob
import os
import pickle


rel_mapping = {'front': 'in front of', 'behind': 'behind', 'right': 'to the right of', 'left': 'to the left of'}

color_mapping = {"gray": [87, 87, 87],
"red": [173, 35, 35],
"blue": [42, 75, 215],
"green": [29, 105, 20],
"brown": [129, 74, 25],
"purple": [129, 38, 192],
"cyan": [41, 208, 208],
"yellow": [255, 238, 51]}

# normalizing to (0, 1)
for key in color_mapping:
    color_mapping[key] = [float(item) / 255. for item in color_mapping[key]]

discrete_mapping = {
  "shape": [ "cube", "sphere", "cylinder"],
  "color": [ "gray", "red", "blue", "green", "brown", "purple", "cyan", "yellow" ],
  "material": [ "rubber", "metal" ],
  "size": [ "large", "small" ]
}
discrete_keys = discrete_mapping.keys()

# dimension = 18
def basic_feature(ground_truth, idx):
    basic_dict = ground_truth['objects'][idx]
    feature_list = []
    for key in discrete_keys:
        if key != 'color':
            key_feature = np.zeros(len(discrete_mapping[key]))
            # print(discrete_mapping[key])
            # print(basic_dict[key])
            found_idx = discrete_mapping[key].index(basic_dict[key])
            key_feature[found_idx] = 1.0
        else:
            key_feature = color_mapping[basic_dict[key]].copy()
        feature_list.extend(key_feature)
    feature_list.extend(basic_dict['3d_coords'])
    return feature_list

def change_name(json_name, idx):
    return os.path.basename(json_name[:-5]) + '_{}.png'.format(idx+1)


if __name__ == '__main__':

    final_dict = {}
    # filename = '../inc_output/scenes/CLEVR_new_000000.json'
    for filename in sorted(glob.glob('../inc_output/scenes/CLEVR_new_*.json')):
        ground_truth = json.load(open(filename))
        # program for generating 18*4 + 3features

        # Recursively generate vector representations for "objects"
        img_feature = np.zeros(18 * 4 + 3)
        img_feature[-3:] = ground_truth['directions']['right']
        for idx in range(0, 4):
            img_filename = change_name(filename, idx)
            img_feature[idx*18:(idx+1)*18] = basic_feature(ground_truth, idx)
            # add in camera direction
            final_dict[img_filename] = img_feature.copy()

        # # program for generating 18 + 3features
        # for idx in range(0, 4):
        # # for idx in range(0, 1):
        #     img_feature = np.zeros(13 + 3)
        #     img_feature[-3:] = ground_truth['directions']['right']
        #     img_filename = change_name(filename, idx)
        #     img_feature[:13] = basic_feature(ground_truth, idx)
        #     # add in camera direction
        #     final_dict[img_filename] = img_feature

    # np.save('../inc_output/CLEVR_dict.npy', final_dict)
    # np.save('../inc_output/CLEVR_single_obj_dict.npy', final_dict)
    np.save('../inc_output/CLEVR_single_obj_dict_rgb.npy', final_dict)
