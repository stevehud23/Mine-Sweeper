############### Mine Sweeper ###################

import tkinter as tk
from tkinter import messagebox
import random
import pygame
import time
import os

previous_points = 0

def toggle_music():
    global music_enabled
    music_enabled = not music_enabled
    if music_enabled:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()
        
def mineSweeper(rows, cols, numMine):
    # Generate empty minesweeper board
    board = [['*' for _ in range(cols)] for _ in range(rows)]

    # Randomize mines on board
    placedMines = 0
    minePos = []  # List for storing mine positions
    while placedMines < numMine:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)

        # Code for randomizing the #'s
        if board[row][col] != '#':
            board[row][col] = '#'
            minePos.append((row, col))  # Storing mine positions
            placedMines += 1

    # Add extra life items
    extra_lives = 0
    while extra_lives < 3:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)

        if board[row][col] == '*':
            board[row][col] = 'E'
            extra_lives += 1

    # Add power-up item
    while True:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)

        if board[row][col] == '*':
            board[row][col] = 'P'
            break

    return board, minePos

colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']

powerup_active = False
powerup_end_time = 0
powerup_count = 1
original_colors = None


def open_profile_window():
    global user
    profile_window = tk.Toplevel(root)
    profile_window.title("switch User Profile")
    
    # Create labels for the text boxes
    username_label = tk.Label(profile_window, text="Username:")
    username_label.grid(row=0, column=0)

    email_label = tk.Label(profile_window, text="Screen Name:")
    email_label.grid(row=1, column=0)

    # Create entry widgets for user input
    username_entry = tk.Entry(profile_window)
    username_entry.grid(row=0, column=1)

    screen_name_entry = tk.Entry(profile_window)
    screen_name_entry.grid(row=1, column=1)

    # Function to handle form submission
    def submit_profile():
        global user_profile_data, username

        username = username_entry.get()
        screen_name = screen_name_entry.get()

        
        # Perform necessary actions with the form data
        # For example, you can display a message box with the entered data
        messagebox.showinfo("Profile Submission", f"Username: {username}\Screen Name: {screen_name}")

        # Update the username in the HUD
        hud_username_label.config(text=username, fg='blue')

        # Save the user profile data in a dictionary
        user_profile_data = {
            "username": username,
            "wins": 0,
            "losses": 0,
            "level": 1,
            "points": 0
        }
        with open("user_stats.txt", "r") as file:
            lines = file.readlines()

            user_exists = False
            updated_lines = []

    # Iterate over the lines and update the wins for the user
            for line in lines:
                if line.startswith(username):
                    parts = line.strip().split(",")
                    if len(parts) == 2:
                        previous_wins = int(parts[1])
                        updated_wins = previous_wins + user_profile_data['wins']
                        updated_line = f"{username},{updated_wins}\n"
                        updated_lines.append(updated_line)
                        user_exists = True
                else:
                    updated_lines.append(line)

            if not user_exists:
                new_entry = f"{username},{user_profile_data['wins']}, {points}\n"
                updated_lines.append(new_entry)

            # Use a temporary file to store the updated contents
            temp_file = "user_stats_temp.txt"

            with open(temp_file, "w") as temp:
                temp.writelines(updated_lines)

            # Rename the temporary file to the original file
            os.replace(temp_file, "user_stats.txt")

    # Add a button to submit the form
    submit_button = tk.Button(profile_window, text="Submit", command=submit_profile)
    submit_button.grid(row=2, columnspan=2)

def update_user_profile(username, new_wins, new_points):
 
    with open("user_stats.txt", "r") as file:
        lines = file.readlines()

    # Update the wins and points for the specific user
    for i in range(len(lines)):
        line = lines[i].strip().split(",")
        if line[0] == username:
            if len(line) == 1:
                # The line only contains the username, so add the wins and points
                line.append(str(new_wins))
                line.append(str(new_points))
            elif len(line) == 2:
                # The line contains the username and wins, so add the points
                line.append(str(new_points))
            else:
                # The line contains the username, wins, and points, so update both
                line[1] = str(new_wins)
                line[2] = str(new_points)
            lines[i] = ",".join(line) + "\n"

    # Write the updated data back to the file
    with open("user_stats.txt", "w") as file:
        file.writelines(lines)
        # Truncate the remaining content in case the new entry is shorter than the previous content
        file.truncate()

        # Close the file
        file.close()

def open_leaderboard():
    leaderboard_window = tk.Toplevel(root)
    leaderboard_window.title("Leaderboard")

    # Read the user stats from the file and display them in a leaderboard format
    with open("user_stats.txt", "r") as file:
        leaderboard_data = []
        for line in file:
            parts = line.strip().split(",")
            if len(parts) >= 3:
                username = parts[0]
                wins = int(parts[1])
                points = int(parts[2])
                leaderboard_data.append((username, wins, points))

    if leaderboard_data:
        # Sort the leaderboard data based on wins in descending order
        leaderboard_data.sort(key=lambda x: x[1], reverse=True)

        # Create a label to display the leaderboard
        leaderboard_label = tk.Label(leaderboard_window, text="Leaderboard", font=("Arial", 16))
        leaderboard_label.pack()

        for i, (username, wins, points) in enumerate(leaderboard_data):
            label_text = f"{i + 1}. {username}: {wins} wins, {points} points"
            entry_label = tk.Label(leaderboard_window, text=label_text)
            entry_label.pack()
    else:
        no_data_label = tk.Label(leaderboard_window, text="No leaderboard data available.")
        no_data_label.pack()


def login_screen():
    global username
    login_sound.play()

    # Disable game menu items
    file_menu.entryconfig("New Game", state='disabled')
    file_menu.entryconfig("Exit", state='normal')
    user_menu.entryconfig("User Profile", state='disabled')

    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.transient(root)  # Set the login window as a transient window of the root window


    def on_login_window_close():
        # Show the root window again
        root.deiconify()

    # Configure the login window close event
    login_window.protocol("WM_DELETE_WINDOW", on_login_window_close)
     # Set the position of the login window to the center of the screen
    login_window_width = 300
    login_window_height = 90
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (login_window_width / 2))
    y_coordinate = int((screen_height / 2) - (login_window_height / 2))
    login_window.geometry(f"{login_window_width}x{login_window_height}+{x_coordinate}+{y_coordinate}")
    # Create a label and entry widget for the username
    username_label = tk.Label(login_window, text="Username:")
    username_label.grid(row=0, column=0)
    username_entry = tk.Entry(login_window)
    username_entry.grid(row=0, column=1)
    options_menu.add_command(label="Leaderboard", command=open_leaderboard)
    # Create a button to submit the login
    login_button = tk.Button(login_window, text="Login", command=lambda: submit_login(login_window, username_entry.get()))
    login_button.grid(row=1, columnspan=2)
    disable_game_buttons()
    
    def bring_login_window_to_front():
        login_window.lift()

        # Configure the root window focus event to bring the login window to the front
        root.bind("<FocusIn>", lambda event: bring_login_window_to_front())

    # Function to handle login submission
    def submit_login(window, entered_username):
        global username, user_profile_data, previous_points
        if entered_username:
            username = username_entry.get()
            login_window.lift()
            login_ok_sound.play()
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
             # Update the username in the HUD
            hud_username_label.config(text=username, fg='blue')
            window.destroy()
            # Enable the game buttons
            enable_game_buttons()
            # Initialize user profile data
            user_profile_data = {
                        "username": username,
                        "wins": 0,
                        "losses": 0,
                        "level": 1,
                        "points": 0
                                }
            #with open("user_stats.txt", "a") as file:
                #file.write(f"{username},{user_profile_data['wins']}\n")

            with open("user_stats.txt", "r+") as file:
                lines = file.readlines()
                file.seek(0)  # Move the file pointer to the beginning of the file

                user_exists = False  # Flag to check if the user already exists in the file
                updated_lines = []

    # Iterate over the lines and update the wins for the user
                for line in lines:
                    if line.startswith(username):
                        parts = line.strip().split(",")
                        if len(parts) == 2:
                            previous_wins = int(parts[1])
                            updated_wins = previous_wins + user_profile_data['wins']
                            updated_line = f"{username},{updated_wins}\n"
                            updated_lines.append(updated_line)
                        if len(parts) == 4:
                            previous_points = int(parts[2])
                            updated_points = previous_points + user_profile_data['points']
                            updated_line = f"{username},{updated_wins},{updated_points}\n"
                            updated_lines.append(updated_line)
                        
                            user_exists = True
                    else:
                        updated_lines.append(line)

                # If the user doesn't exist, write a new entry
                if not user_exists:
                    new_entry = f"{username},{user_profile_data['wins']},{user_profile_data['points']}\n"
                    updated_lines.append(new_entry)

    # Write the updated lines back to the file
                file.writelines(updated_lines)

    # Truncate the remaining content in case the new entry is shorter than the previous content
                file.truncate()
            if user_exists:
                user_profile_data['wins'] += previous_wins
                user_profile_data['points'] += previous_points



        else:
            messagebox.showerror("Invalid Username", "Please enter a valid username.")

    # Disable the game buttons until the user logs in
            disable_game_buttons()

def enable_game_buttons():
    global game_enabled
    game_enabled = True
    for i in range(rows):
        for j in range(cols):
            button[i][j].config(state='normal')

    # Re-enable game menu items
    file_menu.entryconfig("New Game", state='normal')
    file_menu.entryconfig("Exit", state='normal')
    user_menu.entryconfig("User Profile", state='normal')

# Disables in game functionality when called 
def disable_game_buttons():
    global game_enabled
    game_enabled = False
    for i in range(rows):
        for j in range(cols):
            button[i][j].config(state='disabled')

# achievements function
def show_achievement(message):
    global acheivements_count
    achievement_sound1.play()
    messagebox.showinfo(f"Achievement Unlocked!", message)
    acheivements_count += 1
    achievement_count_label.config(text=f"Achievements: {acheivements_count}")

# Keeps count of E cells collected and sets a global variable     
def check_extra_lives_collected():
    global extra_lives_collected
    extra_lives_collected = 0
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == 'E' and clicked[i][j]:
                extra_lives_collected += 1

# Checks if all E cells collected and returns an acheivement if requiremnts are met 
def check_all_extra_lives_collected():
    global all_extra_lives_collected
    if extra_lives_collected == 3 and not all_extra_lives_collected:
        all_extra_lives_collected = True
        show_achievement(f"You Collected All Extra Lives!\n\n***** + 150 POINTS *****")
        extra_point.play()

# Count all X point squares pressed
def count_X_squares():
    global square_count, x_cell
    square_count = rows * cols - numMines - powerup - 3
    x_cell = square_count
    return x_cell - 1 

# Basic Animation fx     
def animate_glitter(row, col, duration, interval):
    colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']

    def glitter():
        nonlocal duration  # Use nonlocal to access and modify the duration variable
        if duration <= 0:
            button[row][col].config(bg='green')  # Change the color back to green after animation
            return

        if board[row][col] == 'E':  # Apply glitter effect only to 'E' squares
            color = random.choice(colors)
            button[row][col].config(bg=color)
        root.after(interval, glitter)
        duration -= interval

    glitter()

# This function Reveals cells and determines if the powerup function is activated 
def reveal_cell(row, col):
    global points, square_count, tries_left, extra_lives, powerup_active, powerup_end_time, powerup_count, original_colors, extra_lives_label
    if powerup_active and time.time() < powerup_end_time:
        # Power-up is active
        for i in range(rows):
            for j in range(cols):
                random_color = random.choice(colors)
                button[i][j].config(bg=random_color)
                is_cell_clickable[i][j] = True

        if clicked[row][col] or not is_cell_clickable[row][col]:
            return

        clicked[row][col] = True

        # Determines if all # cells have been clicked, 
        # plays a sound for ever # cell clicked,
        # and keeps a countdown to determine if player has used an extra life if collected
        # also adds animation for an E cell clicked  
        if board[row][col] == '#':
            button[row][col].config(text='#', bg='red')
            explosion_sound.play()
            tries_left -= 1
            if tries_left == 0:
                if extra_lives > 0:
                    tries_left = 1
                    extra_lives -= 1
                    messagebox.showinfo("Game Over", f"You clicked on a mine! But you have an extra life. Total Points: {points}")
                else:
                    messagebox.showinfo("Game Over", f"You clicked on a mine! Game Over. Total Points: {points}")
                    reset_game()
                    points = 0
        elif board[row][col] == 'E':
            button[row][col].config(text='E', bg='green')
            extra_lives += 1
            points += 150
            extra_life_sound.play()
            button[row][col].config(state='disabled')
            extra_lives_label.config(text=f"Extra Lives: {extra_lives}")
            check_extra_lives_collected()  # Call the function to check extra lives collected
            check_all_extra_lives_collected()  # Call the function to check all extra lives collected
            if extra_lives % 3 == 0:
                points += 150
            # Call the glitter effect animation for the E square
            animate_glitter(row, col, duration=10000, interval=50)

        elif board[row][col] == 'P':
            button[row][col].config(text='P', bg='orange')
            powerup_sound.play()
            powerup_active = True
            powerup_end_time = time.time() + 15
            powerup_count -= 1
            powerup_count_label.config(text=f"Power-ups: {powerup_count}")
            button[row][col].config(state='disabled')
            for i in range(rows):
                for j in range(cols):
                    if board[i][j] != '#':
                        random_color = random.choice(colors)
                        button[i][j].config(bg=random_color)
                        is_cell_clickable[i][j] = False
            original_colors = [[button[i][j]['bg'] for j in range(cols)] for i in range(rows)]
            
        else:
            button[row][col].config(text='X', bg='grey')
            # Play a different sound for points collected during power-up
            point_powerup_sound.play()
            points += 2
            square_count -= 1  # Decrease the value of square_count by 1
            #print(square_count)
            update_hud()
            check_win()
            # Update the points in the user profile
            update_user_profile(username, user_profile_data['wins'], points)
            return square_count
            
    else:
        if clicked[row][col] or not is_cell_clickable[row][col]:
            return
        clicked[row][col] = True

        if board[row][col] == '#':
            button[row][col].config(text='#', bg='red')
            explosion_sound.play()
            tries_left -= 1
            if tries_left == 0:
                if extra_lives > 0:
                    tries_left = 1
                    extra_lives -= 1
                    messagebox.showinfo("Game Over", f"You clicked on a mine! But you have an extra life. Total Points: {points}")
                else:
                    messagebox.showinfo("Game Over", f"You clicked on a mine! Game Over. Total Points: {points}")
                    reset_game()
                    points = 0
                    

        elif board[row][col] == 'E':
            button[row][col].config(text='E', bg='green')
            extra_lives += 1
            points += 5
            extra_life_sound.play()
            button[row][col].config(state='disabled')
            extra_lives_label.config(text=f"Extra Lives: {extra_lives} Collected")
            check_extra_lives_collected()  # Call the function to check extra lives collected
            check_all_extra_lives_collected()  # Call the function to check all extra lives collected
            if extra_lives % 3 == 0:
                points += 150
            # Call the glitter effect animation for the E square
            animate_glitter(row, col, duration=10000, interval=50)

        elif board[row][col] == 'P':
            button[row][col].config(text='P', bg='orange')
            powerup_sound.play()
            powerup_active = True
            powerup_end_time = time.time() + 15
            powerup_count -= 1
            powerup_count_label.config(text=f"Power-ups: {powerup_count}")
            button[row][col].config(state='disabled')

        else:
            button[row][col].config(text='X', bg='grey')
            # Play the original points collected sound when a point ('X') cell is revealed
            point_sound.play()
            points += 1
            square_count -= 1  # Decrease the value of square_count by 1
            #print(square_count)
            update_hud()
            check_win()
            return square_count
            
            
    if powerup_active and time.time() >= powerup_end_time:
        powerup_active = False
        for i in range(rows):
            for j in range(cols):
                if not clicked[i][j]:  # Only reset unclicked squares
                    #if board[i][j] != '#':
                        if original_colors is not None:
                            button[i][j].config(bg=original_colors[i][j])
                        else:
                            button[i][j].config(bg='red' if developer_mode else 'SystemButtonFace')
                    #is_cell_clickable[i][j] = True  # Make all cells clickable again

        # Reset original_colors variable after power-up ends
        original_colors = None

    # Update the HUD labels after each click
    update_hud()
    # Check for a win after revealing a cell
    check_win()

####################### DEVELOPER MODE TOOLS ####################
def reveal_all_cells():
    # Function to reveal all cells' content (for debug purposes)
    global clicked
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == '#':
                button[i][j].config(text='#', bg='red')
            elif board[i][j] == 'E':
                button[i][j].config(text='E', bg='green')
            elif board[i][j] == 'P':
                button[i][j].config(text='P', bg='orange')
            # else:
            #     button[i][j].config(text='X', bg='grey')
            # clicked[i][j] = True  # Mark all buttons as clicked           
######################################################################

achieved_1000_points = False  # Initialize flag variable
# Function to check if all points have been collected check win status
def check_win():
    global points, previous_points, all_extra_lives_collected, username, user_profile_data, update_user_profile, achieved_1000_points
    
    # Counts down the remainder of the X squares left in the game returns a win if all X squares are == 0 
    if square_count == 0:
        pygame.mixer.music.stop()  # stop main music 
        winner_sound.set_volume(0.4) 
        winner_sound.play()
        achievement_sound1.play()
        messagebox.showinfo("Level Completed!", f"Congratulations! You collected all points\nTotal Points: {points}")
        user_profile_data["wins"] += 1
        user_profile_data["points"] += points
        update_user_profile(username, user_profile_data['wins'], points)
        reset_game()

    # Unlocks an acheivement if player score reaches 1000 points 
    if points >= 1000 and not achieved_1000_points:
        points += 1000
        show_achievement("Congratulations!! You made it to: 1000pts\nYou gained: +1000pts")
        update_hud()
        achievement_sound1.play()
        extra_point.play()
        achieved_1000_points = True  # Set flag to True after executing the achievement

        
    
# updates in game HUD with relevent game information
def update_hud():
    points_label.config(text=f"Points: {points}")
    tries_left_label.config(text=f"Tries Left: {tries_left}")
    extra_lives_label.config(text=f"Extra Lives: {extra_lives} Collected ")

def reset_game():
    global board, clicked, points, tries_left, all_extra_lives_collected, extra_lives, powerup_count, powerup_active, powerup_end_time, is_cell_clickable, previous_points
    all_extra_lives_collected = False
    # Reset game state variables
    board, minePos = mineSweeper(rows, cols, numMines)
    clicked = [[False for _ in range(cols)] for _ in range(rows)]
    tries_left = 3
    extra_lives = 0
    powerup_count = 1
    powerup_active = False
    powerup_end_time = 0

    count_X_squares()
    is_cell_clickable = [[True for _ in range(cols)] for _ in range(rows)]  # Initialize cell clickable status
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.5)  # Set the volume to 50%
    winner_sound.set_volume(0.0)
    # Reset buttons
    for i in range(rows):
        for j in range(cols):
            button[i][j].config(text='', bg='SystemButtonFace', state='normal')

    # Reset HUD labels
    update_hud()
    powerup_count_label.config(text=f"Power-ups: {powerup_count}")
    # Check if all game buttons are disabled
    all_buttons_disabled = all(button[i][j]['state'] == 'disabled' for i in range(rows) for j in range(cols))
    if all_buttons_disabled:
        confirm_exit = messagebox.askyesno("Exit", "Are you sure you want to exit the game?")
        if confirm_exit:
            root.destroy()  # Close the main window
    

# Initialize game parameters
rows = 6
cols = 6
numMines = 5
tries_left = 3
extra_lives = 0
powerup = 1
powerup_count = 1
powerup_active = False
powerup_end_time = 0
square_count = rows * cols - numMines - powerup - 3
x_cell = square_count
is_cell_clickable = [[True for _ in range(cols)] for _ in range(rows)]  # Initialize cell clickable status
developer_mode = False  # Variable to keep track of developer mode
all_extra_lives_collected = False  # Variable to keep track of all extra lives collected
acheivements_count = 0
# Create mine sweeper board
board, minePos = mineSweeper(rows, cols, numMines)
# Initialize clicked status for each cell
clicked = [[False for _ in range(cols)] for _ in range(rows)]


# Initialize Pygame mixer for sound
pygame.mixer.init()
explosion_sound = pygame.mixer.Sound('explosion.wav')
point_sound = pygame.mixer.Sound('point.wav')
extra_life_sound = pygame.mixer.Sound('extra_life.wav')
powerup_sound = pygame.mixer.Sound('powerup (2).wav')
point_powerup_sound = pygame.mixer.Sound('point_powerup.wav')
achievement_sound1 = pygame.mixer.Sound('acheivement_sound1.wav')
extra_point = pygame.mixer.Sound('extra_point.wav')
extra_point_volume = 1.0
extra_point.set_volume(extra_point_volume)
winner_sound = pygame.mixer.Sound('winner.mp3')
login_sound = pygame.mixer.Sound('futureistic.wav')
login_ok_sound = pygame.mixer.Sound('login_ok.wav')
bonus_points_sound = pygame.mixer.Sound('transition-sweep.wav')
# Initialize Tkinter GUI
default_width = 700
default_height = 600
root = tk.Tk()
root.title("Mine Sweeper")
root.geometry(f"{default_width}x{default_height}")


# Create buttons
button = []
for i in range(rows):
    button.append([])
    for j in range(cols):
        btn = tk.Button(root, width=2, command=lambda row=i, col=j: reveal_cell(row, col))
        btn.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")
        button[i].append(btn)


# Configure grid weights for resizing
for i in range(rows):
    tk.Grid.columnconfigure(root, i, weight=1)
for j in range(cols):
    tk.Grid.rowconfigure(root, j, weight=1)

# initalise points variable
points = 0

# Create HUD labels
points_label = tk.Label(root, text=f"Points: {points}", font=('Arial', 12))
points_label.grid(row=rows+1, column=0, columnspan=cols, pady=5, sticky='w')
tries_left_label = tk.Label(root, text=f"Tries Left: {tries_left}", font=('Arial', 12))
tries_left_label.grid(row=rows+2, column=0, columnspan=cols, pady=5, sticky='w')
extra_lives_label = tk.Label(root, text=f"Extra Lives: {extra_lives} Collected", font=('Arial', 12))
extra_lives_label.grid(row=rows+3, column=0, columnspan=cols, pady=5, sticky='w')
powerup_count_label = tk.Label(root, text=f"Power-ups: {powerup_count}", font=('Arial', 12))
powerup_count_label.grid(row=rows+4, column=0, columnspan=cols, pady=5, sticky='w')
achievement_count_label = tk.Label(root, text=f"Acheivements: {acheivements_count}", font=('Arial', 12))
achievement_count_label.grid(row=rows+5, column=0, columnspan=cols, pady=5, sticky='w')
# Create a label in the HUD for displaying the username
hud_username_label = tk.Label(root, text=f"Enter User Name:", font=("Arial", 16), fg="red")
hud_username_label.grid(row=rows+1, column=0, columnspan=cols, pady=5)

############ Create developer option button ################
developer_button = tk.Button(root, text="Developer Option", command=lambda: toggle_developer_mode(developer_button))
developer_button.grid(row=rows + 6, column=0, columnspan=cols, pady=5)

def toggle_developer_mode(button):
    global developer_mode
    developer_mode = not developer_mode
    if developer_mode:
        button.config(text="Exit Developer Mode")
        reveal_all_cells()  # Reveal all cells when entering developer mode
    else:
        button.config(text="Developer Option")
##############################################################

# Create the menu bar
menu_bar = tk.Menu(root)

# Create the "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New Game", command=reset_game)
file_menu.add_command(label="Exit", command=root.destroy)

# Create the "Options" menu
options_menu = tk.Menu(menu_bar, tearoff=0)
options_menu.add_command(label="Toggle Music", command=toggle_music)

# Create the "User" menu
user_menu = tk.Menu(menu_bar, tearoff=0)
user_menu.add_command(label="User Profile", command=login_screen)

# Add the menus to the menu bar
menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Options", menu=options_menu)
menu_bar.add_cascade(label="Switch User", menu=user_menu)

# Configure the root window with the menu bar
root.config(menu=menu_bar)
#root.attributes("-fullscreen", True)

# Load and play background music
playlist = ['phantom.mp3', 'the_shield.mp3']
current_track = 0
pygame.mixer.music.load(playlist[current_track])
pygame.mixer.music.set_volume(0.4)  # Set the volume to 40% 
music_enabled = True
pygame.mixer.music.play(-1)
login_screen()
root.mainloop()















