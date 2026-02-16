import cProfile
import pstats

import swopy

previous_system = swopy.systems.arabic.Arabic
numeral = 10

with cProfile.Profile() as pr:
    for _, system in swopy.get_all_systems().items():
        for _ in range(1000):
            numeral = swopy.swop(numeral, previous_system, system)
            previous_system = system

    stats = pstats.Stats(pr)
    stats.sort_stats("tottime").print_stats(50)
