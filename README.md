# Lab 5: Static Code Analysis — Fitness Club Class Booking Ledger

**Main script:** `gym_system.py`

## About the program

A booking ledger for gym classes such as Yoga, HIIT, and Spin. It books members into classes up to a capacity limit, handles cancellations, and exports the rosters to `gym_schedule.json`.

The code has been analyzed and refactored using static analysis tools (**Pylint**, **Bandit**, and **Flake8**) to ensure high code quality, robust error handling, PEP 8 compliance, and protection against security vulnerabilities.

## How to Run the Program

The project uses a Python virtual environment located in `.lab5/`.

### 1. Activating the Virtual Environment

From the root of this project (`L5_04_fitness_booking`), activate the virtual environment:

```bash
source .lab5/bin/activate
```

*(Optional: If recreating the environment from scratch)*
```bash
python3 -m venv .lab5
source .lab5/bin/activate
pip install -r requirements.txt
```

### 2. Running the Program

With the virtual environment activated:

```bash
python gym_system.py
```

Alternatively, you can run it directly without activating the environment in your shell:

```bash
./.lab5/bin/python gym_system.py
```

When prompted:
```text
How many walk-in guests for HIIT? (Enter for 1):
```
Press **Enter** to accept the default value (`1`) or enter a number of walk-in guests.

### 3. Running Static Analysis Tools

You can verify code quality, security, and formatting using the tools installed in the environment:

- **Pylint** (Code quality and design review):
  ```bash
  pylint gym_system.py
  ```
- **Bandit** (Security vulnerability scanning):
  ```bash
  bandit -r gym_system.py
  ```
- **Flake8** (PEP 8 style and syntax enforcement):
  ```bash
  flake8 gym_system.py
  ```
