# import files
import pygame
import time
import random
import shelve
pygame.font.init()

# window settings
WIDTH, HEIGHT = 1200, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodger")

# get background img
bg_img = pygame.image.load("bg.png")

scale_factor = .6
new_size = (int(bg_img.get_width() * scale_factor), int(bg_img.get_height() * scale_factor))

BG = pygame.transform.scale(bg_img, new_size)

# player character
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 80
PLAYER_SPEED = 10

# asteroids
ASTEROID_WIDTH = 40
ASTEROID_HEIGHT = 40
ASTEROID_SPEED = 8

# main theme
pygame.mixer.init()
pygame.mixer.music.load("pygame-theme.mp3")

FONT = pygame.font.SysFont("comicsans", 50)
MENU_FONT = pygame.font.SysFont("comicsans", 120)

# draw function
def draw(player_rect, elapsed_time, asteroids):
    # bg
    WIN.blit(BG, (-500, -200))

    # player
    pygame.draw.rect(WIN, (255,255,255), player_rect)

    # asteroids
    for asteroid in asteroids:
        pygame.draw.rect(WIN, "red", asteroid)

    # score
    score_text = FONT.render(f"SCORE: {round(elapsed_time)}", 1, "white")
    WIN.blit(score_text, (WIDTH/2 - (score_text.get_width()/2), 10))

    # update display
    pygame.display.update()

# main function
def main():
    # run timer
    run = True

    # player rect
    player = pygame.Rect(WIDTH/2 - (PLAYER_WIDTH/2), (HEIGHT - PLAYER_HEIGHT) - 5, PLAYER_WIDTH, PLAYER_HEIGHT)

    # clock
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    # asteroids
    asteroid_add_increment = 500 # milliseconds
    asteroid_count = 0

    asteroids = []
    hit = False

    # game loop
    while run:
        # fps locker
        asteroid_count += clock.tick(75)
        elapsed_time = time.time() - start_time

        if asteroid_count > asteroid_add_increment:
            asteroid_x = random.randint(0, WIDTH - ASTEROID_WIDTH)
            asteroid = pygame.Rect(asteroid_x, -ASTEROID_HEIGHT, ASTEROID_WIDTH, ASTEROID_HEIGHT)
            asteroids.append(asteroid)

            asteroid_add_increment = max(200, asteroid_add_increment - 5)
            asteroid_count = 0

        # detect for window closing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # input
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x - PLAYER_SPEED >= 0:
            player.x -= PLAYER_SPEED
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x + PLAYER_SPEED + player.width <= WIDTH:
            player.x += PLAYER_SPEED

        # move asteroids
        for asteroid in asteroids[:]:
            asteroid.y += ASTEROID_SPEED
            if asteroid.y > HEIGHT:
                asteroids.remove(asteroid)
            elif asteroid.y + ASTEROID_HEIGHT >= player.y and asteroid.colliderect(player):
                asteroids.remove(asteroid)
                hit = True
                break
        
        if hit:
            game_over_text = FONT.render("You Lost.", 1, "red")
            WIN.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - game_over_text.get_height()/2))

            pygame.display.update()
            time.sleep(2)
            menu()
            break

        # draw
        draw(player, elapsed_time, asteroids)

    # if the loop stops (exit window), we close the window
    pygame.quit()

# menu function
def menu():
    run = True
    play = False
    while run:
         # detect for window closing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            play = True

        if play == True:
            main()
            break

        # show bg
        WIN.blit(BG, (-500, -200))

        # show title
        title_text = MENU_FONT.render("SPACE DODGER", 1, "white")
        WIN.blit(title_text, (WIDTH/2 - (title_text.get_width()/2), (HEIGHT/2 - (title_text.get_height()/2))))

        # show caption 
        caption_text = FONT.render("Press space to play!", 1, "green")
        WIN.blit(caption_text, (WIDTH/2 - (caption_text.get_width()/2), (HEIGHT/2 - (caption_text.get_height()/2)) + 85))

        # update
        pygame.display.update()

# run main
if __name__ == "__main__":
    pygame.mixer.music.play(-1)
    menu()