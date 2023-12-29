import pygame
import math
from point import *
from path import *
from algorithm import *

height =800
width = 800
point_radius = 8
line_thickness = 8
path_thickness = 4
colors = {
    "START":(200,0,0),
    "END":(0,0,200),
    "PSTART":(200,200,0),
    "PEND":(0,200,200),
    "LINE": (100,100,100),
    "PATH": (250,0,250)
}

mouse_state = None
start_point = None
end_point = None
paths = []
active_path_start = None
show_line = False

screen = pygame.display.set_mode((width, height))

def process_click():
    global start_point
    global end_point
    global active_path_start
    global mouse_state
    if mouse_state == "START":
        start_point = Point()
        start_point.x, start_point.y = mouse_coord()
    elif mouse_state == "END":
        end_point = Point()
        end_point.x, end_point.y = mouse_coord()
    elif mouse_state == "PSTART":
        active_path_start = Point()
        active_path_start.x, active_path_start.y = mouse_coord()
        mouse_state = "PEND"
    elif mouse_state == 'PEND' and active_path_start != None:
        temp_end = Point()
        temp_end.x, temp_end.y = mouse_coord()
        paths.append(Path(active_path_start,temp_end))
        active_path_start = None
        mouse_state = 'PSTART'
    pass


def mouse_coord(): # returns co-ordinates of mouse-pointer
    global height
    global width
    x, y =  pygame.mouse.get_pos()
    return x-width/2, height/2-y

def to_screen(x, y):
    global height
    global width
    return x+width/2, height/2-y


def draw():
    if start_point != None:
        pygame.draw.circle(screen,colors["START"],to_screen(start_point.x,start_point.y),point_radius)
    if end_point != None:
        pygame.draw.circle(screen,colors["END"],to_screen(end_point.x,end_point.y),point_radius)
    if active_path_start != None:
        pygame.draw.line(screen,colors["LINE"],to_screen(active_path_start.x,active_path_start.y),pygame.mouse.get_pos(),line_thickness)
        pygame.draw.circle(screen,colors["PSTART"],to_screen(active_path_start.x,active_path_start.y),point_radius)
        
    for p in paths:
        pygame.draw.line(screen,colors["LINE"],to_screen(p.start.x,p.start.y),to_screen(p.end.x,p.end.y),line_thickness)
        pygame.draw.circle(screen,colors["PSTART"],to_screen(p.start.x,p.start.y),point_radius)
        pygame.draw.circle(screen,colors["PEND"],to_screen(p.end.x,p.end.y),point_radius)
        
    if mouse_state != None:
        pygame.draw.circle(screen,colors[mouse_state],pygame.mouse.get_pos(),point_radius)
    if show_line:
        if start_point and end_point:
            sp = shortest(start_point, paths, end_point)
            for p in sp:
                pygame.draw.line(screen,colors["PATH"],to_screen(p.start.x,p.start.y),to_screen(p.end.x,p.end.y),path_thickness)
                pygame.draw.circle(screen,colors["PATH"],to_screen(p.start.x,p.start.y),point_radius)
                pygame.draw.circle(screen,colors["PATH"],to_screen(p.end.x,p.end.y),point_radius)
        
running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                mouse_state = "START"
            elif event.key == pygame.K_r:
                mouse_state = "END"
            elif event.key == pygame.K_w:
                mouse_state = "PSTART"
            elif event.key == pygame.K_e:
                mouse_state = "PEND"
            elif event.key == pygame.K_c:
                if len(paths) != 0:
                    paths.pop()
            elif event.key == pygame.K_j:
                show_line = not show_line

        if event.type == pygame.MOUSEBUTTONDOWN:
            process_click()

    screen.fill((0, 0, 0))
    draw()

    pygame.display.update()
    
