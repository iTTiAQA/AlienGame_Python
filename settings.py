class Settings:
    """储存游戏中所有设置的类"""

    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.fleet_direction = 1
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (0, 0, 0)

        # 飞船设置
        self.ship_speed = 8
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed = 10
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (230, 230, 230)
        self.bullets_allowed = 10

        # 外星人设置
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10

        # 以什么速度加快游戏节奏
        self.speedup_scale = 1.8

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏而变化的设置"""
        self.ship_speed = 8
        self.bullet_speed = 10
        self.alien_speed = 1.0
        self.bullet_height = 15

        # fleet_direction 为1表示向右移动，为-1表示向左移动
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度值"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_height *= self.speedup_scale
