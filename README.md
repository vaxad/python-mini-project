# Python Mini Project

## Project Overview

This project is an implementation of a simple online and offline multiplayer game application in Python. The games include "Rock, Paper, Scissors" and "Tic Tac Toe". The project is divided into two parts: the client-side code and the server-side code.

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Game Descriptions](#game-descriptions)
- [Multiplayer Setup](#multiplayer-setup)
- [Offline Mode](#offline-mode)
- [Contributors](#contributors)
- [License](#license)

## Getting Started

To get started, follow the instructions below.

### Prerequisites

- Python 3.11

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/vaxad/python-mini-project.git
   ```

2. Change into the project directory:

   ```bash
   cd python-mini-project
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the multiplayer game application, execute the following commands:

1. Open two terminal/command prompt windows.

2. In the first window, navigate to the project directory and run the server:

   ```bash
   python server.py
   ```

3. In the second window, navigate to the project directory and run the client:

   ```bash
   python client.py
   ```

   Follow the on-screen instructions to select the game mode and make moves.

## Game Descriptions

### Rock, Paper, Scissors

- **Online Mode:** Play against another player online. Both players make their moves simultaneously, and the winner is determined based on the game rules.

- **Offline Mode:** Play against the computer. The computer randomly chooses its move, and the winner is determined based on the game rules.

### Tic Tac Toe

- **Online Mode:** Play against another player online. Both players take turns making moves, and the winner is determined based on the classic Tic Tac Toe rules.

- **Offline Mode:** Play against the computer. The computer makes intelligent moves, aiming to win or block the player from winning.

## Multiplayer Setup

1. **Server Configuration:**
   - Open `server.py` and configure the `hostIp` and `portNumber` variables to match your desired server IP address and port.

2. **Client Configuration:**
   - Open `client.py` and configure the `hostIp` and `portNumber` variables to match the server's IP address and port.

## Offline Mode

For offline mode, you can play against the computer in both "Rock, Paper, Scissors" and "Tic Tac Toe." The computer makes moves based on the game rules and its intelligence in the case of Tic Tac Toe.

## Contributors

- [Varad](https://github.com/vaxad)
- [Tirath](https://github.com/Tirath5504)
- [Vikas](https://github.com/codesbyvikas)

## License

This project is licensed under the [MIT License](LICENSE).

**Note:** The game project may have additional dependencies not listed here. Ensure that you have a compatible Python environment and install any required packages before running the application.
