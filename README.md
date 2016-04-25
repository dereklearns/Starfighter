# Starfighter
Top down scroller.
Uses pygame.
-includes use of hitbox detection, sprites to create animated graphics, and a basic targeting on AI.

#The Basics
I have the user's ship spawning and moveable with arrow keys. I have also added in enenmy ships that spawn and move down the screen. Basic collision is working and when user's ship collides, Game Over.

![The Basics](https://raw.githubusercontent.com/dadam88/Starfighter/master/Progress_Images/starship_progress_thebasics.gif)

#New Ship
I implemented a new ship, in the future I would like to have many different types of ships and so this was a big step for me using a ship class. These new ships have more health and in the future will have different projectile and movement mechanics.

![New Ship](https://raw.githubusercontent.com/dadam88/Starfighter/master/Progress_Images/starship_progress_newship.gif)

#Basic Explosions
It is not very exciting to just have a sprite/image disappear when you destory it with your ship cannon. Testing on death mechanics in the game loop and adding an image on the current position was another great leap. 

![Basic Explosions](https://raw.githubusercontent.com/dadam88/Starfighter/master/Progress_Images/starship_progress_basicexplosion.gif)

#Real Explosions and Enemies Shoot!
Our basic explosion was just a test to get images appearing, now it was time to loop through a series of images to create an explosion animation. Our eneimies now shoot bullets in a straight line and thus we have a working game, yay!

![Real Explosions](https://raw.githubusercontent.com/dadam88/Starfighter/master/Progress_Images/starship_progress_realexplosions.gif)

#Testing Pixel-to-Pixel Collision
The most basic way to test for collisions is using rectangles, our ship is displayed with a transparaent background but it is still a rectangle. This means that if you dodged a bullet on the screen and the bullet still hits the edge of the transparent rectangle, you will explode. This was simply a test to make sure I understood how to implement a more complicated and demanding collision test, pixel-to-pixel. You will notice, a collision is only detected when the actual ship collides, not the transparent rectangle the ship belongs too.

![Testing Pixel-to-Pixel Collision](https://raw.githubusercontent.com/dadam88/Starfighter/master/Progress_Images/starship_progress_testpixelcolision.gif)

#Almost a Real Game
I implemented the ships targetting system to shoot their projectile at the user's ships current location. The bullets of the enemy need to rotate properly to face the direction they are shot in. You will notice I have a math error currently when the enemy ships shoot to the left. Game is already fun to play and ships just continue to spawn at random spots. I haven't implemented the Pixel-to-Pixel collision yet, but I do know how to implement it. 

![Almost a Real Game](https://raw.githubusercontent.com/dadam88/Starfighter/master/Progress_Images/starship_progress_bulletsflywrongway.gif)
