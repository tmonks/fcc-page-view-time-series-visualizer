import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean the data by filtering out days when the page views were 
# in the top 2.5% of the dataset or bottom 2.5% of the dataset.
bottom = df['value'].quantile(0.025)
top = df['value'].quantile(0.975)
mask = (df['value'] > bottom) & (df['value'] < top)
df = df[mask]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(14, 4))

    ax.plot(df.index, df['value'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar = df.pivot_table(index=df.index.year, columns=df.index.strftime('%B'), values='value', aggfunc='mean')
    df_bar = df_bar[months]

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(12, 6))
    df_bar.plot.bar(xlabel='Years', ylabel='Average Page Views', ax=ax, label='Months')
    ax.legend(title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    months_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=months_short, ordered=True)

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(14, 6))
    sns.boxplot(data=df_box, x='year', y='value', ax=ax1)
    sns.boxplot(data=df_box, x='month', y='value', ax=ax2)

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    ax2.set_title('Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
