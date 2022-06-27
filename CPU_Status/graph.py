import matplotlib.pyplot as plt
import matplotlib.animation as anim
#Creating new figure
fig = plt.figure()

#Creating subplot with 1 row,1 column and 1 index
subplot = fig.add_subplot(1, 1, 1)

class Graphh:
    #Creating the function that reads data from cpu.txt and feeds it to subplot
    def animation_function(self,i):
        cpu_data = open(".\\cpu.txt").readlines()
        #List to hold CPU values
        x = []

        #Adding each value in the CPU data to the list-x and if statement is to  exclude any blank lines 
        for each_value in cpu_data:
            if len(each_value) > 1:
                x.append(float(each_value))

        #Refreshing the figure to avoid unnecessary overwriting for each new poll
        subplot.clear()

        #Plotting the values in then list
        subplot.plot(x)


    def plot_graph(self):
        global fig  
        #Using the figure,the function and polling interval of 10000ms (10s) to build animation
        graph_animation = anim.FuncAnimation(fig, self.animation_function, interval=1000)

        #Displaying the graph to the screen
        plt.show()

grp = Graphh()
grp.plot_graph()