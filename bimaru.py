# -*- coding: utf-8 -*-

from BacktrackingBimaruSolver import BacktrackingBimaruSolver
import time
import string
import math
from random import randrange
from itertools import chain
import constraint as csp
import sys
sys.path.append("./python-constraint-1.2")

# ------------------------------------------------------------------------------
# Bimaru to solve (add "0" where no number is given)
# ------------------------------------------------------------------------------

debugAssigned = False

bow_up = 1
bow_right = 2
bow_down = 3
bow_left = 4
center = 5
single = 6
water = 7

# puzzle from instructions
# puzzle = [
#     [0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 5, 0, 0],
#     [0, 7, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0],
#     [0, 1, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0],
# ]

# parts_in_row = [3, 2, 2, 0, 2, 1]
# parts_in_col = [0, 4, 0, 3, 1, 2]

# target_boat_single = 3
# target_boat_double = 2
# target_boat_triple = 1
# target_boat_quadrouple = 0

# Solution to instruction puzzle
# solution = [
#     [7, 1, 7, 1, 7, 6],
#     [7, 3, 7, 5, 7, 7],
#     [7, 7, 7, 3, 7, 6],
#     [7, 7, 7, 7, 7, 7],
#     [7, 1, 7, 7, 6, 7],
#     [7, 3, 7, 7, 7, 7],
# ]

# "Easy" puzzle
puzzle = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 3, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 6, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

# solution = [
#     [7, 7, 7, 7, 6, 7, 4, 2],
#     [7, 7, 1, 7, 7, 7, 7, 7],
#     [6, 7, 3, 7, 7, 4, 5, 2],
#     [7, 7, 7, 7, 7, 7, 7, 7],
#     [7, 7, 7, 7, 6, 7, 7, 7],
#     [4, 5, 2, 7, 7, 7, 4, 2],
#     [7, 7, 7, 7, 7, 7, 7, 7],
#     [7, 6, 7, 4, 5, 5, 2, 7],
# ]
# puzzle = solution

parts_in_row = [3, 1, 5, 0, 1, 5, 0, 5]
parts_in_col = [2, 2, 3, 1, 3, 2, 4, 3]

target_boat_single = 4
target_boat_double = 3
target_boat_triple = 2
target_boat_quadrouple = 1


# "Hard" 8x8 puzzle
# puzzle = [
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 6, 0, 0, 0, 0, 0],
#     [3, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 3, 0, 0],
# ]

# solution = [
#     [1, 0, 0, 0, 4, 2, 0, 1],
#     [5, 0, 6, 0, 0, 0, 0, 3],
#     [3, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 4, 5, 5, 2, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [4, 5, 2, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 0, 6],
#     [6, 0, 6, 0, 0, 3, 0, 0],
# ]
# puzzle = solution

# parts_in_row = [4, 3, 1, 4, 0, 3, 2, 3]
# parts_in_col = [5, 1, 3, 1, 2, 4, 1, 3]

# target_boat_single = 4
# target_boat_double = 3
# target_boat_triple = 2
# target_boat_quadrouple = 1

# "Hard" 10x10 puzzle
# puzzle = [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 6, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 5, 0, 0],
#     [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
# ]

# solution = [
#     [7, 7, 7, 7, 7, 7, 7, 7, 7, 1],
#     [7, 7, 7, 7, 7, 7, 7, 6, 7, 3],
#     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
#     [7, 7, 4, 5, 2, 7, 7, 7, 7, 7],
#     [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
#     [7, 7, 6, 7, 7, 7, 7, 7, 7, 1],
#     [6, 7, 7, 7, 7, 7, 7, 1, 7, 5],
#     [7, 7, 7, 7, 7, 6, 7, 5, 7, 3],
#     [7, 4, 2, 7, 7, 7, 7, 5, 7, 7],
#     [7, 7, 7, 7, 4, 2, 7, 3, 7, 7],
# ]
# puzzle = solution

# parts_in_row = [1, 2, 0, 3, 0, 2, 3, 3, 3, 3]
# parts_in_col = [1, 1, 3, 1, 2, 2, 0, 5, 0, 5]

# target_boat_single = 4
# target_boat_double = 3
# target_boat_triple = 2
# target_boat_quadrouple = 1


parts = [
    bow_up,
    bow_right,
    bow_down,
    bow_left,
    center,
    single,
]

targetBoatTypes = {
    1: target_boat_single,
    2: target_boat_double,
    3: target_boat_triple,
    4: target_boat_quadrouple,
}

numberOfRows = len(puzzle)
numberOfColumns = len(puzzle[0])

rownames = list(range(numberOfRows))
colnames = [*string.ascii_letters[0:numberOfColumns]]

rows = []
for i in rownames:
    row = []
    for j in colnames:
        row.append(j+str(i))
    rows.append(row)

cols = []
for j in colnames:
    col = []
    cols.append(col)
    for i in rownames:
        col.append(j+str(i))

flatVariables = list(chain.from_iterable(rows))

boxes = []

for i in range(numberOfRows-2):
    for j in range(numberOfColumns-2):
        box = []
        for rowi in range(3):
            for coli in range(3):
                box.append(rows[i+rowi][j+coli])
        boxes.append(box)

border_boxes_left = []
for i in range(numberOfRows-2):
    box = []
    for j in range(3):
        box.append(rows[i+j][0])
        box.append(rows[i+j][1])
    border_boxes_left.append(box)

border_boxes_right = []
for i in range(numberOfRows-2):
    box = []
    for j in range(3):
        box.append(rows[i+j][numberOfColumns-2])
        box.append(rows[i+j][numberOfColumns-1])
    border_boxes_right.append(box)

border_boxes_top = []
for i in range(numberOfColumns-2):
    box = []
    for j in range(3):
        box.append(rows[0][i+j])
        box.append(rows[1][i+j])
    border_boxes_top.append(box)

border_boxes_bottom = []
for i in range(numberOfColumns-2):
    box = []
    for j in range(3):
        box.append(rows[numberOfRows-2][i+j])
        box.append(rows[numberOfRows-1][i+j])
    border_boxes_bottom.append(box)

corner_top_left_box = [
    rows[0][0],
    rows[0][1],
    rows[1][0],
    rows[1][1],
]

corner_top_right_box = [
    rows[0][len(cols)-2],
    rows[0][len(cols)-1],
    rows[1][len(cols)-2],
    rows[1][len(cols)-1],
]

corner_bottom_left_box = [
    rows[len(rows)-2][0],
    rows[len(rows)-2][1],
    rows[len(rows)-1][0],
    rows[len(rows)-1][1],
]

corner_bottom_right_box = [
    rows[len(rows)-2][len(cols)-2],
    rows[len(rows)-2][len(cols)-1],
    rows[len(rows)-1][len(cols)-2],
    rows[len(rows)-1][len(cols)-1],
]

# ----- Lookup table for bimaru solver -----
neighbourLookupTable = {}
for box in boxes:
    neighbourLookupTable[box[4]] = [*box[0:4], *box[5:]]

# borders
for box in border_boxes_top:
    neighbourLookupTable[box[2]] = [*box[0:2], *box[3:]]

for box in border_boxes_right:
    neighbourLookupTable[box[3]] = [*box[0:3], *box[4:]]

for box in border_boxes_bottom:
    neighbourLookupTable[box[3]] = [*box[0:3], *box[4:]]

for box in border_boxes_left:
    neighbourLookupTable[box[2]] = [*box[0:2], *box[3:]]

# corners
neighbourLookupTable[corner_top_left_box[0]] = [*corner_top_left_box[1:]]
neighbourLookupTable[corner_top_right_box[1]] = [*corner_top_right_box[0:1], *corner_top_right_box[2:]]
neighbourLookupTable[corner_bottom_left_box[2]] = [*corner_bottom_left_box[0:2], *corner_bottom_left_box[3:]]
neighbourLookupTable[corner_bottom_right_box[3]] = [*corner_bottom_right_box[0:3]]

# ------------------------------------------------------------------------------
# formulate bimaru as CSP
# ------------------------------------------------------------------------------
bimaru = csp.Problem(BacktrackingBimaruSolver(neighbourLookupTable))

for i, row in enumerate(rows):
    for j, col in enumerate(row):
        bimaru.addVariable(col,
                           list(range(1, 8)) if puzzle[i][j] == 0 else [puzzle[i][j]])


def getNumberOfPartsConstraint(exactNumberOfParts, rowIndex=-1, colIndex=-1):
    def constraint(*args, assignments=None, _unassigned=csp.Unassigned):
        numberOfParts = 0
        anyUnassigned = False

        for value in args:
            if (value == _unassigned):
                anyUnassigned = True
            numberOfParts += 1 if value in parts else 0

        unassignedAndOk = anyUnassigned and numberOfParts <= exactNumberOfParts
        exact = not anyUnassigned and numberOfParts == exactNumberOfParts
        if unassignedAndOk or exact:
            return True
        else:
            return False

    return constraint


def noNeighbourConstraintFunction(a, b, c, d, e, f, g, h, i, assignments=None, _unassigned=csp.Unassigned):
    if (e == single):
        water_values = [a, b, c, d, f, g, h, i]
        for value in water_values:
            if value != water and value != _unassigned:
                return False

    if (e == bow_up):
        if (h not in (bow_down, center, _unassigned)):
            return False
        water_values = [a, b, c, d, f, g, i]
        for value in water_values:
            if value != water and value != _unassigned:
                return False

    if (e == bow_down):
        if (b not in (bow_up, center, _unassigned)):
            return False
        water_values = [a, c, d, f, g, h, i]
        for value in water_values:
            if value != water and value != _unassigned:
                return False

    if (e == bow_left):
        if (f not in (bow_right, center, _unassigned)):
            return False
        water_values = [a, b, c, d, g, h, i]
        for value in water_values:
            if value != water and value != _unassigned:
                return False

    if (e == bow_right):
        if (d not in (bow_left, center, _unassigned)):
            return False
        water_values = [a, b, c, f, g, h, i]
        for value in water_values:
            if value != water and value != _unassigned:
                return False
    
    if (e == center):

        if b in (bow_up, center) and (
            d not in (water, _unassigned) 
            or f not in (water, _unassigned)
            or h == water
        ):
            return False

        if h in (bow_down, center) and (
            d not in (water, _unassigned)
            or f not in (water, _unassigned)
            or b == water
            ):
            return False

        if d in (bow_left, center) and (
            b not in (water, _unassigned) 
            or h not in (water, _unassigned)
            or f == water
        ):
            return False

        if f in (bow_right, center) and (
            b not in (water, _unassigned) 
            or h not in (water, _unassigned)
            or d == water
        ):
            return False

        water_values = [a, c, g, i]
        for value in water_values:
            if value != water and value != _unassigned:
                return False

    return True


def borderTopConstraintFunction(a1, a2, b1, b2, c1, c2, assignments=None, _unassigned=csp.Unassigned):
    if b1 == bow_down:
        return False

    if (not noNeighbourConstraintFunction(7, 7, 7, a1, b1, c1, a2, b2, c2, _unassigned)):
        return False

    return True


def borderBottomConstraintFunction(a1, a2, b1, b2, c1, c2, assignments=None, _unassigned=csp.Unassigned):
    if b2 == bow_up:
        return False

    if (not noNeighbourConstraintFunction(a1, b1, c1, a2, b2, c2, 7, 7, 7, _unassigned)):
        return False

    return True


def borderLeftConstraintFunction(a1, b1, a2, b2, a3, b3, assignments=None, _unassigned=csp.Unassigned):
    if a2 == bow_right:
        return False

    if (not noNeighbourConstraintFunction(7, a1, b1, 7, a2, b2, 7, a3, b3, _unassigned)):
        return False

    return True


def borderRightConstraintFunction(a1, b1, a2, b2, a3, b3, assignments=None, _unassigned=csp.Unassigned):
    if b2 == bow_left:
        return False

    if (not noNeighbourConstraintFunction(a1, b1, 7, a2, b2, 7, a3, b3, 7, _unassigned)):
        return False

    return True


for rowIndex, numberOfParts in enumerate(parts_in_row):
    row = rows[rowIndex]
    constraint = csp.FunctionConstraint(getNumberOfPartsConstraint(
        numberOfParts, rowIndex=rowIndex), assigned=debugAssigned)
    bimaru.addConstraint(constraint, row)

for colIndex, numberOfParts in enumerate(parts_in_col):
    col = cols[colIndex]
    constraint = csp.FunctionConstraint(getNumberOfPartsConstraint(
        numberOfParts, colIndex=colIndex), assigned=debugAssigned)
    bimaru.addConstraint(constraint, col)

noNeighbourConstraint = csp.FunctionConstraint(
    noNeighbourConstraintFunction, assigned=debugAssigned)
for box in boxes:
    bimaru.addConstraint(noNeighbourConstraint, box)


borderTopConstraint = csp.FunctionConstraint(
    borderTopConstraintFunction, assigned=debugAssigned)
for box in border_boxes_top:
    bimaru.addConstraint(borderTopConstraint, box)

borderBottomConstraint = csp.FunctionConstraint(
    borderBottomConstraintFunction, assigned=debugAssigned)
for box in border_boxes_bottom:
    bimaru.addConstraint(borderBottomConstraint, box)

borderLeftConstraint = csp.FunctionConstraint(
    borderLeftConstraintFunction, assigned=debugAssigned)
for box in border_boxes_left:
    bimaru.addConstraint(borderLeftConstraint, box)

borderRightConstraint = csp.FunctionConstraint(
    borderRightConstraintFunction, assigned=debugAssigned)
for box in border_boxes_right:
    bimaru.addConstraint(borderRightConstraint, box)


def cornerTopLeftConstraintFunction(b2, c2, b3, c3, assignments=None, _unassigned=csp.Unassigned):
    if b2 in (bow_right, bow_down, center):
        return False

    if (not noNeighbourConstraintFunction(7, 7, 7, 7, b2, c2, 7, b3, c3, _unassigned)):
        return False

    return True


def cornerTopRightConstraintFunction(a2, b2, a3, b3, assignments=None, _unassigned=csp.Unassigned):
    if b2 in (bow_left, bow_down, center):
        return False

    if (not noNeighbourConstraintFunction(7, 7, 7, a2, b2, 7, a3, b3, 7, _unassigned)):
        return False

    return True


def cornerBottomRightConstraintFunction(a1, b1, a2, b2, assignments=None, _unassigned=csp.Unassigned):
    if b2 in (bow_left, bow_up, center):
        return False

    if (not noNeighbourConstraintFunction(a1, b1, 7, a2, b2, 7, 7, 7, 7, _unassigned)):
        return False

    return True


def cornerBottomLeftConstraintFunction(b1, c1, b2, c2, assignments=None, _unassigned=csp.Unassigned):
    if b2 in (bow_right, bow_down, center):
        return False

    if (not noNeighbourConstraintFunction(7, b1, c1, 7, b2, c2, 7, 7, 7, _unassigned)):
        return False

    return True


                     
def cornerTopRightConstraintFunction(a2, b2, a3, b3, assignments=None, _unassigned=csp.Unassigned):
    if b2 in (bow_left, bow_down, center):
        return False

    if (not noNeighbourConstraintFunction(7, 7, 7, a2, b2, 7, a3, b3, 7, _unassigned)):
        return False

    return True


cornerTopLeftConstraint = csp.FunctionConstraint(
    cornerTopLeftConstraintFunction, assigned=debugAssigned)
bimaru.addConstraint(cornerTopLeftConstraint, corner_top_left_box)

cornerTopRightConstraint = csp.FunctionConstraint(
    cornerTopRightConstraintFunction, assigned=debugAssigned)
bimaru.addConstraint(cornerTopRightConstraint, corner_top_right_box)

cornerBottomRightConstraint = csp.FunctionConstraint(
    cornerBottomRightConstraintFunction, assigned=debugAssigned)
bimaru.addConstraint(cornerBottomRightConstraint, corner_bottom_right_box)

cornerBottomLeftConstraint = csp.FunctionConstraint(
    cornerBottomLeftConstraintFunction, assigned=debugAssigned)
bimaru.addConstraint(cornerBottomLeftConstraint, corner_bottom_left_box)

def partTypeCountConstraintFunction(*args, assignments=None, _unassigned=csp.Unassigned):
    count_bow_up = args.count(bow_up)
    count_bow_right = args.count(bow_right)
    count_bow_down = args.count(bow_down)
    count_bow_left = args.count(bow_left)
    count_boat_single = args.count(single)
    count_unassigned = args.count(_unassigned)
    count_centers = args.count(center)

    target_nr_big_boats = target_boat_double + \
        target_boat_triple + target_boat_quadrouple
    target_centers = target_boat_triple + 2*target_boat_quadrouple

    if (count_bow_up + count_bow_left) > target_nr_big_boats:
        return False
    if (count_bow_down + count_bow_right) > target_nr_big_boats:
        return False

    if (count_boat_single > target_boat_single):
        return False

    if count_centers > target_centers:
        return False

    if count_unassigned == 0:
        if (count_bow_up + count_bow_left) != target_nr_big_boats:
            return False
        if count_centers != target_centers:
            return False

        if count_bow_up != count_bow_down or count_bow_left != count_bow_right:
            return False

    return True


partTypeCountConstraint = csp.FunctionConstraint(
    partTypeCountConstraintFunction, assigned=debugAssigned)
bimaru.addConstraint(partTypeCountConstraint, flatVariables)


def boatTypeCountConstraintFunction(*args, assignments=None, _unassigned=csp.Unassigned):
    boatTypes = {}
    anyBoatIncomplete = False

    for i, value in enumerate(args):
        colIndex = i % len(cols)
        rowIndex = int(i / len(cols))
        boatLength = 0

        if value == bow_up:
            for j in range(1, 4):
                if i + j*len(cols) > len(args)-1:
                    return False

                field = args[i + j*len(cols)]
                if field in [center, bow_down]:
                    if field == bow_down:
                        boatLength = j+1
                        break
                else:
                    anyBoatIncomplete = True
                    break

        if value == bow_left:
            for j in range(1, 4):
                if colIndex + j > len(cols)-1:
                    return False

                field = args[i + j]
                if field in [center, bow_right]:
                    if field == bow_right:
                        boatLength = j+1
                        break
                else:
                    anyBoatIncomplete = True
                    break

        if value == single:
            boatLength = 1

        if boatLength != 0:
            boatTypes[boatLength] = boatTypes.get(boatLength, 0) + 1

    if args.count(_unassigned) == 0:
        if len(boatTypes) != len(targetBoatTypes) or anyBoatIncomplete:
            return False
        for boatType, count in boatTypes.items():
            if targetBoatTypes[boatType] != count:
                return False
    else:
        for boatType, count in boatTypes.items():
            if boatType not in targetBoatTypes:
                return False

            if targetBoatTypes[boatType] < count:
                return False

    return True

boatTypeCountConstraint = csp.FunctionConstraint(
    boatTypeCountConstraintFunction, assigned=debugAssigned)
bimaru.addConstraint(boatTypeCountConstraint, flatVariables)

# ------------------------------------------------------------------------------
# solve CSP
# ------------------------------------------------------------------------------
start_time = time.time()
solutions = bimaru.getSolutions()

# solutions = [solutions[randrange(len(solutions)-1)]]
# solutions = [bimaru.getSolution()]

print('')
print('Time taken:')
print(f"--- {time.time() - start_time} seconds ---")

print('')
print(f'Number of solutions found: {len(solutions)}')

part_map = {
    1: '∩',
    2: '⊃',
    3: '∪',
    4: '⊂',
    5: '□',
    6: '○',
    7: '░',
}

for solution in solutions:
    col_count = len(cols)
    row_count = len(cols)
    h_length = (4*col_count)-1
    space_between_cols = math.floor((h_length)/2)

    print('')
    print('┌' + space_between_cols*'─' + '┬' + space_between_cols*'─' + '┐')
    for i, row in enumerate(rows):
        for j, col in enumerate(row):
            print(
                (" " if j > 0 else "") + \
                ("| " if j % (col_count/2) == 0 else "  ") + \
                str(part_map[solution[col]]) \
            , end="")
        print(' |')
        if i == math.floor(row_count/2) - 1:
            print('├' + space_between_cols*'─' + '┼' + space_between_cols*'─' + '┤')
        elif i < row_count-1:
            print('│' + space_between_cols*' ' + '│' + space_between_cols*' ' + '│')
    print('└' + space_between_cols*'─' + '┴' + space_between_cols*'─' + '┘')

    # break
