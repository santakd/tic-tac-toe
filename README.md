# Tic-Tac-Toe — Game Variations (Pygame + AI)

Tic-Tac-Toe Game Variations is a Pygame-based collection of Tic-Tac-Toe implementations with multiple board sizes, game modes, and AI difficulty levels. The project is focused on exploring different rulesets and AI techniques (random, heuristic checks, and minimax with alpha–beta pruning).

## Features

- Multiple board/win-size variations (standard 3x3 and advanced 4x4 variants).
- Game modes: Human vs AI and AI vs AI.
- AI difficulty levels:
  - Easy — immediate win/block checks, otherwise random.
  - Medium — minimax with alpha–beta pruning limited to a search depth (configurable).
  - Hard — full minimax with alpha–beta pruning (no depth limit).
- Interactive menu and real-time board visualization using Pygame.
- Performance logging: node counts, computation times, and evaluated move rankings.
- Configurable AI vs AI move delay and comprehensive logging to aid debugging.

## Demo / Screenshot

Run the game locally to see the Pygame window and menu. You can capture screenshots or GIFs from your session and add them here.

## Requirements

- Python 3.8+
- pygame

Install dependencies with pip:

```bash
pip install pygame
# or, if you have a requirements.txt:
# pip install -r requirements.txt
```

## Running the game

From the repository root run:

```bash
python main.py
# or
python3 main.py
```

If your entry point is in a different file or folder (for example `src/main.py`), run that file instead.

## How to play

- Use the menu to choose the game mode (Human vs AI or AI vs AI) and difficulty.
- For human play, click on an empty cell to place your mark (X by default).
- The game shows win/draw outcomes and allows resetting or exiting.

Controls may vary depending on how the Pygame UI is implemented — typically mouse clicks are used to select cells and buttons.

## AI Details

- Easy: Checks for any immediate winning move for itself, then checks for moves that block the opponent's immediate win, otherwise selects a random available cell. This avoids obvious blunders while remaining beatable.

- Medium: Uses minimax with alpha–beta pruning but with a configurable depth limit (the previous README noted depth=4 or 5). Depth limits reduce computation and make the AI less than perfect.

- Hard: Uses full minimax with alpha–beta pruning and no depth limit (searches to terminal states), which produces optimal play for smaller boards.

## Logging & Debugging

The project logs information useful for debugging and performance analysis, including:
- Move validation and coordinates
- Minimax depth notifications, pruning events, and evaluation scores
- Node counts and computation times for AI decisions
- Ranked best moves (top evaluated moves)

These logs can be toggled or redirected to a file for offline analysis.

## Project structure (example)

Adjust these paths to match the repository layout.

```
README.md
main.py               # Game entry point
requirements.txt      # Optional: dependencies
/game                  # Game logic and modules
/game/ai.py            # AI implementations (easy, minimax, etc.)
/game/ui.py            # Pygame UI code
/game/utils.py         # Helpers and logging
```

## Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Make changes and add tests where appropriate.
4. Open a pull request describing your changes.

Please include descriptive commit messages and keep changes focused.

## Tests

If you add unit tests, include instructions to run them here (for example, using pytest):

```bash
pip install pytest
pytest
```

## Future improvements / TODO

- Add a simple GUI menu system if not already present or polish existing UI.
- Add configurable board sizes and rule variations in the menu.
- Add more AI strategies (Monte Carlo Tree Search, Reinforcement Learning agents).
- Add persistence for game statistics and leaderboards.
- Add unit tests and continuous integration (GitHub Actions).

## License

No license is specified in this repository. If you want to make this project open source, add a LICENSE file (MIT is a common choice).

## Contact

If you have questions or suggestions, open an issue or submit a pull request. Mention @santakd for visibility.