import RenderObject, Configuration, Footer
import os, Keys, RenderControl, Common
import pygame, sys
from operator import itemgetter

class AbstractList(RenderObject.RenderObject):
    config = Configuration.getConfiguration()
    theme = Configuration.getTheme()
    pygame.font.init()
    entryList = []
    background = None
    selection = None
    footer = None

    previewCache = {}
    previewEnabled = False
    previewPath = None
    preview_final = None

    previewBoxSize = 200


    headerHeight = 20
    initialPath =""
      
    titleFont = pygame.font.Font('theme/NotoSans-Regular.ttf', 20)
    entryFont = pygame.font.Font('theme/NotoSans-Regular.ttf', 16)
     
    maxListEntries = 12  

    currentIndex = 0
    currentWrap = 0

    def render(self, screen):
        screen.blit(self.background, (0,0))
        self.renderHeader(screen)
    
        self.footer.render(screen)
  
        self.renderEntries(screen)
        self.renderSelection(screen)

        self.renderPreview(screen)

    def renderPreview(self, screen):
        if(not self.previewEnabled):
            return
        
        if(self.currentIndex == -1):
            print("index - 1")
            return

        previewBox = pygame.Surface((self.previewBoxSize, self.previewBoxSize), pygame.SRCALPHA)
        previewBox.fill(Configuration.toColor(self.theme["footer"]["color"]))

        if(self.preview_final != None and os.path.exists(self.preview_final)):
            print("render " + self.preview_final)
                 
            image = None
            if(not self.preview_final in self.previewCache):
                image = Common.loadImage(self.preview_final)
                image = Common.aspect_scale(image, self.previewBoxSize - 10, self.previewBoxSize - 10)
                self.previewCache[self.preview_final] = image
            else:
                image = self.previewCache[self.preview_final]

            xOffset = (previewBox.get_width() - image.get_width()) / 2
            yOffset = (previewBox.get_height() - image.get_height()) / 2
            previewBox.blit(image,(xOffset,yOffset))


        screen.blit(previewBox, (self.config["screenWidth"] - previewBox.get_width() ,self.headerHeight))
        

    def renderHeader(self, screen):
        screen.blit(self.header, (0,0))
        

    def renderSelection(self, screen):
        if(len(self.entryList) == 0):
            self.currentIndex = -1
            return
        

        offset = self.listEntryHeight * (self.currentIndex - self.currentWrap) + self.headerHeight
        screen.blit(self.selection, (0,offset))

    def handleEvents(self, events):
        for event in events:    
            if event.type == pygame.KEYDOWN:
                if(not len(self.entryList) <= 1):              
                    self.preview_final = None

                if event.key == Keys.DINGOO_BUTTON_UP:
                    if(not len(self.entryList) <= 1):
                        self.up()
                        self.onChange()
                        RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_DOWN:
                    if(not len(self.entryList) <= 1):   
                        self.down()
                        self.onChange()
                        RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_L:
                    self.up(self.maxListEntries)
                    self.onChange()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_R:
                    self.down(self.maxListEntries)
                    self.onChange()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_A:
                    self.onSelect()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_B:
                    self.onExit()
                    RenderControl.setDirty()
                if event.key == Keys.DINGOO_BUTTON_Y:
                    self.previewEnabled = not self.previewEnabled
                    RenderControl.setDirty()
            if event.type == pygame.KEYUP:
               self.preview_final = self.previewPath
               RenderControl.setDirty()

    def onSelect(self):
        pass
    
    def onExit(self):
        pass

    def onChange(self):
        if(len(self.entryList) <= 1):
            return

        pass

    def renderEntry(self, index, yOffset):
        pass
   

    def renderEntries(self, screen):
        max = 0
        if(len(self.entryList) >  self.maxListEntries ):
            max = self.maxListEntries
        else:
            max = len(self.entryList)

        for i in range(0, max):
            self.renderEntry(screen, i + self.currentWrap, i * self.listEntryHeight + self.headerHeight)

        
    def up(self, count=1):
        self.currentIndex -= count
        if(self.currentIndex  < 0):
            self.currentIndex = 0
        
        if(self.currentIndex  <= self.currentWrap):
            self.currentWrap -= count
        
        if(self.currentWrap < 0 or len(self.entryList) < self.maxListEntries):
            self.currentWrap = 0
    
    def down(self, count=1):
        self.currentIndex += count
        if(self.currentIndex > len(self.entryList) - 1 ):
            self.currentIndex = len(self.entryList) - 1

        if(self.currentIndex >= self.maxListEntries + self.currentWrap):
            self.currentWrap += count

        if(self.currentWrap > len(self.entryList) - self.maxListEntries):
            self.currentWrap = len(self.entryList) - self.maxListEntries   
        
        if(len(self.entryList) < self.maxListEntries):
            self.currentWrap = 0

    def initBackground(self):       
        if("background" in self.options):
            self.background = Common.loadImage(self.options["background"])
            surface =  pygame.Surface((self.config["screenWidth"],self.config["screenHeight"]), pygame.SRCALPHA)
            surface.fill(self.backgroundColor)
            self.background.blit(surface, (0,0))          
        else:
            self.background = pygame.Surface((self.config["screenWidth"],self.config["screenHeight"]))
            self.background.fill(self.backgroundColor)

        for i in range(0, self.maxListEntries):
            y = i * self.listEntryHeight + self.headerHeight
            pygame.draw.line(self.background, (105,105,105), (0, y), (self.config["screenWidth"], y), 1)

    def initHeader(self):
        self.header = pygame.Surface((self.config["screenWidth"], self.headerHeight), pygame.SRCALPHA)
        self.header.fill(Configuration.toColor(self.theme["header"]["color"]))
        self.titleText = self.titleFont.render(self.title, True,self.textColor)
        self.header.blit(self.titleText, (4, (self.headerHeight - self.titleText.get_height()) / 2))
   
    def initSelection(self):
        self.selection = pygame.Surface((self.config["screenWidth"],self.listEntryHeight),pygame.SRCALPHA)
        self.selection.fill((255,255,255, 160))

    def setFooter(self, footer):
        self.footer = footer
        self.listHeight = self.config["screenHeight"] - self.headerHeight - self.footer.getHeight()
        self.listEntryHeight = int(self.listHeight / self.maxListEntries)

    def __init__(self, screen, titel, options):
        self.screen = screen           
       
        self.title = titel
        self.options = options
        self.setFooter(Footer.Footer([],[],(255,255,255)))

        self.previewBoxSize = int(self.config["screenWidth"] * 0.5)
        if(self.previewBoxSize > 200):
            self.previewBoxSize = 200
       

        if("textColor" in self.options):
            self.textColor = options["textColor"]
        else:
            self.textColor = (0,0,0)
        
        if("backgroundColor" in self.options):
            self.backgroundColor = options["backgroundColor"]
        else:
            self.backgroundColor = (255,255,255, 160)
               
        self.initBackground()
        self.initHeader()   
        self.initSelection()

       