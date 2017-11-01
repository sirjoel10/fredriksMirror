import tkinter
import time
import datetime

#tday = datetime.date.today()
#print(tday.weekday())
#print(tday.isoweekday())
#t = datetime.datetime.now()


class clock(tkinter.Frame):

    def __init__(self):

        self.time1 = ''
        self.timeLb1 = tkinter.Label(self, font=('Helvetica', 100, 'bold'), bg ='black', fg ='white')
        self.timeLb1.pack(side='top', anchor='e')
        self.tick()

    def tick(self):

        time2 = time.strftime('%H:%M')

        if time2 != time1:
            self.time1 = time2
            self.timeLb1.config(text=time2)


            self.timeLb1.after(200, tick)





class fullscreen:

    def __init__(self):

        # Skapar fönsteret
        self.window = tkinter.Tk()
        self.window.config(background='black')
        self.window.geometry('700x500')

        self.topframe = tkinter.Frame(self.window, background='black')
        self.bottomframe = tkinter.Frame(self.window, background='black')

        self.topframe.pack(side = 'top', fill = 'both', expand = 'YES')
        self.bottomframe.pack(side = 'bottom', fill='both', expand = 'YES')

        # Inför klockan till fönstret
        self.clock = self.clock(self.topframe)
        self.clock.pack( side = 'right', anchor ='n', padx = '100', pady = '60')

        # Inför vädret till fönstret


w = fullscreen()
w.window.mainloop()

