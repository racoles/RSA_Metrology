# RSA_Metrology
## LSST Metrology for RSAs
This program simulates the absolute height of RSAs (Raft Sensor Assembly) measured at TS2 with the OGP machine. Put simply, you would use this program to simulate the height of nine sensors sitting on top of their baseplate.

## Input Data Requirements
### LSST CCD Sensors
You will need absolute hight measurements for each of the nine sensors that you plan use on your RSA. The OGP output files will be of the type ".xlsx" with a file name that looks something like: "E2V-239_AbsZ_20170307-13H11M_run1_ABSZ_CCD_data.xlsx". The contents of the file should look like:

```
E2V-239_AbsZ_20170307-13H11M_run1	Wed 8 Mar 2017 10:00:42	{"X(mm)", "Y(mm)", "Z(micron)"}
0.487862	0.490007	-1.7518159596
1.463572	0.489664	-1.7678105472
2.579398	0.484861	-1.8851661102
3.675131	0.477293	-1.6058965777
4.545258	0.47152	        -1.8731041048
5.512888	0.464853	-2.1436831095
6.578916	0.458489	-1.3355275472
....
```

### Raft Baseplate 
The program has optional text boxes to enter Raft baseplate data. If all you want is to see the flatness of nine sensors relative to each other, then you can leave these text boxes empty. If you want to simulate the flatness of the sensors when installed on a Raft baseplate, then you will need to fill in the text boxes with the relevant baseplate analysis results. The "Datum Plane Equation" and "Raft Fit Equation" are generated using the Raft Baseplate Mathematica Analysis Routine (created by Peter Takacs). This routine analyzes Raft baseplate measurements taken with the OGP using Peter's OGP measurement routines. The file that contains the equations that you will need is usually named something like: "ECM-018_AbsZ_170214_run1_M6_1.36_Zhgts_summary.txt" and contains data that looks like:

```
ECM-018_AbsZ_170214_run1_M6_1.36
Mean raft height = 	29.7932
 Datum plane eqn
53.0234 + 0.0010629 x + 0.00322188 y
 Raft fit eqn:
82.8247 + 0.00104857 x + 0.00319674 y
 PV AbsZ stats
PV100= 	6.90133
PV99 = 	6.58251
PV95 = 	4.7876
 Raft Abs height above ball centers
LL ball = 	29.7935
LR ball = 	29.7913
UC ball = 	29.794
```

## Downloading and Running RSA_Metrology

You don't need to *install* RSA_Metrology, but there are multiple ways to run the program.

### Python

If you know that you have Python 3 installed on your system as well as the typical math packages like: numpy, matplotlib, scipy, and tkinter, then you can just download the "source_code" file and run RSA_Metrology using the command:

```python3 main.py```

If you don't have Python installed on your system, you can download it [here](https://www.python.org/downloads/). You can then use "pip" to install all the extra dependencies. The pip Python file can be downloaded [here](https://bootstrap.pypa.io/get-pip.py), and installed with the command:

```python3 get-pip.py```

With pip, you can download and install the needed dependencies using the following commands:

```
pip3 install numpy
pip3 install matplotlib
pip3 install scipy
pip3 install openpyxl
pip3 install ntpath
```

### Linux (Stand Alone Program Version)

If you don't have Python 3 installed on your Linux system, or are otherwise having difficulty getting RSA_Metrology to run using your Python 3 installation, you can download the RSA_Metrology_Linux folder and run RSA_Metrology using the command:

```./rsa```

Warning: the RSA_Metrology_Linux folder is bulky. This is because Python itself is an interpretive language, and so the stand alone program includes the Python interpreter and all the imported modules needed for the program to run. It will save your bandwidth and hard drive space to use source_code version of RSA_Metrology mentioned in the [Python](#python) subsection.

## Using RSA_Metrology

To create a RSA simulation using RSA_Metrology:

1. In the "Load Sensor Metrology Files" section of the RSA_Metrology GUI, click the colored buttons to place the OGP measured sensor data (.xlsx file) in the locations that you plan to put the sensors on the RSA. *RSA_Metrology requires all nine sensor position to be filled to create a simulation*. The sensors are laid out using the machine coordinate system (MCS) setup by the OGP. The button labels show the S## RSA sensor locations as designated in the LSST document LCA-13381.

⋅⋅⋅Note: Sensor data from the OGP is measured in part coordinate system (PCS). RSA_Metrology automatically preforms the appropriate coordinate transform of all the sensors to MCS.

2. (Optional) Enter the Raft plane equations in the appropriate text boxes if you want to see the absolute height of the sensors on a given Raft baseplate. If all you want is to see the flatness of nine sensors relative to each other, then you can leave these text boxes empty. More information on where to find these equations can be found in the [Raft Baseplate](#raft-baseplate) subsection.

3. Click the "Plot virtual RSA for manually selected sensor positions" button in the "Process and Plot Data" section of the GUI.

4. Two windows will emerge showing the absolute height of the sensors as a 3D plot and a contour map. The 3D projection can be rotated as needed to see the RSA at different angles, and both can be saved using the save button found in the menu bar at the top of the image. The camera coordinate system Raft baseplate labels, that are printed on the Raft baseplate, are shown on both plots: +Y, -Y, +X, -X.

...Note: To reduce processing time, the 3D plot will only show every tenth measured point. An output file containing all the measured points in the simulation will be saved to the RSA_Metrology program directory. More information about this file can be found in the [Output Results File](#output-results-file) subsection.

## Output Results File

Upon a successful creation of an RSA simulation, an output file containing relevant simulation data will be saved to the RSA_Metrology program directory. The file name will include a data and time stamp and will look something like: "20170809-101320_manually_placed_virtualRSA.csv". The coma delineated file will contain data that looks like:

```
41.0135640,41.0002590,12.9947659,6
40.0485600,41.0028700,12.9947060,6
38.9782560,41.0071810,12.9941101,6
37.9098520,41.0127930,12.9940603,6
37.0888500,41.0178040,12.9948480,6
36.1328450,41.0235130,12.9941576,6
35.0804410,41.0299250,12.9940010,6
33.9447370,41.0367380,12.9938922,6
32.7047330,41.0450510,12.9936395,6
32.0779380,41.0487550,12.9935327,6
30.7811480,41.0562630,12.9936839,6
30.1098540,41.0604670,12.9935797,6
...
```
Where the columns are:
1. X location of the measured point in millimeters.
2. Y location of the measured point in millimeters.
3. Z height of the measured point in millimeters. If you included Raft data in your simulation, this value will include both the measured sensor height as well as the measured height of the Raft at that point.
4. Color code for sensor. This number is used by RSA_Metrology to color code the points for the 3D RSA plot. The following table shows the color code for all of sensor positions:

| Color Number | 3D Plot Color | LSST RSA Sensor Location Designator |
| -------------|---------------| ------------------------------------|
| 0            | white         | S00                                 |
| 1            | purple        | S01                                 |
| 2            | yellow        | S02                                 |
| 3            | cyan          | S10                                 |
| 4            | blue          | S11                                 |
| 5            | orange        | S12                                 |
| 6            | magenta       | S20                                 |
| 7            | green         | S21                                 |
| 8            | red           | S22                                 |

⋅⋅⋅More information on the LSST RSA sensor location designators can be found in the LSST document LCA-13381.

## Troubleshooting

#### I can't open the program (or the program crashes immediately upon opening)

If you are running the source code via Python 3, this usually means that you are missing a dependency, or the needed module wasn't installed correctly. The console output should give you some hint as to what you are missing. If the problem persists, even with a functioning install of python three and the needed dependences, you could always give the stand alone program version (described in the [Downloading and Running RSA_Metrology](#downloading-and-running-rsa_metrology) section) a shot.

#### My xlsx files won't load (or crashes the program)

If you are having difficulty loading the sensor xlsx files, it's worth trying to open them in your spreadsheet editor of choice and saving over the file (you don't need to make any changes to the actual data). Ofter times this is all that is needed to fix the issue.

#### The simulation doesn't complete (or crashes the program)

First, make sure that you filled in all nine sensor locations with your desired xlsx sensor metrology files. Most of the time, this issue occurs when a sensor position is left empty. If you are sure that all sensor positions were filled, check the content of your xlsx files. The files should only have one row of text, followed by a series of rows with three columns of data (X(mm), Y(mm), Z(micron)). If the data in your files doesn't follow this format, you may need to remeasure the sensor.

#### The resulting simulation does not look as expected

Most of the time this occurs when you have an anomaly in your data set. RSA_Metrology creates RSA simulation by:

1. Reading the user entered sensor metrology xlsx files from the OGP measurement.
2. Preforming a coordinate transform on the sensor data sets to take them from a part coordinate system (PCS) to a machine coordinate system (MCS).
3. Place the sensor data in the selected positions on the virtual RSA.
4. Subtract the Raft Baseplate from virtual RSA (if the user entered Raft baseplate equation data).
5. Generates plots of the simulated RSA.

Therefore, if your RSA simulation looks strange, it may be that your sensor data wasn't measured in PCS or was missing large sections of the sensor. If you entered Raft plane equations, the issue may be that the Raft metrology measurements were incorrect, or that the Raft metrology Mathematica analysis routine failed to properly fit a plane to the measured data.

### Contact Information

If you suspect that there is an issue with the RSA_Metrology program itself, you can can contact the author at rebecca.coles@wayne.edu
