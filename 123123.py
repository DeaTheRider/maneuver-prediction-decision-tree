import pickle

with open('output1/inD-dataset-v1.0_00_dataset.pickle', 'rb') as f:
    data_new = pickle.load(f)

print(data_new)
print(len(data_new))