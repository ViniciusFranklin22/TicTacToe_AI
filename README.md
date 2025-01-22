# Tic Tac Toe AI  

This project demonstrates the implementation of an **unbeatable AI** for the classic game of Tic Tac Toe using the **Minimax algorithm**.  

## Overview  
The primary objective was to create an AI that could never lose while also exploring different techniques to achieve this. Initially, I experimented with machine learning models like KNN, SVM, and Neural Networks, but they didn't perform well for this problem.  
Eventually, I discovered and implemented the **Minimax algorithm**, optimizing it for faster and more efficient results.  

## Features  
- **Unbeatable AI**: Implements the Minimax algorithm with branch pruning for optimal decision-making.  
- **Tkinter GUI**: A simple interface for playing against the AI.  
- **Game Data Logging**: Saves game data to `jogadas.csv` for further analysis.  
- **Custom Scoring System**: Prioritizes faster wins by modifying the Minimax scoring logic.  

## How It Works  
The Minimax algorithm evaluates all possible game states and chooses the optimal path based on:  
1. **Maximizing/Minimizing**: The AI either maximizes its score or minimizes the opponent’s.  
2. **Scoring System**: Scores are weighted by the number of rounds, prioritizing faster victories.  
3. **Branch Pruning**: Stops searching further when an optimal result is found in a branch.  

## Files

For more information about the model and how it works, make sure to check the `explanation.pdf` file in this repository.  
The main Python file for this application is `tictactoe.py`.

## Getting Started  
### Requirements  
- Python 3.x  
- Tkinter (built-in with Python)  

### How to Run  
1. Clone the repository:  
   ```bash
   git clone <repository-url>
   cd tic-tac-toe-ai
