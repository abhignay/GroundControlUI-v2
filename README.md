# Ground Control UI v2
## About
This is a Ground Control UI for model rockets. It's a more bare-bones version of my older Ground Control UI that can be found [here.](https://github.com/abhignay/GroundControlUI)

This UI displays and updates basic telemetry data sent from your rocket in real-time.

The front end for the UI is written in Python with the PyQt5 library (you will need to install it). Unlike the original Ground Control UI, this version omits the rapidly updating graphs and cuts down on the amount of data displayed.

![image](https://user-images.githubusercontent.com/74813604/236617546-253ac738-3dc6-46a9-ad41-3e32c2a93091.png)

## Code Explanation

The GUI class has all the functions that create the main GUI window, create the boxes that display data, and update it with telemetry data. The def __init__(): function creates and starts QTimer and runs the window setup function. The window_setup(): function creates the GUI window and runs all the other functions. Your telemetry data should follow the order mentioned on [line 290.](https://github.com/abhignay/GroundControlUI-v2/blob/0521ad3339be119e323aca8ab638086a2fe2d8f6/GCS-v2.py#L290)


## A couple of other things

I've only tested this GUI on Windows 11, so let me know if you have any problems using it with other platforms (Mac and Linux)

If you're using the UI on a laptop and see that all the text is overlapping try changing your display scale to 100% instead of 150%.

Feel free to open up an issue if you have any questions, comments, or feedback.

## License

Code in this repository is licensed under the terms of the MIT license.
