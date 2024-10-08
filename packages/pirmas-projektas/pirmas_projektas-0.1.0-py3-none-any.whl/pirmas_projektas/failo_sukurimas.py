import pickle
import os

def parodyti_biudzeta():
    if os.path.exists("Biudžetas.pkl"):
        with open("Biudžetas.pkl", 'rb') as pickle_in:
            return pickle.load(pickle_in)
    else:
        return None

def saugoti_biudzeta(biudzetas):
    with open("Biudžetas.pkl", 'wb') as pickle_out:
        pickle.dump(biudzetas, pickle_out)