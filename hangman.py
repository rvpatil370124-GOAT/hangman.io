import pygame
import math
import random

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)
MESSAGE_FONT = pygame.font.SysFont('comicsans', 50)

RADIUS = 20
GAP = 15
START_X = (WIDTH - (RADIUS * 2 + GAP) * 13) // 2
START_Y = 400
A = 65  # ASCII value for 'A'
letters = []
for i in range(26):
    x = START_X + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = START_Y + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True]) # [x, y, char, visible]

hangman_status = 0
words = ["PYTHON", "PYGAME", "DEVELOPER", "HANGMAN", "CODING", "PROGRAMMING"]
word = ""
guessed = []


def setup_game():
    """Resets the game to its initial state."""
    global hangman_status, guessed, word
    
    hangman_status = 0
    word = random.choice(words)
    guessed = []
    
    for letter in letters:
        letter[3] = True

def draw():
    WIN.fill(WHITE)
    
    title_text = TITLE_FONT.render("Hangman", 1, BLACK)
    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    
    word_text = WORD_FONT.render(display_word, 1, BLACK)
    WIN.blit(word_text, (400, 200))

    for letter in letters:
        x, y, char, visible = letter
        if visible:
            pygame.draw.circle(WIN, BLACK, (x, y), RADIUS, 2)
            text = LETTER_FONT.render(char, 1, BLACK)
            WIN.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

    # Draw hangman
    # Base
    pygame.draw.line(WIN, BLACK, (100, 350), (250, 350), 4)
    # Pole
    pygame.draw.line(WIN, BLACK, (150, 350), (150, 100), 4)
    # Top beam
    pygame.draw.line(WIN, BLACK, (150, 100), (250, 100), 4)
    # Rope
    pygame.draw.line(WIN, BLACK, (250, 100), (250, 150), 2)
    
    if hangman_status >= 1:
        # Head
        pygame.draw.circle(WIN, BLACK, (250, 170), 20, 2)
    if hangman_status >= 2:
        # Body
        pygame.draw.line(WIN, BLACK, (250, 190), (250, 270), 2)
    if hangman_status >= 3:
        # Left Arm
        pygame.draw.line(WIN, BLACK, (250, 210), (220, 240), 2)
    if hangman_status >= 4:
        # Right Arm
        pygame.draw.line(WIN, BLACK, (250, 210), (280, 240), 2)
    if hangman_status >= 5:
        # Left Leg
        pygame.draw.line(WIN, BLACK, (250, 270), (220, 300), 2)
    if hangman_status >= 6:
        # Right Leg
        pygame.draw.line(WIN, BLACK, (250, 270), (280, 300), 2)

    pygame.display.update()

def display_message(message, color=BLACK):
    """Displays a message on the screen for a short time."""
    WIN.fill(WHITE) # Clear the screen
    text = MESSAGE_FONT.render(message, 1, color)
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000) # Pause for 3 seconds

def main():
    global hangman_status, guessed, word

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    setup_game() # Initialize the first game

    while run:
        clock.tick(FPS)
        
  for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                
                for letter in letters:
                    x, y, char, visible = letter
                    if visible:
                        # Check if click is within the button's circular area
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False # Make button invisible
                            guessed.append(char)
                            
                            # Check if guess is incorrect
                            if char not in word:
                                hangman_status += 1
                draw()
                
        # Check for win
        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        
        if won:
            display_message("You Won!", GREEN)
            setup_game() # Start a new game
            
        # Check for loss
        if hangman_status == 6:
            display_message(f"You Lost! The word was: {word}", RED)
            setup_game() # Start a new game

    pygame.quit()

if __name__ == "__main__":
    main()
