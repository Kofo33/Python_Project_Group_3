import pygame
import sys
from classes.constant import WIDTH, HEIGHT, WHITE, BLACK, YELLOW  # Import constants for screen size and colors

# Set up screen dimensions
SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create the main game window

# Load background image for username input screen
input_bg = pygame.image.load("assets/img/Background/bg_username.png").convert_alpha()

def combat(player, enemy, keys): 
    action = None  # Variable to store the chosen action

    # Map key input to actions
    if keys == 1:  # Attack  # Sets actiion = 1 for Action (key A)
        action = 1
    elif keys == 2:  # Heal    # Sets action = 2 for Heal (key H).
        action = 2
    elif keys == 3:  # Flee   #  Sets action = 3 for Flee (key ESC).
        action = 3

    # Execute the chosen action
    if action == 1:  # Attack action
        print("You chose to attack!")
        result, damage = player.use_skill("Basic Attack", enemy)
        if damage == 0:  # If the attack misses, prints “You missed!”.
            print("You missed!")
        else:
            print(result)

    elif action == 2:  # Heal action
        result, _ = player.use_skill("Heal")
        print(result)

    elif action == 3:  # Flee action
        print("You fled the battle!")
        return "fled"  # Exit combat

    # Check if the enemy has been defeated
    if enemy.health <= 0:
        enemy.death()
        print(f"{enemy.name} defeated!")

        # Player gains XP
        leveled_up = player.gain_xp(50)
        if leveled_up:
            print(f"{player.name} leveled up to level {player.level}! Heal skill upgraded.")

    
        return "victory"  # Combat won

    # Enemy attacks after player's turn
    pygame.time.delay(500)  # Short delay before enemy attacks
    damage = enemy.attack_player(player)
    if damage == 0:
        print(f"{enemy.name} missed!")
    else:
        print(f"{enemy.name} deals {damage} damage to you!")

    # Check if player has been defeated
    if player.health <= 0:
        player.death()
        print("You were defeated...")
        return "defeat"

    return None  # Continue combat if neither side has won

def get_username():
    """
    Displays a username input screen and returns the entered username.
    Ensures username is not empty and limited to 15 characters.
    """
    username = ""  # Stores the entered username
    font = pygame.font.SysFont('Comic Sans MS', 25)  # Font for text display
    input_active = True  # Flag to keep the input loop running

    while input_active:
        screen.fill(BLACK)  # Fill screen with black
        screen.blit(input_bg, (10, -50))  # Draw background image

        # Display prompt text
        prompt_text = font.render("Enter your username:", True, YELLOW)
        screen.blit(prompt_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

        # Draw input box
        input_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 40)
        pygame.draw.rect(screen, YELLOW, input_rect, 2)

        # Render the current typed text
        text_surface = font.render(username, True, WHITE)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.flip()   # Updates the screen to show the prompt and input box.

        for event in pygame.event.get():      # it uses a for loop to iterate through events
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:  # Exits the loop if Enter is pressed and the username isn’t empty.
                if event.key == pygame.K_RETURN and username.strip() != "":
                    input_active = False  # Exit loop if username entered
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]  # Remove last character
                else:
                    if len(username) < 15:  # Limit username length
                        username += event.unicode  # Add typed character

    return username  # Return the final username
