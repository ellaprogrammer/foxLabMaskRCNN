import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import matplotlib as mpl

import sys

mpl.rcParams['toolbar'] = 'None'

class DrawRectangle:
    def __init__(self, fig, ax, image_file):
        self.fig = fig
        self.ax = ax
        self.image_file = image_file
        self.click_corner = (0,0)
        self.release_corner = (0,0)
        self.rois = []
        self.draw_image()

    def draw_image(self):
        img = mpimg.imread(self.image_file)
        self.ax.imshow(img) 

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.fig.canvas.mpl_connect( 'button_press_event', self.onclick)
        self.cidrelease = self.fig.canvas.mpl_connect( 'button_release_event', self.onrelease)
        self.cidkeypress = self.fig.canvas.mpl_connect('key_press_event', self.onkey)

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.fig.canvas.mpl_disconnect(self.cidpress)
        self.fig.canvas.mpl_disconnect(self.cidrelease)
        self.fig.canvas.mpl_disconnect(self.cidkeypress)

    def onclick(self, event):
        self.click_corner = (event.xdata, event.ydata)
        print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
            (event.button, event.x, event.y, event.xdata, event.ydata))

    def onrelease(self, event):
        self.release_corner = (event.xdata, event.ydata) 
        self.draw_rect() 
        print('release button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
            (event.button, event.x, event.y, event.xdata, event.ydata))

    def draw_rect( self ):
        region_size = (self.release_corner[0]-self.click_corner[0], self.release_corner[1]-self.click_corner[1])
        self.ax.add_patch( patches.Rectangle( self.click_corner, region_size[0], region_size[1],
            fill=False, lw=3, color='r' ))
        self.rois.append( [self.click_corner, self.release_corner] )
        self.fig.canvas.draw()

    def onkey(self, event):
        print('you pressed', event.key, event.xdata, event.ydata)
        if event.key == 's': #save
            self.save_rect()
        if event.key == 'w': #close
            self.close_fig()
        if event.key == 'r': #reset
            self.reset_rois()

    def reset_rois(self):
        self.rois = []

        self.ax.clear()
        self.draw_image()
        self.fig.canvas.draw()

    def close_fig(self):
        plt.close(self.fig)

    def save_rect( self ):
        text_file = self.image_file[:-4]+'.csv'
        item_list = []
        for item in self.rois:
            item_list.append([str(num) for num in [item[0][0], item[0][1], item[1][0], item[1][1]] ])
        
        with open(text_file, 'wb') as fp:
            for item in item_list:
                fp.write(",".join(item)+'\n' )
                print(','.join(item))
        fp.close()
        

for img_file in sys.argv[1:]:
    w,h = (640,480)
    f, ax = plt.subplots(1,1,figsize=(10,10.0/w*h))
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    my_rect = DrawRectangle(f,ax,img_file)
    my_rect.connect()
    plt.show()




