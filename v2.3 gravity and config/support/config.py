
from dataclasses import dataclass, field
from .cdataclasses import *
import pygame
import time

#Create configs
@dataclass
class WindowConfig:
    window_name:str="idiot's attempt at physics"
    padding:int=10
    
    render_chunks_bool:bool=False
    show_ball_id:bool=False

    # COLOR INFO
    wall_color:tuple=(108, 147, 199)
    game_area_bg_color:tuple=(247, 241, 245)
    win_bg_color:tuple=(157, 165, 188)
    ball_color:tuple=(0,0,200)
    plan_color:tuple=(200,0,0)
    chunk_color:tuple=(241, 64, 165)
    ball_id_color:tuple=(0,255,0)

    # TEXT INFO
    txtpad:int=5
    
    font_color:tuple=(200,200,200)

    # sizings
    gdim:Vector2=field(default_factory=lambda : Vector2(500,500))
    cdim:Vector2=field(default_factory=lambda : Vector2(200,400))

    # set by game obj
    w=None
    h=None
    wdim:Vector2=None
    font:pygame.font.Font=None

    controls_guide_path=r"v2.3 gravity and config/support/static/instructions.txt"

    ball_trail_list_len=20
    trail_color=(109, 191, 184)


@dataclass
class GameConfig:
    max_ball_size:int=50
    g_coef:int=0

    do_ball_ball_collisions:bool=True
    do_wall_ball_collisions:bool=True
    do_equal_mass_collisions:bool=False
    do_gravity:bool=True


@dataclass
class Config():

    windowConfig=WindowConfig()
    gameConfig=GameConfig()
    
