import matplotlib.pyplot as plt
import numpy as np
import decimal

ctx = decimal.Context()
ctx.prec = 20

def float_to_str(f):
    """
    Convert the given float to a string,
    without resorting to scientific notation
    """
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')

def clearvars(hjd,mag,magerr,ra,dec):
    hjd.clear()
    mag.clear()
    magerr.clear
    ra.clear()
    dec.clear()
def main():
    #read in file and obtain individual lines in list
    Glines = np.loadtxt("testGaia.txt", delimiter = ',', usecols = (0,3,4,5,8,9), dtype = float)
    Oidlines = np.loadtxt("targetG.txt")
    #get each column of data
    hjd = []
    mag = []
    magerr = []
    ra = 0
    dec = 0
    j = 0
    #split data by individual oids
    for i in Oidlines:
        ind = np.where(Glines[:,0] == i)[0]
        j += 1
        print(str(j) + ":" + str(len(Oidlines)))
        hjd = Glines[ind,1]
        mag = Glines[ind,2]
        magerr = Glines[ind, 3]
        ra = Glines[ind,4]
        dec = Glines[ind,5]
        #read each plot point and determine which points if any have a stddev greater than 3 sigma
        sigmacounter = 0
        threesigcounter = 0
        sigma = 0
        meanmag = 0
        sigma = np.std(mag)
        meanmag = np.mean(mag)
        #remove outliers from the data and calculate new standard deviations (up to 5)
        for z in range(1,3):
            mcopy  = mag[np.where(Glines[ind,2] - meanmag < 3 * sigma)]
            sigma = np.std(mcopy)
            meanmag = np.mean(mcopy)
        for k in range(len(mag)):
            if (mag[k]-meanmag) > (5*sigma):
                sigmacounter += 1
            if (mag[k] -meanmag) > (3*sigma):
                threesigcounter += 1
        if sigmacounter >= 1:
            fig,AX= plt.subplots()
       ##plot points wrt hjd v mag with magerr error bars and standard deviations
            AX.errorbar(hjd, mag, yerr = magerr, xerr = None, fmt ='bo')
            AX.axhline((meanmag + sigma), color = 'y', ls = '--')
            AX.axhline((meanmag + 3*sigma), color = 'c', ls = '--')
            AX.axhline((meanmag + 5*sigma), color = 'm', ls = '--')
            AX.axhline(meanmag)
            AX.invert_yaxis()
            AX.set_xlabel("days")
            AX.set_ylabel("magnitude")
            AX.set_title("OID:" + float_to_str(i) + " Dec:" + str(dec[0]))
            ##save plot figure if sigmacounter>1 (will test out file save before create if statement)
            print((str(threesigcounter) + "_"+ str(ra[0]) + "_" + str(dec[0]) + "_" + float_to_str(i)+ "_.png"))
            #fig.savefig(str(threesigcounter) + "_"+ str(ra[0]) + "_" + str(dec[0]) + "_" + str(i)+ "_.png")
            plt.show()
            #fig.clf()
main()
   