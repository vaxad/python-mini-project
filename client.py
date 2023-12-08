from socket import *
from threading import *
from tkinter import *
import random
from tkinter import messagebox
import tictactoe
import copy

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

hostIp = "192.168.29.163"
portNumber = 7500

clientSocket.connect((hostIp, portNumber))
gameName = "none"
rps_p1 = []
rps_p2 = []
gameName = "none"   # setting initial game name to make it accessible globally
# function for sending messages to server
def sendMessage(player_choice):
    print(player_choice)
    messsage = str(player_choice)
    clientSocket.send(messsage.encode("utf-8"))

# function for receiving messages from server
def recvMessage():
    try:
        while True:
            serverMessage = clientSocket.recv(1024).decode("utf-8")
            if "RPS" in serverMessage and gameName == "RPS":               # when game is Rock, Paper, Scissors
                rps_p2.append(serverMessage.split(":")[1])
                if len(rps_p1) == len(rps_p2) and len(rps_p1)!= 0:
                    result = determine_winner(rps_p1[-1], rps_p2[-1])
                    txtMessages.insert(END, "\n"+result)                   # taking the "move" from received "RPS:move" message
                elif len(rps_p1) < len(rps_p2):
                    txtMessages.insert(END, "\n"+"other player has choose his move")
            elif "TicTacToe" in serverMessage and gameName == "TicTacToe": # when game is TicTacToe
                row, col = serverMessage.split(":")[1].split(",")          # taking the "row,col" part from received "TicTacToe:row,col" message
                print(row,col)
                game.make_move_mp(int(row), int(col),'O')
    except Exception as e:
        print(e)
        clientSocket.close()

recvThread = Thread(target=recvMessage)     # the recvThread will run the recvMessage functioning the background
recvThread.daemon = True                    # this will make sure that the recvThread is killed when the main thread is killed
recvThread.start()

# function for playing the rps game in multiplayer online mode
def play_game_mp(player_choice):
    rps_p1.append(player_choice)                                            # adding the move to the list   
    sendMessage("RPS:"+player_choice)
    if len(rps_p1) == len(rps_p2) and len(rps_p1)!= 0:
        result = determine_winner(rps_p1[-1], rps_p2[-1])
        txtMessages.insert(END, "\n"+result)
    elif len(rps_p1) > len(rps_p2):
        txtMessages.insert(END, "\n"+"Waiting for other player to choose")  

# function for playing the rps game in single player offline mode
def play_game_sp(player_choice):
    choices = ["Rock", "Paper", "Scissors"]
    computer_choice = random.choice(choices)                                # making the computer choose a random move
    result = determine_winner(player_choice, computer_choice)
    txtMessages.insert(END, "\n"+f"Computer chose {computer_choice}\n{result}")

# function to determine the winner of rps game
def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "It's a tie!"
    elif (
        (player_choice == "Rock" and computer_choice == "Scissors") or
        (player_choice == "Paper" and computer_choice == "Rock") or
        (player_choice == "Scissors" and computer_choice == "Paper")
    ):
        return f"You win! Your choice: {player_choice}, Player2 choice: {computer_choice}"
    else:
        return f"You Loose! Your choice: {player_choice}, Player2 choice: {computer_choice}"

# function to open the rps game in multiplayer online mode
def open_rps_game_mp():
    global gameName
    gameName="RPS"                                                    # setting the game name to "RPS"  
    global txtMessages
    rps_window = Toplevel(start_screen)                                # creating a new window
    rps_window.title("Rock, Paper, Scissors")

    rock_button = Button(rps_window, text="Rock", command=lambda: play_game_mp("Rock"))
    rock_button.pack(pady=10)

    paper_button = Button(rps_window, text="Paper", command=lambda: play_game_mp("Paper"))
    paper_button.pack(pady=10)

    scissors_button = Button(rps_window, text="Scissors", command=lambda: play_game_mp("Scissors"))
    scissors_button.pack(pady=10)

    quit_button = Button(rps_window, text="Quit", command=rps_window.destroy)
    quit_button.pack(pady=10)
    
    txtMessages = Text(rps_window, width=50)
    txtMessages.pack(pady=10)

# function to open the rps game in single player offline mode
def open_rps_game_sp():
    global gameName
    gameName="RPS"                                                          # setting the game name to "RPS"  
    global txtMessages
    rps_window = Toplevel(start_screen)                                     # creating a new window
    rps_window.title("Rock, Paper, Scissors")

    rock_button = Button(rps_window, text="Rock", command=lambda: play_game_sp("Rock"))
    rock_button.pack(pady=10)

    paper_button = Button(rps_window, text="Paper", command=lambda: play_game_sp("Paper"))
    paper_button.pack(pady=10)

    scissors_button = Button(rps_window, text="Scissors", command=lambda: play_game_sp("Scissors"))
    scissors_button.pack(pady=10)

    quit_button = Button(rps_window, text="Quit", command=rps_window.destroy)
    quit_button.pack(pady=10)
    
    txtMessages = Text(rps_window, width=50)
    txtMessages.pack(pady=10)
    
# class for TicTacToe game
class TicTacToe:
    def __init__(self, master, type):
        global gameName
        gameName="TicTacToe"                                            # setting the game name to "TicTacToe"
        self.master = master
        self.master.title("Tic-Tac-Toe")
        self.type=type
        self.board = [[' ' for _ in range(3)] for _ in range(3)]        # Initialize the game board
        self.current_player_sp='X'                                      # Variable to keep track of the current player
        
        # Create buttons for the game grid
        if(self.type=="mp"):
            self.buttons = [[Button(master, text=' ', font=('normal', 20), width=6, height=3, command=lambda row=row, col=col: self.make_move_mp(row, col, 'X')) for col in range(3)] for row in range(3)]
        elif(self.type=="sp1"):
            self.buttons = [[Button(master, text=' ', font=('normal', 20), width=6, height=3, command=lambda row=row, col=col: self.make_move_sp1(row, col)) for col in range(3)] for row in range(3)]
        elif(self.type=="sp2"):
            self.buttons = [[Button(master, text=' ', font=('normal', 20), width=6, height=3, command=lambda row=row, col=col: self.make_move_sp2(row, col)) for col in range(3)] for row in range(3)]
        self.ttt_previous_player=' '
        # Place buttons on the grid
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].grid(row=row, column=col)
    
    # function to make move in multiplayer mode
    def make_move_mp(self, row, col, ttt_current_player):
        try:
            message = "TicTacToe:"+str(row)+","+str(col)
            print(row,col,ttt_current_player)
            if self.board[row][col] == ' ' and ttt_current_player != self.ttt_previous_player:          # Check if the selected cell is empty AND the current player is not the previous player
                # Update the board and button text
                self.board[row][col] = ttt_current_player
                self.buttons[row][col]['text'] = ttt_current_player
                sendMessage(message)
                
                # Check for a winner
                if self.check_winner():
                    if(ttt_current_player=='X'):
                        messagebox.showinfo("Tic-Tac-Toe", f"You win!")
                    else:
                        messagebox.showinfo("Tic-Tac-Toe", f"You Loose!")
                    self.reset_board()
                else:
                    # Check for a tie
                    if self.check_tie():
                        messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")
                        self.reset_board()
                    else:
                        self.ttt_previous_player = ttt_current_player
        except Exception as e:
            print(e)
            
    # function to find the best possible move
    def find_best_move(self):
        # Check for a winning move
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == ' ':
                        # Check if making this move results in a win
                        self.board[row][col] = 'O'
                        if self.check_winner():
                            self.board[row][col] = ' '
                            return row, col

                        # Undo the move
                        self.board[row][col] = ' '

            # Check for a blocking move (to prevent the player from winning)
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == ' ':
                        # Check if blocking this move prevents the player from winning
                        self.board[row][col] = 'X'  # Assume player is 'X'
                        if self.check_winner():
                            self.board[row][col] = ' '
                            return row, col
                        self.board[row][col] = ' '
            # Generate a random move
            empty_cells = [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == ' ']
            row, col = random.choice(empty_cells)
            return row, col

    # function to make move in single player mode using minimax
    def computer_move_minimax(self):
        copy_board = copy.deepcopy(self.board)
        for i in range(len(copy_board)):
            for j in range(len(copy_board[i])):
                if copy_board[i][j] == ' ':
                    copy_board[i][j] = None
        move = tictactoe.minimax(copy_board)
        if move is not None:
            row, col = move
            self.board[row][col] = 'O'
            self.buttons[row][col]['text'] = 'O'

    def computer_move(self):
        # Function for generating computer move
        if random.choice([True, True, True, True, False]):
            self.computer_move_minimax()
        else:
            self.computer_move_random()

        if self.check_winner():
            messagebox.showinfo("Tic-Tac-Toe", f"Player {self.current_player_sp} wins!")
            self.reset_board()
        else:
            # Check for a tie
            if self.check_tie():
                messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")
                self.reset_board()
            else:
                self.current_player_sp = 'X'

    def computer_move_random(self):
        # Function for generating a random move
        empty_cells = [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == ' ']
        row, col = random.choice(empty_cells)
        self.board[row][col] = 'O'
        self.buttons[row][col]['text'] = 'O'
    
    # function to make move in single player player offline mode
    def make_move_sp1(self, row, col):
        # Check if the selected cell is empty
        if self.board[row][col] == ' ':
            # Update the board and button text
            self.board[row][col] = 'X'
            self.buttons[row][col]['text'] = 'X'
            
            # Check for a winner
            if self.check_winner():
                messagebox.showinfo("Tic-Tac-Toe", f"Player {self.current_player_sp} wins!")
                self.reset_board()
            else:
                # Check for a tie
                if self.check_tie():
                    messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")
                    self.reset_board()
                else:
                    self.current_player_sp = 'O'
                    self.computer_move()                # call the function to make the computer move
                    
        else:
            messagebox.showwarning("Tic-Tac-Toe", "Invalid move. Cell already occupied.")
    
    
    # function to make move in multiplayer player offline mode
    def make_move_sp2(self, row, col):
        # Check if the selected cell is empty
        if self.board[row][col] == ' ':
            # Update the board and button text
            self.board[row][col] = self.current_player_sp
            self.buttons[row][col]['text'] = self.current_player_sp
            
            # Check for a winner
            if self.check_winner():
                messagebox.showinfo("Tic-Tac-Toe", f"Player {self.current_player_sp} wins!")
                self.reset_board()
            else:
                # Check for a tie
                if self.check_tie():
                    messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")
                    self.reset_board()
                else:
                    # Switch to the other player
                    self.current_player_sp = 'O' if self.current_player_sp == 'X' else 'X'
        else:
            messagebox.showwarning("Tic-Tac-Toe", "Invalid move. Cell already occupied.")
    
    # function to check if there is a winner
    def check_winner(self):
        # Check rows, columns, and diagonals for a win
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True
        return False
    
    # function to check if there is a tie
    def check_tie(self):
        # Check if the board is full
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    return False
        return True
    
    # function to reset the board
    def reset_board(self):
        # Reset the board and button text
        for row in range(3):
            for col in range(3):
                self.board[row][col] = ' '
                self.buttons[row][col]['text'] = ' '

# function to open the TicTacToe game in multiplayer online mode
def open_tic_tac_toe_mp():
    global game
    root = Tk()
    root.geometry("500x500")

    # Create and start the game
    game = TicTacToe( master=root, type="mp")
    root.mainloop()
    
# function to open the TicTacToe game in multiplayer offline mode
def open_tic_tac_toe_sp_2p():
    global game
    root = Tk()
    root.geometry("500x500")
    # Create and start the game
    game = TicTacToe(master=root, type="sp2")
    root.mainloop()

# function to open the TicTacToe game in single player offline mode
def open_tic_tac_toe_sp_1p():
    global game
    root = Tk()
    root.geometry("500x500")
    # Create and start the game
    game = TicTacToe(master=root, type="sp1")
    root.mainloop()

def main():
    global start_screen
    root = Tk()
    root.title("Game Selection")
    
    heading = Label(root, text="Python project by Varad, Tirath and Vikas", font=("Helvetica", 16))
    heading.pack(pady=10, padx=20)
    
    start_screen = Frame(root)
    start_screen.pack(expand=True, fill='both')

    rps_button = Button(start_screen, text="Rock, Paper, Scissors (Online)", command=open_rps_game_mp)
    rps_button.pack(pady=10)
    
    rps_button2 = Button(start_screen, text="Rock, Paper, Scissors (Offline)", command=open_rps_game_sp)
    rps_button2.pack(pady=10)

    tic_tac_toe_button = Button(start_screen, text="Tic Tac Toe (Online)", command=open_tic_tac_toe_mp)
    tic_tac_toe_button.pack(pady=10)

    tic_tac_toe_button2 = Button(start_screen, text="Tic Tac Toe (Offline - 2p)", command=open_tic_tac_toe_sp_2p)
    tic_tac_toe_button2.pack(pady=10)

    tic_tac_toe_button3 = Button(start_screen, text="Tic Tac Toe (Offline - 1p)", command=open_tic_tac_toe_sp_1p)
    tic_tac_toe_button3.pack(pady=10)

    # function to quit the program
    def quit_program():
        answer = messagebox.askyesno("Quit", "Are you sure you want to quit?")
        if answer:
            clientSocket.close()
            root.destroy()

    quit_button = Button(start_screen, text="Quit", command=quit_program)
    quit_button.pack(pady=10)
    
    for widget in start_screen.winfo_children():
        widget.pack(side="top", anchor="center")        # center aligning the widgets

    root.mainloop()

try:
    main()
except Exception as e:
    print(e)
