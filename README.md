# FBS-Auto-Booker
A program to help automate the booking of facilities in the Facility Booking System (FBS).

## Demos

### Demo 1
![](assets/demo.gif)

### Demo 2
![](assets/demo2.gif)

## Usage guide
1. Download and run the latest .exe from [releases](https://github.com/Alwyn-Ong/FBS-Auto-Booker/releases).
    1. Alternatively, you can also run the script using the deployment guide above.
    2. Running the .exe will take some time to startup as it is installing the dependencies into a cache in your computer
2. For first time use, follow the instructions to create a `userpw.txt` and a `details.txt`. 
    * The files will be created in the same directory as the .exe/.py file.
    * `userpw.txt` is used to store your credentials for login. It is saved on same directory as the .exe.
        * The file structure is as follows:
            * username=x.2020@x.smu.edu.sg
            * password=123
    * `details.txt` is used to store the details of the booking.
        * The file structure is as follows:
            * preference= numbers, based on school (e.g. 3210)
            * date=DD-MMM-YYYY (e.g. 16-Dec-2020)
            * start_time=HH:MM (e.g. 13:00)
            * end_time=HH:MM (e.g. 16:00)
            * co_booker=name (be as specific as possible. e.g. Alwyn Ong)

    * If the files already exist, you can simply edit the files to make a new booking.


3. Enter 0/1 to select either GSR booking or Project Room booking.
4. The program will search through the schools to find a booking, based on the order of preference in `details.txt`.
5. If a room is found:
    * The details for the confirmation will be filled in, with the reason as "meeting". 
    * You will need to manually click accept to accept the booking.
6. If no room is found:
    * The program will list out the next longest durations within the time duration you specify.
    * You can select the number beside the alternatives to book that room in the specified time.
    * The program will then continue to book the room as per step 5.

## Deployment Guide
1. `git-clone` the repo to your local directory
2. Run `activate.bat` to run the virtual environment
3. Run `FBS Auto Booker vX.X.py` to run the script. The version may be subject to change.

## Compiling Guide
1. Run `activate.bat` to run the virtual environment
2. In the cmd prompt opened, run `compile.bat` to compile the executable file.
3. The file generated should be in `./dist/FBS Auto Booker vX.X/`

