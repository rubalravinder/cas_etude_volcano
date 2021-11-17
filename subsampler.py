import pandas as pd
from collections import Counter

def balanced_subsampler(df:pd.DataFrame, samples_per_class:int) -> pd.DataFrame:
    if samples_per_class > df.event.value_counts().min():
        raise ValueError(f"There are less than {samples_per_class} samples in at least one class.")
    
    counter = Counter()
    indices = []

    df = df.sample(frac=1)
    for index, row in df.iterrows():
        if counter[row.event] >= samples_per_class:
            continue
        indices.append(index)
        counter[row.event] += 1

    return df[df.Index.isin(indices)].copy().sample(frac=1)