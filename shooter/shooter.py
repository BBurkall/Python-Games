import pygame, random  # Importing necessary libraries

WIDTH = 800  # Width of the game window
HEIGHT = 600  # Height of the game window
BLACK = (0, 0, 0)  # Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
AMMO = 3  # Initial ammunition count

pygame.init()  # Initialize Pygame
pygame.mixer.init()  # Initialize sound mixer
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set up game window
pygame.display.set_caption("Shooter")  # Set the window title
clock = pygame.time.Clock()  # Create a clock object to control the frame rate


# Function to draw text on the screen
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)  # Choose font and size
    text_surface = font.render(text, True, WHITE)  # Create text surface
    text_rect = text_surface.get_rect()  # Get the rectangle around the text
    text_rect.midtop = (x, y)  # Set the position of the text
    surface.blit(text_surface, text_rect)  #Put the text onto the surface


# Function to draw the shield bar
def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGTH = 100  # Length of the shield bar
    BAR_HEIGHT = 10  # Height of the shield bar
    fill = (percentage / 100) * BAR_LENGTH  # Calculate the fill percentage
    border = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)  # Create the border rectangle
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)  # Create the fill rectangle
    pygame.draw.rect(surface, GREEN, fill)  # Draw the filled portion of the shield bar
    pygame.draw.rect(surface, WHITE, border, 2)  # Draw the border of the shield bar


# Function to draw the ammunition bar
def draw_bullets_bar(surface, x, y, ammo):
    BAR_HEIGHT = 50  # Height of the ammunition bar
    BAR_LENGTH = AMMO * 20  # Length of the ammunition bar
    border = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)  # Create the border rectangle
    for i in range(ammo):
        # Create each bullet rectangle and draw them
        bullet = pygame.Rect(x + (i * 20) + 4, y + 4, 12, BAR_HEIGHT * (0.8))
        pygame.draw.rect(surface, RED, bullet)

    pygame.draw.rect(surface, WHITE, border, 2)  # Draw the border of the ammunition bar


# Function to create a new meteor
def create_meteor():
    meteor = Meteor()  # Create a new Meteor object
    all_sprites.add(meteor)  # Add the meteor to the sprite group
    meteor_list.add(meteor)  # Add the meteor to the meteor list


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()  # Load player image
        self.image.set_colorkey(BLACK)  # Set transparent color
        self.rect = self.image.get_rect()  # Get the rectangle around the player image
        self.rect.centerx = WIDTH // 2  # Set initial x-coordinate
        self.rect.bottom = HEIGHT - 10  # Set initial y-coordinate
        self.speed_x = 0  # Horizontal speed
        self.speed_y = 0  # Vertical speed
        self.shield = 100  # Player's shield strength

    def update(self):
        self.speed_x = 0  # Reset horizontal speed
        self.speed_y = 0  # Reset vertical speed
        keystate = pygame.key.get_pressed()  # Get the state of all keyboard keys
        if keystate[pygame.K_LEFT]:  # Move left
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:  # Move right
            self.speed_x = 5
        if keystate[pygame.K_UP]:  # Move up
            self.speed_y = -5
        if keystate[pygame.K_DOWN]:  # Move down
            self.speed_y = 5
        self.rect.x += self.speed_x  # Update x-coordinate
        self.rect.y += self.speed_y  # Update y-coordinate
        # Ensure the player stays within the screen boundaries
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    # Method to shoot bullets
    def shoot(self):
        if len(bullets) < AMMO:  # Ensure maximum ammunition count is not exceeded
            bullet = Bullet(self.rect.centerx, self.rect.top)  # Create a new bullet
            all_sprites.add(bullet)  # Add the bullet to the sprite group
            bullets.add(bullet)  # Add the bullet to the bullet group
            laser_sound.play()  # Play shooting sound


# Meteor class
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)  # Choose a random meteor image
        self.image.set_colorkey(BLACK)  # Set transparent color
        self.rect = self.image.get_rect()  # Get the rectangle around the meteor image
        self.rect.x = random.randrange(WIDTH - self.rect.width)  # Random x-coordinate
        self.rect.y = random.randrange(-140, -100)  # Random y-coordinate above the screen
        self.speedy = random.randrange(1, 10)  # Random vertical speed
        self.speedx = random.randrange(-5, 5)  # Random horizontal speed

    def update(self):
        self.rect.y += self.speedy  # Update y-coordinate
        self.rect.x += self.speedx  # Update x-coordinate
        # If meteor goes off-screen, reset its position and speed
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)
            self.speedx = random.randrange(-5, 5)


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")  # Load bullet image
        self.image.set_colorkey(BLACK)  # Set transparent color
        self.rect = self.image.get_rect()  # Get the rectangle around the bullet image
        self.rect.y = y  # Set initial y-coordinate
        self.rect.centerx = x  # Set initial x-coordinate
        self.speedy = -10  # Bullet speed

    def update(self):
        self.rect.y += self.speedy  # Update y-coordinate
        if self.rect.bottom < 0:  # If bullet goes off-screen, remove it
            self.kill()


# Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]  # Load first frame of explosion animation
        self.rect = self.image.get_rect()  # Get the rectangle around the explosion image
        self.rect.center = center  # Set explosion center
        self.frame = 0  # Current frame of the explosion animation
        self.last_update = pygame.time.get_ticks()  # Time of last update
        self.frame_rate = 50  # Frame rate of the explosion animation

    def update(self):
        now = pygame.time.get_ticks()  # Current time
        if now - self.last_update > self.frame_rate:  # If it's time to update the frame
            self.last_update = now  # Update last update time
            self.frame += 1  # Move to the next frame
            if self.frame == len(explosion_anim):  # If all frames have been shown
                self.kill()  # Remove the explosion sprite
            else:
                center = self.rect.center  # Store current center
                self.image = explosion_anim[self.frame]  # Update image to next frame
                self.rect = self.image.get_rect()  # Get the rectangle around the new image
                self.rect.center = center  # Set the center of the new image


# Function to show the game over screen
def show_gameover_screen():
    screen.blit(background, [0, 0])  # Draw background
    draw_text(screen, "SHOOTER", 65, WIDTH // 2, HEIGHT // 4)  # Draw game title
    draw_text(screen, "Press SPACE to shoot and the arrows to move", 27, WIDTH // 2, HEIGHT // 2)  # Draw instructions
    draw_text(screen, "Press S to Start", 20, WIDTH // 2, HEIGHT * 3 / 4)  # Draw start prompt
    pygame.display.flip()  # Update display
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                return True
            if event.type == pygame.KEYUP and event.key == pygame.K_s:
                waiting = False
                return False


# Load meteor images
meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png",
               "assets/meteorGrey_big4.png",
               "assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png",
               "assets/meteorGrey_small2.png",
               "assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]

for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())

# Load explosion images
explosion_anim = []
for i in range(9):
    file = "assets/regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70, 70))
    explosion_anim.append(img_scale)

# Load background image
background = pygame.image.load("assets/background.png").convert()

# Load sounds
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.2)

pygame.mixer.music.play(loops=-1)

# Game loop
game_over = True
running = True
while running:
    if game_over:
        game_over = show_gameover_screen()
        if game_over:
            break

        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)
        for i in range(8):
            create_meteor()

        score = 0

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    # Collision between meteor and bullets
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 100
        explosion_sound.play()
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        create_meteor()

    # Check for collisions between player and meteors
    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    if hits:
        player.shield -= 25
        create_meteor()
        if player.shield <= 0:
            game_over = True

    screen.blit(background, [0, 0])

    all_sprites.draw(screen)

    # Display score
    draw_text(screen, str(score), 25, WIDTH // 2, 10)

    # Draw shield bar
    draw_shield_bar(screen, 5, 5, player.shield)

    # Draw ammunition bar
    draw_bullets_bar(screen, WIDTH - (20 * AMMO + 5), 5, AMMO - len(bullets))

    pygame.display.flip()
pygame.quit()