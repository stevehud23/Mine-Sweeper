# Self study project 1
=============================================================================

                                       Mine Sweeper
                            
=============================================================================

Table of Contents:
------------------
1. Introduction
     
2. Usage
     
3.0 Function Documentation

    3.1. Acknowledgements:
    3.2. More game info / video
   
1. Introduction:
----------------
BEFORE RUNNING THIS APP PLEASE INSTALL THE FOLLOWING:

tkinter: Python's standard GUI package -- pip install tkinter

pygame: Library for audio playback     -- pip install pygame


# This game was originally taken from a mock interview question on list comprehention for hashes and dashes. I initially just wanted to see my code do something outside of a terminal there is much work left to do with this game.

    - Update GUI
    - Add more functionality to the game
    - Create more achievements
    - Refactorise the code
    - level selection menu



This code provides a basic implementation of the Mine Sweeper game using the Tkinter library for the graphical user interface (GUI) and the Pygame library for sound effects.  A player must try to score as much points as possible without getting a game over or the points will be set to zero.

---------

2. Usage:
To start Mine Sweeper, follow these steps:

    1. Clone the repository or download the code files to your local machine.
    2. Navigate to the directory where the code files are located.
    3. Run the following command to start the Mine Sweeper game:   python minesweeper.py

    4. The game window will open, and you can start playing by clicking on the buttons to reveal the cells. 
    Avoid clicking on the mine cells, collect points and power-ups, and try to reveal all X (point) squares to win the game.
    You can access additional features, such as user profiles and leaderboards, by interacting with the provided windows and buttons within the game.
  
    5. The game application window will open, displaying a login screen with several options disabled.
    6. create or enter a username already used.
    7. Follow the on-screen instructions or prompts, if any.
    8. To exit the application befor game start, select the "X"(close) button from window or click the file options menu from the menu bar and select Exit.

--------------------------------
3.0 Function Documentation:
        
        The code is divided into several functions, each serving a specific purpose. Here is an overview of the main functions:

        - toggle_music()
            This function toggles the background music on/off. It uses the pygame.mixer.music module to control the music playback.

        - mineSweeper(rows, cols, numMine)
            This function generates a Mine Sweeper board with the specified number of rows, columns, and mines. It returns the generated board as a 2D list and a list of mine positions.

        - open_profile_window()
            This function opens a new window for the user to enter their profile information, such as username and screen name. It uses the tkinter library to create the window and handle user input.

        - update_user_profile(username, new_wins, new_points)
            This function updates the user profile data in the user_stats.txt file. It takes the username, new number of wins, and new points as input and modifies the corresponding entry in the file.

        - open_leaderboard()
            This function opens a leaderboard window that displays the user statistics from the user_stats.txt file. It reads the data from the file, sorts it based on wins, and displays it in the window.

        - login_screen()
            This function creates a login screen window where the user can enter their username. It also handles the submission of the login form, updates the user profile, and enables/disables game buttons based on the login status.

        - enable_game_buttons() and disable_game_buttons()
            These functions enable/disable the game buttons based on the login status. They are called when the user logs in or logs out.

        - show_achievement(message)
            This function displays an achievement message box with the provided message. It also increments the achievement count and updates the corresponding label.

        - check_extra_lives_collected() and check_all_extra_lives_collected()
            These functions check if the user has collected all extra lives. They are called when an extra life is collected to update the count and check if all lives have been collected.

        - count_X_squares()
            This function counts the number of X (point) squares remaining on the board and returns the count.

        - animate_glitter(row, col, duration, interval)
            This function creates an animation effect on the E (extra life) squares. It changes their background color randomly for a specified duration and interval.

        - reveal_cell(row, col)
            This function handles the revealing of a cell on the board when the user clicks on a button. It updates the board state, checks for mines, extra lives, power-ups, and X squares, and updates the HUD and game status accordingly.

        - check_win()
            This function checks if the game has been won by checking if all X (point) squares have been revealed. If so, it stops the music, plays a winning sound, displays a congratulatory message, updates the user profile, and resets the game.

        - reset_game()
            This function resets the game state, including the board, clicked status, points, tries left, extra lives, power-up count, and other variables. It also resets the buttons, HUD labels, and checks if all buttons are disabled to prompt a confirmation dialog before exiting the game.

------------------------------ 
3.1  Acknowledgements:

        - Acknowledgements:
            This code is based on a sample implementation of the Mine Sweeper game and has been modified and expanded to include additional features such as user profiles, achievements, and a leaderboard. The original code was created using the Tkinter and Pygame libraries, which are widely used for GUI and game development in Python.
        
------------------------------
3.2. More game info / video:

[this file has not been uploaded to youtube yet please download to view 'click the link & view raw to download'](https://github.com/stevehud23/Mine-Sweeper/blob/main/MineSweeper(2).mp4)
    

Note: The code provided in the documentation may not include the complete implementation details. Please refer to the actual code for the complete implementation.
