# N-Queens Problem Solution using Hill Climbing

## Overview
This project implements the Hill Climbing algorithm to solve the N-Queens problem, where the objective is to place N queens on an N×N chessboard such that no two queens threaten each other. The solution includes variations of the algorithm and performance evaluations for different board sizes.

## Requirements

- Python 3.x

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/NikTsiop/QueensProblem.git
   cd QueensProblem
   ```

2. **(Optional) Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following command:

```bash
python queens_problem.py
```

This will execute the Hill Climbing algorithm to find a solution to the N-Queens problem.

## Features

- **Hill Climbing Algorithm:** Implements the basic Hill Climbing algorithm to find solutions for the N-Queens problem.
- **Lateral Moves:** Includes a variation of the algorithm that allows lateral moves to escape local maxima.
- **Performance Evaluation:** Provides performance metrics and evaluations for different board sizes to analyze the efficiency of the algorithm.

## License

This project is licensed under the [Apache License 2.0](LICENSE).

## Author

Developed by NikTsiop.

