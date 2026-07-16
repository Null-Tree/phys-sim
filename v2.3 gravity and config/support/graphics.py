


from .modeling import *





class Game:
    def __init__(self,config=Config()):

        # initalises pygame
        pygame.init()
        

        self.config=config

        # creates world object
        self.world=World(config=config,
                         gameobj=self)

        # WINDOW CREATION
        # window
        config.windowConfig.w=config.windowConfig.gdim.x + (3*config.windowConfig.padding) + config.windowConfig.cdim.x
        config.windowConfig.h=max(config.windowConfig.gdim.y,config.windowConfig.cdim.y)+2*config.windowConfig.padding
        config.windowConfig.wdim=Vector2(config.windowConfig.w,config.windowConfig.h)


        # note setmode makes the window
        self.window=pygame.display.set_mode((self.config.windowConfig.w,self.config.windowConfig.h))
        pygame.draw.rect(self.window, config.windowConfig.win_bg_color, pygame.Rect(0,0,config.windowConfig.wdim.x,config.windowConfig.wdim.y))
        x0,y0=self.world_to_screen_v(Vector2(0,0)).as_tup()
        pygame.draw.rect(self.window, config.windowConfig.game_area_bg_color, pygame.Rect(x0,y0,config.windowConfig.gdim.x,config.windowConfig.gdim.y))
        pygame.display.set_caption(config.windowConfig.window_name)
        config.windowConfig.font=pygame.font.Font(None,20)

        # initalise var
        self.toggle_ball_trails=False

    
    def world_to_screen_v(self,p:Vector2):
        """
        converts a vector from inworld to onscreen(px)
        
        :param p: position inworld
        :type p: Vector2
        """
        return p+ Vector2(self.config.windowConfig.padding,self.config.windowConfig.padding)
    
    def screen_to_world_v(self,p):
        """
        converts a vector from onscreen to inworld(px)
        
        :param p: position onscreen
        :type p: Vector2
        """
        return p- Vector2(self.config.windowConfig.padding,self.config.windowConfig.padding)
    
    def draw_line(self,inw_p1:Vector2,inw_p2:Vector2,color,width=1,is_in_world_cord:bool=True):
        """
        draws a line in world
        
        :param inw_p1: Point 1
        :type inw_p1: Vector2
        :param inw_p2: Point 2
        :type inw_p2: Vector2
        :param color: RGB color
        :param width: Width int
        :param is_in_world_cord: specifies if it is inworld cords
        :type is_in_world_cord: bool
        """
        
        if is_in_world_cord:
            wp1=self.world_to_screen_v(inw_p1)
            wp2=self.world_to_screen_v(inw_p2)
        else:
            wp1=inw_p1
            wp2=inw_p2
        
        pygame.draw.line(self.window,color,wp1.as_tup(),wp2.as_tup(),width=width)
    
    def draw_all_walls(self,wl:list=None):
        """
        Draws all walls unless specified
        
        :param wl: wall list
        """
        if wl == None:
            wl=self.world.walls
        for wall in wl:
            self.draw_line(wall.p1,wall.p2,self.config.windowConfig.wall_color,2)
     
    
    def draw_all_balls(self,bl=None):
        """
        Draws all balls unless specified

        :param bl: ball list
        """
        if bl ==None:
            bl=self.world.balls
        # print(bl)
        for ball in bl:
            pygame.draw.circle(self.window,self.config.windowConfig.ball_color,self.world_to_screen_v(ball.pos).as_tup(),ball.r)
    
    def reset(self):
        """reset graphic window"""
        x0,y0=self.config.windowConfig.padding,self.config.windowConfig.padding

        pygame.draw.rect(self.window, self.config.windowConfig.win_bg_color, pygame.Rect(0,0,self.config.windowConfig.wdim.x,self.config.windowConfig.wdim.y))
        pygame.draw.rect(self.window, self.config.windowConfig.game_area_bg_color, pygame.Rect(x0,y0,self.config.windowConfig.gdim.x,self.config.windowConfig.gdim.y))


    def render_world(self):
        """renders all world objects"""

        if self.toggle_ball_trails:
            self.render_all_ball_trails()
        
        self.draw_all_balls()
        self.draw_all_walls()
        
    # Progress up to here #TODO
    def handle_events(self,events):
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
                self.check_toggles()

                # print(event.key)
                
                if event.key==pygame.K_2:
                    self.mode="wall"
                elif event.key==pygame.K_1:
                    self.mode="ball"
                elif event.key==pygame.K_0:
                    self.mode=""
                elif event.key==pygame.K_c:
                    self.world.clear()

                elif event.key == pygame.K_e:
                    self.world.edge_walls()

                elif event.key==pygame.K_t:
                    # note the setting to change if past positions is tracked
                    # is monitered through tracktoggles not in the following funct
                    # tis is just to free memory while trails is not being used
                    self.world.trailtoggle_toggleTrailQueueADT()

                # DEBUG key
                elif event.key == pygame.K_d:
                    print(self.world.ball_base)
                
                elif event.key==pygame.K_r:
                    self.world.add_ball()


                

            elif event.type==pygame.KEYUP:
                self.held_keys.discard(event.key)
                self.check_toggles()
            
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
                        self.world.add_ball(Ball(oldp,dv,r=self.creator_ball_radius,mass=self.default_radius_to_mass(self.creator_ball_radius),fixed=self.ball_creator_fixed))
                    elif self.mode=="wall":
                        self.world.add_wall(Wall(oldp,newp))

                    self.mouse_down_pos=None
            
            elif event.type==pygame.MOUSEWHEEL:
                if self.mode=="ball" :

                    if event.y>0 and self.creator_ball_radius < self.config.gameConfig.max_ball_size:
                        self.creator_ball_radius+=1
                    elif event.y<0 and self.creator_ball_radius >1:
                        self.creator_ball_radius-=1

    
    def check_toggles(self):
        """
        Checks if debug toggled graphics should be toggled
        """
        self.show_ball_id=(pygame.K_i in self.toggled_keys)
        self.render_chunks_bool=(pygame.K_g in self.toggled_keys)
        self.ball_creator_fixed=(pygame.K_f in self.toggled_keys)
        self.toggle_ball_trails=(pygame.K_t in self.toggled_keys)

    
    def ui_to_window_xy(self,v:Vector2):
        """
        Docstring for ui_to_window_xy
        
        :param v: UI box xy to window xy, topleft = (0,0)
        :type v: Vector2
        """
        return Vector2(self.config.windowConfig.padding*2+self.config.windowConfig.gdim.x,self.config.windowConfig.padding)+v
        
    def place_text(self,content:str,window_pos:Vector2,color,center:bool=False):
        """
        places text in window
        
        :param content: text to be displayed
        :type content: str
        :param window_pos: vector position of where content should be placed (topleft)
        :type window_pos: Vector2
        :param color: rgbcolor of color
        :param center: center text?
        :type center: bool
        """
        text=self.config.windowConfig.font.render(content,True,color,None)
        text_rect=text.get_rect()
        text_rect.x+=window_pos.x
        text_rect.y+=window_pos.y
        if center:
            text_rect.x -= int(0.5 * text_rect.w)
            text_rect.y-=int(0.5 * text_rect.h)
        self.window.blit(text,text_rect)
    
    def default_radius_to_mass(self,r):
        return r ** 2
    
    def side_UI_text_rend(self,text_string:str=None):
        """
        print text into ui
        if blank will incrememnt line
        
        :param text_string: content
        :type text_string: str
        """
        if text_string==None or text_string=="":
            self.curr_gui_line+=1
            return        
        
        wpos=Vector2(
            self.ui_tl_v.x + self.config.windowConfig.txtpad,
            self.curr_gui_line * (self.config.windowConfig.txtpad + self.config.windowConfig.font.get_height()) +self.ui_tl_v.y
        )

        self.place_text(text_string,wpos,self.config.windowConfig.font_color)
        self.curr_gui_line+=1


        return

    def render_all_ball_trails(self):
        for ball in self.world.balls:
            cl=[self.world_to_screen_v(vec).as_tup() for vec in ball.trail_cl.list]
            if len(cl)>=2:
                pygame.draw.lines(self.window,self.config.windowConfig.trail_color,False,cl)

    
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

        if not ui_toggled:
            self.side_UI_text_rend("U - UI Toggle")
        else:
            self.side_UI_text_rend()
            
            # controls 
            file_path = self.config.windowConfig.controls_guide_path
            with open(file_path, 'r') as file:
                for line in file:
                    self.side_UI_text_rend(line.rstrip())
            self.side_UI_text_rend()

            if self.mode == "":
                self.side_UI_text_rend()
                self.side_UI_text_rend(f"{len(self.world.balls)} Balls")
                self.side_UI_text_rend(f"{len(self.world.walls)} Walls")
                self.side_UI_text_rend()

                total_E=0
                for ball in self.world.balls:
                    total_E+= 0.5 * ball.mass * (ball.v.mag_sqr())
                self.side_UI_text_rend(f"Total kinetic energy: {round(total_E,1)}")
            else:
                self.side_UI_text_rend(f"Mode: {self.mode}")
                self.side_UI_text_rend()

            
            if self.mode=="ball":
                self.side_UI_text_rend(f"Brush Ball Size: {self.creator_ball_radius}")
                self.side_UI_text_rend(f"Brush Ball Mass: {self.default_radius_to_mass(self.creator_ball_radius)}")
                if self.ball_creator_fixed:
                    self.side_UI_text_rend("Fixed ball toggled")
                if self.mouse_down_pos == None:
                    pygame.draw.circle(self.window,self.config.windowConfig.plan_color,self.curr_mouse_pos.as_tup(),self.creator_ball_radius)
                else:
                    pygame.draw.circle(self.window,self.config.windowConfig.plan_color,self.mouse_down_pos.as_tup(),self.creator_ball_radius)
            
            if sdt !=0:
                sim_hz=round(1/sdt)
                self.side_UI_text_rend(f"Sim Hz: {sim_hz}")
            if rdt !=0:
                rend_hz=round(1/rdt)
                self.side_UI_text_rend(f"Render Hz: {rend_hz}")
            

            # render inworld gui items
            if self.mouse_down_pos != None:
                self.draw_line(self.curr_mouse_pos,self.mouse_down_pos,self.config.windowConfig.plan_color,is_in_world_cord=False)

                if self.mode == "ball":
                    pygame.draw.circle(self.window,self.config.windowConfig.plan_color,self.mouse_down_pos.as_tup(),self.creator_ball_radius)
                    self.side_UI_text_rend()
                    vmag=round((self.curr_mouse_pos-self.mouse_down_pos).magnitude())
                    self.side_UI_text_rend(f"V: {vmag}")
                    m=1
                    e=(self.curr_mouse_pos-self.mouse_down_pos).magnitude()**2 * 0.5 * m
                    self.side_UI_text_rend(f"E: {round(e)}")

                    # ball ting
                    v_diff=(self.curr_mouse_pos-self.mouse_down_pos)
                    if not v_diff.is_zero():
                        norm=Vector2(v_diff.y,-v_diff.x).scale_to_mag(self.creator_ball_radius)
                        for c in [-1,1]:
                            d=norm*c
                            self.draw_line(self.curr_mouse_pos+d,self.mouse_down_pos+d,self.config.windowConfig.plan_color,is_in_world_cord=False)
                        
            if self.toggle_ball_trails:
                self.side_UI_text_rend("Toggled Trail rendering")

            if self.render_chunks_bool:
                self.render_chunks()
            if self.show_ball_id:
                self.render_ball_debug()

    
    def render_chunks(self):
        """
        renders chunks and heatmap
        """
        if self.mode == "ball":
            ref=self.world.ball_base
        elif self.mode=="wall":
            ref=self.world.wall_base
        else:
            return
        
        ndim=ref.cdim
        
        tx,ty=self.world_to_screen_v(Vector2.to_V2(ref.cdim) * ref.side_len).as_tup()

        for x in range(ndim[0]+1):
            
            wx = x * ref.side_len + self.config.windowConfig.padding

            pygame.draw.line(self.window,self.config.windowConfig.chunk_color,(wx,self.config.windowConfig.padding),(wx,ty),2)

            
        for y in range(ndim[0]+1):
            wy= y * ref.side_len + self.config.windowConfig.padding
            pygame.draw.line(self.window,self.config.windowConfig.chunk_color,(self.config.windowConfig.padding,wy),(tx,wy),2)
        
        for x in range(ndim[0]):
            for y in range(ndim[1]):
                wpos=self.world_to_screen_v((Vector2(x,y) + (0.5,0.5))*ref.side_len)
                text=str(len(ref[x,y]))
                # text=str((x,y))
                self.place_text(text,wpos,self.config.windowConfig.chunk_color,True)

    
    def render_ball_debug(self):
        """renders debug info on balls"""

        for ball in self.world.balls:

            
            wpos=self.world_to_screen_v(ball.pos)

            bbl=self.world.ball_base.get_all_adj_chunk_items(ball.pos,True)
            if id in bbl:
                bbl.remove(id)
            else:
                print(f"{id} could not find self {bbl}")

            # code to get number of proximity balls
            # text=str(len(bbl)) if len(bbl) !=0 else " "
            # text = str(id) + "|" + text

            if not ball.v.is_zero():
                if ball.r !=1:
                    for b2id in bbl:
                        ball2pos=self.world.balls[b2id].pos
                        wpos2=self.world_to_screen_v(ball2pos)
                        self.draw_line(wpos,wpos2,(0,255,0),is_in_world_cord=False)


            self.place_text(ball.debug_info,wpos,self.config.windowConfig.ball_id_color)




    
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

        self.creator_ball_radius=3

        # needed to initalise toggle setting attributes
        self.check_toggles()

        # keep game running till running is true
        while self.running:
            ct=time.time()
            dt=ct-oldt
            oldt=ct


            # Check for event if user has pushed
            # any event in queue
            self.handle_events(pygame.event.get())


                    
            
            
            
            
            # print(dt)
            

            ct=time.time()
            g_dt=ct-old_g_t
            if g_dt> 1/50:
                old_g_t=ct
                self.reset()
                self.world.tstep(dt)
                ui_toggled=pygame.K_u in self.toggled_keys
                

                
                self.render_gui(dt,g_dt,ui_toggled)

                self.render_world()

                pygame.display.flip() 
            else:
                self.world.tstep(dt)
                
            

        pygame.quit() 


