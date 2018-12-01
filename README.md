# Eye tracking via laptop camera

I want my laptop to know on which monitor I am looking at: external or built in.

First step is to distinguish between 2 monitors, second is to track eyesight.

Data for monitors is from active window: xdtools, xprop adn xrandr.

Data for eyesight is from mouse cursor when it's moving. 

# Approach

1. Use Haar-cascade from opencv to detect face and then eyes while working.
2. Save images together with active monitor.
3. Train a neural network.
4. ?????
6. PROFIT!!!

0. Track mouse position. If it's moving do the following.
1. Use Haar-cascade from opencv to detect face and then eyes while working.
2. Save images together with cursor position.
3. Train a neural network regression.
4. ?????
5. PROFIT!!!
