import pygame
import random

# 상수 정의
WIDTH, HEIGHT = 360, 640
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
FPS = 60

# 블록 관리
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        # 벽돌 크기
        self.w, self.h = 40, 20
        self.image = pygame.Surface([self.w, self.h])
        self.image.fill(color)
        # 벽돌 위치
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit_count = 1
    def take_hit(self):
        self.hit_count -= 1
        if self.hit_count <= 0:
            self.kill()
            return True
        return False

# 메인 게임 관리
class BreakOutGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Break Out")
        self.clock = pygame.time.Clock() # 시간제어

        # 폰트
        self.TITLE_FONT = pygame.font.SysFont("showcardgothic", 45, False, False)
        self.ANY_FONT = pygame.font.SysFont(None, 30, False, False)
        self.START_FONT = pygame.font.SysFont(None, 100)

        # 버튼 초기화
        self.START_BUTTON = pygame.Rect(WIDTH//2-80, HEIGHT//2, 160, 50)
        self.RECODE_BUTTON = pygame.Rect(WIDTH//2-80, HEIGHT//2+80, 160, 50)
        self.EXIT_BUTTON = pygame.Rect(WIDTH//2-80, HEIGHT//2+160, 160, 50)
        self.BACK_BUTTON = self.EXIT_BUTTON

        # 게임 상태 변수
        self.screen_state = "start"
        self.running = True
        self.game_start = False
        self.countdown_time = 3
        self.countdown_start_ticks = 0

        # 게임 객체, 그룹 생성
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()

        self.creat_blocks()

    def creat_blocks(self):
        colors = [RED, (255, 255, 0), (255, 165, 0), (0, 128, 0)]
        for row_index in range(4):
            for col_index in range(5):
                x = 30+col_index*(40+20)
                y = 50+row_index*(20+10)
                color = colors[row_index]

                block = Block(x, y, color)
                self.blocks.add(block)
                self.all_sprites.add(block)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.screen_state == "start":
                    if self.START_BUTTON.collidepoint(event.pos):
                        self.screen_state = "game"
                        self.countdown_start_ticks = pygame.time.get_ticks()
                    elif self.RECODE_BUTTON.collidepoint(event.pos):
                        self.screen_state = "recode"
                    elif self.EXIT_BUTTON.collidepoint(event.pos):
                        self.running = False
                elif self.screen_state == "recode":
                    if self.BACK_BUTTON.collidepoint(event.pos):
                        self.screen_state = "start"

    def game_logic(self):
        pass

    def check_collisions(self):
        pass

    # 시작 화면
    def start_screen(self):
        self.screen.fill(WHITE)
        # 제목
        title_text = self.TITLE_FONT.render("<Break OUT>", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//2-180))
        self.screen.blit(title_text, title_rect)
        # 시작 버튼
        pygame.draw.ellipse(self.screen, RED, self.START_BUTTON)
        start_button_text = self.ANY_FONT.render("Start", True, WHITE)
        self.screen.blit(start_button_text, start_button_text.get_rect(center=(self.START_BUTTON.center)))
        # 기록 버튼
        pygame.draw.ellipse(self.screen, GRAY, self.RECODE_BUTTON)
        recode_button_text = self.ANY_FONT.render("Recode", True, WHITE)
        self.screen.blit(recode_button_text, recode_button_text.get_rect(center=(self.RECODE_BUTTON.center)))
        # 나가기 버튼
        pygame.draw.ellipse(self.screen, BLACK, self.EXIT_BUTTON)
        exit_button_text = self.ANY_FONT.render("Exit", True, WHITE)
        self.screen.blit(exit_button_text, exit_button_text.get_rect(center=(self.EXIT_BUTTON.center)))

    # 게임 화면
    def game_screen(self):
        self.screen.fill(WHITE)

        # 카운트다운 로직
        if not self.game_start:
            elapsed_time = (pygame.time.get_ticks() - self.countdown_start_ticks) /100
            if elapsed_time < self.countdown_time:
                countdowns_sec = self.countdown_time- int(elapsed_time)
                countdown_text = self.START_FONT.render(str(countdowns_sec), True, GRAY)
                text_rect = countdown_text.get_rect(center=(WIDTH//2, HEIGHT//2))
                self.screen.blit(countdown_text, text_rect)
            else:
                self.game_start = True

        # 게임 로직 업데이트, 그리기
        if self.game_start:
            self.game_logic()
            self.check_collisions()

        self.all_sprites.draw(self.screen)

    def recode_screen(self):
        self.screen.fill(WHITE)
        recode_text = self.TITLE_FONT.render("Recode", True, BLACK)
        recode_rect = recode_text.get_rect(center=(WIDTH//2, 80))
        self.screen.blit(recode_text, recode_rect)

        # Back Button
        pygame.draw.ellipse(self.screen, BLACK, self.BACK_BUTTON)
        back_button_text = self.ANY_FONT.render("Back", True, WHITE)
        self.screen.blit(back_button_text, back_button_text.get_rect(center=(self.BACK_BUTTON.center)))

    # 메인 루프
    def run(self):
        while self.running:
            self.handle_input()

            if self.screen_state == "start":
                self.start_screen()
            elif self.screen_state == "game":
                self.game_screen()
            elif self.screen_state == "recode":
                self.recode_screen()

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = BreakOutGame()
    game.run()
    pygame.quit()
    # sys.exit()
