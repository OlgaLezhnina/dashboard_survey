# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# read the data
mydata = pd.read_csv('DashboardOrkgSurvey.csv')
# get means and standard deviations
mydata.mean().round(2) 
mydata.std().round(2)

# descriptives sample
mydata.U1.value_counts()
mydata.U2.value_counts()
mydata.U3.value_counts()

# results of the UEQ-S for all participants
df1 = pd.DataFrame(mydata.filter(regex = 'Q1').mean(), columns = ['means'])
df1['Item'] = [1 + x//2 for x in range(16)]
df1['index'] = ['DC'[x%2] for x in range(16)]
# the plot
sns.barplot(x ='Item', y = 'means', hue ='index', palette = 'rocket', data = df1)
plt.ylim(0, 3)

# plotting subgroups
# define the function
def plotgroup(df, names, palette):
    dfD = df.filter(regex = '\[1\]') 
    dfD.columns = list('12345678')
    dfC = df.filter(regex = '\[2\]')
    dfC.columns = list('12345678')
    dfB = pd.concat([dfD, dfC], sort = False)
    dfB.index = names
    sns.barplot(x = 'Item', y = 'value', hue = 'index', palette = palette,
            data = dfB.reset_index().melt(id_vars = 'index', var_name = 'Item'))
    plt.ylim(0, 3)

# technical vs humanitarian
df2 = mydata.groupby(['U1']).mean().iloc[::2, 0:16]
df2.index = ['Hum', 'Tech']
plotgroup(df2, ['Hum-D', 'Tech-D', 'Hum-C', 'Tech-C'], 'Greens_d')

# quantitative vs qualitative
df3 = mydata.groupby(['U2']).mean().iloc[:2, 0:16]
df3.index = ['QL', 'QN']
df3 = df3.reindex(['QN', 'QL'])
plotgroup(df3, ['QN-D', 'QL-D', 'QN-C', 'QL-C'], 'Blues_d')

# frequently vs occasionally
df4 = mydata.groupby(['U3']).mean().iloc[:, 0:16]
df4.index = ['OC', 'FR']
df4 = df4.reindex(['FR', 'OC'])
plotgroup(df4, ['Fr-D', 'Oc-D', 'Fr-C', 'Oc-C'], 'Reds_d')

# part 2 answers
dataQ2 = mydata.filter(regex = 'V1') 
df5 = pd.DataFrame({
    'Item':    [1,1,2,2,3,3,4,4,5,5],
    'service': list('DCDCDCDCDC'),
    'value':   dataQ2.mean()
})
barV = sns.barplot(x = 'Item', y = 'value', data = df5, hue = 'service', 
                   palette = 'mako')
plt.ylim(1, 5)
plt.legend(loc = 'lower right')
# THE END
