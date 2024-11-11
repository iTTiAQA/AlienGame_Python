import sys
import pygame

from time import sleep

from settings import Settings
from ship import Ship
from game_stats import GameStats
from bullet import Bullet
from aliens import Alien
from button import Button


class AlienInvasion:
    """管理游戏资源与行为的类"""

    def __init__(self):
        """初始化游戏资源"""
        pygame.init()
        # 导入设置
        self.settings = Settings()

        # 设置时钟，以设置帧率
        self.clock = pygame.time.Clock()

        # 设置窗口长宽
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        """在全屏模式下运行游戏:
        self.screem = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        全屏模式下确认有推出的快捷键"""
        # 设置窗口标题
        pygame.display.set_caption("Alien Invasion")

        # 绘制飞船
        self.ship = Ship(self)

        # 导入子弹
        self.bullets = pygame.sprite.Group()

        # 设置舰队
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        """"# 设置背景色"""
        """self.bg_color = (230, 230, 230)"""

        # 创建一个用于储存信息的实例
        self.stats = GameStats(self)

        # 控制游戏开始与结束
        self.game_active = False
        # 创建play按钮
        self.play_button = Button(self, "Play")

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        # 将ship_left减一,并将飞船放在屏幕底部的中央
        self.ship.center_ship()

        # 清空外星人列表和子弹列表
        self.aliens.empty()
        self.bullets.empty()

        # 创建一个外形舰队
        self._create_fleet()

        # 飞船减一
        self.stats.ships_left += -1

        if self.stats.ships_left <= 0:
            # 让游戏处于非激活状态
            self.game_active = False

        # 暂停
        # sleep(0.5)

    def _create_fleet(self):
        """创建一个外星军队"""
        # 创建一个外星人，再不断的添加，直到没有空间为止
        # 外星人的距离为外星人的宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 8 * alien_height):
            while current_x < (self.settings.screen_width - 3 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # 添加一个外星人后，重置x并递增y值
            current_x = alien_width
            current_y += 1.5 * alien_height

    def _create_alien(self, x_position, y_position):
        """创建一个外星人并将其放到当前的行中"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.y = y_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _change_fleet_direction(self):
        """将整个舰队向下移动,并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
            alien.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        """在有外星人达到边缘时采取相应措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _update_aliens(self):
        """更新外形舰队中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.stats.ships_left -= 1
        while pygame.sprite.spritecollide(self.ship, self.aliens, True):
            self._ship_hit()
            # 将ship_left减一,并将飞船放在屏幕底部的中央

            print("Ship hit!!!")

    def _check_events(self):
        # 侦听键盘和鼠标事件
        for event in pygame.event.get():
            # 摁下右上角’x‘退出游戏
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                # 移动飞船
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                if event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                if event.key == pygame.K_UP:
                    self.ship.moving_up = True
                if event.key == pygame.K_DOWN:
                    self.ship.moving_down = True
                if event.key == pygame.K_SPACE:
                    self._fire_bullet()
                # 添加退出游戏的快捷键
                if event.key == pygame.K_q:
                    sys.exit()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                if event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
                if event.key == pygame.K_UP:
                    self.ship.moving_up = False
                if event.key == pygame.K_DOWN:
                    self.ship.moving_down = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单击时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # 重置游戏信息
            self.stats.reset_stats()
            self.game_active = True

            # 清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()

            # 创建一个新的外星舰队，并将飞船放在屏幕底部中央
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏光标
            pygame.mouse.set_visible(False)

        else: pygame.mouse.set_visible(True)

    def _fire_bullet(self):
        """创建一颗子弹,并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_bullet_alien_collision(self):
        """响应子弹和外星人碰撞"""
        # 删除发生碰撞的子弹和外星人
        pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if not self.aliens:
            # 删除现有的子弹并创建一个新的外星舰队
            """self.bullets.empty()"""
            self._create_fleet()
            self.settings.increase_speed()

    def _update_bullets(self):
        """更新子弹位置并删除已经消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()

        # 删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _update_screen(self):
        # 每次循环结束时都重新绘制屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.aliens.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullets()

        # 让最近绘制的屏幕可见
        pygame.display.flip()

        # 如果游戏处于非活动状态,就创建Play按钮
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def run_game(self):
        """开始游戏的主循环"""
        count = 1
        while True:
            # 游戏管理
            self._check_events()
            # 更新飞船位置
            self.ship.update()
            # 将屏幕刷新分离
            self._update_screen()
            if self.game_active:
                # 更新子弹位置
                self._update_bullets()
                # 更新外星人
                self._update_aliens()
                # 刷新子弹
                if count % 10 == 0:
                    self._fire_bullet()
                count += 1
                """self._fire_bullet()"""
            # 设置刷新速度
            self.clock.tick(60)


if __name__ == '__main__':
    # 创建实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()