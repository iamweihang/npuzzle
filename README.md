# COMP9001
COMP9001 Final Project - npuzzle
A Python implementation of the classic sliding puzzle game (n-Puzzle) with a graphical user interface built using **Tkinter**.  
The game supports **3×3, 4×4, and 5×5** boards and includes timer, step counter, user login, leaderboard, and optional hint functionality.

---

## ✨ Features

- **Multiple board sizes**: 3×3, 4×4, 5×5
- **Timer & step counter**: Real-time display of elapsed time and steps
- **User login**: Enter a username before playing  
  - `admin` account unlocks management features
- **Leaderboard**:
  - Records best times separately for each board size
  - Tracks each user’s personal best time
  - Runs are **excluded** from the leaderboard if a hint was used
  - `admin` can clear scores or delete specific records
- **Hint option**: Available once per game; disables leaderboard entry
- **Success page**: Displays upon solving the puzzle
- **Debug mode**: Optional “Finish Now” button for testing/demo

---

## 📂 Project Structure
npuzzle/
├─ src/
│ ├─ app.py # Entry point
│ ├─ ui_login.py # Login screen
│ ├─ ui_home.py # Home screen (choose board size)
│ ├─ ui_game.py # Game board (timer, steps, hints)
│ ├─ ui_success.py # Success screen
│ ├─ ui_leaderboard.py # Leaderboard (with admin tools)
│ ├─ core_board.py # Board logic & tile movement
│ ├─ core_scramble.py # Puzzle shuffling
│ ├─ core_timer.py # Timer logic
│ └─ io_leaderboard.py # Leaderboard data (JSON)
├─ data/
│ └─ leaderboard.json # Automatically created/updated
└─ README.md

---

## 🚀 How to Run
python src/app.py

---

## 🎮 How to Play

1. Log in with a username (admin enables management functions).

2. Select a board size (3×3, 4×4, or 5×5).

3. Click tiles adjacent to the blank space to move them.

4. Optionally use one Hint (but the run will not count in the leaderboard).

5. Solve the puzzle → after 0.5 second, you’ll be redirected to the success page and your time will be saved.

---

## 💾 Data Storage

- **Leaderboard data is saved to data/leaderboard.json**

- **admin can:**

  - Clear the leaderboard for the current board size

  - Delete specific records

- **To reset manually, delete the leaderboard.json file.**
