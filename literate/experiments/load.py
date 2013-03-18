import pandas as pd
import hook

series = pd.Series([n*n for n in range(10)])
series.plot()

print 'hijacks:', hook.hijacks