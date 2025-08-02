import pygame
import os
import json
from dotenv import load_dotenv
from PIL import Image # For loading image for Gemini
import google.generativeai as genai

load_dotenv()

# --- Configuration ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (255, 100, 100)
PLATFORM_COLOR = (50, 150, 50)  # For solid platforms (e.g., vertical walls)
PLATFORM_COLOR_PASSTHROUGH = (100, 200, 100) # Lighter green for pass-through
LOADING_TEXT_COLOR = (200, 200, 200)
ERROR_TEXT_COLOR = (255, 50, 50)

# Player settings
PLAYER_ACC = 0.7
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.7
PLAYER_JUMP_STRENGTH = -15

# Platform generation settings
PLATFORM_THICKNESS = 8

# --- Gemini API Setup ---
try:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=GOOGLE_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.0-flash') # Using a common, generally available model
    print("Gemini API configured successfully with gemini-2.0-flash.")
except Exception as e:
    print(f"Error configuring Gemini API with 'gemini-2.0-flash': {e}")
    print("Attempting fallback to 'gemini-pro-vision'...")
    try:
        gemini_model = genai.GenerativeModel('gemini-pro-vision')
        print("Gemini API configured successfully with 'gemini-pro-vision'.")
    except Exception as e2:
        print(f"Error configuring Gemini API with 'gemini-pro-vision' as fallback: {e2}")
        gemini_model = None

# --- Player Class (Copied from above with the emphasized fix) ---
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
        keys = pygame.key.get_pressed()

        self.acc = pygame.math.Vector2(0, PLAYER_GRAVITY)
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > SCREEN_WIDTH - self.rect.width:
            self.pos.x = SCREEN_WIDTH - self.rect.width
            self.vel.x = 0
        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x = 0

        if self.on_ground and keys[pygame.K_DOWN]:
            self.rect.y += 1
            peek_hits = pygame.sprite.spritecollide(self, platforms, False)
            self.rect.y -= 1
            for platform_below in peek_hits:
                if platform_below.is_passthrough and abs(self.rect.bottom - platform_below.rect.top) < 5: # 5px tolerance for drop
                    self.pos.y += 2 # Nudge player down
                    self.on_ground = False
                    break

        self.rect.x = int(self.pos.x)
        self.collide_with_platforms(platforms, 'x')

        self.on_ground = False # Reset before Y collision check
        self.rect.y = int(self.pos.y)
        self.collide_with_platforms(platforms, 'y')

        if self.rect.top > SCREEN_HEIGHT + 50: # Fallen off screen
            self.pos.y = 0
            self.pos.x = SCREEN_WIDTH / 2
            self.vel.y = 0
            self.on_ground = False

    def collide_with_platforms(self, platforms, direction):
        keys = pygame.key.get_pressed()

        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, platforms, False)
            for hit in hits:
                # --- CRITICAL CHECK FOR PASS-THROUGH PLATFORMS ---
                if hit.is_passthrough:
                    continue  # Skip X-collision for pass-through platforms
                # ----------------------------------------------------
                
                # This code below should ONLY run for SOLID (non-passthrough) platforms
                if self.vel.x > 0: # Moving right
                    self.rect.right = hit.rect.left
                elif self.vel.x < 0: # Moving left
                    self.rect.left = hit.rect.right
                self.pos.x = self.rect.x # Sync float pos with int rect after snap
                self.vel.x = 0
        
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, platforms, False)
            for hit in hits:
                if self.vel.y > 0:  # Player is moving DOWN
                    is_dropping_or_falling_through = keys[pygame.K_DOWN] and hit.is_passthrough
                    if is_dropping_or_falling_through:
                        # Condition to allow dropping: player's feet are within the vertical span of the platform
                        if self.rect.bottom > hit.rect.top and self.rect.bottom < (hit.rect.top + PLATFORM_THICKNESS + 2): # +2 for a slightly larger safety margin
                            continue # Pass through this platform when dropping
                    
                    # Standard landing collision
                    # Player's feet are at/below platform top, and player's head was above platform top
                    if self.rect.bottom >= hit.rect.top and self.rect.top < hit.rect.top:
                        self.rect.bottom = hit.rect.top
                        self.pos.y = self.rect.y # Sync float pos
                        self.vel.y = 0
                        self.on_ground = True
                
                elif self.vel.y < 0:  # Player is moving UP
                    if hit.is_passthrough:
                        continue # Player passes through passthrough platforms upwards
                    
                    # Else (it's a SOLID platform, not passthrough)
                    # Bonk head if player's top hits the bottom of the solid platform
                    if self.rect.top <= hit.rect.bottom and self.rect.bottom > hit.rect.bottom:
                        self.rect.top = hit.rect.bottom
                        self.pos.y = self.rect.y # Sync float pos
                        self.vel.y = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# --- Platform Class ---
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, is_passthrough=False):
        super().__init__()
        self.is_passthrough = is_passthrough
        self.image = pygame.Surface((w, h))
        if self.is_passthrough:
            self.image.fill(PLATFORM_COLOR_PASSTHROUGH)
        else:
            self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# --- Image Processing Function (Using Gemini) ---
def process_image_to_platforms_gemini(image_path, screen_for_loading):
    if not gemini_model:
        return [], None, "Gemini model not initialized. Check API key and setup."
    if not os.path.exists(image_path):
        return [], None, f"Error: Image path '{image_path}' not found."
    try:
        img_pil = Image.open(image_path)
        img_width_orig, img_height_orig = img_pil.size
    except Exception as e:
        return [], None, f"Error loading image with Pillow: {e}"

    prompt = f"""
    You are an expert image analyst helping design levels for a 2D platformer game.
    Analyze the provided image which is {img_width_orig} pixels wide and {img_height_orig} pixels high.
    Identify prominent, distinct, and reasonably long straight horizontal line segments that could act as platforms for a character to stand on.
    Also, identify prominent, distinct, and reasonably long straight vertical line segments that could act as walls.
    Avoid very small, cluttered, or overly complex areas. Focus on the main structural elements in the foreground.
    Return your findings as a JSON object with a single key "lines".
    The value of "lines" should be a list of JSON objects.
    Each line object must have:
    - "type": A string, either "horizontal" or "vertical".
    - "x1": The starting x-coordinate of the line.
    - "y1": The starting y-coordinate of the line.
    - "x2": The ending x-coordinate of the line.
    - "y2": The ending y-coordinate of the line.

    For a horizontal line, y1 and y2 should be the same (or very close, use y1 for platform top).
    For a vertical line, x1 and x2 should be the same (or very close, use x1 for wall left edge).

    Example:
    {{
      "lines": [
        {{"type": "horizontal", "x1": 50, "y1": 400, "x2": 250, "y2": 400}},
        {{"type": "vertical", "x1": 300, "y1": 100, "x2": 300, "y2": 300}}
      ]
    }}
    Ensure the coordinates are within the image boundaries (0 to {img_width_orig-1} for x, 0 to {img_height_orig-1} for y).
    The top-left of the image is (0,0). Only return the JSON object.
    Prioritize clear, well-defined lines on foreground objects suitable for gameplay.
    """
    platform_data = []
    error_message = None
    try:
        print("Sending image to Gemini for analysis...")
        if screen_for_loading:
            font = pygame.font.Font(None, 48)
            text_surface = font.render("Analyzing image with Gemini...", True, LOADING_TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen_for_loading.fill(BLACK)
            screen_for_loading.blit(text_surface, text_rect)
            pygame.display.flip()
        
        response = gemini_model.generate_content([prompt, img_pil], stream=False)
        response.resolve()
        print(f"Gemini Response Text (raw):\n{response.text}")
        
        cleaned_response_text = response.text.strip()
        if cleaned_response_text.startswith("```json"):
            cleaned_response_text = cleaned_response_text[7:]
        if cleaned_response_text.endswith("```"):
            cleaned_response_text = cleaned_response_text[:-3]
        cleaned_response_text = cleaned_response_text.strip()

        gemini_output = json.loads(cleaned_response_text)
        
        if "lines" not in gemini_output or not isinstance(gemini_output["lines"], list):
            raise ValueError("Gemini response does not contain a valid 'lines' list.")

        scale_x = SCREEN_WIDTH / img_width_orig
        scale_y = SCREEN_HEIGHT / img_height_orig

        for line in gemini_output["lines"]:
            line_type = line.get("type")
            try:
                x1, y1, x2, y2 = float(line.get("x1")), float(line.get("y1")), float(line.get("x2")), float(line.get("y2"))
            except (TypeError, ValueError):
                print(f"Warning: Invalid coordinate data from Gemini: {line}")
                continue

            is_platform_passthrough = False
            if line_type == "horizontal":
                plat_x = int(min(x1, x2) * scale_x)
                plat_y = int(y1 * scale_y) 
                plat_w = int(abs(x2 - x1) * scale_x)
                plat_h = PLATFORM_THICKNESS
                is_platform_passthrough = True
                if plat_w > 5: # Min width for a platform
                     platform_data.append({"x": plat_x, "y": plat_y, "w": plat_w, "h": plat_h, "passthrough": is_platform_passthrough})
            elif line_type == "vertical":
                plat_x = int(x1 * scale_x) 
                plat_y = int(min(y1, y2) * scale_y)
                plat_w = PLATFORM_THICKNESS
                plat_h = int(abs(y2 - y1) * scale_y)
                # is_platform_passthrough remains False (solid wall)
                if plat_h > 5: # Min height for a wall
                    platform_data.append({"x": plat_x, "y": plat_y, "w": plat_w, "h": plat_h, "passthrough": is_platform_passthrough})
        print(f"Generated {len(platform_data)} platforms from Gemini's analysis.")
    except genai.types.generation_types.BlockedPromptException as bpe:
        error_message = f"Gemini API Error: Prompt blocked. {bpe}"
    except json.JSONDecodeError as jde:
        error_message = f"Error decoding Gemini JSON: {jde}. Response: {response.text[:500]}"
    except Exception as e:
        error_message = f"Error processing with Gemini: {e}"
    
    background_pygame_image = None
    try:
        if img_pil.mode != 'RGB': img_pil = img_pil.convert('RGB')
        background_pygame_image = pygame.image.fromstring(img_pil.tobytes(), img_pil.size, img_pil.mode)
        background_pygame_image = pygame.transform.scale(background_pygame_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception as e:
        if not error_message: error_message = "Error creating background image."
        print(f"Error converting PIL to Pygame: {e}")
    return platform_data, background_pygame_image, error_message

# --- Game State Enum ---
class GameState:
    IMAGE_SELECTION = 1
    LOADING_LEVEL = 2
    GAMEPLAY = 3
    SHOW_ERROR = 4

# --- Main Game Function ---
def game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Photo Platformer (Gemini - PassThrough)")
    clock = pygame.time.Clock()

    current_state = GameState.IMAGE_SELECTION
    player, background_image, current_error_message = None, None, None
    all_sprites_group = pygame.sprite.Group()
    platforms_group = pygame.sprite.Group()
    font = pygame.font.Font(None, 36)
    input_text, image_path_holder = "", ""
    input_active = True
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if current_state == GameState.IMAGE_SELECTION:
                if event.type == pygame.KEYDOWN and input_active:
                    if event.key == pygame.K_RETURN:
                        image_path_holder = input_text.strip()
                        if image_path_holder:
                            current_state = GameState.LOADING_LEVEL
                            input_active = False
                    elif event.key == pygame.K_BACKSPACE: input_text = input_text[:-1]
                    else: input_text += event.unicode if len(input_text) < 150 else ""
            elif current_state == GameState.GAMEPLAY:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player: player.jump()
                    if event.key == pygame.K_r:
                        current_state, input_text, input_active = GameState.IMAGE_SELECTION, "", True
                        player, background_image = None, None
                        all_sprites_group.empty(); platforms_group.empty()
            elif current_state == GameState.SHOW_ERROR:
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    current_state, input_text, input_active, current_error_message = GameState.IMAGE_SELECTION, "", True, None

        if current_state == GameState.LOADING_LEVEL:
            platform_coords_list, bg_img, error_msg = process_image_to_platforms_gemini(image_path_holder, screen)
            if error_msg: current_error_message, current_state = error_msg, GameState.SHOW_ERROR
            elif bg_img:
                all_sprites_group.empty(); platforms_group.empty()
                for p_data in platform_coords_list:
                    platform = Platform(p_data["x"], p_data["y"], p_data["w"], p_data["h"], p_data["passthrough"])
                    platforms_group.add(platform)
                player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
                all_sprites_group.add(player)
                background_image, current_state = bg_img, GameState.GAMEPLAY
            else: current_error_message, current_state = "Level gen failed: No background.", GameState.SHOW_ERROR
            image_path_holder = ""

        if current_state == GameState.GAMEPLAY and player: player.update(platforms_group)

        screen.fill(BLACK)
        if current_state == GameState.IMAGE_SELECTION:
            prompt_surf = font.render("Enter image path and press Enter:", True, WHITE)
            screen.blit(prompt_surf, (50, SCREEN_HEIGHT // 2 - 50))
            input_box_rect = pygame.Rect(50, SCREEN_HEIGHT // 2, SCREEN_WIDTH - 100, 40)
            pygame.draw.rect(screen, WHITE, input_box_rect, 2)
            input_surf = font.render(input_text, True, WHITE)
            screen.blit(input_surf, (input_box_rect.x + 5, input_box_rect.y + 5))
            if pygame.time.get_ticks() % 1000 < 500 and input_active:
                 cursor_x = input_box_rect.x + 5 + input_surf.get_width()
                 pygame.draw.line(screen, WHITE, (cursor_x, input_box_rect.y + 5), (cursor_x, input_box_rect.y + 35), 2)
        elif current_state == GameState.LOADING_LEVEL: pass # Handled in process_image
        elif current_state == GameState.GAMEPLAY:
            if background_image: screen.blit(background_image, (0, 0))
            platforms_group.draw(screen)
            all_sprites_group.draw(screen)
        elif current_state == GameState.SHOW_ERROR and current_error_message:
            font_error_small = pygame.font.Font(None, 28)
            words = current_error_message.split(' '); lines = []
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if font_error_small.size(test_line)[0] < SCREEN_WIDTH - 100: current_line = test_line
                else: lines.append(current_line); current_line = word + " "
            lines.append(current_line)
            y_offset = SCREEN_HEIGHT // 2 - (len(lines) * 15) # Adjusted spacing
            for i, line_text in enumerate(lines):
                err_surf = font_error_small.render(line_text.strip(), True, ERROR_TEXT_COLOR)
                screen.blit(err_surf, err_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 30)))
            instr_surf = pygame.font.Font(None, 24).render("Click or press any key to continue", True, WHITE)
            screen.blit(instr_surf, instr_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset + len(lines) * 30 + 20)))
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    game()