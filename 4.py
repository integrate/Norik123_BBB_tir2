import time,wrap, random, math
from time import sleep
from wrap import sprite, actions, world, sprite_text
from random import randint, choice

world.create_world(600, 600, 680, 30)


mario = sprite.add("mario-1-big", 100, 560,"stand")
costume=3

pacman=sprite.add("pacman",100,70,"player2")
sizew=450
sizeh=450
sprite.set_size_percent(pacman,sizew,sizeh)

spisok_enemy=[]
spisok_bullet=[]
speed=5

@wrap.always(50)
def move_pacman():
    sprite.move_at_angle_dir(pacman,speed)

    if sprite.get_right(pacman)>=600:
        sprite.set_reverse_x(pacman,True)
    elif sprite.get_left(pacman)<=0:
        sprite.set_reverse_x(pacman,False)

    collide_pacman()


@wrap.on_mouse_move
def move_mario(pos_x):
    sprite.move_to(mario,pos_x,560)

@wrap.on_mouse_down(wrap.BUTTON_LEFT)
def fire():
    if sprite.is_visible(mario):
        x=sprite.get_x(mario)
        y=sprite.get_top(mario)
        enemy= sprite.add("pacman", x, y,"enemy_blue_up2")
        spisok_enemy.append(enemy)
    collide_enemy_bullet()


@wrap.always(50)
def enemy_move():
    for enemy in spisok_enemy:
        sprite.move_at_angle(enemy,0,10)

        if sprite.get_top(enemy)<=0:
            sprite.remove(enemy)
            spisok_enemy.remove(enemy)

    collide_pacman()
    collide_enemy_bullet()



def collide_pacman():
    global speed,sizew,sizeh
    if sprite.is_collide_any_sprite(pacman,spisok_enemy) and sprite.is_visible(mario):
        a=sprite.is_collide_any_sprite(pacman, spisok_enemy)
        spisok_enemy.remove(a)
        sprite.remove(a)
        speed+=5
        sizew-=50
        sizeh-=50
        sprite.set_size_percent(pacman,sizew,sizeh)

        if sprite.get_width(pacman)==0:
            sprite.hide(pacman)
            sprite.add_text("Победа",300,300,font_size=80,text_color=[247,255,43])

@wrap.always(1000)
def bullet_show():
    if sprite.is_visible(pacman):
        x = sprite.get_x(pacman)
        y = sprite.get_bottom(pacman)
        bullet = sprite.add("battle_city_items", x, y,"bullet")
        sprite.set_size_percent_of(bullet,800)
        sprite.set_angle(bullet,180)
        spisok_bullet.append(bullet)

@wrap.always(50)
def bullet_move():
    for bullet in spisok_bullet:
        sprite.move_at_angle_dir(bullet,10)

        if sprite.get_top(bullet)>=600:
            sprite.remove(bullet)
            spisok_bullet.remove(bullet)

    collide_mario()


def collide_mario():
    global costume
    if sprite.is_collide_any_sprite(mario,spisok_bullet) and sprite.is_visible(pacman):
        a=sprite.is_collide_any_sprite(mario, spisok_bullet)
        spisok_bullet.remove(a)
        sprite.remove(a)
        costume-=1

        if costume>0:
            sprite.set_costume_next(mario)
        elif costume==0:
            sprite.hide(mario)
            sprite.add_text("Ты проиграл", 300, 300, font_size=80, text_color=[247, 255, 43])

def collide_enemy_bullet():
    for enemy in spisok_enemy:
        if sprite.is_collide_any_sprite(enemy,spisok_bullet):
            a = sprite.is_collide_any_sprite(enemy, spisok_bullet)
            sprite.remove(a)
            spisok_bullet.remove(a)
            sprite.remove(enemy)
            spisok_enemy.remove(enemy)
