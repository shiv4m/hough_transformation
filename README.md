# hough_transformation
Implementation of Hough Transformation in python to detect lines and circles in different orientation.

Hough transform for lines is pretty straightforward algorithm. The idea here is that for every line in the image, there is a point in the Hough space. The Hough space consist of bunch of sinusoidal waves. The brightest spots in the Hough space are the lines in the image space. 

A line in the image space is calculated by y = mx + b.

A point in the Hough space is calculated by 
p = x*cos(theta) + y*sin(theta), 
where (x, y) are the coordinates of every point in the image. Theta is the angle on which the p is calculated. For every (x, y), we calculate 180 values of p, i.e. 180 different angles for each coordinate point. The theta range we defined is -90 to 90. The theta is always in radians and not in degrees.

After calculating each value of p we need to save this value in a space called as accumulator or a (p, theta) space. To save this value into the (p, theta) space, we need to do the voting. The voting is conducted to see what points in the Hough space are stronger (or the brightest). 

Algorithm to calculate the Hough space – 

	
for all (x, y) of nonzero values in image:
	for all theta from -90 to +90:
		p = x * cos(radians(theta)) + y * sin(radians(theta))
		accumulator [p, theta] = accumulator [p, theta] + 1 //Voting

Now, once we have the (p, theta) space, we have set a threshold on the space and choose the values greater than the threshold with their corresponding angles (theta values). We then filter out the (p, theta) combination to get the results. The filtered out (p, theta) combination is then used to draw the line on the original image. 
