#!/usr/bin/env python3
import matplotlib.pyplot as plt
import networkx as nx
import pygame as pg
import math
import yaml
import matplotlib.image as mpimg

run = True
pg.init()
pg.font.init()

w=1280
h=720

# w=800
# h=600


screen = pg.display.set_mode((w,h))
timer = pg.time.Clock()
font = pg.font.SysFont("Cordia New",h//24,True,False)
small_font = pg.font.SysFont("Cordia New",h//30,True,False)
black = pg.Color('black')
color_inactive = pg.Color('lightskyblue3')
color_active = pg.Color('chartreuse4')
color_light = pg.Color('aquamarine3')
color_dark = pg.Color('aquamarine4')
dark_red = pg.Color('firebrick4')
light_red =  pg.Color('firebrick2')
color = color_inactive
active = False
text_add = font.render('add' , True , 'white')
text_remove = font.render('remove' , True , 'white')
start_box = pg.Rect(500, 600, 50, 50)
G = nx.Graph()

def buildtext(text,posx,posy):
    pos=(posx,posy)
    screen.blit(font.render(str(text),True, (255 ,255 ,255)),pos)
    pg.display.update()
          
def drawtext(txt,box):
    txt_surface = font.render(txt, True,(255, 0, 0))
    screen.blit(txt_surface, (box.x+5, box.y+5))
    pg.draw.rect(screen, color, box, 2)
    pg.display.flip()
    pg.display.update()

def text_get(txt):
    text_inbox = txt
    return text_inbox

def addNode(nodename):
    G.add_node(nodename)

def addEdge(list_edge):
    G.add_edge(list_edge[0],list_edge[1])

def shownumnode(num):
    pos = (w/18.28,h/2.57)
    screen.blit(font.render(str(num),True, (255 ,255 ,255)),pos)
    pg.display.update()

def drawcircle(posx,posy,radius,name):
    pg.draw.circle(screen, (0, 255, 0),[posx, posy], radius, 3)
    screen.blit(small_font.render(str(name),True, (255 ,0 ,0)),(posx-radius/4,posy -radius/2))
    pg.display.update()

def main():
    nodename= ''
    nodeA=''
    nodeB=''
    my_state=0
    txt=''
    text_inbox=''
    list_nodename=[]
    list_edge=[nodeA,nodeB]
    num_pressadd=0
    num=0
    last_node=0
    maxrow=0
    main_list=[]
    sub_list=[]
    width = screen.get_width()
    height = screen.get_height()
    diffx = float(0)
    diffy = float(0)
    input_box = pg.Rect(width/18.28, height/12.5+height/30, width/12.8, height/24)
    text = ''
    font = pg.font.SysFont("Cordia New",height//24,True,False)
    small_font = pg.font.SysFont("Cordia New",height//30,True,False)
    black = pg.Color('black')
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('chartreuse4')
    color_light = pg.Color('aquamarine3')
    color_dark = pg.Color('aquamarine4')
    dark_red = pg.Color('firebrick4')
    light_red =  pg.Color('firebrick2')
    color = color_inactive
    active = False
    while (1):
        if my_state==0:
            pg.display.set_caption('GUI')
            buildtext('Select resolution (dpi)       *Input only number',width/24,height/25)
            buildtext('recommend at 180',width/5.12,height/12.5+height/30)
            my_state=1
        elif my_state==1:   
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                        if input_box.collidepoint(event.pos):
                            active = True
                        else:
                            active = False
                        color = color_active if active else color_inactive
                if event.type == pg.KEYDOWN:
                        if event.key == pg.K_RETURN:
                                text_get(text)
                                my_state=2
                        elif event.key == pg.K_BACKSPACE:
                                text = text[:-1]
                                pg.display.update()
                        else:
                                text += event.unicode
            if active:
                color = color_active
            else:
                color = color_inactive
            drawtext(text,input_box)

        elif my_state==2:
            screen.fill(black)
            pg.display.update()
            plt.figure(dpi=int(text))
            buildtext('Add graph node  (Click ADD for add node / REMOVE for delete node)',width/25.6,height/4)
            buildtext('Total node = ' +str(num_pressadd),width/18.28,height/2.57)
            my_state=3

        elif my_state==3:
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    exit()
                if ev.type == pg.MOUSEBUTTONDOWN:
                    if width/18.28 <= mouse[0] <= width/18.28 + width/9.14 and height/3.27 <= mouse[1] <= height/3.27 +height/18:
                        pg.draw.rect(screen,black,(width/18.28,height/2.57,width/18.28+ width/8,height/2.57 +height/14.4))
                        num_pressadd+=1
                        buildtext('Total node = ' +str(num_pressadd),width/18.28,height/2.57)
                    if width/4.26 <= mouse[0] <= width/4.26 + width/9.14 and height/3.27 <= mouse[1] <= height/3.27 +height/18:
                        pg.draw.rect(screen,black,(width/18.28,height/2.57,width/18.28+ width/8,height/2.57 +height/14.4))
                        if num_pressadd>0:
                            num_pressadd-=1
                            buildtext('Total node = '+str(num_pressadd),width/18.28,height/2.57)
                        else:
                            num_pressadd=0
                            buildtext('Total node = '+str(num_pressadd),width/18.28,height/2.57)
                if ev.type == pg.KEYDOWN:
                        if ev.key == pg.K_RETURN:
                                my_state=4
            mouse = pg.mouse.get_pos()
            if width/18.28 <= mouse[0] <= width/18.28 + width/30 and height/3.27  <= mouse[1] <= height/3.27 + height/72:
                pg.draw.rect(screen,color_light,[width/18.28,height/3.27,width/9.14,height/18])   
            else:
                pg.draw.rect(screen,color_dark,[width/18.28,height/3.27,width/9.14,height/18])
                screen.blit(text_add, (width/18.28 + width/30,height/3.27 + height/72))
                pg.display.update()

            if width/4.26 <= mouse[0] <= width/4.26 + width/25.6 and height/3.27  <= mouse[1] <= height/3.27 +height/72:
                pg.draw.rect(screen,light_red,[width/4.26,height/3.27,width/9.14,height/18])
            else:
                pg.draw.rect(screen,dark_red,[width/4.26,height/3.27,width/9.14,height/18])
                screen.blit(text_remove, (width/4.26 + width/64,height/3.27 +height/72))
                pg.display.update()  
            pg.display.update()


        elif my_state==4:
            screen.fill(black)
            pg.display.update()
            my_state=5
        
        elif my_state==5:
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    exit()
                if ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_q:
                        screen.fill(black)
                        pg.display.update()
                        my_state=2
                    if event.key == pg.K_RETURN:
                        my_state=7
                if ev.type == pg.MOUSEBUTTONDOWN:
                    diffx = 1+ round((mouse[0] - width/25.6)/50)
                    diffy = 1+ round((mouse[1] - height/14.4)/(height/14.4))
                    maxrow = math.floor(width/50)
                    if diffy==1:
                        if (diffx*50-height/36-maxrow/2 <=mouse[0]<= diffx*50+height/36-maxrow/2) and ((diffy*height/14.4)-height/36<=mouse[1]<=(diffy*height/14.4)+height/36) and diffx<=num_pressadd  :
                            sub_list+=[diffx]
                            if len(sub_list)==2:
                                main_list.append(sub_list)
                                sub_list=[]
                                my_state=6
                    if diffy==3:
                        if (diffx*50-height/36-maxrow/2 <=mouse[0]<= diffx*50+height/36-maxrow/2) and ((diffy*height/14.4)-height/36<=mouse[1]<=(diffy*height/14.4)+height/36) and diffx+maxrow<=num_pressadd  :
                            sub_list+=[diffx+maxrow]
                            if len(sub_list)==2:
                                main_list.append(sub_list)
                                sub_list=[]
                                my_state=6

            mouse = pg.mouse.get_pos()      
            for i in range(0,num_pressadd):
                if (i*50)+width/25.6 + height/36 <= width:
                    drawcircle((i*50)+width/25.6,height/14.4,height/36,str(i+1))
                    last_node=i
                elif(i*50)+width/25.6 + height/36 > width:
                    drawcircle(((i-last_node-1)*50)+width/25.6,height/4.8,height/36,str(i+1))
            
            buildtext('Select Edge pair by click on Node',width/25.6,height/2.4)
            

        elif my_state==6:
            pg.draw.rect(screen,black,(width/18.28,height/2,width- width/18.28,height - height/2))
            buildtext('Selected Edge : ' + str(main_list),width/18.28,height/2)
            pg.display.update()
            my_state=5
        
        elif my_state==7:
            for j in range (0,len(main_list)):
                addEdge(main_list[j])
            my_state=9

        elif my_state==9:  #drawnode and plot
            nx.draw(G,with_labels=1)
            plt.show()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                    exit()
    pg.quit()
    exit()

def main2():
    bg = pg.image.load(image_file)
    bg = pg.transform.scale(bg, (1280, 720))
    rect = bg.get_rect()
    screen.fill((255,255,255))
    rect = rect.move((0, 0))
    while (1):
         screen.blit(bg,rect)
         pg.display.update()

def main3():
    nodeA=''
    nodeB=''
    my_state=0
    list_edge=[nodeA,nodeB]
    num_pressadd=0
    node_select=[]
    main_list=[]
    sub_list=[]
    all_node=[]
    dup_node =[]
    single_node=[]
    width = screen.get_width()
    height = screen.get_height()
    diffx = float(0)
    diffy = float(0)
    input_box = pg.Rect(width/18.28, height/12.5+height/30, width/12.8, height/24)
    text = ''
    font = pg.font.SysFont("Cordia New",height//24,True,False)
    small_font = pg.font.SysFont("Cordia New",height//30,True,False)
    black = pg.Color('black')
    gray = pg.Color('grey80')
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('chartreuse4')
    scrren_list=[]
    color = color_inactive
    active = False
    bg = pg.image.load(image_file)
    bg = pg.transform.scale(bg, (width, height))
    rect = bg.get_rect()
    rect = rect.move((0, 0))
    while (1):
        if my_state==0:
            pg.display.set_caption('GUI')
            buildtext('Select resolution (dpi)       *Input only number',width/24,height/25)
            buildtext('recommend at 180',width/5.12,height/12.5+height/30)
            my_state=1
        elif my_state==1:   
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                        if input_box.collidepoint(event.pos):
                            active = True
                        else:
                            active = False
                            color = color_active if active else color_inactive
                if event.type == pg.KEYDOWN:
                        if event.key == pg.K_RETURN:
                                my_state=2
                        elif event.key == pg.K_BACKSPACE:
                                text = text[:-1]
                                pg.display.update()
                        else:
                                text += event.unicode
            if active:
                color = color_active
            else:
                color = color_inactive
            drawtext(text,input_box)

        elif my_state==2:
            screen.fill(black)
            pg.display.update()
            plt.figure(dpi=int(text))
            my_state=3

        elif my_state==3:
            screen.blit(bg,rect)
            buildtext('Add node(Left click at map) | Remove current node (Press q)',width/25.6,height/14.4)
            pg.display.update()
            my_state=4
            
        elif my_state==4:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    current_screen = pg.Surface.copy(screen)
                    scrren_list.append(current_screen)
                    num_pressadd+=1
                    pg.draw.rect(screen,gray,(width/18.28,height/7.2,width/18.28+ width/8,height/14.4))
                    buildtext('Total node = ' +str(num_pressadd),width/18.28,height/7.2)
                    drawcircle(mouse[0],mouse[1],width//64,str(num_pressadd))                 
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                            my_state=5
                    if event.key == pg.K_q:
                        num_pressadd-=1
                        if num_pressadd>=0:
                            pg.draw.rect(screen,gray,(width/18.28,height/7.2,width/18.28+ width/8,height/14.4))
                            buildtext('Total node = ' +str(num_pressadd),width/18.28,height/7.2)
                            screen.blit(scrren_list[num_pressadd],(0,0))
                            current_screen = pg.Surface.copy(screen)
                        if num_pressadd<0:
                            num_pressadd=0
                            pg.draw.rect(screen,gray,(width/18.28,height/7.2,width/18.28+ width/8,height/14.4))
                            buildtext('Total node = ' +str(num_pressadd),width/18.28,height/7.2)
                            screen.blit(scrren_list[num_pressadd],(0,0))

            mouse = pg.mouse.get_pos() 
            pg.display.update()

        elif my_state==5:
            screen.fill(black)
            pg.display.update()
            my_state=6
        
        elif my_state==6:
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    exit()
                if ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_q:
                        screen.fill(black)
                        pg.display.update()
                        my_state=2
                    if event.key == pg.K_RETURN:
                        my_state=8
                if ev.type == pg.MOUSEBUTTONDOWN:
                    diffx = 1+ round((mouse[0] - width/25.6)/50)
                    diffy = 1+ round((mouse[1] - height/14.4)/(height/14.4))
                    maxrow = math.floor(width/50)
                    if diffy==1:
                        if (diffx*50-height/36-maxrow/2 <=mouse[0]<= diffx*50+height/36-maxrow/2) and ((diffy*height/14.4)-height/36<=mouse[1]<=(diffy*height/14.4)+height/36) and diffx<=num_pressadd  :
                            sub_list+=[diffx]
                            node_select+=[diffx]
                            if len(sub_list)==2:
                                main_list.append(sub_list)
                                sub_list=[]
                                my_state=7
                    if diffy==3:
                        if (diffx*50-height/36-maxrow/2 <=mouse[0]<= diffx*50+height/36-maxrow/2) and ((diffy*height/14.4)-height/36<=mouse[1]<=(diffy*height/14.4)+height/36) and diffx+maxrow<=num_pressadd  :
                            sub_list+=[diffx+maxrow]
                            node_select+=[diffx+maxrow]
                            if len(sub_list)==2:
                                main_list.append(sub_list)
                                sub_list=[]
                                my_state=7
            mouse = pg.mouse.get_pos()      
            for i in range(0,num_pressadd):
                if (i*50)+width/25.6 + height/36 <= width:
                    drawcircle((i*50)+width/25.6,height/14.4,height/36,str(i+1))
                    last_node=i
                elif(i*50)+width/25.6 + height/36 > width:
                    drawcircle(((i-last_node-1)*50)+width/25.6,height/4.8,height/36,str(i+1))
            
            buildtext('Select Edge pair by click on Node',width/25.6,height/2.4)

        elif my_state==7:
            pg.draw.rect(screen,black,(width/18.28,height/2,width- width/18.28,height - height/2))
            buildtext('Selected Edge : ' + str(main_list),width/18.28,height/2)
            pg.display.update()
            my_state=6
        
        elif my_state==8:
            for i in range(1,num_pressadd+1):
                all_node.append(i)
            for j in range (0,len(main_list)):
                addEdge(main_list[j])
            dup_node = set(all_node).intersection(node_select)
            dup_node = list(dup_node)
            single_node = list(set(all_node)-set(node_select))
            for k in range(0,len(single_node)):
                addNode(single_node[k])
            my_state=9

        elif my_state==9:  #draw node and plot
            nx.draw(G,with_labels=1)
            plt.show()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
    pg.quit()
    exit()

if __name__ == '__main__' :
    with open('map_done.yaml','r') as f:
        yml_dict = yaml.safe_load(f)
    image_file = yml_dict.get('image')
    main3()

    

    # elif my_state==3:
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             run = False
    #             pg.quit()
    #             exit()
    #         if event.type == pg.MOUSEBUTTONDOWN:
    #                 if input_box2.collidepoint(event.pos):
    #                     active = True
    #                 else:
    #                     active = False
    #                 color = color_active if active else color_inactive
    #         if event.type == pg.KEYDOWN:
    #                 if event.key == pg.K_RETURN:
    #                         text_get(text_node)
    #                         buildtext("Here is your added Node :  " + text_node,100,300)
    #                         my_state=4
    #                 elif event.key == pg.K_BACKSPACE:
    #                         text_node = text_node[:-1]
    #                         pg.display.update()
    #                 else:
    #                         text_node += event.unicode
    #     if active:
    #         color = color_active
    #     else:
    #         color = color_inactive
    #     drawtext(text_node,input_box2)

    # elif my_state==4:
    #     text_node = text_node.replace(' ','')
    #     text_node = text_node.replace(','," ")
    #     list_nodename = list(text_node.split(" "))
    #     # buildtext(str(len(list_nodename)),100,450)
    #     for i in range(0,len(list_nodename)):
    #         addNode(list_nodename[i])
    #     my_state=5



    # elif my_state==5:
    #     buildtext('Add edge(s)     (Example : [node1,node2],[node2,node3])',50,400)
    #     my_state=6
    
    # elif my_state==6:
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             run = False
    #             pg.quit()
    #             exit()
    #         if event.type == pg.MOUSEBUTTONDOWN:
    #                 if input_box3.collidepoint(event.pos):
    #                     active = True
    #                 else:
    #                     active = False
    #                 color = color_active if active else color_inactive
    #         if event.type == pg.KEYDOWN:
    #                 if event.key == pg.K_RETURN:
    #                         text_get(text_edge)
    #                         buildtext("Here is your added Edge :  " + text_edge,100,500)
    #                         my_state=7
    #                 elif event.key == pg.K_BACKSPACE:
    #                         text_edge = text_edge[:-1]
    #                         pg.display.update()
    #                 else:
    #                         text_edge += event.unicode
    #     if active:
    #         color = color_active
    #     else:
    #         color = color_inactive
    #     drawtext(text_edge,input_box3)

    # elif my_state==7:
    #     adapt_text = text_edge
    #     adapt_text = adapt_text.replace(" ",'')
    #     adapt_text = adapt_text[1:-1]

    #     adapt_text=adapt_text.split('],[')

    #     for i in range(0,len(adapt_text)):
    #         adapt_text[i] = adapt_text[i].split(",")

    #     # buildtext(len(adapt_text),100,550)
    #     my_state=8
    
    # elif my_state==8:
    #     for i in range (0,len(adapt_text)):
    #         addEdge(adapt_text[i])
    #     my_state=9



