# collision_avoidance
This repo contains the code I came across while researching on collision avoidance. 


Firsly I came across a pretty cool algorithm but realised that it was specific to drones. As it depended on free movment of robots in any direction.    
In my case, however, the robots are warehouse robots which have restricted movement, restricted upto the instructed path.  
So ultimately, I had to scrape that algorithm and totally devise something of my own.  
It required 1 month but I made a good rnough system for collision avoidance using simple concepts of geometry and multiple conditions condensed into two statements. It is not possible to condense it in a readme as the actual documentation is of many pages.  
  
Anyhow, I decided that it would be best to just show the output:
  
## collision-avoidance-final
My Traffic Manager works on the principal of pausing one robot before intersection, the distance at which it is paused is called 'collision circle'.  
![image](https://github.com/gkushalg01/collision_avoidance/assets/57442239/5d502092-f27a-434b-82dd-6702d018556e)
  
Here you can fidget with this concept - the yellow/red circle is the collision circle - try to move only the head of the robots. [https://www.geogebra.org/geometry/cdg6jcz9](https://www.geogebra.org/geometry/cdg6jcz9)  
  
I have also created a rosbag file of my creation, so that you can see it on your device at runtime - [https://github.com/gkushalg01/collision_avoidance/blob/main/gold-filtered.bag](https://github.com/gkushalg01/collision_avoidance/blob/main/gold-filtered.bag)  
Just a simple ```rosbag play gold-filtered.bag``` is sufficient to run this.  
  
You can view the above rosbag in rviz using command ```rviz -d botjobtracker.rviz``` - [https://github.com/gkushalg01/collision_avoidance/blob/main/botjobtracker.rviz](https://github.com/gkushalg01/collision_avoidance/blob/main/botjobtracker.rviz)  
  
Color Index:  
Collision Circle will be in White Color  
Red circle is the rotational radius only if bot rotates at target, nothing otherwise  
Green point is the Target  
Blue point is the Pose of robot  
Yellow Square is collision point  
Green Rectangle is the robot's current trajectory  
Purple Square is the point where Paused signal was sent  
Robot IDs are shown near their current pose  
It also shows live "MOVING" or "PAUSED" status  
  
  
  
If you are too lazy/busy, here is a video for quick reference -  
This video contains realtime mobile robot data which are moving and pausing as per traffic manager.  
You can also see when exactly the PAUSE/RESUME signal is sent on topic ```/report/trafficmanager```  
  
https://github.com/gkushalg01/collision_avoidance/assets/57442239/ba8cba74-125c-4645-af7d-e5f98725dbdc
  
  
## collision-avoidance-original
This program is based on drones which have free movement in 2D space.  
The solid red dot is trying to consume the empty red dot while 4 empty white dots are chasing the solid red dot.  
The background contains 64 more dots.  
All the dots are avoiding collsion from each other.  

https://github.com/gkushalg01/collision_avoidance/assets/57442239/423b739d-f03c-4ffc-96d0-09c9ca7e43b2  




## collision-predictor
This program is taking all the dots (red or white doesn't matter) and predicting the time to collision with any other dot.  

https://github.com/gkushalg01/collision_avoidance/assets/57442239/cb1cd5bb-8610-4113-baea-c5768e171ee5  

## snowflake
This has nothing to do with collision avoidance or prediction, I just liked it, found it while searching.  

https://github.com/gkushalg01/collision_avoidance/assets/57442239/2af56d33-b831-4f2b-ba61-ff29f0df5c29  








