'''
Standard 3x3 Tic-Tac-Toe Game with AI Opponents, 3 in a Row Win Condition

A Pygame-based implementation of Tic-Tac-Toe with multiple game modes and AI difficulty levels.

Game Modes:
    - Human vs AI: Player (X) competes against the computer (O)
    - AI vs AI: Two AI opponents play against each other

Difficulty Levels:
    - Easy: AI checks for immediate wins, blocks opponent wins, otherwise plays randomly
    - Medium: Uses minimax algorithm with alpha-beta pruning, limited to depth 5
    - Hard: Uses full minimax algorithm with alpha-beta pruning, unlimited depth

Features:
    - Interactive menu system for mode and difficulty selection
    - Real-time board visualization using Pygame
    - Minimax algorithm with alpha-beta pruning for optimal AI moves
    - Performance metrics (node count and computation time logging)
    - Game state management (menu, difficulty selection, active game, game over)
    - Configurable AI vs AI move delay
    - Comprehensive logging for debugging and performance analysis

Constants:
    - BOARD_SIZE: 3x3 grid
    - WIDTH, HEIGHT: 360x360 pixel window
    - Player symbols: X (human/AI1) and O (AI/AI2)
    - Color scheme for board, symbols, buttons, and UI elements

Logging Features
1. Move Validation & Execution
✓/✗ indicators for successful/failed moves
Position coordinates in logs

2. Minimax Algorithm
Depth limit reached notifications
Terminal state detection (WIN/LOSS/DRAW)
Pruning triggers with alpha/beta values
Move evaluation scores at each level
Best move tracking

3. Easy AI Strategy
Priority level indicators (🎯 WINNING, 🛡️ BLOCKING, 🎲 RANDOM)
Available cell count
Selected move details

4. Best Move Calculation
🤖 AI move calculation start/end markers
Player, difficulty, and mode info
Depth limit notifications
Top 3 evaluated moves ranked by score
Performance metrics (time, nodes evaluated)
Comprehensive separation lines for clarity

5. Game State Management
Game loop initialization
Mode selection (HUMAN vs AI / AI vs AI)
Difficulty selection
Game start notifications
Win/Draw/Tie outcomes with emojis
Turn notifications (waiting for moves)
Game reset confirmations

6. Visual Indicators
🎮 Game start
🤖 AI calculations
📊 Algorithm details
🎉 Game outcomes
⏳ Waiting states
🔄 Reset operations
👋 Exit events

The game initializes with a mode selection menu, followed by difficulty selection,
and then proceeds to the active game state where players/AIs take turns making moves.

Easy Difficulty: Previously, it was purely random moves. 
Now, the AI first checks for an immediate winning move (if placing its mark wins the game). 
If not, it checks for an immediate block (if the opponent would win on their next move, it blocks that spot). 
If neither, it picks a random empty cell. This makes the easy AI smarter without being unbeatable, 
as it won't miss obvious wins or losses.
Medium Difficulty: Previously, it used minimax with a depth limit of 4. 
Now, the depth limit is increased to 5, allowing the AI to look further ahead in the game tree. 
This makes it harder as it can plan more moves in advance, but still not as perfect as hard mode (full depth).
'''
import pygame
import sys
import logging
import time
from copy import deepcopy
import random

# Set up logging for debugging and performance metrics
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for the game
BOARD_SIZE = 3  # 3x3 Tic-Tac-Toe board
WIDTH, HEIGHT = 360, 360  # Window dimensions
LINE_WIDTH = 15  # Width of lines on the board
WIN_LINE_WIDTH = 20  # Width of winning line
BOARD_ROWS, BOARD_COLS = BOARD_SIZE, BOARD_SIZE
SQUARE_SIZE = WIDTH // BOARD_COLS  # Size of each square
CIRCLE_RADIUS = SQUARE_SIZE // 3  # Radius for O
CIRCLE_WIDTH = 15  # Width of O circle
CROSS_WIDTH = 25  # Width of X lines
SPACE = SQUARE_SIZE // 4  # Spacing for drawing X and O

# Colors (RGB)
BG_COLOR = (28, 170, 156)  # Background teal
LINE_COLOR = (23, 145, 135)  # Line color darker teal
CIRCLE_COLOR = (239, 231, 200)  # Light for O
CROSS_COLOR = (77, 77, 77)  # Dark for X
WIN_LINE_COLOR = (255, 0, 0)  # Red for winning line
BUTTON_COLOR = (28, 245, 28)  # Green for button
BUTTON_HOVER_COLOR = (22, 200, 22)  # Darker green for hover
BUTTON_TEXT_COLOR = (22, 22, 22)  # Black for button text

# Player symbols
PLAYER_X = 'X'  # Human or AI1
PLAYER_O = 'O'  # AI or AI2

# Difficulty levels
DIFFICULTY_EASY = 'easy'    # Random moves
DIFFICULTY_MEDIUM = 'medium'  # Minimax with limited depth (e.g., 5)
DIFFICULTY_HARD = 'hard'    # Full minimax with alpha-beta pruning

class TicTacToe:
    def __init__(self, ai_vs_ai_delay=0.5):
        """
        Initialize the Tic-Tac-Toe game.
        :param ai_vs_ai_delay: Delay in seconds between moves in AI vs AI mode
        """
        # Initialize Pygame library
        pygame.init()
        
        # Game configuration
        self.ai_vs_ai_delay = ai_vs_ai_delay  # Delay for AI vs AI mode visibility
        self.mode = None  # Game mode selected in menu ('human_vs_ai' or 'ai_vs_ai')
        self.difficulty = None  # Difficulty level selected in menu
        
        # Initialize the 3x3 game board with empty cells
        self.board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        
        # Game state variables
        self.current_player = PLAYER_X  # Start with X (human or first AI)
        self.game_over = False  # Flag to track if game has ended
        self.winner = None  # Stores the winner if game is won
        self.node_count = 0  # Tracks nodes evaluated in minimax for performance metrics
        
        # Pygame display setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Tic-Tac-Toe')
        self.screen.fill(BG_COLOR)
        self.draw_board_lines()  # Draw initial board grid
        
        # Font setup for rendering text on screen
        self.font = pygame.font.SysFont(None, 50)  # Default font for game result text
        self.button_font = pygame.font.SysFont(None, 40, bold=True)  # Bold font for menu buttons
        
        # Game state management (determines what UI/logic to display)
        self.state = 'mode_menu'  # Start with mode selection menu
        logging.info("Tic Tac Toe game initialized")

    def draw_board_lines(self):
        """Draw the grid lines on the board."""
        # Draw horizontal lines to create rows
        for row in range(1, BOARD_ROWS):
            pygame.draw.line(self.screen, LINE_COLOR, (0, SQUARE_SIZE * row), (WIDTH, SQUARE_SIZE * row), LINE_WIDTH)
        
        # Draw vertical lines to create columns
        for col in range(1, BOARD_COLS):
            pygame.draw.line(self.screen, LINE_COLOR, (SQUARE_SIZE * col, 0), (SQUARE_SIZE * col, HEIGHT), LINE_WIDTH)

    def draw_symbols(self):
        """Draw X and O symbols on the board."""
        # Iterate through each cell in the 3x3 board
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.board[row][col] == PLAYER_O:
                    # Draw circle (O) at the center of the cell
                    pygame.draw.circle(self.screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                                                   int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                       CIRCLE_RADIUS, CIRCLE_WIDTH)
                elif self.board[row][col] == PLAYER_X:
                    # Draw X as two diagonal lines intersecting in the cell
                    # First line from top-left to bottom-right
                    pygame.draw.line(self.screen, CROSS_COLOR,
                                     (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                     (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                    # Second line from top-right to bottom-left
                    pygame.draw.line(self.screen, CROSS_COLOR,
                                     (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                     (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                     CROSS_WIDTH)

    def is_valid_move(self, row, col):
        """Check if the move is valid (empty cell)."""
        is_valid = 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS and self.board[row][col] == ' '
        if not is_valid:
            logging.warning(f"Invalid move attempted at ({row}, {col}) - Cell occupied or out of bounds")
        return is_valid

    def make_move(self, row, col, player):
        """Make a move on the board."""
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            logging.info(f"✓ Move made: {player} at row {row}, col {col}")
            return True
        logging.error(f"✗ Failed to place {player} at ({row}, {col})")
        return False

    def check_win(self, player, board=None):
        """Check if the player has won on the given board."""
        # Use provided board or default to current game board
        if board is None:
            board = self.board
        
        # Check all three rows for a winning condition
        for row in range(BOARD_ROWS):
            if all([board[row][col] == player for col in range(BOARD_COLS)]):
                return True
        
        # Check all three columns for a winning condition
        for col in range(BOARD_COLS):
            if all([board[row][col] == player for row in range(BOARD_ROWS)]):
                return True
        
        # Check main diagonal (top-left to bottom-right)
        if all([board[i][i] == player for i in range(BOARD_ROWS)]):
            return True
        
        # Check anti-diagonal (top-right to bottom-left)
        if all([board[i][BOARD_ROWS - 1 - i] == player for i in range(BOARD_ROWS)]):
            return True
        
        return False  # No winning condition found

    def check_draw(self, board=None):
        """Check if the game is a draw (board full) on the given board."""
        # Use provided board or default to current game board
        if board is None:
            board = self.board
        
        # Draw occurs when all cells are filled with no winner
        return all([cell != ' ' for row in board for cell in row])

    def get_empty_cells(self, board=None):
        """Get list of empty cells (row, col) on the given board."""
        # Use provided board or default to current game board
        if board is None:
            board = self.board
        
        # Return list of all empty cell coordinates
        return [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] == ' ']

    def evaluate_board(self, board, maximizer):
        """
        Evaluate the board: +10 if maximizer wins, -10 if opponent wins, 0 otherwise.
        :param board: The board to evaluate
        :param maximizer: The player who is the maximizer (AI's symbol)
        """
        # Determine the opponent (minimizer)
        opponent = PLAYER_X if maximizer == PLAYER_O else PLAYER_O
        
        # Check if maximizer (AI) has won
        if self.check_win(maximizer, board):
            return 10  # Best case scenario
        
        # Check if opponent (minimizer) has won
        elif self.check_win(opponent, board):
            return -10  # Worst case scenario
        
        return 0  # Game is still ongoing (neither player has won)

    def minimax(self, board, depth, alpha, beta, is_maximizing, maximizer, depth_limit=float('inf')):
        """
        Minimax algorithm with alpha-beta pruning for finding optimal moves.
        :param board: Current board state
        :param depth: Current depth in the game tree
        :param alpha: Alpha value for pruning (maximizer's best option)
        :param beta: Beta value for pruning (minimizer's best option)
        :param is_maximizing: True if maximizing player's turn, False if minimizing
        :param maximizer: The symbol of the maximizing player
        :param depth_limit: Maximum depth to search (prevents excessive computation)
        :return: Best score for the current position
        """
        # Base case: stop searching if depth limit reached
        if depth >= depth_limit:
            score = self.evaluate_board(board, maximizer)
            logging.debug(f"Depth limit reached at depth {depth}. Evaluating board: score={score}")
            return score

        # Count nodes for performance analysis
        self.node_count += 1

        # Check if someone has won (terminal state)
        score = self.evaluate_board(board, maximizer)
        if score != 0:  # Win or loss found
            if score > 0:
                result = score - depth  # Faster wins are better
                logging.debug(f"Terminal state (WIN) found at depth {depth}. Maximizer score: {score}, adjusted: {result}")
                return result
            else:
                result = score + depth  # Delayed losses are better
                logging.debug(f"Terminal state (LOSS) found at depth {depth}. Opponent score: {score}, adjusted: {result}")
                return result
        
        # Check if board is full (draw condition)
        if self.check_draw(board):
            logging.debug(f"Draw state detected at depth {depth}")
            return 0

        # Determine the minimizer (opponent of maximizer)
        minimizer = PLAYER_X if maximizer == PLAYER_O else PLAYER_O

        # MAXIMIZING PLAYER'S TURN: Find the move with highest score
        if is_maximizing:
            max_eval = -float('inf')
            player_type = "MAXIMIZER"
            for row, col in self.get_empty_cells(board):
                # Try placing maximizer's symbol at this position
                board[row][col] = maximizer
                eval = self.minimax(board, depth + 1, alpha, beta, False, maximizer, depth_limit)
                board[row][col] = ' '  # Undo the move
                
                # Update best score for maximizer
                if eval > max_eval:
                    max_eval = eval
                    logging.debug(f"{player_type} at depth {depth}: New best move ({row},{col}) with score {eval}")
                
                alpha = max(alpha, eval)  # Update alpha for pruning
                
                # Alpha-beta pruning: stop if beta <= alpha
                if beta <= alpha:
                    logging.debug(f"{player_type} at depth {depth}: PRUNING TRIGGERED (alpha={alpha}, beta={beta}) - skipping remaining moves")
                    break
            
            logging.debug(f"{player_type} at depth {depth}: Returning best score {max_eval} from {self.node_count} nodes")
            return max_eval
        
        # MINIMIZING PLAYER'S TURN: Find the move with lowest score
        else:
            min_eval = float('inf')
            player_type = "MINIMIZER"
            for row, col in self.get_empty_cells(board):
                # Try placing minimizer's symbol at this position
                board[row][col] = minimizer
                eval = self.minimax(board, depth + 1, alpha, beta, True, maximizer, depth_limit)
                board[row][col] = ' '  # Undo the move
                
                # Update best score for minimizer
                if eval < min_eval:
                    min_eval = eval
                    logging.debug(f"{player_type} at depth {depth}: New best move ({row},{col}) with score {eval}")
                
                beta = min(beta, eval)  # Update beta for pruning
                
                # Alpha-beta pruning: stop if beta <= alpha
                if beta <= alpha:
                    logging.debug(f"{player_type} at depth {depth}: PRUNING TRIGGERED (alpha={alpha}, beta={beta}) - skipping remaining moves")
                    break
            
            logging.debug(f"{player_type} at depth {depth}: Returning best score {min_eval}")
            return min_eval

    def get_easy_move(self, ai_player):
        """Get move for easy difficulty: Check for win, then block, then random."""
        # Determine the opponent
        opponent = PLAYER_X if ai_player == PLAYER_O else PLAYER_O
        empty_cells = self.get_empty_cells()
        logging.debug(f"Easy AI calculating move for {ai_player}. Available cells: {len(empty_cells)}")

        # Priority 1: Check for winning move (place AI symbol and check if it wins)
        for row, col in empty_cells:
            self.board[row][col] = ai_player
            if self.check_win(ai_player):
                self.board[row][col] = ' '  # Undo the test move
                logging.info(f"🎯 Easy AI PRIORITY 1 - Found WINNING move at ({row}, {col})")
                return (row, col)  # Return the winning move
            self.board[row][col] = ' '  # Undo the test move

        # Priority 2: Check for blocking move (place opponent symbol and check if it wins)
        for row, col in empty_cells:
            self.board[row][col] = opponent
            if self.check_win(opponent):
                self.board[row][col] = ' '  # Undo the test move
                logging.info(f"🛡️  Easy AI PRIORITY 2 - Found BLOCKING move at ({row}, {col}) to prevent {opponent} win")
                return (row, col)  # Return the blocking move
            self.board[row][col] = ' '  # Undo the test move

        # Priority 3: Make a random move if no immediate win or block
        random_move = random.choice(empty_cells) if empty_cells else None
        logging.info(f"🎲 Easy AI PRIORITY 3 - Making RANDOM move at {random_move}")
        return random_move

    def get_best_move(self):
        """Find the best move using minimax with alpha-beta pruning or easy logic."""
        # Start timing to measure AI computation performance
        start_time = time.time()
        self.node_count = 0  # Reset node count for this move
        
        # Variables to track best move found
        best_score = -float('inf')
        best_move = None
        
        # Determine which player is maximizing:
        # - Human vs AI: AI (O) is maximizing
        # - AI vs AI: Current player is maximizing
        maximizer = PLAYER_O if self.mode == 'human_vs_ai' else self.current_player
        
        # Set depth limit based on difficulty level
        # Hard: unlimited depth (full minimax), Medium: depth 5, Easy: no limit (uses heuristic)
        depth_limit = float('inf') if self.difficulty == DIFFICULTY_HARD else 5 if self.difficulty == DIFFICULTY_MEDIUM else 0
        
        logging.info(f"\n{'='*60}")
        logging.info(f"🤖 AI MOVE CALCULATION STARTED")
        logging.info(f"Player: {self.current_player} | Difficulty: {self.difficulty} | Mode: {self.mode}")
        logging.info(f"{'='*60}")

        # EASY DIFFICULTY: Use simple heuristic strategy instead of minimax
        if self.difficulty == DIFFICULTY_EASY:
            best_move = self.get_easy_move(maximizer)
            logging.info(f"Easy AI move selected: {best_move}")
            return best_move

        # Log depth limit for medium and hard difficulty
        if depth_limit != float('inf'):
            logging.info(f"📊 Medium Difficulty: Using depth limit of {depth_limit} levels")
        else:
            logging.info(f"📊 Hard Difficulty: Using UNLIMITED depth (full minimax search)")

        # MEDIUM/HARD DIFFICULTY: Use minimax algorithm
        # Create a copy of the board to simulate moves
        logging.info(f"🔍 Evaluating {len(self.get_empty_cells())} possible moves...")
        board_copy = deepcopy(self.board)
        move_scores = []  # Track all move evaluations for logging
        
        for row, col in self.get_empty_cells():
            # Simulate the move for the maximizer
            board_copy[row][col] = maximizer
            # Evaluate this move using minimax (minimizer's turn next)
            score = self.minimax(board_copy, 0, -float('inf'), float('inf'), False, maximizer, depth_limit=depth_limit)
            board_copy[row][col] = ' '
            
            move_scores.append((row, col, score))
            logging.debug(f"Move evaluation: ({row},{col}) → Score: {score}")
            
            # Track best move
            if score > best_score:
                best_score = score
                best_move = (row, col)
                logging.debug(f"   → NEW BEST MOVE!")

        # Log all move evaluations sorted by score
        move_scores.sort(key=lambda x: x[2], reverse=True)
        logging.info(f"📋 Top 3 evaluated moves:")
        for i, (r, c, score) in enumerate(move_scores[:3], 1):
            marker = "✓ SELECTED" if (r, c) == best_move else ""
            logging.info(f"   {i}. ({r},{c}): Score {score:+.0f} {marker}")

        # Calculate and log performance metrics
        time_taken = time.time() - start_time
        logging.info(f"⏱️  Computation time: {time_taken:.4f}s | Nodes evaluated: {self.node_count}")
        logging.info(f"✅ Final decision: Move {best_move} with score {best_score}")
        logging.info(f"{'='*60}\n")
        
        return best_move

    def draw_win_line(self):
        """Draw the winning line (placeholder: can be implemented for visual feedback)."""
        # For simplicity, not implementing detailed win line drawing here, but can add based on win condition
        pass

    def reset_game(self):
        """Reset the game board and prepare for a new game."""
        # Clear the board and reset all cells to empty
        self.board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        
        # Reset game state
        self.current_player = PLAYER_X  # Start with X again
        self.screen.fill(BG_COLOR)
        self.draw_board_lines()
        self.game_over = False
        self.winner = None
        logging.info(f"🔄 Game reset - Ready for new game")

    def run(self):
        """Main game loop that handles events, AI moves, and rendering."""
        # Initialize clock for frame rate control
        clock = pygame.time.Clock()
        running = True
        logging.info("🎮 Game loop started - Waiting for user input...")

        while running:
            # Get current mouse position for button hover detection
            mouse_pos = pygame.mouse.get_pos()
            
            # Process all pending events
            for event in pygame.event.get():
                # Handle window close event
                if event.type == pygame.QUIT:
                    running = False
                    logging.info("👋 Game window closed - Exiting...")
                    pygame.quit()
                    sys.exit()

                # MENU STATE: Handle mode selection
                if self.state == 'mode_menu':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.human_ai_rect.collidepoint(mouse_pos):
                            self.mode = 'human_vs_ai'
                            self.state = 'difficulty_menu'
                            logging.info("📌 Game mode selected: HUMAN vs AI")
                        elif self.ai_ai_rect.collidepoint(mouse_pos):
                            self.mode = 'ai_vs_ai'
                            self.state = 'difficulty_menu'
                            logging.info("📌 Game mode selected: AI vs AI")
                
                # DIFFICULTY MENU STATE: Handle difficulty selection
                elif self.state == 'difficulty_menu':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.easy_rect.collidepoint(mouse_pos):
                            self.difficulty = DIFFICULTY_EASY
                            self.state = 'game'
                            logging.info(f"⚙️  Difficulty set: {self.difficulty.upper()}")
                            logging.info(f"🏁 Starting game - Mode: {self.mode} | Difficulty: {self.difficulty}")
                        elif self.medium_rect.collidepoint(mouse_pos):
                            self.difficulty = DIFFICULTY_MEDIUM
                            self.state = 'game'
                            logging.info(f"⚙️  Difficulty set: {self.difficulty.upper()}")
                            logging.info(f"🏁 Starting game - Mode: {self.mode} | Difficulty: {self.difficulty}")
                        elif self.hard_rect.collidepoint(mouse_pos):
                            self.difficulty = DIFFICULTY_HARD
                            self.state = 'game'
                            logging.info(f"⚙️  Difficulty set: {self.difficulty.upper()}")
                            logging.info(f"🏁 Starting game - Mode: {self.mode} | Difficulty: {self.difficulty}")
                
                # GAME STATE: Handle gameplay
                elif self.state == 'game':
                    if self.game_over:
                        # Game is over: allow reset via 'R' key or button click
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:  # Press R to reset
                            self.reset_game()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if self.button_rect.collidepoint(mouse_pos):
                                self.reset_game()
                    else:
                        # Game is active: handle human player's move
                        if self.mode == 'human_vs_ai' and self.current_player == PLAYER_X:  # Human's turn
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_x, mouse_y = event.pos
                                col = mouse_x // SQUARE_SIZE
                                row = mouse_y // SQUARE_SIZE
                                logging.debug(f"Human clicked at pixel ({mouse_x}, {mouse_y}) → Board position ({row}, {col})")
                                if self.make_move(row, col, PLAYER_X):
                                    self.draw_symbols()
                                    if self.check_win(PLAYER_X):
                                        self.winner = PLAYER_X
                                        self.game_over = True
                                        logging.info("🎉 HUMAN WINS! Congratulations!")
                                    elif self.check_draw():
                                        self.game_over = True
                                        logging.info("🤝 DRAW! Game ended in a tie.")
                                    else:
                                        self.current_player = PLAYER_O
                                        logging.info("⏳ Waiting for AI move...")

            # Handle AI move if it's AI's turn
            if self.state == 'game' and not self.game_over and (self.mode == 'ai_vs_ai' or (self.mode == 'human_vs_ai' and self.current_player == PLAYER_O)):
                # Get AI's best move
                row, col = self.get_best_move()
                if row is not None and col is not None:
                    self.make_move(row, col, self.current_player)
                    self.draw_symbols()
                    
                    # Check win condition
                    if self.check_win(self.current_player):
                        self.winner = self.current_player
                        self.game_over = True
                        logging.info(f"🤖 AI ({self.current_player}) WINS!")
                    
                    # Check draw condition
                    elif self.check_draw():
                        self.game_over = True
                        logging.info("🤝 DRAW! Game ended in a tie.")
                    
                    # Switch to next player
                    else:
                        self.current_player = PLAYER_X if self.current_player == PLAYER_O else PLAYER_O
                        if self.mode == 'human_vs_ai':
                            logging.info("⏳ Waiting for human move...")
                    
                    # Add delay for AI vs AI visibility
                    if self.mode == 'ai_vs_ai':
                        logging.debug(f"AI vs AI delay: {self.ai_vs_ai_delay}s")
                        time.sleep(self.ai_vs_ai_delay)

            # Clear screen and redraw everything
            self.screen.fill(BG_COLOR)

            # Render appropriate UI based on current state
            if self.state == 'mode_menu':
                # Draw mode selection menu
                menu_text = self.font.render("Select Mode", True, (255, 255, 255))
                self.screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, 50))

                # Human vs AI button
                self.human_ai_rect = pygame.Rect(WIDTH // 2 - 150, 150, 300, 50)
                human_ai_color = BUTTON_HOVER_COLOR if self.human_ai_rect.collidepoint(mouse_pos) else BUTTON_COLOR
                pygame.draw.rect(self.screen, human_ai_color, self.human_ai_rect)
                human_ai_text = self.button_font.render("Human vs AI", True, BUTTON_TEXT_COLOR)
                self.screen.blit(human_ai_text, (self.human_ai_rect.x + (self.human_ai_rect.width - human_ai_text.get_width()) // 2,
                                                 self.human_ai_rect.y + (self.human_ai_rect.height - human_ai_text.get_height()) // 2))

                # AI vs AI button
                self.ai_ai_rect = pygame.Rect(WIDTH // 2 - 150, 220, 300, 50)
                ai_ai_color = BUTTON_HOVER_COLOR if self.ai_ai_rect.collidepoint(mouse_pos) else BUTTON_COLOR
                pygame.draw.rect(self.screen, ai_ai_color, self.ai_ai_rect)
                ai_ai_text = self.button_font.render("AI vs AI", True, BUTTON_TEXT_COLOR)
                self.screen.blit(ai_ai_text, (self.ai_ai_rect.x + (self.ai_ai_rect.width - ai_ai_text.get_width()) // 2,
                                              self.ai_ai_rect.y + (self.ai_ai_rect.height - ai_ai_text.get_height()) // 2))
            
            elif self.state == 'difficulty_menu':
                # Draw difficulty selection menu
                menu_text = self.font.render("Select Difficulty", True, (255, 255, 255))
                self.screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, 50))

                # Easy button
                self.easy_rect = pygame.Rect(WIDTH // 2 - 100, 150, 200, 50)
                easy_color = BUTTON_HOVER_COLOR if self.easy_rect.collidepoint(mouse_pos) else BUTTON_COLOR
                pygame.draw.rect(self.screen, easy_color, self.easy_rect)
                easy_text = self.button_font.render("Easy", True, BUTTON_TEXT_COLOR)
                self.screen.blit(easy_text, (self.easy_rect.x + (self.easy_rect.width - easy_text.get_width()) // 2,
                                             self.easy_rect.y + (self.easy_rect.height - easy_text.get_height()) // 2))

                # Medium button
                self.medium_rect = pygame.Rect(WIDTH // 2 - 100, 220, 200, 50)
                medium_color = BUTTON_HOVER_COLOR if self.medium_rect.collidepoint(mouse_pos) else BUTTON_COLOR
                pygame.draw.rect(self.screen, medium_color, self.medium_rect)
                medium_text = self.button_font.render("Medium", True, BUTTON_TEXT_COLOR)
                self.screen.blit(medium_text, (self.medium_rect.x + (self.medium_rect.width - medium_text.get_width()) // 2,
                                               self.medium_rect.y + (self.medium_rect.height - medium_text.get_height()) // 2))

                # Hard button
                self.hard_rect = pygame.Rect(WIDTH // 2 - 100, 290, 200, 50)
                hard_color = BUTTON_HOVER_COLOR if self.hard_rect.collidepoint(mouse_pos) else BUTTON_COLOR
                pygame.draw.rect(self.screen, hard_color, self.hard_rect)
                hard_text = self.button_font.render("Hard", True, BUTTON_TEXT_COLOR)
                self.screen.blit(hard_text, (self.hard_rect.x + (self.hard_rect.width - hard_text.get_width()) // 2,
                                             self.hard_rect.y + (self.hard_rect.height - hard_text.get_height()) // 2))
            
            elif self.state == 'game':
                # Draw the game board and symbols
                self.draw_board_lines()
                self.draw_symbols()

                # Display result if game over
                if self.game_over:
                    if self.winner:
                        text = self.font.render(f"{self.winner} wins!", True, (255, 255, 255))
                    else:
                        text = self.font.render("Draw!", True, (255, 255, 255))
                    self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 60))

                    # Draw play again button
                    self.button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 50)
                    button_color = BUTTON_HOVER_COLOR if self.button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
                    pygame.draw.rect(self.screen, button_color, self.button_rect)
                    button_text = self.button_font.render("Play Again", True, BUTTON_TEXT_COLOR)
                    self.screen.blit(button_text, (self.button_rect.x + (self.button_rect.width - button_text.get_width()) // 2,
                                                   self.button_rect.y + (self.button_rect.height - button_text.get_height()) // 2))

            # Update display with all drawn elements
            pygame.display.update()
            
            # Cap frame rate at 60 FPS
            clock.tick(60)

if __name__ == "__main__":
    game = TicTacToe()
    game.run()