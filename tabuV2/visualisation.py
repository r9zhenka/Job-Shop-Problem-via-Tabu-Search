import matplotlib.pyplot as plt
# making Gant chart
# Declaring a figure "gnt"
fig, gnt = plt.subplots()
# Setting Y-axis limits
gnt.set_ylim(0, 50)
# Setting X-axis limits
gnt.set_xlim(0, 160)
# Setting labels for x-axis and y-axis
gnt.set_xlabel('seconds since start')
gnt.set_ylabel('machine')

# Setting ticks on y-axis
gnt.set_yticks([x*10 for x in range(1,11)])
# Labelling tickes of y-axis
gnt.set_yticklabels([str(x) for x in range(1, 11)])

# Setting graph attribute
gnt.grid(True)

# Declaring a bar in schedule
gnt.broken_barh([(40, 50)], (30, 9), facecolors=('tab:orange'))

# Declaring multiple bars in at same level and same width
gnt.broken_barh([(110, 10), (150, 10)], (10, 9),
                facecolors='tab:blue')

gnt.broken_barh([(10, 50), (100, 20), (130, 10)], (20, 9),
                facecolors=('tab:red'))
plt.show()
# plt.savefig("gantt1.png")