from flask import Flask, request
from flask import render_template
from flask import jsonify
import json
import os
import sys
import numpy as np
o_path = os.getcwd()
sys.path.append(o_path)
sys.path.append('../')
from scripts import nnetSolve


app = Flask(__name__)


@app.route('/')
def mainPage():
    return render_template('mofang.html')

@app.route('/test')
def mofang3D():
    return render_template('mofang3D.html')


@app.route('/initState', methods=['POST'])
def initState():
    FEToState = [6, 3, 0, 7, 4, 1, 8, 5, 2, 15, 12, 9, 16, 13, 10, 17, 14, 11, 24, 21, 18, 25, 22, 19, 26, 23, 20, 33,
                 30, 27, 34,
                 31, 28, 35, 32, 29, 38, 41, 44, 37, 40, 43, 36, 39, 42, 51, 48, 45, 52, 49, 46, 53, 50, 47]
    legalMoves = ["U_-1", "U_1", "D_-1", "D_1", "L_-1", "L_1", "R_-1", "R_1", "B_-1", "B_1", "F_-1", "F_1"]
    rotateIdxs_new = {
        "B_-1": [36, 37, 38, 38, 41, 44, 44, 43, 42, 42, 39, 36, 2, 5, 8, 35, 34, 33, 15, 12, 9, 18, 19, 20],
        "B_1": [36, 37, 38, 38, 41, 44, 44, 43, 42, 42, 39, 36, 2, 5, 8, 35, 34, 33, 15, 12, 9, 18, 19, 20],
        "D_-1": [9, 10, 11, 11, 14, 17, 17, 16, 15, 15, 12, 9, 18, 21, 24, 36, 39, 42, 27, 30, 33, 45, 48, 51],
        "D_1": [9, 10, 11, 11, 14, 17, 17, 16, 15, 15, 12, 9, 18, 21, 24, 36, 39, 42, 27, 30, 33, 45, 48, 51],
        "F_-1": [45, 46, 47, 47, 50, 53, 53, 52, 51, 51, 48, 45, 0, 3, 6, 24, 25, 26, 17, 14, 11, 29, 28, 27],
        "F_1": [45, 46, 47, 47, 50, 53, 53, 52, 51, 51, 48, 45, 0, 3, 6, 24, 25, 26, 17, 14, 11, 29, 28, 27],
        "L_-1": [18, 19, 20, 20, 23, 26, 26, 25, 24, 24, 21, 18, 0, 1, 2, 44, 43, 42, 9, 10, 11, 45, 46, 47],
        "L_1": [18, 19, 20, 20, 23, 26, 26, 25, 24, 24, 21, 18, 0, 1, 2, 44, 43, 42, 9, 10, 11, 45, 46, 47],
        "R_-1": [27, 28, 29, 29, 32, 35, 35, 34, 33, 33, 30, 27, 6, 7, 8, 51, 52, 53, 15, 16, 17, 38, 37, 36],
        "R_1": [27, 28, 29, 29, 32, 35, 35, 34, 33, 33, 30, 27, 6, 7, 8, 51, 52, 53, 15, 16, 17, 38, 37, 36],
        "U_-1": [0, 1, 2, 2, 5, 8, 8, 7, 6, 6, 3, 0, 20, 23, 26, 47, 50, 53, 29, 32, 35, 38, 41, 44],
        "U_1": [0, 1, 2, 2, 5, 8, 8, 7, 6, 6, 3, 0, 20, 23, 26, 47, 50, 53, 29, 32, 35, 38, 41, 44]}
    rotateIdxs_old = {
        "B_-1": [38, 41, 44, 44, 43, 42, 42, 39, 36, 36, 37, 38, 18, 19, 20, 2, 5, 8, 35, 34, 33, 15, 12, 9],
        "B_1": [42, 39, 36, 36, 37, 38, 38, 41, 44, 44, 43, 42, 35, 34, 33, 15, 12, 9, 18, 19, 20, 2, 5, 8],
        "D_-1": [11, 14, 17, 17, 16, 15, 15, 12, 9, 9, 10, 11, 45, 48, 51, 18, 21, 24, 36, 39, 42, 27, 30, 33],
        "D_1": [15, 12, 9, 9, 10, 11, 11, 14, 17, 17, 16, 15, 36, 39, 42, 27, 30, 33, 45, 48, 51, 18, 21, 24],
        "F_-1": [47, 50, 53, 53, 52, 51, 51, 48, 45, 45, 46, 47, 29, 28, 27, 0, 3, 6, 24, 25, 26, 17, 14, 11],
        "F_1": [51, 48, 45, 45, 46, 47, 47, 50, 53, 53, 52, 51, 24, 25, 26, 17, 14, 11, 29, 28, 27, 0, 3, 6],
        "L_-1": [20, 23, 26, 26, 25, 24, 24, 21, 18, 18, 19, 20, 45, 46, 47, 0, 1, 2, 44, 43, 42, 9, 10, 11],
        "L_1": [24, 21, 18, 18, 19, 20, 20, 23, 26, 26, 25, 24, 44, 43, 42, 9, 10, 11, 45, 46, 47, 0, 1, 2],
        "R_-1": [29, 32, 35, 35, 34, 33, 33, 30, 27, 27, 28, 29, 38, 37, 36, 6, 7, 8, 51, 52, 53, 15, 16, 17],
        "R_1": [33, 30, 27, 27, 28, 29, 29, 32, 35, 35, 34, 33, 51, 52, 53, 15, 16, 17, 38, 37, 36, 6, 7, 8],
        "U_-1": [2, 5, 8, 8, 7, 6, 6, 3, 0, 0, 1, 2, 38, 41, 44, 20, 23, 26, 47, 50, 53, 29, 32, 35],
        "U_1": [6, 3, 0, 0, 1, 2, 2, 5, 8, 8, 7, 6, 47, 50, 53, 29, 32, 35, 38, 41, 44, 20, 23, 26]}
    state = [2, 5, 8, 1, 4, 7, 0, 3, 6, 11, 14, 17, 10, 13, 16, 9, 12, 15, 20, 23, 26, 19, 22, 25, 18, 21, 24, 29, 32,
             35, 28, 31, 34, 27, 30, 33, 42, 39, 36, 43, 40, 37, 44, 41, 38, 47, 50, 53, 46, 49, 52, 45, 48, 51]
    stateToFE = [2, 5, 8, 1, 4, 7, 0, 3, 6, 11, 14, 17, 10, 13, 16, 9, 12, 15, 20, 23, 26, 19, 22, 25, 18, 21, 24, 29,
                 32, 35, 28, 31, 34, 27, 30, 33, 42, 39, 36, 43, 40, 37, 44, 41, 38, 47, 50, 53, 46, 49, 52, 45, 48, 51]
    data = {'FEToState': FEToState, 'legalMoves': legalMoves, 'rotateIdxs_new': rotateIdxs_new,
            'rotateIdxs_old': rotateIdxs_old, 'state': state, 'stateToFE': stateToFE}
    return jsonify(data)


@app.route('/solve', methods=['POST'])
def solve():
    FEToState = [6, 3, 0, 7, 4, 1, 8, 5, 2, 15, 12, 9, 16, 13, 10, 17, 14, 11, 24, 21, 18, 25, 22, 19, 26, 23, 20, 33,
                 30, 27, 34,
                 31, 28, 35, 32, 29, 38, 41, 44, 37, 40, 43, 36, 39, 42, 51, 48, 45, 52, 49, 46, 53, 50, 47]
    # data = request.get_data()
    # print(data)
    stateUnicode = request.form.get('state')
    print(stateUnicode)
    stateStr = stateUnicode.encode('utf-8')
    # print(type(stateStr))
    stateStr = stateStr.replace("[", "")
    stateStr = stateStr.replace("]", "")
    # print(stateStr)
    stateSpilt = stateStr.split(",")
    stateArray = []
    for stickers in stateSpilt:
        stateArray.append(int(stickers))
    print(stateArray)
    print(len(stateArray))
    stateArray2 = reOrderArray(stateArray, FEToState)
    state = np.array(stateArray2)
    soln = nnetSolve.solve(state)
    # moves = ["U_-1", "R_1", "B_1", "F_1", "U_1", "U_1", "F_1", "U_-1", "B_1", "D_1", "U_-1", "B_-1", "U_1", "L_1",
    #          "D_1", "L_-1", "U_-1", "F_-1", "R_1", "D_1", "D_1", "R_-1", "U_-1", "R_1", "D_-1"]
    moves = []
    moves_rev = []
    solve_text = []
    for step in soln:
        if step[1] == -1:
            moves.append(step[0] + "_-1")
            moves_rev.append(step[0] + "_1")
            solve_text.append(step[0] + "'")
        else:
            moves.append(step[0] + "_1")
            moves_rev.append(step[0] + "_-1")
            solve_text.append(step[0])
    data = {'moves': moves, 'moves_rev': moves_rev, 'solve_text': solve_text}
    return jsonify(data)


@app.route('/a', methods=['GET'])
def test():
    stateArray = [33, 16, 38, 3, 4, 41, 29, 10, 24, 51, 1, 18, 34, 13, 12, 2, 52, 26, 36, 50, 6, 32, 22, 14, 44, 37, 27, 45, 5, 8, 43, 31, 25, 42, 39, 0, 20, 28, 47, 7, 40, 46, 15, 30, 35, 53, 21, 11, 48, 49, 19, 17, 23, 9]
    state = np.array(stateArray)
    res = nnetSolve.solve(state)
    return "a"


def reOrderArray(arr, indecies):
    temp = []
    for i in range(len(indecies)):
        index = indecies[i]
        temp.append(arr[index])
    return temp


if __name__ == '__main__':
    app.run()
