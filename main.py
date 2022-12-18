import sys

import pygame

import balloon_shooter
import dodge_the_ball
import stacks

WIDTH = 500
HEIGHT = 600


class Button:
    def __init__(self, text, width, height, pos, elevation):
        # Core attributes
        self.pressed = False
        # Location, Resting State (not pressed)
        self.elevation = elevation
        # Location, Pressed State
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        # text
        self.text = text
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def change_text(self, new_text):
        self.text_surf = gui_font.render(new_text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        # Ibababa yung height nung shadow
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.bottom_color,
                         self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color,
                         self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        return self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
                self.change_text(f"{self.text}")
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.pressed = False
                    self.change_text(self.text)
                    return True
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'
        return False


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
gui_font = pygame.font.Font(None, 30)
text_font = pygame.font.Font(None, 60)

# Name, Width, Height, Position (X n Y), Elevation (Shadow)
game1_btn = Button('Game 1', 200, 40, (150, 260), 5)
game2_btn = Button('Game 2', 200, 40, (150, 320), 5)
game3_btn = Button('Game 3', 200, 40, (150, 380), 5)
controls_btn = Button('Controls', 200, 40, (150, 440), 5)

first_text = text_font.render(
    'Point and Click', True, '#475F77')
second_text = text_font.render(
    'Games Collection', True, '#475F77')
textrect_first = first_text.get_rect(center=(WIDTH / 2, HEIGHT / 6))
textrect_second = second_text.get_rect(center=(WIDTH / 2, HEIGHT / 4))


def show_controls():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        screen.fill('#DCDDD8')

        controls_font = pygame.font.Font(None, 40)
        about_font = pygame.font.Font(None, 25)
        r_text = controls_font.render(
            "Press 'r' to restart game", True, '#475F77')
        q_text = controls_font.render(
            "Press 'q' to quit game", True, '#475F77')
        esc_text = controls_font.render(
            "Press 'esc' to go back to main menu", True, '#475F77')
        about1_text = text_font.render(
            "Made by:", True, '#475F77')
        about2_text = about_font.render(
            "Mel Mathew Palaña, Jeffrey Mamac and Matthew Prieto", True, '#475F77')

        r_text_rect = r_text.get_rect(center=(WIDTH / 2, HEIGHT / 6))
        q_text_rect = q_text.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        esc_text_rect = esc_text.get_rect(center=(WIDTH / 2, HEIGHT / 2.5))
        about1_text_rect = about1_text.get_rect(center=(WIDTH / 2, HEIGHT - 150))
        about2_text_rect = about2_text.get_rect(center=(WIDTH / 2, HEIGHT - 100))

        screen.blit(r_text, r_text_rect)
        screen.blit(q_text, q_text_rect)
        screen.blit(esc_text, esc_text_rect)
        screen.blit(about1_text, about1_text_rect)
        screen.blit(about2_text, about2_text_rect)

        pygame.display.update()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('#DCDDD8')
        screen.blit(first_text, textrect_first)
        screen.blit(second_text, textrect_second)

        pygame.display.set_caption('PCG Collection')

        if game1_btn.draw():
            pygame.display.set_caption("Balloon Shooter")
            balloon_shooter.game_loop()
        if game2_btn.draw():
            pygame.display.set_caption("Dodge the Ball")
            dodge_the_ball.game_loop()
        if game3_btn.draw():
            pygame.display.set_caption("Stacks")
            stacks.game_loop()
        if controls_btn.draw():
            pygame.display.set_caption("Controls")
            show_controls()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
