from EcoOpen.core import *

df = FindPapers(query="Climate change in croatia", number_of_papers=10)
df = DownloadPapers(df, "~/test/data")
df = FindOpenData(df, "keywords")
df = DownloadData(df, "~/test/data")
