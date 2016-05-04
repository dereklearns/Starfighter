import pygame, random, math
 
#--- Global constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512

def get_distance(origin, destination):
    x = origin[0] - destination[0]
    y = origin[1] - destination[1]
    return math.sqrt(x*x + y*y)

def get_angle(origin, destination):
    """Returns angle in radians from origin to destination.
    This is the angle that you would get if the points were
    on a cartesian grid. Arguments of (0,0), (1, -1)
    return .25pi(45 deg) rather than 1.75pi(315 deg).
    """
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    # print math.atan2(-y_dist, x_dist) % (2 * math.pi)
    return math.atan2(-y_dist, x_dist) % (2 * math.pi)

def project(pos, angle, distance):
    """Returns tuple of pos projected distance at angle
    adjusted for pygame's y-axis.
    """
    return (pos[0] + (math.cos(angle) * distance),
            pos[1] - (math.sin(angle) * distance))

class Ship(pygame.sprite.Sprite):
    """ Generic Ship Class """
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.speed = 1
        self.health_points = 1
        
    def death_animation(self):
        
        explode = Explosion()

        explode.rect.x = self.rect.x + self.rect.width*.25
        explode.rect.y = self.rect.y + self.rect.height*.25

        return explode

class EnemyBasicShip(Ship):

    health_points = 3
    lazer_recharge = 200
    lazer_recharge_cooldown = 200
    speed = 1

    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
     
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        zigzag_waypoint = [[0,0],[100,100],[200,0],[300,100],[400,0],[500,100],
                            [500,200],[400,100],[300,200],[200,100],[100,100]]

        self.waypoints = iter(zigzag_waypoint)
        self.destination = next(self.waypoints)

    def shoot_bullet(self, target):
        bullet = BasicEnemyBullet()
        bullet.rect.x = self.rect.x + (self.rect.width / 2) - (bullet.rect.width /2)
        bullet.rect.y = self.rect.y + self.rect.height/2
        return bullet

    def reached_destination(self):
        return self.rect.center == (self.destination[0],self.destination[1]) 

    def move_to_next_waypoint(self):
        self.distance = get_distance(self.rect.center, self.destination)
        self.angle = get_angle(self.rect.center, self.destination)
        self.rect.center = project(self.rect.center, self.angle, min(self.distance,self.speed))

    def update(self):
       

        if self.reached_destination():
            try:
                self.destination = next(self.waypoints)

            except StopIteration:
                print "No more waypoints - moving down screen"
                self.destination = (self.rect.center[0], 700)
        

        self.move_to_next_waypoint()

        if self.rect.y >= 0:
            self.lazer_recharge -= 1

        if self.lazer_recharge < 0:
            self.lazer_recharge += self.lazer_recharge_cooldown

class SprinterShip(EnemyBasicShip):
    
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
     
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        zigzag_waypoint = list()
        zigzag_waypoint = [[0,0],[100,100],[200,0],[300,100],[400,0],[500,100],
                            [500,200],[400,100],[300,200],[200,100],[100,100]]

        self.waypoints = iter(zigzag_waypoint)
        self.destination = next(self.waypoints)

    def reached_destination(self):
            return self.rect.center == (self.destination[0],self.destination[1])
         
    def move_to_next_waypoint(self):
        self.distance = get_distance(self.rect.center, self.destination)
        self.angle = get_angle(self.rect.center, self.destination)
        self.rect.center = project(self.rect.center, self.angle, min(self.distance,self.speed))


    def update(self):
        if self.reached_destination():
            try:
                self.destination = next(self.waypoints)

            except StopIteration:
                print "No more waypoints"
                self.destination = (self.rect.center[0], 700)

        self.move_to_next_waypoint()

class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
 
    # --- Class attributes.
    # In this case, all the data we need
    # to run our game.
    player_list = None
    enemy_bullet_list = None
    explosion_list = None
    bullet_list = None
    enemy_list = None
    all_sprites_list = None
    enemy_hit_list = None
    background_image = None
    # Sprite lists
 
    # Other data
    game_over = False
    score = 0

    # --- Class methods
    # Set up the game
    def __init__(self):

        self.score = 0
        self.game_over = False

        self.background_image = pygame.image.load("Images/background.jpg").convert()

        # Create sprite lists
        self.all_sprites_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
 


    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False
 
    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over:
            # calls update on all classes
            self.all_sprites_list.update()
             
    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(WHITE)
        screen.blit(self.background_image, [0,0])
        font = pygame.font.SysFont("serif", 25)
        text = font.render("Score %s" % self.score, True, WHITE)
        screen.blit(text, [0,0])
 
        if self.game_over:
            #font = pygame.font.Font("Serif", 25)
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, SPACE to restart", True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])
 
        if not self.game_over:
            self.all_sprites_list.draw(screen)
 
        pygame.display.flip()
 
def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()
 
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("My Game")
    pygame.mouse.set_visible(False)
 
    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()
 
    # Create an instance of the Game class
    game = Game()
 
    # Main game loop
    while not done:
 
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()
 
        # Update object positions, check for collisions
        game.run_logic()
 
        # Draw the current frame
        game.display_frame(screen)
 
        # Pause for the next frame
        clock.tick(60)
 
    # Close window and exit
    pygame.quit()
 
# Call the main function, start up the game
if __name__ == "__main__":
    main()