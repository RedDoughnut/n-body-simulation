from planet import Planet
from vec2 import vec2
import math
import pygame
from time import sleep

pygame.init()
pygame.font.init()

def draw_arrow(surface, color, start, end, thickness=5, head_size=15):
    pygame.draw.line(surface, color, start, end, thickness)
    
    angle = math.atan2(start[1] - end[1], end[0] - start[0])
    
    left_point = (end[0] + head_size * math.cos(angle + math.radians(150)),
                  end[1] - head_size * math.sin(angle + math.radians(150)))
    right_point = (end[0] + head_size * math.cos(angle - math.radians(150)),
                   end[1] - head_size * math.sin(angle - math.radians(150)))
    
    pygame.draw.polygon(surface, color, [end, left_point, right_point])

def main():
    window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

    planetList = []#[Planet(800, 600, 1000, vec2(0,-25)), Planet(400, 600, 1000, vec2(0,25))]#, Planet(1600, 800, 100), Planet(500,800,100)]
    dt = 0
    FPSfont = pygame.font.SysFont("Arial", 16)
    font = pygame.font.SysFont("Arial", 30)
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
        window.fill((0,0,0))
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
                    curEnteringMass = False
                    curSettingVector = True
            if event.type==pygame.KEYDOWN and event.key == pygame.K_q and curSettingVector:
                curVel = vec2(0,0)
                planet = Planet(clickx, clicky, curMass, curVel)
                curMass = 0
                planetList.pop()
                planetList.append(planet) 
                curSettingVector = False

        if curEnteringMass:
            text_surface = font.render(f"Unesi masu: {curMass} * 10^15kg", True, (255,0,0))
            width, height = text_surface.get_size()
            window.blit(text_surface, (700 - width // 2, 50 - height // 2))
            text_surface = font.render("Pristini ENTER kad si gotov", True, (255,0,0))
            width, height = text_surface.get_size()
            window.blit(text_surface, (700 - width // 2, 80 - height // 2))
        if curSettingVector:
            text_surface = font.render("Podesi vektor pocetne brzine", True, (255,0,0))
            width, height = text_surface.get_size()
            window.blit(text_surface, (700 - width // 2, 50 - height // 2))
            text_surface = font.render("Pritisni Q da stavis pocetnu brzinu na 0", True, (255,0,0))
            width, height = text_surface.get_size()
            window.blit(text_surface, (700 - width // 2, 80 - height // 2))
            pos = pygame.mouse.get_pos()
            draw_arrow(window, (255,0,0), (clickx, clicky), pos)
        if buildMode:
            text_surface = font.render(f"KLIKNI NA EKRAN DA BI DODAO TELO", True, (255,0,0))
            width, height = text_surface.get_size()
            window.blit(text_surface, (700 - width // 2, 770 - height // 2))
            text_surface = font.render(f"PRITISNI SPACE DA BI POKRENUO SIMULACIJU", True, (255,0,0))
            width, height = text_surface.get_size()
            window.blit(text_surface, (700 - width // 2, 800 - height // 2))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                buildMode = False
            for planet in planetList:
                planet.update(window)
            clock.tick(FPS)
            continue
        dt = clock.tick(FPS) / 1000.0
        curFPS = 1.0 / dt
        text_surface = FPSfont.render(f"{round(curFPS,2)}FPS", True, (255,0,0))
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
