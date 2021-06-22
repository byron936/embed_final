# embed_final
Let the BBcar go thrpugh a line. At the end of the line, there are three Apriltags. One is just on the extension of the line, and the other two are on the left and right of the line.  
We can use these Apriltags to check if our line detection is perfect. If we detect the middle of the Apriltag, we send a messenge "great!" by XBee. If we detect the left of the Apriltag, we send a messenge "too left!" by XBee. If we detect the right Apriltag, we send a messenge "too right!" by XBee.  
Use the following command to compile the code

    sudo mbed compile --source . --source ~/ee2405/mbed-os-build/ -m B_L4S5I_IOT01A -t GCC_ARM -f

