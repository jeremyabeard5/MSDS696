# itertest.py

from itertools import combinations, permutations

locations = ['Location1', 'Location2']

for locationA, locationB in permutations(locations):
   print(f'LocationA: {locationA}, LocationB: {locationB}')
   
def find_pairs(location_list):
    pairs = []
    locations_reversed = location_list[::-1]
    pairs = list(combinations(location_list, 2))
    reversed_pairs = list(combinations(locations_reversed, 2))
    pairs.extend(reversed_pairs)
    return pairs


print(f'Pairs: {find_pairs(locations)}')
