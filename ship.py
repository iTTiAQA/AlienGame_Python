import pygame

from settings import Settings


class Ship:
    """管理飞船的类"""

    def __init__(self, ai_game):
        """初始化飞船并设置其位置"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = Settings()

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('image\ship.png')
        self.rect = self.image.get_rect()

        # 每艘飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 在飞船的属性x,y中存储一个浮点数
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 移动标志（一开始不动）
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """根据移动标志移动飞船"""
        # 更新飞船属性x的值，而非其外接矩形的属性x的值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.y > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # 根据self.x和self.y跟新rect对象
        self.rect.x = self.x
        self.rect.y = self.y

    def center_ship(self):
        """将飞船放在屏幕底部中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

        # Pygame 中，(0,0)位于屏幕的左上角，当一个点向右下方移动时，坐标增大
        # 右下角坐标为setting中的最大值，坐标对应游戏窗口而非物理屏幕

