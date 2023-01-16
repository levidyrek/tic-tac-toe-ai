class TicTacToe:
  def __init__(self):
    self.board = [[
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
    ], [
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
    ]]
    self.turn = 0

  def __str__(self) -> str:
    result = []
    for rowIndex in range(3):
      row = []
      for colIndex in range(3):
        p1 = self.board[0][rowIndex][colIndex]
        p2 = self.board[1][rowIndex][colIndex]

        if p1:
          row.append('X')
        elif p2:
          row.append('O')
        else:
          row.append('_')

      result.append(' | '.join(row))

    return '\n'.join(result)

  def reset(self):
    self.board = [[
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
    ], [
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
    ]]
    self.turn = 0

  def play(self, row: int, col: int) -> bool:
    opponent = 1 - self.turn
    if self.board[self.turn][row][col] or self.board[opponent][row][col]:
      return False

    self.board[self.turn][row][col] = 1
    self.turn = opponent
    return True

  def get_winner(self) -> int or None:
    for player in range(2):
      for rowIndex in range(3):
        if self.board[player][rowIndex][0] and self.board[player][rowIndex][1] and self.board[player][rowIndex][2]:
          return player

      for colIndex in range(3):
        if self.board[player][0][colIndex] and self.board[player][1][colIndex] and self.board[player][2][colIndex]:
          return player

      if self.board[player][0][0] and self.board[player][1][1] and self.board[player][2][2]:
        return player

      if self.board[player][0][2] and self.board[player][1][1] and self.board[player][2][0]:
        return player

    return None

  def is_over(self) -> bool:
    for rowIndex in range(3):
      for colIndex in range(3):
        if not (self.board[0][rowIndex][colIndex] or self.board[1][rowIndex][colIndex]):
          return False

    return True

  def get_legal_plays(self) -> list:
    moves = []
    for rowIndex in range(3):
      for colIndex in range(3):
        if not (self.board[0][rowIndex][colIndex] or self.board[1][rowIndex][colIndex]):
          moves.append((rowIndex, colIndex))

    return moves
