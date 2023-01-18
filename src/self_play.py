import numpy as np
from src.tic_tac_toe import TicTacToe
from tensorflow import keras

def self_play_game(model: keras.Model, game: TicTacToe):
    while not game.is_over():
        next_play = get_next_play(model, game)
        game.play(next_play['row'], next_play['col'])

def get_next_play(model: keras.Model, game: TicTacToe):
    board = game.board

    # flip the board if player 2 to be consistent with training data
    if game.turn == 1:
        board = np.flip(board, axis=0)

    legal_plays = game.get_legal_plays()
    if len(legal_plays) == 0:
        return None

    legal_plays_matrix = game.get_legal_plays_matrix()

    boards = np.array([board])
    prediction = model({'board': boards})

    play_dists = prediction[0][0]
    suggested_move = {
        'row': legal_plays[0][0],
        'col': legal_plays[0][1],
        'probability': 0,
    }
    for rowIndex, row in enumerate(play_dists):
        for colIndex, col in enumerate(row):
            if legal_plays_matrix[rowIndex][colIndex] == 1 and col > suggested_move['probability']:
                suggested_move['row'] = rowIndex
                suggested_move['col'] = colIndex
                suggested_move['probability'] = col

    return suggested_move
