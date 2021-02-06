# Digital-DTMF-Analysis
Uses Signal Processing techniques to determine numbers given DTMF keypad frequencies given in a csv file. Libraries Used: Numpy, Matplotlib, Scipy

### What it does
  - analyzes a given tone in a csv file of floats between +2 and -2. The resulting frequency is cross referenced to a given number. 
  - A Windowing filter is applyed then data is normalized. 
  
### How to run (linux)
  - sudo apt-get install Python3.x matplotlib, numpy, scipy
  - run -> python3 dtmf.py [filename.csv]
  
 ### Frequency Response
 ![alt text](https://github.com/AbiriaPlacide/Digital-DTMF-Analysis/blob/main/images/freqResponse.png)
 
 ### Spectrogram
 ![alt text](https://github.com/AbiriaPlacide/Digital-DTMF-Analysis/blob/main/images/spectrogram.png)
 
