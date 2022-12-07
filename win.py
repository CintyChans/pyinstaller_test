from tkinter import ttk,messagebox,Tk,Label,Entry,Button,Frame,StringVar,IntVar
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
class Window(Tk):
    def __init__(self):
        super().__init__()
        self.title('TOFSense-M_Test')
        self.connecting=False
        self.initUI()

    def initUI(self):
        self.frame1=Frame(self)
        self.baudrateval=IntVar()
        self.baudrateval.set('921600')
        self.predictval=StringVar()
        self.stdval=StringVar()
        self.predictval=StringVar()
        self.port_btn=Button(self.frame1,text='扫描串口',bg='white')
        self.port_box=ttk.Combobox(self.frame1,state='readonly',width=10)
        self.port_btn.grid(row=0,column=0,sticky="we",pady=5,padx=5)
        self.port_box.grid(row=0,column=1,sticky="we",pady=5,padx=5)
        self.baudrate=Entry(self.frame1,textvariable=self.baudrateval,width=10)
        baudrate=Label(self.frame1,text='baudrate:')
        baudrate.grid(row=0,column=2,sticky="we",pady=5,padx=5)
        self.baudrate.grid(row=0,column=3,sticky="we",pady=5,padx=5)
        Label(self.frame1,text='pixel:').grid(row=0,column=4,sticky="we",pady=5,padx=5)
        self.pixel=ttk.Combobox(self.frame1,state='readonly',width=10)
        self.pixel['value'] = ['8x8','4x4']
        self.pixel.current(0)
        self.pixel.grid(row=0,column=5,sticky="we",pady=5,padx=5)
        self.connect_btn=Button(self.frame1,text='连接串口',bg='white')
        self.connect_btn.grid(row=0,column=6,sticky="we",pady=5,padx=5)
        Label(self.frame1,text='std:').grid(row=1,column=0)
        self.std=Label(self.frame1,textvariable=self.stdval)
        self.std.grid(row=1,column=1)
        Label(self.frame1,text='平面:').grid(row=1,column=2,sticky="we",pady=5,padx=5)
        self.predict=Label(self.frame1,textvariable=self.predictval,font=('黑体', 50))
        self.predict.grid(row=1,column=3)
        self.frame1.pack()
        self.fig,self.ax=plt.subplots(subplot_kw={"projection": "3d"})
        self.ax.set_zlim(0, 4)
        X= np.linspace(0, 8,8)
        self.X,self.Y=np.meshgrid(X,X)
        self.Z=np.zeros((8,8))
        self.surf = self.ax.plot_surface(self.X,self.Y,self.Z, rstride=1,cstride=1,cmap = 'summer')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  
        self.ani = animation.FuncAnimation(self.fig, self.animate, blit=False)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)


    def animate(self,frame_number):
        if self.connecting:
            self.surf.remove()
            self.surf=self.ax.plot_surface(self.X,self.Y,self.Z, rstride=1,cstride=1,cmap = 'summer')
            return self.surf,




