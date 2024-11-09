from flask import Flask, jsonify, request

app = Flask(__name__)

ROWS, COLS = 6, 7
PLAYER1, PLAYER2 = 'red', 'yellow'
EMPTY = '⚪'
PIECES = {'red': '🔴', 'yellow': '🟡'}

class thing:
    def __init__(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = PLAYER1
        self.winner = None
    
    def reset(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = PLAYER1
        self.winner = None

    def droppiece(self, col):
        if self.winner or col < 0 or col >= COLS:
            return False
        row = self.rowsearch(col)
        if row is None:
            return False
        self.board[row][col] = PIECES[self.current_player]
        if self.wincheck(row, col):
            self.winner = self.current_player
        else:
            self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1
        return True

    def rowsearch(self, col):
        for row in reversed(range(ROWS)):
            if self.board[row][col] == EMPTY:
                return row
        return None

    def wincheck(self, row, col):
        piece = PIECES[self.current_player]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            if self.countconsc(row, col, dr, dc) >= 4:
                return True
        return False

    def countconsc(self, row, col, dr, dc):
        piece = PIECES[self.current_player]
        count = 0
        for i in range(-3, 4):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == piece:
                count += 1
                if count == 4:
                    return count
            else:
                count = 0
        return count

    def autowin(self):
        self.winner = self.current_player
        for row in range(ROWS-1, -1, -1):
            if self.board[row][0] == EMPTY:
                self.board[row][0] = PIECES[self.current_player]
            if row <= ROWS-4:
                break

game = thing()

def formatstat():
    return {
        "board": [
            "".join(row) for row in game.board
        ],
        "current_player": PIECES[game.current_player],
        "winner": PIECES[game.winner] if game.winner else "None"
    }

@app.route('/drop', methods=['POST'])
def drop():
    col = request.json.get('col')
    if col is None:
        return jsonify({"error": "Column not specified", "game_status": formatstat()}), 400
    if game.winner:
        return jsonify({"error": f"Game over. {PIECES[game.winner]} won!", "game_status": formatstat()}), 400
    
    success = game.droppiece(col)
    if not success:
        return jsonify({"error": "Invalid move", "game_status": formatstat()}), 400

    return jsonify({
        "message": "Piece dropped successfully",
        "game_status": formatstat()
    })

@app.route('/board', methods=['GET'])
def board():
    return jsonify({
        "game_status": formatstat()
    })

@app.route('/reset', methods=['POST'])
def reset():
    game.reset()
    return jsonify({
        "message": "Game has been reset",
        "game_status": formatstat()
    })

@app.route('/cheating', methods=['POST'])
def autowin():
    if game.winner:
        return jsonify({"error": f"Game over. {PIECES[game.winner]} won!", "game_status": formatstat()}), 400
    
    game.autowin()
    return jsonify({
        "message": f"Auto-win activated 👽. {PIECES[game.winner]} wins!",
        "game_status": formatstat()
    })

if __name__ == '__main__':
    app.run(debug=True)
