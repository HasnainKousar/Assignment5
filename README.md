# Advance calculator with Advance Testing

## Project Overview

### Advanced Testing Practices

This project demonstrates comprehensive testing methodologies:

- **Unit Testing:**
  Each function and class method is tested in isolation using pytest, with over 100% code coverage including edge cases and error conditions.

- **Test Framework:**
  Uses [pytest](https://pytest.org/) with advanced features like fixtures, parameterized tests, and comprehensive assertion methods.

- **Mocking and Patching:**
  Extensive use of `unittest.mock.patch` to isolate units under test, mock dependencies, and simulate error conditions.

- **Fixture-Based Testing:**
  pytest fixtures provide consistent test setup with temporary directories and isolated calculator instances.

- **Error Path Testing:**
  Comprehensive testing of exception handling, including custom exceptions, logging verification, and graceful error recovery.

- **Integration Testing:**
  REPL command testing verifies end-to-end functionality with mocked user input and output verification.

- **Coverage Analysis:**
  Uses pytest-cov to ensure high test coverage and identify untested code paths.

- **Test Organization:**
  Tests are organized by module with clear naming and comprehensive docstrings describing test scenarios.




### Available REPL Commands
- `add`, `subtract`, `multiply`, `divide`, `power`, `root` — Perform arithmetic operations
- `history` — Display calculation history
- `undo` / `redo` — Undo or redo the last operation
- `clear` — Clear the calculation history
- `save` / `load` — Save or load history to/from CSV file
- `help` — Show available commands
- `exit` — Exit the calculator

### Configuration
The calculator can be configured through environment variables:
- `CALCULATOR_AUTO_SAVE` — Enable/disable automatic history saving (default: true)
- `CALCULATOR_MAX_HISTORY` — Maximum number of history entries (default: 100)
- `CALCULATOR_LOG_LEVEL` — Logging level (default: INFO)Module 5 assignment, where we create a modular, extensible calculator application written in Python.  
This project demonstrates demonstrates advanced software engineering practices, including modular design, design patterns (Memento, Observer, Strategy), persistent history, and comprehensive unit testing.

## Advanced Software Engineering Practices

This project demonstrates several advanced software engineering practices and design patterns:

### Design Patterns Implementation

- **Strategy Pattern:** 
  The `Operation` abstract base class defines arithmetic operations, with concrete implementations like `Addition`, `Subtraction`, etc. The calculator can switch between different operations easily.

- **Factory Pattern:** 
  The `OperationFactory` creates operation objects based on string commands, providing a clean interface for operation instantiation without exposing concrete classes.

- **Observer Pattern:** 
  The calculator implements observers (`LoggingObserver`, `AutoSaveObserver`) that automatically respond to calculation events, enabling loose coupling between the calculator core and auxiliary features.

- **Memento Pattern:** 
  The `CalculatorMemento` class captures and restores the calculator's state, enabling undo/redo functionality while maintaining encapsulation.

### Object-Oriented Programming Principles

- **Abstraction:** 
  Abstract base classes like `Operation` and `HistoryObserver` define clear interfaces while hiding implementation details.

- **Encapsulation:**  
  Each module encapsulates its responsibilities - `Calculation` manages individual operations, `Calculator` manages state and history, `InputValidator` handles validation logic.

- **Inheritance:**  
  Concrete operation classes inherit from the `Operation` base class, sharing common structure while implementing specific behaviors.

- **Polymorphism:**  
  The calculator can work with any `Operation` subclass through the common interface, enabling runtime flexibility.




### Error Handling and Logging

- **Custom Exception Classes:** 
  `OperationError` and `ValidationError` provide specific error types for different failure scenarios.

- **Comprehensive Logging:** 
  All operations, errors, and state changes are logged using Python's logging module for debugging and audit trails.

- **Graceful Error Recovery:** 
  The REPL handles various error conditions (KeyboardInterrupt, EOFError, validation errors) without crashing.




## Key Features

- **Arithmetic Operations:** Addition, subtraction, multiplication, division, power, and root operations with robust error handling.
- **Interactive REPL Interface:** Command-line interface with support for operation cancellation, help system, and graceful error handling.
- **History Management:** Calculation history with CSV export/import, automatic saving, and configurable history limits.
- **Undo/Redo Functionality:** Full state management using the Memento pattern for reversible operations.
- **Observer-Based Architecture:** Automatic logging and history saving through configurable observer patterns.
- **Advanced Input Validation:** Comprehensive validation with custom error types and user-friendly error messages.
- **Configurable Logging System:** Structured logging with configurable levels, formats, and output destinations.
- **High Test Coverage:** Extensive unit and integration tests with mocking, fixtures, and error path testing.
- **Error Handling:** Graceful handling of user interrupts, file I/O errors, and unexpected exceptions.

## Project Structure

```
mod5prac/
├── app/
│   ├── __init__.py
│   ├── calculation.py          
│   ├── calculator.py           
│   ├── calculator_config.py    
│   ├── calculator_memento.py   
│   ├── calculator_repl.py      
│   ├── exceptions.py           
│   ├── history.py              
│   ├── input_validators.py     
│   └── operations.py           
├── tests/
│   ├── __init__.py
│   ├── conftest.py             
│   ├── test_calculation.py     
│   ├── test_calculator.py      
│   ├── test_config.py          
│   ├── test_exceptions.py      
│   ├── test_history.py         
│   ├── test_memento.py         
│   ├── test_operations.py      
│   └── test_validators.py      
│   └── calculator_history.csv  
├── logs/
│   └── calculator.log          
├── htmlcov/                    
├── main.py                     
├── requirements.txt           
├── pytest.ini                 
└── README.md
```
## Extending the Calculator

The modular design makes extending functionality straightforward:


## License

This project is licensed under the MIT License.

---

*Created for educational purposes.*

## Setup
- WSL (Windows Subsystem for Linux): developed by Microsoft to enable users to run a Linux enviroment directly on Windows machine. 
- Git: open-source distributed version control system that enables developers to track changes in the source code. 
- VSCode (Visual Studio Code): use to set up python virtual enviroment, and isolating project dependencies
- Python: main programming language for the calculator and tests
- pytest: for advanced testing of the code
- Homebrew(for mac users): for installing packages on macOS

## Setup Instruction

# 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.  
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

## WSL:
On powershell and type the following command to see a list of valid distributions that can be installed.

```bash
wsl --list --online
```
From the list install Ubuntu using the following command:

```bash
wsl --install -d Ubuntu-24.04
```
After it's installed, create a new UNIX username and set password (make sure you remember the password, as there is no way to get it back)

# 🧩 2. Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).  
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ 4. Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).  
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## Create and Activate a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

---

# 🐳 5. (Optional) Docker Setup

> Skip if Docker isn't used in this module.

## Install Docker

- [Install Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- [Install Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## Build Docker Image

```bash
docker build -t <image-name> .
```

## Run Docker Container

```bash
docker run -it --rm <image-name>
```

---

# 🚀 6. Running the Project

- **Without Docker**:

```bash
python main.py
```

(or update this if the main script is different.)

- **With Docker**:

```bash
docker run -it --rm <image-name>
```

---

# 📝 7. Submission Instructions

After finishing your work:

```bash
git add .
git commit -m "Complete Module X"
git push origin main
```

Then submit the GitHub repository link as instructed.

---

# 🔥 Useful Commands Cheat Sheet

| Action                         | Command                                          |
| ------------------------------- | ------------------------------------------------ |
| Install Homebrew (Mac)          | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Install Git                     | `brew install git` or Git for Windows installer |
| Configure Git Global Username  | `git config --global user.name "Your Name"`      |
| Configure Git Global Email     | `git config --global user.email "you@example.com"` |
| Clone Repository                | `git clone <repo-url>`                          |
| Create Virtual Environment     | `python3 -m venv venv`                           |
| Activate Virtual Environment   | `source venv/bin/activate` / `venv\Scripts\activate.bat` |
| Install Python Packages        | `pip install -r requirements.txt`               |
| Build Docker Image              | `docker build -t <image-name> .`                |
| Run Docker Container            | `docker run -it --rm <image-name>`               |
| Push Code to GitHub             | `git add . && git commit -m "message" && git push` |

---

# 📋 Notes

- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and **virtual environments** for Python projects.
- **Docker** is optional depending on the project.

---

# 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)