import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv(
    'fcc-forum-pageviews.csv',
    index_col=0,
    parse_dates=True
)

# Clean data
df = df[
    (df['value']>df['value'].quantile(0.025))&
    (df['value']<df['value'].quantile(0.975))
]


def draw_line_plot():
    # Draw line plot
    fig, axes=plt.subplots(figsize=(18,6))
    axes.plot(df.index,df['value'],color='red')
    axes.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    axes.set_xlabel('Date')
    axes.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.reset_index()
    df_bar['year']=df_bar['date'].dt.year
    df_bar['Months']=df_bar['date'].dt.month
    df_bar.drop(columns=['date'])
    df_bar=df_bar.groupby(['year','Months'],as_index=False).agg('mean')
    df_bar=df_bar.pivot(index='year',columns='Months',values='value')
    month_map={
    1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',
    7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'           
}
    
    df_bar.columns=df_bar.columns.map(month_map)

    # Draw bar plot
    fig=df_bar.plot(kind='bar',figsize=(12,9),xlabel='Years',ylabel='Average Page Views')
    fig=fig.figure

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig,axes=plt.subplots(1,2,figsize=(20,9))
    sns.boxplot(data=df_box,x='year',y='value',ax=axes[0])
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    axes[0].set_title('Year-wise Box Plot (Trend)')

    sns.boxplot(data=df_box,x='month',y='value',ax=axes[1],order=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    axes[1].set_title('Month-wise Box Plot (Seasonality)')


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
