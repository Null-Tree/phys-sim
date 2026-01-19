
from .modeling import *
import pygame
import time


    

class Game:
    def __init__(self,dim:tuple,max_ball_size:int=50):
        """
        Docstring for __init__
        Creates the game object
        
        :param dim: dimensions of Game window (x,y) tuple
        :type dim: tuple
        :param max_ball_size: max ball size of balls, aids in chunking
        :type dim: int
        """

        # initalises pygame
        pygame.init()

        # initalises cosmetic information
        self.window_name="idiot's attempt at physics"
        self.pad=10
        self.wall_color=(108, 147, 199)
        self.g_bg=(247, 241, 245)
        self.w_bg=(157, 165, 188)
        self.ball_color=(0,0,200)
        self.plan_color=(200,0,0)
        self.txtpad=5
        self.font=pygame.font.Font(None,20)
        self.font_color=(200,200,200)


        # set maxball size
        self.max_ball_size=max_ball_size

        # creates world object
        self.world=World(dim,max_ball_size)

        # VECTOR DATA
        # game area
        self.gsize=Vector2.to_V2(dim)

        # control area
        self.csize=Vector2(200,400)

        # WINDOW CREATION
        # window
        self.w=self.gsize.x + (3*self.pad) + self.csize.x
        self.h=max(self.gsize.y,self.csize.y)+2*self.pad
        self.wsize=Vector2(self.w,self.h)

        
        # note setmode makes the window
        self.window=pygame.display.set_mode((self.w,self.h))

        pygame.draw.rect(self.window, self.w_bg, pygame.Rect(0,0,self.wsize.x,self.wsize.y))
        

        # print((self.w,self.h))

        x0,y0=self.world_to_screen_v(Vector2(0,0)).as_tup()
        pygame.draw.rect(self.window, self.g_bg, pygame.Rect(x0,y0,self.gsize.x,self.gsize.y))

        pygame.display.set_caption(self.window_name)


    

    
    def world_to_screen_v(self,p:Vector2):
        """
        converts a vector from inworld to onscreen(px)
        
        :param p: position inworld
        :type p: Vector2
        """
        return p+ Vector2(self.pad,self.pad)
    
    def screen_to_world_v(self,p):
        """
        converts a vector from onscreen to inworld(px)
        
        :param p: position onscreen
        :type p: Vector2
        """
        return p- Vector2(self.pad,self.pad)
    
    
    
    def draw_all_walls(self,wl:list=None):
        """
        Draws all walls unless specified
        
        :param wl: wall list
        """
        if wl == None:
            wl=self.world.walls
        for wall in wl:
            t1=self.world_to_screen_v(wall.p1).as_tup()
            t2=self.world_to_screen_v(wall.p2).as_tup()
            pygame.draw.line(self.window,self.wall_color,t1,t2,2)
     
    
    def draw_all_balls(self,bl=None):
        """
        Draws all balls unless specified

        :param bl: ball list
        """
        if bl ==None:
            bl=self.world.balls
        # print(bl)
        for ball in bl:
            pygame.draw.circle(self.window,self.ball_color,self.world_to_screen_v(ball.pos).as_tup(),ball.r)
    
    def reset(self):
        """reset graphic window"""
        x0,y0=self.pad,self.pad

        pygame.draw.rect(self.window, self.w_bg, pygame.Rect(0,0,self.wsize.x,self.wsize.y))
        pygame.draw.rect(self.window, self.g_bg, pygame.Rect(x0,y0,self.gsize.x,self.gsize.y))


    def render_world(self):
        """renders all world objects"""
        self.draw_all_walls()
        self.draw_all_balls()
        pygame.display.flip() 

    def handel_events(self,events):
        """parses inputs by user"""
        self.curr_mouse_pos = Vector2.to_V2(pygame.mouse.get_pos())

        for event in events:
            # if event is of type quit then 
            # set running bool to false
            if event.type == pygame.QUIT:
                self.running=False
            
            elif event.type==pygame.KEYDOWN:
                self.held_keys.add(event.key)
                if event.key not in self.toggled_keys:
                    self.toggled_keys.add(event.key)
                else:
                    self.toggled_keys.discard(event.key)

                # print(event.key)
                
                if event.key==pygame.K_w:
                    self.mode="wall"
                elif event.key==pygame.K_b:
                    self.mode="ball"
                    
                # print(mode)

                if event.key==pygame.K_c:
                    self.world.clear()

                if event.key == pygame.K_e:
                    self.world.edge_walls()

            elif event.type==pygame.KEYUP:
                self.held_keys.discard(event.key)
            
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1: #leftclick only
                    self.mouse_down_pos=self.curr_mouse_pos.copy()
                    # print(mouse_down_pos)
            
            elif event.type==pygame.MOUSEBUTTONUP:
                if event.button==1: # left button only
                    if self.mouse_down_pos == None:
                        continue
                    dv=self.curr_mouse_pos-self.mouse_down_pos
                    oldp=self.screen_to_world_v(self.mouse_down_pos)
                    newp=self.screen_to_world_v(self.curr_mouse_pos)
                    if self.mode == "ball":
                        self.world.add_ball(Ball(oldp,dv,r=self.creator_ball_size))
                    elif self.mode=="wall":
                        self.world.add_wall(Wall(oldp,newp))

                    self.mouse_down_pos=None
            
            elif event.type==pygame.MOUSEWHEEL:
                if self.mode=="ball" :

                    if event.y>0 and self.creator_ball_size < self.max_ball_size:
                        self.creator_ball_size+=1
                    elif event.y<0 and self.creator_ball_size >1:
                        self.creator_ball_size-=1
    
    def ui_to_window_xy(self,v:Vector2):
        """
        Docstring for ui_to_window_xy
        
        :param v: UI box xy to window xy, topleft = (0,0)
        :type v: Vector2
        """
        return Vector2(self.pad*2+self.gsize.x,self.pad)+v
    
    def text_rend(self,text_string:str=None):
        """
        print text into ui
        if blank will incrememnt line
        
        :param text_string: content
        :type text_string: str
        """
        if text_string==None or text_string=="":
            self.curr_gui_line+=1
            return        
        text=self.font.render(text_string,True,self.font_color,None)
        text_rect=text.get_rect()
        
        text_rect.x+=self.ui_tl_v.x + self.txtpad
        text_rect.y+= self.curr_gui_line * (self.txtpad + self.font.get_height()) +self.ui_tl_v.y
        self.window.blit(text,text_rect)
        self.curr_gui_line+=1


        return
    
    def render_gui(self,sdt,rdt,ui_toggled:bool):
        """
        renders all UI
        
        :param sdt: time since last simulation
        :param rdt: time since last rendered frame
        :param ui_toggled: show ui?
        """

                
        
        # render text gui
        self.curr_gui_line=0
        self.ui_tl_v=self.ui_to_window_xy(Vector2(0,0))

        self.text_rend("U - UI Toggle")

        if ui_toggled:
            self.text_rend()
            file_path = 'v2/support/static/instructions.txt'
            with open(file_path, 'r') as file:
                for line in file:
                    self.text_rend(line.rstrip())

            self.text_rend()

            if sdt !=0:
                sim_hz=round(1/sdt)
                self.text_rend(f"Sim Hz: {sim_hz}")
            if rdt !=0:
                rend_hz=round(1/rdt)
                self.text_rend(f"Render Hz: {rend_hz}")

            self.text_rend()
            self.text_rend(f"{len(self.world.balls)} Balls")
            self.text_rend(f"{len(self.world.walls)} Walls")
            self.text_rend()
            self.text_rend(f"Mode: {self.mode}")
            if self.mode=="ball":
                self.text_rend(f"Brush Ball Size: {self.creator_ball_size}")
                if self.mouse_down_pos == None:
                    pygame.draw.circle(self.window,self.plan_color,self.curr_mouse_pos.as_tup(),self.creator_ball_size)
                else:
                    pygame.draw.circle(self.window,self.plan_color,self.mouse_down_pos.as_tup(),self.creator_ball_size)

            self.text_rend()
            total_E=0
            for ball in self.world.balls:
                m=1
                total_E+= 0.5 * m * (ball.v.mag_sqr())
            self.text_rend(f"Total energy: {round(total_E,1)}")


            # render inworld gui items
            if self.mouse_down_pos != None:
                pygame.draw.line(self.window,self.plan_color,self.curr_mouse_pos.as_tup(),self.mouse_down_pos.as_tup())

                if self.mode == "ball":
                    pygame.draw.circle(self.window,self.plan_color,self.mouse_down_pos.as_tup(),self.creator_ball_size)
                    self.text_rend()
                    vmag=round((self.curr_mouse_pos-self.mouse_down_pos).magnitude())
                    self.text_rend(f"V: {vmag}")
                    m=1
                    e=(self.curr_mouse_pos-self.mouse_down_pos).magnitude()**2 * 0.5 * m
                    self.text_rend(f"E: {round(e)}")
                    
        
        



    
    def main_loop(self):  
        """starts game window"""

        # creating a bool value which checks
        # if game is running

        self.running = True

        oldt=time.time()
        old_g_t=time.time()

        
        self.held_keys=set()
        self.toggled_keys=set()
        self.mode=""
        self.mouse_down_pos=None

        self.creator_ball_size=3

        

        # keep game running till running is true
        while self.running:
            ct=time.time()
            dt=ct-oldt
            oldt=ct


            # Check for event if user has pushed
            # any event in queue
            self.handel_events(pygame.event.get())
                    
            
            
            
            self.world.tstep(dt)
            # print(dt)
            

            ct=time.time()
            g_dt=ct-old_g_t
            if g_dt> 1/50:
                old_g_t=ct
                self.reset()

                ui_toggled=pygame.K_u in self.toggled_keys
                self.render_gui(dt,g_dt,ui_toggled)

            

                self.render_world()
            

        pygame.quit() 


