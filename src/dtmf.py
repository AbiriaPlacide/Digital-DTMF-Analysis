"""
    year: 2020
    Abiria Placide, 21
"""
from scipy.signal import freqz
from scipy.signal import spectrogram
import sys
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt

def plotSpectrogram(data,fs):
    ###spectrogram
    ft, t, Sxx = spectrogram(data, fs)
    plt.pcolormesh(t, ft, Sxx)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()

def plotFreqResponse(freqData,fs):

    for i in freqData:
        temp = np.copy(i)
        x,y = freqz(temp,1)
        scalar = int(4000/(max(x))) #used to scale to 4k values 
        plt.plot(x*scalar,abs(y))
    plt.title("Frequency Response of Bandpass Filters")
    plt.xlabel("Hertz")
    plt.show()


def processTones(name, L, fs, samplesPerTone) :
    #### read csv file ####
    data = genfromtxt(name,delimiter=',')

    ###plot 1
    plotSpectrogram(data,fs)

    splits = data.size/samplesPerTone 
    data = np.split(data,splits) #get number of splits which is 4000 per tone

    #filter Coefficients
    filterBank = [697,770,852,941,1209,1336,1477]
    filterCoef = np.arange(0,L-1,1)
    filterResponse = np.array([]) #place holder for filter coefficients

    #create filters for all 7 frequencies
    for fb in filterBank:
        temp = np.array([])
        for n in filterCoef:
            num = 2*np.pi*fb*n
            res = (2/L)*np.cos(num/fs)
            temp = np.append(temp, res)
        
        #fill out first row due to dimension errors
        if fb == 697:
            filterResponse = np.append(filterResponse,temp) 
            temp = np.array([])
        else:
            filterResponse = np.vstack((filterResponse,temp))
            temp = np.array([])
    
    ###plot freq response of each filter

    plotFreqResponse(filterResponse,fs)

    #convolve each filter by each set of 4k points and find the mean values
    meanFreqValues = np.array([]) #holder for mean frequecies

    i = 0 #counter due to dimension errors
    for sample in data:
        temp = np.array([])
        for freq in filterResponse:
            output = np.convolve(sample,freq)
            mean = np.mean(output**2)
            temp = np.append(temp,mean)
        if i == 0:
            meanFreqValues = np.append(meanFreqValues, temp)
        else:
            meanFreqValues = np.vstack((meanFreqValues,temp))
        i+=1

    ##find two highest index values and make signal
    message = ""

    Dict = {1906: "1", 2033: "2", 2174: "3", 1979: "4", 2106: "5", 2247: "6",
            2061: "7", 2188: "8", 2329: "9", 2150: "*", 2277: "0", 2418: "#"} 

    if meanFreqValues.size > 7:

        for i in meanFreqValues:
            index = np.argmax(i) #fist max value
            i[index] = -1
            index2 = np.argmax(i) #second max value
            i[index2] = -1

            signalTone = filterBank[index] + filterBank[index2]
            message+= Dict[signalTone]
    else:
            index = np.argmax(meanFreqValues) #fist max value
            meanFreqValues[index] = -1
            index2= np.argmax(meanFreqValues) #second max value
            meanFreqValues[index2] = -1

            signalTone = filterBank[index] + filterBank[index2] #add the two frequencies
            message+= Dict[signalTone]


    return (message) 

#############  main  #############
if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = str(sys.argv[1])

    else: 
        filename = "tones-7481414.csv"  #  name of file to process

    L = 64                  #  filter length
    fs = 8000               #  sampling rate
    samplesPerTone = 4000   #  4000 samples per tone, 
                            #    NOT the total number of samples per signal

    # returns string of telephone buttons corresponding to tones
    phoneNumber = processTones(filename, L, fs, samplesPerTone)
    print(phoneNumber)

