import numpy as np
import matplotlib.pyplot as plt
import os
import unidec.tools as ud
from unidec.IsoDec.datatools import *
from unidec.IsoDec.match import *
import pickle as pkl
import time
import torch
import matplotlib as mpl
from math import floor
from numba import jit, njit, prange

try:
    mpl.use("WxAgg")
except:
    pass

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"



@njit(fastmath=True)
def encode_phase(centroids, maxz=50, phaseres=8):
    """
    Encode the charge phases for a set of centroids
    :param centroids: Centroids (m/z, intensity)
    :param maxz: Maximum charge state to calculate
    :param phaseres: Resolution of phases to encode in number of bins
    :return: Charge phase histogram (maxz x phaseres)
    """
    phases = np.zeros((maxz, phaseres))
    rescale = centroids[:, 0] / mass_diff_c
    #nhits = np.zeros((maxz, phaseres))
    for i in range(maxz):
        phase = (rescale * (i + 1)) % 1  # Note, this is a much simpler implementation, needs different model
        phaseindexes = np.floor(phase * phaseres)
        for j in range(len(centroids)):
            phases[i, int(phaseindexes[j])] += centroids[j, 1]
            #nhits[i, int(phaseindexes[j])] += 1
    #phases /= nhits
    phases /= np.amax(phases)
    return phases


@njit(fastmath=True)
def encode_phase_all(centroids, peaks, lowmz=-1.5, highmz=5.5, phaseres=8, minpeaks=3, datathresh=0.05):
    """
    Work on speeding this up
    :param centroids:
    :param peaks:
    :param lowmz:
    :param highmz:
    :return:
    """
    goodpeaks = []
    encodingcentroids = []
    outcentroids = []
    indexes = []
    indexvalues = np.arange(len(centroids))

    for i, p in enumerate(peaks):
        peakmz = p[0]
        # Find all centroids in the neighborhood of the peak
        start = fastnearest(centroids[:, 0], peakmz + lowmz)
        end = fastnearest(centroids[:, 0], peakmz + highmz) + 1

        if i < len(peaks)-1:
            nextpeak = peaks[i+1][0]
            nextindex = fastnearest(centroids[:, 0], nextpeak)
            if end >= nextindex:
                end = nextindex

        if end - start < minpeaks:
            continue
        c = centroids[start:end]
        new_c = centroids[start:end]
        if datathresh > 0:
            b1 = c[:,1]> (datathresh * np.amax(c[:,1]))
            new_c = c[b1]

            if len(c) < minpeaks:
                continue

        encodingcentroids.append(new_c)
        goodpeaks.append(p)
        outcentroids.append(c)
        indexes.append(indexvalues[start:end])

    emats = [encode_phase(c, phaseres=phaseres) for c in encodingcentroids]
    return emats, goodpeaks, outcentroids, indexes


@njit(fastmath=True)
def encode_noise(peakmz: float, intensity: float, maxlen=16, phaseres=8):
    mznoise = np.random.uniform(peakmz - 1.5, peakmz + 3.5, maxlen)
    intnoise = np.abs(np.random.normal(0, intensity, maxlen))

    ndata = np.empty((maxlen, 2))
    ndata[:, 0] = mznoise
    ndata[:, 1] = intnoise
    emat = encode_phase(ndata, phaseres=phaseres)
    return emat, ndata, 0


@njit(fastmath=True)
def encode_double(centroid, centroid2, maxdist=1.5, minsep=0.1, intmax=0.2, phaseres=8):
    peakmz = centroid[np.argmax(centroid[:, 1]), 0]
    peakmz2 = centroid2[np.argmax(centroid2[:, 1]), 0]

    # Move peak2 to a random spot around peak1
    shift = minsep + np.random.uniform(-1, 1) * maxdist
    centroid2[:, 0] += peakmz + shift - peakmz2

    # Set into to random value between 0.05 and 0.95% of the max
    centroid2[:, 1] *= np.random.uniform(0.05, intmax) * np.amax(centroid[:, 1]) / np.amax(centroid2[:, 1])

    mergedc = np.empty((len(centroid) + len(centroid2), 2))
    mergedc[:len(centroid)] = centroid
    mergedc[len(centroid):] = centroid2

    emat = encode_phase(mergedc, phaseres=phaseres)

    return emat, mergedc

@njit(fastmath=True)
def encode_harmonic(centroid, z, intmax=0.2, phaseres=8):
    peakmz = centroid[np.argmax(centroid[:, 1]), 0]
    mzshift = 0.5 / float(z)

    centroid2 = centroid.copy()
    centroid2[:, 0] += mzshift

    # Set into to random value between 0.05 and 0.95% of the max
    centroid2[:, 1] *= np.random.uniform(0.05, intmax) * np.amax(centroid[:, 1]) / np.amax(centroid2[:, 1])

    mergedc = np.empty((len(centroid) + len(centroid2), 2))
    mergedc[:len(centroid)] = centroid
    mergedc[len(centroid):] = centroid2

    emat = encode_phase(mergedc, phaseres=phaseres)

    return emat, mergedc


def encode_phase_file(file, maxlen=8, save=True, outdir="C:\\Data\\IsoNN\\multi", name="medium",
                      onedropper=0.95):
    training = []
    test = []
    zdist = []
    # Load pkl file
    if "peaks.pkl" in file:
        return training, test, zdist

    try:
        with open(file, "rb") as f:
            centroids = pkl.load(f)
    except Exception as e:
        print("Error Loading File:", file, e)
        return training, test, zdist
    # Encode each centroid
    print("File:", file, len(centroids))
    for c in centroids:
        centroid = c[0]
        z = c[1]
        if z == 1:
            # toss it out with a 80% chance
            r = np.random.rand()
            if r < onedropper:
                continue
        zdist.append(z)
        emat = encode_phase(centroid, phaseres=maxlen)
        # emat.astype(np.float32)
        emat = torch.as_tensor(emat, dtype=torch.float32)

        # randomly sort into training and test data
        r = np.random.rand()
        if r < 0.9:
            training.append((emat, centroid, z))
        else:
            test.append((emat, centroid, z))
    return training, test, zdist


data_dirs = ["MSV000090488",
             "MSV000091923",
             "RibosomalPfms_Td_Control",
             "PXD045560",
             "PXD046651",
             "PXD027650",
             "PXD041357",
             "PXD042921"
             ]

small_data_dirs = ["MSV000090488",
                   "PXD019247",
                   "PXD045560",
                   ]

if __name__ == "__main__":
    starttime = time.perf_counter()
    # outdir = "C:\\Data\\IsoNN\\multi"
    # file = "C:\\Data\\TabbData\\20170105_L_MaD_ColC4_Ecoli20161108-10_01_10.pkl"
    # file = "Z:\\Group Share\\JGP\\MSV000090488\\20220207_UreaExtracted_SW480_C4_RPLC_01.pkl"
    # directory = "Z:\\Group Share\\JGP\\MSV000090488\\"
    # directory = "Z:\\Group Share\\JGP\\MSV000091923"
    # directory = "Z:\\Group Share\\JGP\\RibosomalPfms_Td_Control"
    # directory = "Z:\\Group Share\\JGP\\PXD019247"
    # os.chdir(directory)
    # directory = "C:\\Data\\TabbData\\"
    # outdir = "C:\\Data\\IsoNN\\training\\MSV000090488\\"

    for d in data_dirs:
        topdir = os.path.join("Z:\\Group Share\\JGP", d)
        outdir = os.path.join("C:\\Data\\IsoNN\\training", d)
        print("Directory:", topdir, "Outdir:", outdir)
        encode_dir(topdir, maxlen=4, name="phase4", onedropper=0.0, maxfiles=None,
                   outdir=outdir)
    # encode_multi_file(file, maxlen=32, nfeatures=2, save=True, name="small32x2")
    print("Time:", time.perf_counter() - starttime)
