![alt text](https://github.com/hunterl/markets/raw/master/yield_curve/september_curve.gif "September Curve Flattening")

Generates the transformation of the yield curve over a period of time. Built this so I could visualize the flattening of the curve in September. Its not quite as pretty as I'd like but does its job good enough. Also translated from a Jupyter notebook so code is a little sloppy.

Running the script will output a bunch of images to `./images`, you can then use whatever tool you like to splice them into a gif. 

On OSX I used ImageMagic and the command 
`convert -delay 5 {1..169}.png -delay 200 170.png september_curve.gif` 
which is helpful in that it adds delay of 200 to only the final frame.