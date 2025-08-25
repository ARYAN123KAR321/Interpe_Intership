import pygame
import time
import math
from datetime import datetime

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Elegant Digital & Analog Clock")

# Colors
DARK_BG = (10, 10, 30)
LIGHT_BG = (220, 230, 255)
DARK_TEXT = (200, 220, 255)
LIGHT_TEXT = (20, 30, 60)
ACCENT = (65, 105, 225)  # Royal blue
ACCENT_HOVER = (30, 70, 200)
TOGGLE_BG = (40, 40, 60)
HOUR_HAND_COLOR = (220, 220, 250)
MINUTE_HAND_COLOR = (180, 180, 240)
SECOND_HAND_COLOR = (255, 80, 80)

# Clock settings
is_24h = False
font_large = pygame.font.Font(None, 120)
font_small = pygame.font.Font(None, 36)

# For smooth transitions
current_bg = list(DARK_BG)
current_text = list(DARK_TEXT)
target_bg = list(DARK_BG)
target_text = list(DARK_TEXT)

# Button dimensions
button_width, button_height = 180, 50
button_x = WIDTH // 2 - button_width // 2
button_y = HEIGHT - 100

# Analog clock settings
analog_center_x = WIDTH // 2
analog_center_y = 170
analog_radius = 120

def draw_clock():
    global current_bg, current_text, target_bg, target_text
    
    # Smooth color transitions
    for i in range(3):
        current_bg[i] += (target_bg[i] - current_bg[i]) * 0.05
        current_text[i] += (target_text[i] - current_text[i]) * 0.05
    
    screen.fill(tuple(current_bg))
    
    # Get current time
    now = datetime.now()
    hours = now.hour
    minutes = now.minute
    seconds = now.second
    milliseconds = now.microsecond // 1000
    
    # Determine if it's day or night for theme
    if 6 <= hours < 18:  # Daytime
        target_bg = list(LIGHT_BG)
        target_text = list(LIGHT_TEXT)
    else:  # Nighttime
        target_bg = list(DARK_BG)
        target_text = list(DARK_TEXT)
    
    # Draw analog clock
    draw_analog_clock(hours, minutes, seconds, milliseconds)
    
    # Format time based on 12/24 hour setting
    if is_24h:
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        period = "AM" if hours < 12 else "PM"
        hours_12 = hours % 12
        if hours_12 == 0:
            hours_12 = 12
        time_str = f"{hours_12:02d}:{minutes:02d}:{seconds:02d} {period}"
    
    # Draw digital time
    time_surface = font_large.render(time_str, True, tuple(current_text))
    time_rect = time_surface.get_rect(center=(WIDTH//2, 350))
    screen.blit(time_surface, time_rect)
    
    # Draw date
    date_str = now.strftime("%A, %B %d, %Y")
    date_surface = font_small.render(date_str, True, tuple(current_text))
    date_rect = date_surface.get_rect(center=(WIDTH//2, 410))
    screen.blit(date_surface, date_rect)
    
    # Draw toggle button
    mouse_pos = pygame.mouse.get_pos()
    button_hover = button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height
    
    button_color = ACCENT_HOVER if button_hover else ACCENT
    pygame.draw.rect(screen, TOGGLE_BG, (button_x - 5, button_y - 5, button_width + 10, button_height + 10), border_radius=15)
    pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height), border_radius=12)
    
    button_text = "Switch to 24H" if not is_24h else "Switch to 12H"
    text_surface = font_small.render(button_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(button_x + button_width//2, button_y + button_height//2))
    screen.blit(text_surface, text_rect)
    
    pygame.display.flip()

def draw_analog_clock(hours, minutes, seconds, milliseconds):
    # Draw clock face
    pygame.draw.circle(screen, tuple([c // 2 for c in current_text]), (analog_center_x, analog_center_y), analog_radius, 2)
    pygame.draw.circle(screen, tuple(current_bg), (analog_center_x, analog_center_y), analog_radius - 5)
    
    # Draw hour markers
    for i in range(12):
        angle = 2 * math.pi * i / 12 - math.pi / 2
        marker_x = analog_center_x + (analog_radius - 15) * math.cos(angle)
        marker_y = analog_center_y + (analog_radius - 15) * math.sin(angle)
        pygame.draw.circle(screen, tuple(current_text), (marker_x, marker_y), 4)
    
    # Draw minute markers
    for i in range(60):
        if i % 5 != 0:  # Skip positions where hour markers are
            angle = 2 * math.pi * i / 60 - math.pi / 2
            marker_x = analog_center_x + (analog_radius - 8) * math.cos(angle)
            marker_y = analog_center_y + (analog_radius - 8) * math.sin(angle)
            pygame.draw.circle(screen, tuple([c // 2 for c in current_text]), (marker_x, marker_y), 1)
    
    # Calculate hand angles with smooth movement for seconds
    second_angle = 2 * math.pi * (seconds + milliseconds/1000) / 60 - math.pi / 2
    minute_angle = 2 * math.pi * (minutes + seconds/60) / 60 - math.pi / 2
    hour_angle = 2 * math.pi * (hours % 12 + minutes/60) / 12 - math.pi / 2
    
    # Draw hour hand
    hour_length = analog_radius * 0.5
    hour_x = analog_center_x + hour_length * math.cos(hour_angle)
    hour_y = analog_center_y + hour_length * math.sin(hour_angle)
    pygame.draw.line(screen, HOUR_HAND_COLOR, (analog_center_x, analog_center_y), (hour_x, hour_y), 6)
    
    # Draw minute hand
    minute_length = analog_radius * 0.7
    minute_x = analog_center_x + minute_length * math.cos(minute_angle)
    minute_y = analog_center_y + minute_length * math.sin(minute_angle)
    pygame.draw.line(screen, MINUTE_HAND_COLOR, (analog_center_x, analog_center_y), (minute_x, minute_y), 4)
    
    # Draw second hand
    second_length = analog_radius * 0.8
    second_x = analog_center_x + second_length * math.cos(second_angle)
    second_y = analog_center_y + second_length * math.sin(second_angle)
    pygame.draw.line(screen, SECOND_HAND_COLOR, (analog_center_x, analog_center_y), (second_x, second_y), 2)
    
    # Draw center cap
    pygame.draw.circle(screen, SECOND_HAND_COLOR, (analog_center_x, analog_center_y), 6)
    pygame.draw.circle(screen, tuple(current_text), (analog_center_x, analog_center_y), 3)

def main():
    global is_24h
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if toggle button is clicked
                if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                    is_24h = not is_24h
        
        draw_clock()
        clock.tick(30)  # 30 FPS for smooth transitions
    
    pygame.quit()

if __name__ == "__main__":
    main()
