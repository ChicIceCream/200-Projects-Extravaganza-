import pygame
import cv2
import numpy as np
import os

# --- Configuration ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PLAYER_COLOR = (255, 100, 100) # A reddish color for the player
PLATFORM_COLOR = (50, 150, 50) # A green for platforms

# Player settings
PLAYER_ACC = 0.7
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.7
PLAYER_JUMP_STRENGTH = -15 # Negative because y-axis is inverted

# Platform generation settings
CANNY_THRESHOLD1 = 10
CANNY_THRESHOLD2 = 450
MIN_CONTOUR_AREA = 50 # Ignore very small contours
MIN_PLATFORM_LENGTH = 30 # Minimum pixel length for a horizontal/vertical segment to be a platform
PLATFORM_THICKNESS = 8 # Thickness of generated platforms/walls

# --- Player Class ---
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.vel.y = PLAYER_JUMP_STRENGTH
            self.on_ground = False

    def update(self, platforms):
        self.acc = pygame.math.Vector2(0, PLAYER_GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # Apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # Equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Keep player on screen (simple boundary)
        if self.pos.x > SCREEN_WIDTH - self.rect.width:
            self.pos.x = SCREEN_WIDTH - self.rect.width
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.x = self.pos.x
        self.collide_with_platforms(platforms, 'x')
        self.rect.y = self.pos.y
        self.on_ground = False # Assume not on ground until collision check
        self.collide_with_platforms(platforms, 'y')

        # If fallen off screen, reset position (simple respawn)
        if self.rect.top > SCREEN_HEIGHT:
            self.pos.y = 0 # Or some other starting y
            self.pos.x = SCREEN_WIDTH / 2
            self.vel.y = 0


    def collide_with_platforms(self, platforms, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, platforms, False)
            for hit in hits:
                if self.vel.x > 0: # Moving right
                    self.rect.right = hit.rect.left
                elif self.vel.x < 0: # Moving left
                    self.rect.left = hit.rect.right
                self.pos.x = self.rect.x
                self.vel.x = 0
        
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, platforms, False)
            for hit in hits:
                if self.vel.y > 0: # Moving down
                    self.rect.bottom = hit.rect.top
                    self.on_ground = True
                elif self.vel.y < 0: # Moving up
                    self.rect.top = hit.rect.bottom
                self.pos.y = self.rect.y
                self.vel.y = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# --- Platform Class ---
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# --- Image Processing Function ---
def process_image_to_platforms(image_path):
    if not os.path.exists(image_path):
        print(f"Error: Image path '{image_path}' not found.")
        return [], None

    try:
        img_cv = cv2.imread(image_path)
        if img_cv is None:
            print(f"Error: OpenCV could not read image '{image_path}'.")
            return [], None
    except Exception as e:
        print(f"Error reading image with OpenCV: {e}")
        return [], None

    img_height_orig, img_width_orig = img_cv.shape[:2]

    # 1. Preprocess
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 2. Canny Edge Detection
    edges = cv2.Canny(blurred, CANNY_THRESHOLD1, CANNY_THRESHOLD2)

    # 3. Find Contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    platform_data = [] # Store (x, y, w, h) for platforms

    # Scaling factors
    scale_x = SCREEN_WIDTH / img_width_orig
    scale_y = SCREEN_HEIGHT / img_height_orig

    # 4. Filter & Convert Contours to Platforms
    for cnt in contours:
        if cv2.contourArea(cnt) < MIN_CONTOUR_AREA:
            continue

        x_cv, y_cv, w_cv, h_cv = cv2.boundingRect(cnt)

        # Attempt to identify horizontal platforms
        if w_cv > h_cv * 2 and w_cv * scale_x > MIN_PLATFORM_LENGTH: # Wider than tall, and long enough
            plat_x = int(x_cv * scale_x)
            plat_y = int(y_cv * scale_y) # Top of the bounding box
            plat_w = int(w_cv * scale_x)
            plat_h = PLATFORM_THICKNESS
            platform_data.append((plat_x, plat_y, plat_w, plat_h))
            # Add another platform at bottom of horizontal feature for 'ceilings'
            # plat_y_ceil = int((y_cv + h_cv) * scale_y) - PLATFORM_THICKNESS
            # platform_data.append((plat_x, plat_y_ceil, plat_w, plat_h))


        # Attempt to identify vertical platforms (walls)
        elif h_cv > w_cv * 2 and h_cv * scale_y > MIN_PLATFORM_LENGTH: # Taller than wide, and tall enough
            plat_x = int(x_cv * scale_x)
            plat_y = int(y_cv * scale_y)
            plat_w = PLATFORM_THICKNESS
            plat_h = int(h_cv * scale_y)
            platform_data.append((plat_x, plat_y, plat_w, plat_h))
            # Add another wall on the other side of vertical feature
            # plat_x_right = int((x_cv + w_cv) * scale_x) - PLATFORM_THICKNESS
            # platform_data.append((plat_x_right, plat_y, plat_w, plat_h))


    print(f"Generated {len(platform_data)} potential platforms from image.")
    
    # Convert OpenCV image (BGR) to Pygame image (RGB)
    # Pygame uses RGB, OpenCV uses BGR
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    # OpenCV images are (height, width, channels), Pygame wants (width, height)
    # The frombuffer needs data, (width,height), format
    # img_cv.shape[1] is width, img_cv.shape[0] is height
    try:
        background_pygame_image = pygame.image.frombuffer(img_rgb.tobytes(), (img_width_orig, img_height_orig), "RGB")
        background_pygame_image = pygame.transform.scale(background_pygame_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception as e:
        print(f"Error converting OpenCV image to Pygame image: {e}")
        return platform_data, None # Return platform data even if background fails

    return platform_data, background_pygame_image


# --- Game State Enum (simple version) ---
class GameState:
    IMAGE_SELECTION = 1
    GAMEPLAY = 2
    SHOW_EDGES_DEBUG = 3 # Optional: For debugging Canny

# --- Main Game Function ---
def game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Photo Platformer")
    clock = pygame.time.Clock()

    current_state = GameState.IMAGE_SELECTION
    
    player = None
    all_sprites = pygame.sprite.Group()
    platforms_group = pygame.sprite.Group()
    background_image = None
    
    # For text input
    font = pygame.font.Font(None, 36)
    input_text = ""
    input_active = True
    
    # Debug image
    debug_edges_image = None


    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0 # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if current_state == GameState.IMAGE_SELECTION:
                if event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            image_path = input_text.strip()
                            platform_coords, bg_img = process_image_to_platforms(image_path)
                            
                            if bg_img: # Successfully processed
                                # Clear old game elements
                                all_sprites.empty()
                                platforms_group.empty()

                                for p_data in platform_coords:
                                    platform = Platform(p_data[0], p_data[1], p_data[2], p_data[3])
                                    platforms_group.add(platform)
                                    # all_sprites.add(platform) # Don't add to all_sprites if only drawing background and player over it

                                player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100) # Start near bottom
                                all_sprites.add(player)
                                
                                background_image = bg_img
                                current_state = GameState.GAMEPLAY
                                input_text = "" # Clear for next time
                                input_active = False # Deactivate input box
                            else:
                                print("Failed to load or process image. Please try another path.")
                                input_text = "" # Clear input on failure
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        else:
                            if len(input_text) < 100: # Limit input length
                                input_text += event.unicode
                
            elif current_state == GameState.GAMEPLAY:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.jump()
                    if event.key == pygame.K_r: # Reset key
                        current_state = GameState.IMAGE_SELECTION
                        input_active = True
                        player = None
                        all_sprites.empty()
                        platforms_group.empty()
                        background_image = None
                    if event.key == pygame.K_d: # Toggle debug edges view
                        if background_image: # Only if an image was loaded
                            # Re-process to get edges image (could be optimized)
                            # For now, let's just switch to a state that shows last Canny
                            temp_img_cv = cv2.imread(image_path_holder) # Need to store image_path
                            if temp_img_cv is not None:
                                gray = cv2.cvtColor(temp_img_cv, cv2.COLOR_BGR2GRAY)
                                blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                                edges_debug = cv2.Canny(blurred, CANNY_THRESHOLD1, CANNY_THRESHOLD2)
                                edges_debug_rgb = cv2.cvtColor(edges_debug, cv2.COLOR_GRAY2RGB)
                                debug_edges_image = pygame.image.frombuffer(edges_debug_rgb.tobytes(), (edges_debug.shape[1], edges_debug.shape[0]), "RGB")
                                debug_edges_image = pygame.transform.scale(debug_edges_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                                current_state = GameState.SHOW_EDGES_DEBUG

            elif current_state == GameState.SHOW_EDGES_DEBUG:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d: # Toggle back
                        current_state = GameState.GAMEPLAY
                        debug_edges_image = None


        # --- Update ---
        if current_state == GameState.GAMEPLAY and player:
            player.update(platforms_group)
            # No need to update static platforms


        # --- Draw ---
        screen.fill(BLACK) # Default background

        if current_state == GameState.IMAGE_SELECTION:
            # Instructions
            text_surface_prompt = font.render("Enter image path and press Enter:", True, WHITE)
            screen.blit(text_surface_prompt, (50, SCREEN_HEIGHT // 2 - 50))
            
            # Input box
            input_box_rect = pygame.Rect(50, SCREEN_HEIGHT // 2, SCREEN_WIDTH - 100, 40)
            pygame.draw.rect(screen, WHITE, input_box_rect, 2)
            text_surface_input = font.render(input_text, True, WHITE)
            screen.blit(text_surface_input, (input_box_rect.x + 5, input_box_rect.y + 5))
            # Blinking cursor (simple)
            if pygame.time.get_ticks() % 1000 < 500 and input_active:
                 cursor_x = input_box_rect.x + 5 + text_surface_input.get_width()
                 pygame.draw.line(screen, WHITE, (cursor_x, input_box_rect.y + 5), (cursor_x, input_box_rect.y + 35), 2)


        elif current_state == GameState.GAMEPLAY:
            if background_image:
                screen.blit(background_image, (0, 0))
            
            # Draw platforms first, then player
            for platform in platforms_group:
                platform.draw(screen) # Or screen.blit(platform.image, platform.rect)
            if player:
                player.draw(screen) # Or screen.blit(player.image, player.rect)
        
        elif current_state == GameState.SHOW_EDGES_DEBUG:
            if debug_edges_image:
                screen.blit(debug_edges_image, (0,0))
            else: # Fallback if something went wrong with debug image
                text_surface_error = font.render("Error showing debug edges. Press D to return.", True, WHITE)
                screen.blit(text_surface_error, (50, SCREEN_HEIGHT // 2 - 20))


        pygame.display.flip()

    pygame.quit()
    # cv2.destroyAllWindows() # Not strictly necessary if not using cv2.imshow()

if __name__ == '__main__':
    image_path_holder = "" # To store the path for debug view
    game()