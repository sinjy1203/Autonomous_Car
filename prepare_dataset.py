##
# with open('/content/dataset/train.txt', 'w') as f:
#   f.write('\n'.join(train_img_list) + '\n')
#
# with open('/content/dataset/val.txt', 'w') as f:
#   f.write('\n'.join(val_img_list) + '\n')

##
import yaml

with open('C:/traffic/data.yaml', 'r') as f:
    data = yaml.load(f)

print(data)

data['train'] = 'C:/traffic/train.txt'
data['val'] = 'C:/traffic/val.txt'

with open('C:/traffic/data.yaml', 'w') as f:
    yaml.dump(data, f)

print(data)

##

