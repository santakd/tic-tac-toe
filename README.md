Tic-Tac-Toe Game with AI Opponents

A Pygame-based implementation of Tic-Tac-Toe with multiple game modes and AI difficulty levels.

Variations:

1. Standard 3x3, 3 in a row wins
2. Advanced 4x4, 4 in a row wins
3. Advanced 4x4, 3 in a row wins
   
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
Medium Difficulty:  it used minimax with a depth limit of 4, allowing the AI to look further ahead in the game tree. 
This makes it harder as it can plan more moves in advance, but still not as perfect as hard mode (full depth).

