import pygame, random, os, math

pygame.init()

# classes
class Trickster(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        super().__init__()

        self.is_selected = False # True - red border
        self.is_blocked = False  # True red circle
        self.id = int(filename.split('.')[0]) # 1,2,3,...10

        self.original_image = pygame.image.load('img/tricksters/' + filename).convert_alpha()
        self.image = pygame.transform.smoothscale(self.original_image, (64, 64))
        pygame.draw.rect(self.image, WHITE, self.image.get_rect(), 1)
        self.rect = self.image.get_rect(topleft = (x, y))

    def draw(self):
        if self.is_blocked:
            pygame.draw.circle(self.image, RED, (32, 32), 20, 3)
            self.is_selected = False
        elif self.is_selected:
            pygame.draw.rect(self.image, RED, self.image.get_rect(), 1)
        else:
            self.image = pygame.transform.smoothscale(self.original_image, (64, 64))
            pygame.draw.rect(self.image, WHITE, self.image.get_rect(), 1)

    def update(self):
        self.draw()

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.is_filled = False
        self.width, self.height = (128, 128)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.image.fill((255, 255, 255, 120))
        self.rect = self.image.get_rect(topleft = (x, y))

    def set_image(self, image):
        self.is_filled = True
        self.image = image
        self.image = pygame.transform.smoothscale(self.image, (128, 128))
    def unset_image(self):
        self.is_filled = False
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.image.fill((255, 255, 255, 120))

class Game():
    def __init__(self):
        self.guests = self.get_guests()
        print(self.guests)
        self.tries_left = 10
        self.winner = False
        self.guess_msg = ''

        # image when we lose the game
        self.tombstone = pygame.image.load('img/tombstone.png').convert_alpha()
        self.tombstone_rect = self.tombstone.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        # image when we win the game
        self.ghost = pygame.image.load('img/ghost.png').convert_alpha()
        self.ghost_rect = self.ghost.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        # background image
        self.bg = pygame.image.load('img/halloween-bg.jpg').convert_alpha()
        self.bg = pygame.transform.smoothscale(self.bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_rect = self.bg.get_rect(topleft = (0, 0))

        # buttons
        self.instruction_btn = pygame.Surface((200, 44))
        self.instruction_btn.fill(CRIMSON)
        self.instruction_btn_rect = self.instruction_btn.get_rect(center = (WINDOW_WIDTH // 2, 120))

        self.guess_btn = pygame.Surface((160, 44))
        self.guess_btn.fill(ORANGE)
        self.guess_btn_rect = self.guess_btn.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 160))

        # instruction panel
        self.show_instructions = False
        self.instructions = pygame.Surface((600, 200))
        self.instructions.fill(BLACK)
        self.instructions_rect = self.instructions.get_rect(midtop = (WINDOW_WIDTH // 2, 94))

        # tricksters
        self.selected_trickster = None
        self.selected_tricksters = [0,0,0]
        self.tricksters = [f for f in os.listdir('img/tricksters') if os.path.join('img/tricksters', f)]
        self.tricksters_group = pygame.sprite.Group()
        PADDING = 10
        MARGIN = (WINDOW_WIDTH - (64 * 10 + PADDING * 9)) // 2
        for i in range(len(self.tricksters)):
            x = MARGIN + (i * 64) + (PADDING * i)
            y = WINDOW_HEIGHT - 100
            trickster = Trickster(self.tricksters[i], x, y)
            self.tricksters_group.add(trickster)

        # tiles
        self.tiles_group = pygame.sprite.Group()
        TILE_PADDING = 20
        TILE_MARGIN = (WINDOW_WIDTH - (128 * 3 + TILE_PADDING * 2)) // 2
        for i in range(3):
            x = TILE_MARGIN + (i * 128) + (TILE_PADDING * i)
            y = WINDOW_HEIGHT - 300
            tile = Tile(x, y)
            self.tiles_group.add(tile)

    def get_guests(self):
        options = list(range(1, 11))
        return random.sample(options, 3)

    def check_guess(self):
        guess1 = self.selected_tricksters[0]
        guess2 = self.selected_tricksters[1]
        guess3 = self.selected_tricksters[2]

        cues = []
        if guess1 != 0 and guess2 != 0 and guess3 != 0:
            # check for win
            if guess1 == self.guests[0] and guess2 == self.guests[1] and guess3 == self.guests[2]:
                self.winner = True
                return ''

            self.tries_left -= 1
            for i in range(3):
                if self.selected_tricksters[i] == self.guests[i]:
                    cues.append('Fermi')
                elif self.selected_tricksters[i] in self.guests:
                    cues.append('Pico')
            if len(cues) == 0:
                return 'Bagels'
            else:
                cues.sort()
                return ' '.join(cues)
        else:
            return 'Select 3 tricksters'

    def update(self, event_list):
        self.draw()
        self.user_input(event_list)

    def draw(self):

        # font
        title_font = pygame.font.Font('fonts/UnfinishedScreamRegular.ttf', 84)
        content_font = pygame.font.Font('fonts/UnfinishedScreamRegular.ttf', 60)
        text_font = pygame.font.SysFont('Arial', 20)

        # text
        title_text = title_font.render('Pico, Fermi, Bagels', True, CRIMSON)
        title_rect = title_text.get_rect(topleft = (130, 10))

        sub_text = content_font.render('Halloween Edition', True, ORANGE)
        sub_rect = sub_text.get_rect(topleft = (500, 20))

        inst_text = text_font.render('I n s t r u c t i o n s', True, WHITE)
        inst_rect = inst_text.get_rect(center = (WINDOW_WIDTH // 2, 120))

        guess_text = text_font.render('G U E S S', True, WHITE)
        guess_rect = guess_text.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 160))

        guess_msg = text_font.render(self.guess_msg, True, GREEN)
        guess_msg_rect = guess_msg.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))

        lines = [
            {
                'text':'The goal is to find which 3 trick-or-treaters are coming',
                'color': GREEN
            },
            {
                'text': 'Trick-or-treaters will be different, no two of the same',
                'color': GREEN
            },
            {
                'text': 'PICO - correct guess, wrong place',
                'color': CRIMSON
            },
            {
                'text': 'FERMI - correct guess, correct place',
                'color': CRIMSON
            },
            {
                'text': 'BAGELS - nothing is correct',
                'color': CRIMSON
            },
            {
                'text': 'You have 10 tries.',
                'color': GREEN
            },
        ]
        tries_left = content_font.render('Tries left', True, WHITE)
        tries_left_rect = tries_left.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))

        tries = title_font.render(str(self.tries_left), True, CRIMSON)
        tries_rect = tries.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 -40))

        # UI
        screen.fill(BLACK)

        if self.tries_left == 0:
            you_died = title_font.render('You died', True, CRIMSON)
            you_died_rect = you_died.get_rect(center = (WINDOW_WIDTH // 2, 40))
            try_again = title_font.render('Try again next Halloween', True, WHITE)
            try_again_rect = try_again.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
            play_again = text_font.render('Or press Space to play again', True, GREEN)
            play_again_rect = play_again.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))

            screen.blit(self.tombstone, self.tombstone_rect)
            screen.blit(you_died, you_died_rect)
            screen.blit(try_again, try_again_rect)
            screen.blit(play_again, play_again_rect)
        elif self.winner:
            you_died = title_font.render('You Won', True, CRIMSON)
            you_died_rect = you_died.get_rect(center = (WINDOW_WIDTH // 2, 40))
            try_again = title_font.render('Congratulation', True, BLACK)
            try_again_rect = try_again.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
            play_again = text_font.render('Press Space to play again', True, GREEN)
            play_again_rect = play_again.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))

            screen.blit(self.ghost, self.ghost_rect)
            screen.blit(you_died, you_died_rect)
            screen.blit(try_again, try_again_rect)
            screen.blit(play_again, play_again_rect)
        else:
            screen.blit(self.bg, self.bg_rect)
            screen.blit(title_text, title_rect)
            screen.blit(sub_text, sub_rect)

            screen.blit(tries_left, tries_left_rect)
            screen.blit(tries, tries_rect)

            screen.blit(self.instruction_btn, self.instruction_btn_rect)
            screen.blit(inst_text, inst_rect)

            screen.blit(self.guess_btn, self.guess_btn_rect)
            screen.blit(guess_text, guess_rect)

            if self.show_instructions:
                screen.blit(self.instructions, self.instructions_rect)
                for index, line in enumerate(lines):
                    line_text = text_font.render(line['text'], True, line['color'])
                    self.instructions.blit(line_text, (10, index * 30 + 10))

                pygame.draw.circle(self.instructions, RED, (580, 20), 10, 2)
                close = text_font.render('x', True, RED)
                close_rect = close.get_rect(center = (580, 18))
                self.instructions.blit(close, close_rect)



            self.tiles_group.draw(screen)
            self.tiles_group.update()

            self.tricksters_group.draw(screen)
            self.tricksters_group.update()

            screen.blit(guess_msg, guess_msg_rect)


    def user_input(self, event_list):
        tricksters = self.tricksters_group.sprites()

        for event in event_list:

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.tries_left = 10
                self.guests = self.get_guests()
                self.selected_trickster = None
                self.selected_tricksters = [0,0,0]
                self.winner = False
                self.guess_msg = ''

                for tile in self.tiles_group:
                    tile.unset_image()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.tries_left != 0:
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]

                # show instruction panel
                if self.instruction_btn_rect.collidepoint(mouse_x, mouse_y):
                    self.show_instructions = True

                # hide instruction panel
                if self.show_instructions:
                    mouse_x = mouse_x - self.instructions_rect.left
                    mouse_y = mouse_y - self.instructions_rect.top

                    sqx = (mouse_x - 580)**2
                    sqy = (mouse_y - 20) ** 2

                    if math.sqrt(sqx + sqy) < 10:
                        self.show_instructions = False

                # check guess button
                if self.guess_btn_rect.collidepoint(mouse_x, mouse_y):
                    self.guess_msg = self.check_guess()

                # select tiles
                for index, tile in enumerate(self.tiles_group):
                    if tile.rect.collidepoint(mouse_x, mouse_y):
                        if self.selected_trickster:
                            tile.set_image(self.selected_trickster.original_image)
                            self.selected_tricksters[index] = int(self.selected_trickster.id)
                            for trickster in tricksters:
                                if trickster.id == self.selected_trickster.id:
                                    trickster.is_blocked = True
                            self.selected_trickster = None
                        elif tile.is_filled:
                            for trickster in tricksters:
                                if trickster.id == self.selected_tricksters[index]:
                                    trickster.is_blocked = False
                            tile.unset_image()
                            self.selected_tricksters[index] = 0

                # select tricksters
                for trickster in tricksters:
                    if trickster.rect.collidepoint(mouse_x, mouse_y) and not trickster.is_blocked:
                        if trickster.is_selected:
                            trickster.is_selected = False
                            self.selected_trickster = None
                        else:
                            trickster.is_selected = True
                            self.selected_trickster = trickster

            # make sure all images are correctly stated
            for trickster in tricksters:
                if trickster.id in self.selected_tricksters:
                    trickster.is_blocked = True
                else:
                    trickster.is_blocked = False

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Pico, Fermi, Bagels')

FPS = 10
clock = pygame.time.Clock()

ORANGE = (255, 127, 0)
CRIMSON = (220, 20, 60)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

game = Game()

running = True
while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    game.update(event_list)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
