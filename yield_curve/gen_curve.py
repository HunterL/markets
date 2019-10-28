import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.gridspec as gridspec
import datetime

def main():
    # Read html table w/ treasury data into pd
    df = pd.read_html("https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/TextView.aspx?data=yield")[1]

    # save off dates for later
    dates = df['Date']
    dates = [datetime.datetime.strptime(d,"%m/%d/%y") for d in dates]

    # drop dates
    df = df.drop(axis=1, columns=['Date'])

    # convert rest of the df to numeric
    df = df.apply(pd.to_numeric)

    steps = 15 # steps inbetween each discrete point, increases workload dramatically
    total_steps = (steps - 1) * (len(dates) - 1) + 1

    x = np.array(df.columns)

    # Setup for the bar chart
    objects = ['']
    values = [d.day for d in dates]
    min_d = min(values)
    max_d = max(values)
    step_size = (max_d - min_d) / total_steps
    y_pos = np.arange(len(objects))

    fig = 0
    # Iterate for each date
    for i in range(0, len(dates)-1):
        y_cur = np.array(df.iloc[i].values)
        y_next = np.array(df.iloc[i+1].values)
        dif_array = []
        # Measure the difference between each bond and its next price
        for j in range(0,len(y_cur)):
            dif_array.append(y_cur[j] - y_next[j])
        # Do the stepping     
        for k in range(1,steps):
            y_dif = []
            for l in range(0, len(y_cur)):
                y_dif.append(y_cur[l] - (dif_array[l] * (k/steps)))
            # Generate a new plot at each step
            gen_plot(x, y_dif, min_d, max_d, step_size, y_pos, objects, fig)
            fig += 1


def gen_plot(x, y, min_d, max_d, step_size, y_pos, objects, num):
    # Setup
    fig = plt.figure(num)
    cols = 12
    rows = 4
    gridspec.GridSpec(ncols=cols, nrows=rows)

    # Large subplot
    plt.subplot2grid((rows,cols),(0,0), colspan=cols-2, rowspan=rows)
    plt.title('Yield Curve for Sepetember 2019', fontsize = 20, weight="bold", pad=20)
    plt.xlabel('Maturity', fontsize = 20, weight="bold", labelpad=20)
    plt.ylabel('Yield', fontsize = 20, weight="bold", labelpad=20)
    plt.ylim(1,2.5)
    # plt.ylim(min(y)-.25, max(y)+.25) # shifting y axis instead of static
    plt.plot(x,y, "-o")
    
    # Small date "thermometer" plot
    plt.subplot2grid((rows,cols),(1,cols-1), colspan=1, rowspan=rows-1)
    v = min_d + (step_size * num)
    plt.xticks(y_pos, objects)
    plt.title('Day', fontsize = 20, weight="bold", pad=20)
    plt.ylim(min_d,max_d)
    plt.grid(b=None)
    plt.bar(y_pos, v, align='center', width=1)
    
    fig.tight_layout
    plt.savefig('images/' + str(num) + '.png')
    
    plt.close


if __name__ == '__main__':
    main()