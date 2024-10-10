import itertools


def transpose(lines: list[list[str]]) -> list[list[str]]:
    return list(map(list, itertools.zip_longest(*lines, fillvalue="")))
