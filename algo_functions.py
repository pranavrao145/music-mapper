"""Functions for calculating edge weights between two songs.
NOTE: lower level functions here may be moved to other files (caculate_edge_weight may be moved to
the importing function after it's implemented, for example.)"""

from Song import Song
import math


def calculate_edge_weight(song1: Song, song2: Song) -> float:
    """When given two song objects, return a float value that represents the weight of the edge between the two.
    The weight represents the similarity between the songs and is calculated through the numerical traits.
    This implementation uses the Euclidean distance. For ML possibilities (i.e. curating the algorithm to match
    the user's preferences), look into Minkowski distance:
    machinelearningmastery.com/distance-measures-for-machine-learning/

    NOTE: normalization/standardization can be implemented in this function OR it can be a calculation that
    is done at the time of encoding the Songs i.e. processing the numerical traits before storing it in Song,
    such that the numerical values of the songs are already normalized/standardized
    Source of normalization/standardization here:
    towardsai.net/p/data-science/how-when-and-why-should-you-normalize-standardize-rescale-your-data-3f083def38ff

    Postcondition:
    - returns a float value between 0 and 1; the higher this value is, the closer they are to each other
    """
    # TODO: determine if this retains the order of variables. If not, numerical_traits must be list and not dict
    v1 = list(song1.numerical_traits.values())
    v2 = list(song2.numerical_traits.values())

    # TODO: STANDARDIZE THE VECTORS FIRST (will need information on the whole dataset)

    # normalization (might be moved elsewhere)
    norm1 = normalize(v1)
    norm2 = normalize(v2)

    # Euclidean distance calculation; function call should return a value b/w 0 and 1
    # '1 -' is added so that the higher the distance, the lesser the difference
    return 1 - euclidean_distance(norm1, norm2)


def normalize(v: list[float]) -> list[float]:
    """Returns the input vector normalized (by Euclidean form). The result should have length 1"""
    norm = euclidean_distance(v, v)
    return [variable / norm for variable in v]


def euclidean_distance(v1: list[float], v2: list[float]) -> float:
    """Returns the Euclidean distance/inner product between the two input vectors."""
    total = sum((v1[i] - v2[i]) ** 2 for i in range(0, len(v1)))
    return total ** (1 / 2)
