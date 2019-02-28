"""Generate a sequential of relational descriptions"""
import json
import numpy as np
import glob
def basic_des(ground_truth, idx):
    basic_dict = ground_truth['objects'][idx]
    return ' '.join((basic_dict['material'], basic_dict['color'], basic_dict['size'], basic_dict['shape']))

rel_mapping = {'front': 'in front of', 'behind': 'behind', 'right': 'to the right of', 'left': 'to the left of'}
if __name__ == '__main__':

    # filename = '../inc_output/scenes/CLEVR_new_000000.json'
    for filename in sorted(glob.glob('../inc_output/scenes/CLEVR_new_*.json')):
        ground_truth = json.load(open(filename))
        # First sentence
        print('-' * 10)
        print('filename:', filename)
        print('there is a {}'.format(basic_des(ground_truth, 0)))
        # Recursively generate following descriptions
        # for i in np.random.permutation([1,2,3]):
        for i in range(1, 4):
            # find one relation, currently in the sequential order, could change to a randomized policy
            rel_flag = False
            for j in np.random.permutation(range(0, i)):
                for relationship in rel_mapping.keys():
                    if i in ground_truth['relationships'][relationship][j]:
                        print('a {} is {} the {}'.format(basic_des(ground_truth, i), rel_mapping[relationship], basic_des(ground_truth, j)))
                        rel_flag = True
                        break
                if rel_flag:
                    break
