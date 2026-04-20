from planet import Planet
from vec2 import vec2
import math
import pygame
import copy
import numpy

pygame.init()
pygame.font.init()


info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

def invert(surface):
    surf = surface.copy()
    rgb = pygame.surfarray.pixels3d(surf)
    alpha = pygame.surfarray.pixels_alpha(surf)
    rgb ^= 255
    del rgb
    del alpha
    return surf

def load_icon(path, size=32):
    icon = pygame.image.load(path).convert_alpha()
    return icon
def draw_arrow(surface, color, start, end, thickness=5, head_size=15):
    pygame.draw.line(surface, color, start, end, thickness)
    
    angle = math.atan2(start[1] - end[1], end[0] - start[0])
    
    tip = (end[0] + head_size * math.cos(angle),
           end[1] - head_size * math.sin(angle))
    
    left_point = (end[0] + head_size * math.cos(angle + math.radians(150)),
                  end[1] - head_size * math.sin(angle + math.radians(150)))
    right_point = (end[0] + head_size * math.cos(angle - math.radians(150)),
                   end[1] - head_size * math.sin(angle - math.radians(150)))
    
    pygame.draw.polygon(surface, color, [tip, left_point, right_point])
def draw_icons(window: pygame.Surface, leftclick, rightclick, add, trash, reset, rbut):
    padding = 10
    margin = 20
    gap = 5
    icon_size = 32

    pairs = [
        (leftclick, add),
        (rightclick, trash),
        (rbut, reset),
    ]

    for i, (icon1, icon2) in enumerate(pairs):
        x = margin
        y = HEIGHT - margin - (len(pairs) - i) * (icon_size + padding)
        window.blit(icon1, (x, y))
        window.blit(icon2, (x + icon_size + gap, y))
def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    planetList = []#[Planet(800, 600, 1000, vec2(0,-25)), Planet(400, 600, 1000, vec2(0,25))]#, Planet(1600, 800, 100), Planet(500,800,100)]
    originalPlanets = planetList
    dt = 0
    FPSfont = pygame.font.SysFont("Arial", 16)
    font = pygame.font.SysFont("Arial", 30)
    
    bg_image = pygame.image.load("background.jpg").convert()
    rightclick = invert(load_icon("icons/rightclick.png"))
    leftclick = invert(load_icon("icons/leftclick.png"))
    add = invert(load_icon("icons/add.png"))
    reset = invert(load_icon("icons/reset.png"))
    trash = invert(load_icon("icons/trash.png"))
    rbut = invert(load_icon("icons/r.png"))

    FPS = 120
    clock = pygame.time.Clock()
    running = True
    buildMode = True
    curEnteringMass = False
    curSettingVector = False
    curMass = 0
    curVel = vec2(0,0)
    clickx = 0
    clicky = 0
    while running:
        pygame.display.update()
        window.blit(bg_image, (0,0))
        # text_surface = FPSfont.render(f"PRITISNI R DA RESTARTUJES", True, (255,0,0))
        # width, height = text_surface.get_size()
        # window.blit(text_surface, (700 - width // 2, 850 - height // 2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and buildMode:
                    if not curEnteringMass and not curSettingVector:
                        curEnteringMass = True
                        clickx, clicky = event.pos
                        planetList.append(Planet(clickx, clicky, 1))
                    elif curSettingVector:
                        end = pygame.mouse.get_pos()
                        curVel = vec2((end[0] - clickx)/2, (end[1] - clicky)/2)
                        planet = Planet(clickx, clicky, curMass, curVel)
                        curVel = vec2(0,0)
                        curMass = 0
                        planetList.pop()
                        planetList.append(planet) 
                        curSettingVector = False
                if event.button == 3 and buildMode and not curSettingVector and not curEnteringMass:
                    click = pygame.mouse.get_pos()
                    for planet in planetList:
                        dist = math.sqrt((click[0] - planet.pos.x)**2 + (click[1] - planet.pos.y)**2)
                        if dist < planet.radius:
                            planetList.remove(planet)
                            break
            if curEnteringMass:
                if event.type != pygame.KEYDOWN:
                    continue
                if event.key == pygame.K_1:
                    curMass = int(str(curMass) + '1')
                elif event.key == pygame.K_2:
                    curMass = int(str(curMass) + '2')
                elif event.key == pygame.K_3:
                    curMass = int(str(curMass) + '3')
                elif event.key == pygame.K_4:
                    curMass = int(str(curMass) + '4')
                elif event.key == pygame.K_5:
                    curMass = int(str(curMass) + '5')
                elif event.key == pygame.K_6:
                    curMass = int(str(curMass) + '6')
                elif event.key == pygame.K_7:
                    curMass = int(str(curMass) + '7')
                elif event.key == pygame.K_8:
                    curMass = int(str(curMass) + '8')
                elif event.key == pygame.K_9:
                    curMass = int(str(curMass) + '9')
                elif event.key == pygame.K_0:
                    curMass = int(str(curMass) + '0')
                elif event.key == pygame.K_BACKSPACE:
                    try:
                        curMass = int(str(curMass)[:-1])
                    except ValueError:
                        curMass = 0
                if event.key == pygame.K_RETURN:
                    if curMass != 0:
                        curEnteringMass = False
                        curSettingVector = True
            if event.type==pygame.KEYDOWN and event.key == pygame.K_q and curSettingVector:
                curVel = vec2(0,0)
                planet = Planet(clickx, clicky, curMass, curVel)
                curMass = 0
                planetList.pop()
                planetList.append(planet) 
                curSettingVector = False
            if event.type==pygame.KEYDOWN and event.key == pygame.K_r:
                buildMode = True
                curEnteringMass = False
                curSettingVector = False
                curMass = 0
                planetList = copy.deepcopy(originalPlanets)
                curVel = vec2(0,0)
                clickx = 0
                clicky = 0
        if curEnteringMass:
            text_surface = font.render(f"Unesi masu: {curMass}×10¹⁵kg", True, (255,0,0))
            width, height = text_surface.get_size()
            window.blit(text_surface, (WIDTH//2 - width // 2, 0.06 * HEIGHT - height // 2))
            text_surface = font.render("Pristini ENTER kad si gotov", True, (255,0,0))
            width, height = text_surface.get_size()
            window.blit(text_surface, (WIDTH//2 - width // 2, 0.06 * HEIGHT + 30 - height // 2))
        if curSettingVector:
            text_surface = font.render("Podesi vektor pocetne brzine", True, (255,0,0))
            width, height = text_surface.get_size()
            window.blit(text_surface, (WIDTH//2 - width // 2, 0.06 * HEIGHT - height // 2))
            text_surface = font.render("Pritisni Q da stavis pocetnu brzinu na 0", True, (255,0,0))
            width, height = text_surface.get_size()
            window.blit(text_surface, (WIDTH//2 - width // 2, 0.06 * HEIGHT + 30 - height // 2))
            pos = pygame.mouse.get_pos()
            draw_arrow(window, (255,0,0), (clickx, clicky), pos)
        if buildMode:
            draw_icons(window, leftclick, rightclick, add, trash, reset, rbut)
            # text_surface = font.render(f"KLIKNI NA EKRAN DA BI DODAO TELO", True, (255,0,0))
            # width, height = text_surface.get_size()
            # window.blit(text_surface, (WIDTH//2 - width // 2, 0.88 * HEIGHT - 60 - height // 2))
            text_surface = font.render(f"Pritisni SPACE da bi pokrenuo simulaciju", True, (255,0,0))
            width, height = text_surface.get_size()
            window.blit(text_surface, (WIDTH//2 - width // 2, 0.88 * HEIGHT - height // 2))
            # text_surface = font.render(f"DESNI KLIK NA TELO DA BI GA OBRISAO", True, (255,0,0))
            # width, height = text_surface.get_size()
            # window.blit(text_surface, (WIDTH//2 - width // 2, 0.88 * HEIGHT - 30 - height // 2))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                buildMode = False
                originalPlanets = copy.deepcopy(planetList)
            for planet in planetList:
                planet.update(window)
            clock.tick(FPS)
            continue
        dt = clock.tick(FPS) / 1000.0
        curFPS = 1.0 / dt
        text_surface = FPSfont.render(f"{round(curFPS)}FPS", True, (255,0,0))
        window.blit(text_surface, (5,5))
        for i, planet1 in enumerate(planetList):
            totalForce = vec2(0,0)
            for j, planet2 in enumerate(planetList):
                if i==j:
                    continue
                totalForce = totalForce + planet1.compare(planet2)
            planet1.vel = planet1.vel + (totalForce / planet1.mass) * dt
            planet1.pos = planet1.pos + planet1.vel * dt
            planet1.update(window)
        pygame.display.update()
    pygame.quit()
if __name__=="__main__":
    main()
