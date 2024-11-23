# Ground Control UI v2
## About
This is a Ground Control UI for model rockets. It's a more bare-bones version of my older Ground Control UI that can be found [here.](https://github.com/abhignay/GroundControlUI)

This UI displays and updates basic telemetry data sent from your rocket in real time.

The front end for the UI is written in Python with the PyQt5 library. Unlike the original Ground Control UI, this version omits the rapidly updating graphs and cuts down on the amount of data displayed.

You will need to install the following Python libraries:-

1) PyQt5
2) Python DateTime
3) PySerial


![Untitled](https://github.com/abhignay/GroundControlUI-v2/assets/74813604/71295d41-f721-47f7-a188-38b806d96108)

## Code Explanation

The GUI class has all the functions that create the main GUI window, create the boxes that display data, and update it with telemetry data. The def __init__(): function creates and starts QTimer and runs the window setup function. The window_setup(): function creates the GUI window and runs all the other functions. Your telemetry packet should follow the order mentioned on [line 290.](https://github.com/abhignay/GroundControlUI-v2/blob/0521ad3339be119e323aca8ab638086a2fe2d8f6/GCS-v2.py#L290)

## Sending Commands

The Command Vehicle section of the GCS can be set up to do whatever you want. Fire parachutes, change your flight computer's state, offset sensors, etc. For my rockets, I need my GCS to send commands to power on or off the cameras, fire pyros, and change the vehicle's state, so that is what it is set up to do. 

Basically how it works is that when the button is clicked a hex value is printed to serial, the ground control hardware will read the received bytes, and after that, you can use an `if-else` statement to operate diferent vehicle sub-systems based on the bytes received, i.e. the buttons pressed. 

Here's an example of how I have done it:-

```c++
if (Serial.available()) {
    char data = Serial.read();

    // turn cameras ON
    if (data == 0xAB){
      cameraState = 1; // or any another value
      Transciever.write(cameraState); // this is dependent on how your telemetry is set up
    }
}

```


## A couple of other things

I've only tested this GUI on Windows 11, so let me know if you have any problems using it with other platforms (Mac and Linux)

If you're using the UI on a laptop and see that all the text is overlapping try changing your display scale to 100% (Windows Specifically).

Feel free to open up an issue if you have any questions, comments, or feedback.

## License

Code in this repository is licensed under the terms of the MIT license.
