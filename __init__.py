# Generation ID: Hutch_1764574166889_oezh124ws (前半)

def myai(board, color):
    """
    オセロ最強AIエンジン
    board: 2次元配列 (6x6 or 8x8, 0=空, 1=黒, 2=白)
    color: 手番 (1=黒, 2=白)
    return: (column, row) or (-1, -1)
    """
    size = len(board)

    def is_valid_move(board, col, row, player):
        if board[row][col] != 0:
            return False

        opponent = 3 - player
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if nr < 0 or nr >= size or nc < 0 or nc >= size:
                continue
            if board[nr][nc] != opponent:
                continue

            while True:
                nr += dr
                nc += dc
                if nr < 0 or nr >= size or nc < 0 or nc >= size:
                    break
                if board[nr][nc] == 0:
                    break
                if board[nr][nc] == player:
                    return True

        return False

    def get_valid_moves(board, player):
        moves = []
        for row in range(size):
            for col in range(size):
                if is_valid_move(board, col, row, player):
                    moves.append((col, row))
        return moves

    def apply_move(board, col, row, player):
        board = [row[:] for row in board]
        opponent = 3 - player
        board[row][col] = player
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            flips = []

            while 0 <= nr < size and 0 <= nc < size and board[nr][nc] == opponent:
                flips.append((nr, nc))
                nr += dr
                nc += dc

            if 0 <= nr < size and 0 <= nc < size and board[nr][nc] == player and flips:
                for fr, fc in flips:
                    board[fr][fc] = player

        return board

    def count_stones(board, player):
        return sum(row.count(player) for row in board)

    def evaluate(board, player, depth, phase):
        opponent = 3 - player

        corner_bonus = 500
        c_x_penalty = -150
        mobility_weight = 100 - (depth * 5)
        frontier_weight = 30
        stone_weight = 1000 if phase == "endgame" else 5

        score = 0
        corners = [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]
        c_x_squares = [(1, 1), (1, size-2), (size-2, 1), (size-2, size-2)] if size == 8 else []

        for cr, cc in corners:
            if board[cr][cc] == player:
                score += corner_bonus
            elif board[cr][cc] == opponent:
                score -= corner_bonus

        for cr, cc in c_x_squares:
            if board[cr][cc] == player:
                score += c_x_penalty
            elif board[cr][cc] == opponent:
                score -= c_x_penalty

        player_moves = len(get_valid_moves(board, player))
        opponent_moves = len(get_valid_moves(board, opponent))
        score += (player_moves - opponent_moves) * mobility_weight

        frontier = 0
        for r in range(size):
            for c in range(size):
                if board[r][c] == player:
                    for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < size and 0 <= nc < size and board[nr][nc] == 0:
                            frontier += 1
                            break
        score -= frontier * frontier_weight

        player_stones = count_stones(board, player)
        opponent_stones = count_stones(board, opponent)
        score += (player_stones - opponent_stones) * stone_weight

        return score

    def determine_phase(board):
        empty = sum(row.count(0) for row in board)
        total = size * size
        filled_ratio = (total - empty) / total
        return "endgame" if filled_ratio > 0.75 else "midgame"

    def minimax(board, depth, alpha, beta, is_maximizing, player):
        phase = determine_phase(board)

        if depth == 0:
            return evaluate(board, player, depth, phase), None

        valid_moves = get_valid_moves(board, player if is_maximizing else (3 - player))

        if not valid_moves:
            opp_moves = get_valid_moves(board, 3 - player if is_maximizing else player)
            if not opp_moves:
                return evaluate(board, player, depth, phase), None
            return minimax(board, depth - 1, alpha, beta, not is_maximizing, player)

        best_move = None

        if is_maximizing:
            max_eval = float('-inf')
            for col, row in valid_moves:
                new_board = apply_move(board, col, row, player if is_maximizing else (3 - player))
                eval_score, _ = minimax(new_board, depth - 1, alpha, beta, False, player)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (col, row)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for col, row in valid_moves:
                new_board = apply_move(board, col, row, 3 - player)
                eval_score, _ = minimax(new_board, depth - 1, alpha, beta, True, player)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (col, row)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    valid_moves = get_valid_moves(board, color)

    if not valid_moves:
        return (-1, -1)

    if len(valid_moves) == 1:
        return valid_moves[0]

    depth = 6 if size == 6 else 5
    _, best_move = minimax(board, depth, float('-inf'), float('inf'), True, color)

    return best_move if best_move else valid_moves[0]

# Generation ID: Hutch_1764574166889_oezh124ws (後半)
