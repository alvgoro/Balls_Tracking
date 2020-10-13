This is a short Python code using OpenCV which is able to track balls using a camera or a video input.

I followed the tutorial from PyImageSearch:
https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/

Thanks a lot *Adrian Rosebrock* for sharing us your knowledges :)

**In my code** I changed several lines to correct some issues.
- Here you **can track more than one ball**.
- If there are 2 or more balls, you need to identify each ball. OpenCV read the frame from right-bottom to left-top (I guess). It is not a problem if you don't want to track, but if you do, you need to **identify and save correctly each ball position**. I got it **using minimun distances** among balls.

**A little error in the code:**
I am not able to know the origin of the error. The paths sometimes cross over. I tried to clear the vector in which I save the positions, but it still be there. 
If anyone has any idea doesn't hesitate to contact me :). I am always open to learn hehehehe.


![alt text](https://github.com/alvgoro/balls_tracking/blob/main/frame2.png)
![alt text](https://github.com/alvgoro/balls_tracking/blob/main/mask2.png)
