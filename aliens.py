import pygame
from pygame.sprite import Sprite
from settings import Settings


class Alien(Sprite):
    """管理alien的类"""

    def __init__(self, ai_game):
        """初始化外星人并显示其位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = Settings()

        # 加载外星人图像并设置其rect值
        self.image = pygame.image.load('image\_alien.png')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕的左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 储存外星人的精确水平位置
        self.x = float(self.rect.x)

    def update(self):
        """向右移动外星人"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def _create_fleet(self):
        """创建一个外星人军队"""
        # 创建一个外星人。不断添加,直到没有外星人为止
        # 外星人的间距为外星人的宽度。
        alien = Alien(self)
        alien_width = alien.rect.width

        current_x = 0.5 * alien.width
        while current_x < (self.settings.screen_width - alien_width):
            new_alien = Alien(self)
            new_alien.x = current_x
            new_alien.rect.x = current_x
            self.alien.add(new_alien)
            current_x += 2 * alien_width

    def check_edges(self):
        """如果外星人位于屏幕边缘,就返回True"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
