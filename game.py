
import pygame
from board import Board
from mouse import Mouse

class Game:

    def __init__(self):

        pygame.init()

        self.screen_width = 580
        self.screen_height = 580
        self.window = pygame.display.set_mode([self.screen_width, self.screen_height])
        pygame.display.set_caption("nots & crosses")

        self.clock = pygame.time.Clock()

        self.board = Board(self.window)
        self.gameOver = False

        self.show_menu = True

        self.is_playing_engine = False
        self.is_playing_human = False

        self.mouse = Mouse()

    def mainLoop(self):

        running = True
        while running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_x]: # setting x to be the reset key
                    self.board.reset()
                    self.gameOver = False
                    self.show_menu = True

            if self.show_menu:
                self.showMenu()
                self.board.reset()
            elif not self.gameOver:
                self.showGame()

            pygame.display.flip()

    def showMenu(self):

        button_width, button_height = 120, 30
        button_color = (0, 0, 0)
        button_distance = 60  # the y distance between 2 buttons

        # coords where the button will appear on the screen
        x_offset = (self.screen_width / 2) - (button_width / 2)
        y_offset = (self.screen_height / 2) - (button_height / 2)

        play_human_button = pygame.Rect(x_offset, y_offset, 
                                        button_width, button_height)
        play_engin_button = pygame.Rect(x_offset, y_offset + button_distance, 
                                        button_width, button_height)

        # checking if any of the 2 buttons have been clicked
        if self.mouse.leftButtonReleased():
            mouse_coords = self.mouse.getMouseCoords()

            if play_human_button.collidepoint(mouse_coords[0], mouse_coords[1]):
                self.is_playing_human = True
                self.is_playing_engine = False
                self.show_menu = False
            if play_engin_button.collidepoint(mouse_coords[0], mouse_coords[1]):
                self.is_playing_engine = True
                self.is_playing_human = False
                self.show_menu = False

        small_font = pygame.font.SysFont("comicsansms", 20)
        big_font = pygame.font.SysFont("comicsansms", 60)

        play_human_text = small_font.render("play human", True, (255, 255, 255))
        play_engine_text = small_font.render("play engine", True, (255, 255, 255))
        title_text = big_font.render("TicTakToe", True, (0, 0, 0))

        self.window.fill((170, 180, 200))
        pygame.draw.rect(self.window, button_color, play_human_button)
        pygame.draw.rect(self.window, button_color, play_engin_button)
        self.window.blit(title_text, (x_offset - 85, self.screen_height / 6))
        self.window.blit(play_human_text, (x_offset + 10, y_offset - 2))
        self.window.blit(play_engine_text, (x_offset + 10, y_offset + button_distance - 2))

    def showGame(self):

        if self.is_playing_engine:
            self.board.playEngine()
        else:
            self.board.playHuman()

        self.board.drawBackground()
        self.board.drawPosition()

        if self.board.checkWinner("X", self.board.board):
            self.showWinner("X is the Winner")
            self.gameOver = True
        elif self.board.checkWinner("O", self.board.board):
            self.showWinner("O is the Winner")
            self.gameOver = True
        elif self.board.checkDraw(self.board.board):
            self.showWinner("Game is a Draw ")
            self.gameOver = True

    def showWinner(self, message):

        font = pygame.font.SysFont("comicsansms", 25)
        win_text = font.render(message, True, (255, 255, 255))
        self.window.blit(win_text, (self.screen_width / 2 - 90, self.screen_height / 2 - 20))

    def __del__(self):

        pygame.quit()
