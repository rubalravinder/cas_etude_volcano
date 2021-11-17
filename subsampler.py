import pandas as pd
from collections import Counter
import os

types_vocab = ["EXP", "HIB", "LP", "PIS", "TOR", "TR", "VT"]
def event_class(event:str):
    if event in types_vocab:
        return event
    else:
        return event[:-1]

def balanced_subsampler(df:pd.DataFrame, samples_per_class:int) -> pd.DataFrame:
    if samples_per_class > df.event.value_counts().min():
        raise ValueError(f"There are less than {samples_per_class} samples in at least one class.")
    
    counter = Counter()
    indices = []

    df = df.sample(frac=1)
    for index, row in df.iterrows():
        if counter[row.event] >= samples_per_class:
            continue
        filename = "data/Extracted/" + row.event + "/" + row.event + "_" + str(row.Index) + ".npy"
        if not os.path.isfile(filename):
            continue
        indices.append(index)
        counter[row.event] += 1

    return df[df.Index.isin(indices)].copy().sample(frac=1)