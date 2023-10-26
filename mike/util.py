"""
UNIVERSITY OF QUEENSLAND TEAM PROJECT 2 2023
Author: Michael Smith 
Student Number: 45838464 
DATE: 06/08/2023
"""


class Artwork:
    """ Class to hold segments """
    def __init__(self):
        self.segments = []


def greatest_common_divisor(a, b):
    while b:
        a, b = b, a % b
    return a
        



