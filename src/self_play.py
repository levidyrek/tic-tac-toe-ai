import numpy as np
from src.tic_tac_toe import TicTacToe
from tensorflow import keras

def self_train(games: int, model: keras.Model):
  game = TicTacToe()
  wins = {
    0: 0,
    1: 0,
    -1: 0,
  }
  for _ in range(games):
    game.reset()
    self_play_game(model, game)

    winner = game.get_winner()
    winner = winner if winner is not None else -1
    wins[winner] += 1

    fit_game(model, game)

  total_games = sum(wins.values())
  print('Wins: ', {
    'X': get_percent(wins[0], total_games),
    'O': get_percent(wins[1], total_games),
    'Draw': get_percent(wins[-1], total_games),
  })

def fit_game(model: keras.Model, game: TicTacToe):
  while len(game.plays) > 0:
    play = game.pop_last_play()
    winner = game.get_winner()

    # If current player is not the winner, do not train on this play
    if (winner is not None and game.turn != winner):
      continue

    board = game.board

    # flip the board if player 2 to be consistent with training data
    if game.turn == 1:
      board = np.flip(board, axis=0)

    boards_np = np.array([board], dtype=np.float32)

    (player, row, col) = play
    play_matrix = [
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
    ]
    play_matrix[row][col] = 1

    plays_np = np.array([[play_matrix]], dtype=np.float32)

    # Train the model
    model.fit(
      x={
        'board': boards_np,
      },
      y={
        'play_dist': plays_np,
      },
      batch_size=1,
      epochs=1,
      verbose=0,
    )

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

def get_percent(x, total):
  return f"{x / total * 100}%"
