import pygame

class menu:

    def __init__(self, window):
        self.heading_colour = (0,0,0)        #black
        self.options_color = (0,0,255)       #blue
        self.hover_color = (0,255,00)
        self.heading_font = pygame.font.Font('freesansbold.ttf',25)
        self.window = window
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = pygame.display.get_window_size()
    

    def run(self):
        self.window.fill((255, 255, 255))
        
        menu_heading, heading_surface = self.createText("Choose an Algorithm to Simulate", self.heading_font, self.heading_colour)
        heading_surface.center = ((self.SCREEN_WIDTH/2),(self.SCREEN_HEIGHT/8))
        self.window.blit(menu_heading, heading_surface)

        
        #draw rectangles for menu options
        options_box1 = pygame.Rect((0, 0), (420, 30))
        options_box1.center = ((self.SCREEN_WIDTH/2),(self.SCREEN_HEIGHT/4))
        options_box2 = pygame.Rect((0, 0), (420, 30))
        options_box2.center = ((self.SCREEN_WIDTH/2),(options_box1.bottom+40))
        options_box3 = pygame.Rect((0, 0), (420, 30))
        options_box3.center = ((self.SCREEN_WIDTH/2),(options_box2.bottom+40))
        options_box4 = pygame.Rect((0, 0), (420, 30))
        options_box4.center = ((self.SCREEN_WIDTH/2),(options_box3.bottom+40))

        # print(options_box1.right)
        

        #display the words in the rectangles
        options_font = pygame.font.Font(None,24)
        btn1=self.createButton("First Come First Serve (FCFS)", options_box1, options_font,\
            self.hover_color,self.options_color, 3)
        
        btn2=self.createButton("Round Robin (RR)", options_box2, options_font,\
            self.hover_color,self.options_color, 3)
        
        btn3=self.createButton("Shortest Process Remaining (SPN)", options_box3, options_font,\
            self.hover_color,self.options_color, 3)
        
        btn4=self.createButton("Shortest Time Remaining (SRT)", options_box4, options_font,\
            self.hover_color,self.options_color, 3)
        
        pygame.display.update()

        if (btn1):
            pygame.display.set_caption("First Come First Serve Simulator")
            return "fcfs"
        elif btn2:
            pygame.display.set_caption("Round Robin Simulator")
            return "rr"
        elif btn3:
            pygame.display.set_caption("Shortest Process Next Simulator")
            return "spn"
        elif btn4:
            pygame.display.set_caption("Shortest Remaining Time Simulator")
            return "srt"
        return None
    

    def createText(self,words, font, colour):
        text = font.render(words, True, colour)
        return text, text.get_rect()

    def createButton(self, words, box, font,color, color2, size):
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        event = False
        if box.right > mouse_pos[0] > box.left and box.bottom > mouse_pos[1] > box.top:
                pygame.draw.rect(self.window, color,box,size)
                if clicked[0] == 1:
                    event = True
        else:
            pygame.draw.rect(self.window, color2, box,3)

        box_text, box_surf = self.createText(words, font, color2)
        box_surf.center = box.center
        self.window.blit(box_text, box_surf)
        return event
