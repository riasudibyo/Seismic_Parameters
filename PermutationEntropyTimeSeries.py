from permuentropy import ordinal_patterns
from permuentropy import p_entropy
import datetime
import os
import obspy

from typing import Tuple, List


def PermutationEntropyTimeSeries(DataTrace: obspy.core.trace.Trace, TimeWindow: Tuple[obspy.core.utcdatetime.UTCDateTime,
                                                                                        obspy.core.utcdatetime.UTCDateTime],
                                   EmbeddingDimension: int, DelayTime: int, SamplingRate: int) -> str:
    trCopy = DataTrace.copy()
    tCutStart = TimeWindow[0]
    tCutEnd = TimeWindow[1]
    tMiddle = TimeWindow[2]
    trCopy.trim(tCutStart, tCutEnd)
    freq_list = ordinal_patterns(trCopy.data, EmbeddingDimension, round(DelayTime*SamplingRate))
    permutationEntropy = p_entropy(freq_list)
    return (str(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")) + "," +
            str(tCutStart) + "," + str(tMiddle) + "," + str(tCutEnd) + "," +
            str(permutationEntropy) + "," + str(EmbeddingDimension) + "," + str(DelayTime) + "\n")
