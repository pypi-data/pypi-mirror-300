from typing import List, Dict

from .timingLabel import *
from .cutExpansion import *
from .cleanupDangling import *
from ..blif import *


def cutlessEnum(graph: BLIFGraph, params: dict = {}) -> dict:
    labels: Dict[str, TimingLabel] = {}
    signal_to_cuts: Dict[str, List[str]] = {}
    maxLeaves = params.get("maxLeaves", 6)
    maxExpLevel = params.get("maxExpLevel", 2)

    for signal in graph.topological_traversal():
        signal_to_cuts[signal] = []

        if graph.is_ci(signal):
            labels[signal] = TimingLabel(0)
            signal_to_cuts[signal].append([signal])
            continue

        optLabel, bestCut = optCutExpansion(
            graph, labels, signal, maxLeaves, maxExpLevel
        )
        labels[signal] = optLabel
        signal_to_cuts[signal].append(bestCut)

    return cleanupDanglingCuts(signal_to_cuts)


def optCutExpansion(
    graph: BLIFGraph, labels: dict, signal: str, maxLeaves: int, maxExpLevel: int
) -> tuple:
    optimal_timing_label = TimingLabel()
    leaves: List[str] = graph.fanins(signal)  # deep copy
    best_leaves: List[str] = leaves[:]  # deep copy
    curr_expansion_level = 0

    # we should also consider the constants
    while True:
        # we count the number of non-constant leaves
        num_leaves: int = 0
        for f in leaves:
            if f in graph.const0 or f in graph.constant1s():
                continue
            num_leaves += 1

        # we stop when the number of leaves is larger than the limit
        if num_leaves > maxLeaves:
            curr_expansion_level += 1
        else:
            curr_expansion_level = 0

        # break if the expansion level is larger than the limit
        if curr_expansion_level > maxExpLevel:
            break

        arrival_times: List[tuple] = [(labels[leaf], leaf) for leaf in leaves]
        maximum_timing_label, _ = max(arrival_times)

        # we only update the result if the cut is valid (curr_expansion_level = 0)
        if num_leaves <= maxLeaves:
            if optimal_timing_label > maximum_timing_label + 1:
                optimal_timing_label = maximum_timing_label + 1
                # we update the best leaves
                best_leaves = [
                    leaf
                    for leaf in leaves
                    if leaf not in graph.constant0s() and leaf not in graph.constant1s()
                ]

        # can't expand further
        if maximum_timing_label == TimingLabel(0):
            break

        # should we stop?
        done: bool = False

        # we prepare for the next expansion
        leaves_to_expand = set()
        for label, leaf in arrival_times:
            if label == maximum_timing_label:
                # the leaf is on the critical path, but we cannot expand it
                if not graph.has_fanin(leaf):
                    done = True
                    break
                leaves_to_expand.add(leaf)

        if done:
            break

        # we expand the cut
        leaves = expandCut(graph, leaves, leaves_to_expand)

    best_cut = list(best_leaves)[:]  # deep copy
    return optimal_timing_label, best_cut
