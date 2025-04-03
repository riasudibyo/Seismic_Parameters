# initiation
import numpy as np
from obspy import read
from PermutationEntropyTimeSeries import PermutationEntropyTimeSeries

# reading and plotting data
import obspy
import glob
import os
import datetime
import multiprocessing
from typing import List, Tuple

if __name__ == '__main__':
    filePath = r'log/test.csv'
    # open the file
    outputFile = open(filePath, 'x')
    outputFile.write(
        "Time,StartTime,MiddleTime,EndTime,PermutationEntropy,EmbeddingDimension,DelayTime\n")

    delaytime =0.02
    embeddingDimension = 5
    windowInSeconds = 3600
 


    for filepath in sorted(glob.iglob(r'permutationentropy/data_test/FLUR__HHZ__20140801_bandpass_0.5_10_.mseed')):
        st = read(filepath)
        # print(st)
        tr = st[0]
        tCutStart = tr.stats.starttime
        tCutEnd = tr.stats.starttime + windowInSeconds
        tMiddle = tr.stats.starttime + 0.5*windowInSeconds
        TimeCuts: List[Tuple[obspy.core.utcdatetime.UTCDateTime,
                            obspy.core.utcdatetime.UTCDateTime, obspy.core.utcdatetime.UTCDateTime]] = []
        while tCutEnd <= tr.stats.endtime:
            tupleTimes = (tCutStart, tCutEnd, tMiddle)
            TimeCuts.append(tupleTimes)
            tCutStart = tCutEnd
            tCutEnd = tCutEnd + windowInSeconds
            tMiddle = tCutStart + 0.5*windowInSeconds
        tCutEnd
        data: List[Tuple[obspy.core.trace.Trace,
                        Tuple[obspy.core.utcdatetime.UTCDateTime, obspy.core.utcdatetime.UTCDateTime, obspy.core.utcdatetime.UTCDateTime], int, float, int, str]] = []
        for timeWindow in TimeCuts:
            data.append((tr, timeWindow, embeddingDimension, delaytime, tr.stats.sampling_rate))

        process_pool = multiprocessing.Pool(22)
        output = process_pool.starmap_async(
            PermutationEntropyTimeSeries, data)
        process_pool.close()
        process_pool.join()

        abc = output.get()
        # reveal_type(output)
        for text in abc:
            outputFile.write(text)
    outputFile.close()