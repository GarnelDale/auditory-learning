# auditory-learning

The included dist folders and .exe files are compiled using PyInstaller on Windows 11. To create an executable for another operating system perform the following steps on your machine:  

1. Make sure you have Python 3.11 installed
2. Download the AuditoryLearning.py file as well as the control and resources files to a single filespace on your machine
3. Using the terminal, either in an IDE or stand alone, install Python Arcade using the command `pip install arcade` on Mac and Linux
4. Next, install the packager using `pip install arcade pyinstaller`
5. Open the AuditoryLearning.py file in a text editor of your choice and make sure to comment out the variables following the comment `# Constants for number of different targets` and to uncomment the variables under the comment `# Control constants`
6. Run the packager by running `PyInstaller AuditoryLearning.py --add-data "control:control"` in the terminal.
7. Once the package is made, rename the file and executable to include Control
8. Revert the changes made in step 5
9. Run the packager for the main version by running `PyInstaller AuditoryLearning.py --add-data "resources:resources"` in the terminal.
   
