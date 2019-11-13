import pickle

data = []

with open("scores.pickle", "wb") as sf:
    pickle.dump(data, sf)
