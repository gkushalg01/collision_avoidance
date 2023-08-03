# collision_avoidance
This repo contains the code I came across while researching on collision avoidance. 


Firsly I camer acrros a pretty cool algorithm but realised that it was specific to drones. As it depended on free movment of robots in any direction.    
In my case, however, the robots are warehouse robots which have restricted movement, restricted upto the instructed path.  
So ultimately, I had to scrape that algorithm and totally devise something of my own.  
It required 1 month but I made a good rnough system for collision avoidance using simple concepts of geometry and multiple conditions condensed into two statements. It is not possible to condense it in a readme as the actual documentation is of many pages.  

Anyhow, I decided that it would be best to just show the output:

# collision-avoidance-original
This program is based on drones which have free movement in 2D space.  
The solid red dot is trying to consume the empty red dot while 4 empty white dots are chasing the solid red dot.  
The background contains 64 more dots.  
All the dots are avoiding collsion from each other.  
