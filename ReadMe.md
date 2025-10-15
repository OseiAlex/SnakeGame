# 🐍 SnakeGame

**Simple Snake Game built for CSE 310 - Module (Game Framework)**  
**Author:** Alex King Osei Junior  
**Date:** September 26, 2025

---

## 📜 Overview

This project is a modernized implementation of the **classic Snake game** built with **Pygame** in Python.  

It goes beyond the basic version by including:
- 🕹 **Main Menu** with multiple options  
- 🎧 **Background music and sound effects** (toggleable)  
- ⏸ **Pause / Resume** with the `P` key  
- 🏆 **High Scores system** saved to a text file  
- 🐢 **Slow starting speed**, which increases as the level progresses  
- 🧮 Live **Score and Level** display on screen  

This game demonstrates:
- Real-time **game loop** and **event handling**  
- Grid-based **movement and collision detection**  
- Persistent **score saving** and file I/O  
- Clean **user interface** and **menu navigation**

---

## 🚀 How to Run

1. **Install requirements**  
   ```bash
   pip install pygame
   ```

2. **Run the game**  
   ```bash
   python3 main.py
   ```

3. Ensure the following **folder structure**:
   ```
   project/
   ├── main.py
   ├── scores.txt              # created automatically
   └── resources/
       ├── background.mp3
       ├── eat.wav
       └── gameover.wav
   ```

---

## 🎮 Controls

| Key                | Action                        |
|---------------------|-------------------------------|
| Arrow Keys / WASD   | Move the snake                |
| `P`                 | Pause / Resume                |
| `ESC`               | Quit                          |
| Any Key (Game Over) | Return to main menu           |

### 🏁 Main Menu Options
```
1 - Start New Game
2 - View High Scores
3 - Toggle Sound
4 - Exit
```

---

## 🏆 High Scores Feature

- Your **final score and level** are automatically saved to `scores.txt` at the end of each game.  
- You can view the top 10 high scores from the **main menu** (Option `2`).  
- Scores are stored in a simple text file — no database needed.

---

## 🧩 Features Checklist

- ✅ Original code  
- ✅ Code documented with function-level comments  
- ✅ Main menu with sound toggle  
- ✅ High scores saved to `scores.txt`  
- ✅ Background music and sound effects (toggleable)  
- ✅ Pause/resume feature with `P` key  
- ✅ Score and level displayed  
- ✅ Smooth speed increase per level  
- ✅ README.md completed  
- ✅ Video demo with talking head  
- ✅ Public GitHub repository

---

## 🖥️ Video Demo

🎥 [Watch the demo on Loom](https://www.loom.com/share/3bbf98bf270c4d1a9a0c786c997d26b4?sid=6e3df31c-67e2-4f0c-9fa5-d4f20ac58510)

---

## 🌐 Repository

🔗 [GitHub Repository](https://github.com/OseiAlex/SnakeGame)

---

## 🪪 License

This project is provided for **educational purposes only** as part of the **CSE 310 – Game Framework module**.
