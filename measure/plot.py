import pandas as pd
import matplotlib.pyplot as plt

# Read data file. Import as a list and turn to dataframe
df_list = pd.read_pickle('/Users/tammy/Documents/GitHub/imu-positioning/measure/data.pkl')
df = pd.DataFrame(df_list)

# Get x and y cordinator
def get_xy(df):
    x = df.iloc[:,5:6]
    y = df.iloc[:,4:5]
    return x
    return y

# Function to plot the position of x and y.
def plot_map_line(x,y):
    plt.plot(x,y,color='green', linestyle='dashed', linewidth = 3, 
         marker='o', markerfacecolor='blue', markersize=12)
    # naming the x axis 
    plt.xlabel('x - axis') 
    # naming the y axis 
    plt.ylabel('y - axis') 
  
    # giving a title to my graph 
    plt.title('Map position') 
    plt.show()

def plot_map_scatter(x,y):
    plt.scatter(x,y)
    plt.show()

plot_map_line(x,y)
# plot_map_scatter(x,y)