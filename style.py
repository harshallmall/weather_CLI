# position
PADDING = 20

# color
RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[33m"
WHITE = "\033[37m"

# color effects
REVERSE = "\033[;7m"
RESET = "\033[0m"

# function to change colors
def change_color(color):
    print(color, end="")
