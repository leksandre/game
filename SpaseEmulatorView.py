import sys, math, pygame, random, os, cv2, imageio
divX = 1
divY = 1
divZ = 1
macWindowW = 0
macWindowH = 0
def corrrectcolor(g):
    if g > 255:
        g = 0
    if g < 0:
        g = 255
    return g
class Point3D:
    def __init__(self, x = 0, y = 0, z = 0 ): # 
        self.x, self.y, self.z = float(x), float(y), float(z)
    def rotateX(self, angle):
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)
    def rotateY(self, angle):
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)
    def rotateZ(self, angle):
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)
    def project(self, win_width, win_height, fov, viewer_distance):
        if (viewer_distance + self.z)==0:
         viewer_distance=viewer_distance+1
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)#(r,g,b) 
class Simulation:
    def __init__(self):

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.display.set_caption('space emulator view')

        infoObject = pygame.display.Info()
        global macWindowW, macWindowH
        macWindowW = infoObject.current_w
        macWindowH = infoObject.current_h
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (infoObject.current_w//7,infoObject.current_h//7)
        self.screen  = pygame.display.set_mode((infoObject.current_w//7*5, infoObject.current_h//7*5), pygame.RESIZABLE)
        
        #self.screen = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)
        #self.screen  = pygame.display.set_mode((0, 0), pygame.RESIZABLE )


        self.clock = pygame.time.Clock()
        randpoints = []
        was = []
        max1 = 4
        min1 = -4
        redndcoclors = []
        for _ in range(1000):
            x=random.randint(min1,max1);
            y=random.randint(min1,max1);
            z=random.randint(min1,max1);
            # randpoints.append(Point3D(x-1,y,z))
            # randpoints.append(Point3D(x,y-1,z))
            # randpoints.append(Point3D(x,y,z-1))
            # randpoints.append(Point3D(x+1,y,z))
            # randpoints.append(Point3D(x,y+1,z))
            # randpoints.append(Point3D(x,y,z+1))
            if [x,y,z] not in was:
             #print(x,y,z)
             randpoints.append(Point3D(x,y,z))
             was.append([x,y,z])
             redndcoclors.append((((random.randint(1,15))),(random.randint(1,15)),(random.randint(1,15))))
             #redndcoclors.append((r,g,b))
             #redndcoclors.append((155,155,155))
        self.vertices = randpoints
        self.verticesC = redndcoclors
        

 
        self.angleX, self.angleY, self.angleZ = 0, 0, 0
 
    def run(self):
        timer12 = 0
        dt = 0
        maxCountImg=200
        currimg = maxCountImg+2
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                 if event.button == 1:
                    if timer12 == 0:  
                        timer12 = 0.001  
                    elif timer12 < 0.5:
                        print('double click')
                        
                        currimg = 0
                        append_images = []
                        #save 1/4 screen
                        # rect = pygame.Rect(25, 25, self.screen.get_width()//2, self.screen.get_height()//2)
                        # sub = self.screen.subsurface(rect)
                        # pygame.image.save(sub, "screenshot.jpg")

                        #minimize maximize
                        # infoObject = pygame.display.Info()
                        # print(infoObject,macWindowW,macWindowH)
                        # if infoObject.current_w!=macWindowW or infoObject.current_h!=macWindowH:
                        #     os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (0,0)
                        #     self.screen  = pygame.display.set_mode((0, 0), pygame.RESIZABLE )
                        #     print('maximize')
                        # else:
                        #     os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (infoObject.current_w//7,infoObject.current_h//7)
                        #     self.screen  = pygame.display.set_mode((infoObject.current_w//7*5, infoObject.current_h//7*5), pygame.RESIZABLE)
                        #     print('minimize')

                        timer12 = 0
                  
            if timer12 != 0:
             timer12 += dt
             if timer12 >= 0.5:
                timer12 = 0

            if currimg<maxCountImg:
                scrName = "screenshot"+str(currimg)+".png"
                pygame.image.save(self.screen, scrName)
                append_images.append(scrName)
                currimg+=1

            if currimg==maxCountImg:
                append_imagesOrig = append_images.copy()
                append_images.reverse()
                images1 = (append_imagesOrig+append_images)
                #print(images1)
                #from images2gif import writeGif
                #writeGif('screensaver.gif', images1, , optimize=True, duration=40, dither=0)
                images2 = []
                for filename in images1:
                  if os.path.isfile(filename):
                    images2.append(imageio.imread(filename))
                gifname = 'screensaver.gif'
                res = imageio.mimsave(gifname, images2, fps=60)
                print(str(gifname)+' is saved')

                image_folder = './'
                video_name = 'screensaver.mp4'

                #images = [img for img in os.listdir(image_folder) if (img.endswith(".jpg") and img.startswith('screenshot'))]
                #fourcc = cv2.cv.FOURCC('8', 'B', 'P', 'S')     #works, large
                #fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
                #fourcc = cv2.VideoWriter_fourcc(*'DIVX') 
                #fourcc = cv2.VideoWriter_fourcc('X','V','I','D') 

                fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                fps = 25
                video = cv2.VideoWriter(video_name,  fourcc, fps,  (self.screen.get_width(),self.screen.get_height()),True)
                for image in images1:
                    video.write(cv2.imread(os.path.join(image_folder, image)))
                cv2.destroyAllWindows()
                video.release()
                print(str(video_name)+' is saved')
                #os.system("ffmpeg -r 1 -i screenshot%01d.jpg -vcodec mpeg4 -y movie.mp4")


                for filename in images1:
                 if os.path.isfile(filename):
                    os.remove(filename)
                currimg+=1

            dt = self.clock.tick(60)/1000#max 60 fps
            self.screen.fill((0,0,0))
            i=0
            for v in self.vertices:
                r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
                p = r.project(self.screen.get_width(), self.screen.get_height(), random.randint(50,50), random.randint(4,4))
                color = self.verticesC[i]
                r = self.verticesC[i][0]
                g = self.verticesC[i][1]
                b = self.verticesC[i][2]
                x, y = int(p.x), int(p.y)
                if random.randint(1,50)==9:
                    r = self.verticesC[i][0]+random.randint(-1,1)
                    r = corrrectcolor(r)
                if random.randint(1,50)==9:
                    g = self.verticesC[i][1]+random.randint(-1,1)
                    g = corrrectcolor(g)
                if random.randint(1,50)==9:
                    b = self.verticesC[i][2]+random.randint(-1,1)
                    b = corrrectcolor(b)
                color = (r,g,b)
                #if i == 10:
                # print(color)
                self.screen.fill(color,(x,y,2,2))
                self.verticesC[i]=color
                if random.randint(1,90)==9:
                    self.screen.fill((r,g,b),(x-1,y,2,2))
                    self.screen.fill((r,g,b),(x,y-1,2,2))
                    self.screen.fill((r,g,b),(x+1,y,2,2))
                    self.screen.fill((r,g,b),(x,y+1,2,2))


                    self.screen.fill((r,g,b),(x-1,y,1,2))
                    self.screen.fill((r,g,b),(x,y-1,1,2))
                    self.screen.fill((r,g,b),(x+1,y,1,2))
                    self.screen.fill((r,g,b),(x,y+1,1,2))

                    self.screen.fill((r,g,b),(x-1,y,2,1))
                    self.screen.fill((r,g,b),(x,y-1,2,1))
                    self.screen.fill((r,g,b),(x+1,y,2,1))
                    self.screen.fill((r,g,b),(x,y+1,2,1))


                    self.screen.fill((r,g,b),(x-1,y,3,2))
                    self.screen.fill((r,g,b),(x,y-1,3,2))
                    self.screen.fill((r,g,b),(x+1,y,3,2))
                    self.screen.fill((r,g,b),(x,y+1,3,2))

                    self.screen.fill((r,g,b),(x-1,y,2,3))
                    self.screen.fill((r,g,b),(x,y-1,2,3))
                    self.screen.fill((r,g,b),(x+1,y,2,3))
                    self.screen.fill((r,g,b),(x,y+1,2,3))
                i=i+1
            
            global divX,divY,divZ
            if random.randint(1,190)==9:
                #divX *= -1
                if (divX==0):
                 while (divX==0):
                  divX = random.randint(-1,1)
                else:
                 if (divY!=0) and (divZ!=0):   
                  divX = 0 
            if random.randint(1,190)==19:
                #divY *= -1
                if (divY==0):
                 while (divY==0):
                  divY = random.randint(-1,1)
                else:
                 if (divX!=0) and (divZ!=0):  
                  divY = 0 
            if random.randint(1,190)==29:
                #divZ *= -1
                if (divZ==0):
                 while (divZ==0):
                  divZ = random.randint(-1,1)
                else:
                 if (divY!=0) and (divX!=0):  
                  divZ = 0   

            self.angleX += divX
            self.angleY += divY
            self.angleZ += divZ
            
            pygame.display.flip()
 
if __name__ == "__main__":
    Simulation().run()