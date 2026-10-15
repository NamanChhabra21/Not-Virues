import splashscreen_engine as splash
import pygame

import threading
import os
import random
import datetime
import tkinter

import DataHandling
import AdditionalUi



# Data handling
data = DataHandling.Uid()
if not data.is_created():
    AdditionalUi.AskName() # Asks name and make Unique ID once only
    settings = AdditionalUi.Settings()
    settings.start()

    # If User Don't wanna run after setup
    if not settings.RUN:
        print("Exited")
        exit()
DataHandling.update_last_played()
DataHandling.save_database()

# Get Preferences Saved By user
import json
with open("Assets/UserData.json", "r", encoding="utf-8") as file:
    Preferences = json.load(file)
    Preferences = Preferences["Settings"]

# Initialize Mixer
pygame.mixer.init()

# Sounds
HorrorSound = pygame.mixer.Sound("Assets/Audios/Horror.mp3")
SignalLost = pygame.mixer.Sound("Assets/Audios/SignalLost.mp3")
ShutterSound = pygame.mixer.Sound("Assets/Audios/CameraShutter.mp3")
PopUps = pygame.mixer.Sound("Assets/Audios/PopUps.mp3")
winCrash = pygame.mixer.Sound("Assets/Audios/windowCrashed.mp3")

# Music Channel
channel = pygame.mixer.Channel(1)
channel.set_volume(0.5)

# Sound Effects
channelEffects = pygame.mixer.Channel(2)
channelEffects.set_volume(0.6)

if Preferences["Sound Effects"] == 1:
    # Play Horror music
    channel.play(HorrorSound,loops=-1)



# Time Calculator
start_time = datetime.datetime.now()

# Setting up screen
screen = splash.Screen()
screen.size(fullscreen=True) # Add more fun
screen.start()
loadingVid = splash.BackgroundVideo(screen,"Assets/Videos/loadingScreen.mp4")
loadingVid.play()

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


# Animate Text
for i in range(0,5):
    for k in range(0,20):
        value+=1
        bar.set_progress(value)
        screen.wait(0.3)
    text.edit(text=init_messages[i])
    print(value)
# screen.wait(2)

# Remove other elements
text.hide()
bar.hide()

# Stop Old Video
loadingVid.delete()

# # Add Videos after Init
bg_video = splash.BackgroundVideo(screen,"Assets/Videos/1.mp4")
bg_video.play()

# Play Sound
if Preferences["Sound Effects"] == 1:
    channelEffects.play(SignalLost)



while bg_video.is_playing:
    screen.wait(0.5)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pass
if Preferences["Sound Effects"] == 1:
    channelEffects.fadeout(2)

if (DataHandling.get_username() != "OWNER") and (Preferences["Open Camera"] == 1):
    # Show opening camera
    text.edit(text="Finding Camera...")
    text.show()

    import Camera

    camera = Camera.OpenCamera()
    DataHandling.save_camera(camera.success)
    if camera.success:
        if Preferences["Sound Effects"] == 1:
            channelEffects.play(ShutterSound)
        text.edit(text="Opening Camera...")
        screen.wait(5)
        threading.Thread(target=camera.show).start()
        screen.wait(11)
        camera.stop()
    else:
        text.edit(text="No Camera Found")
        screen.wait(5)

# Pop Up sound
if Preferences["Sound Effects"] == 1:
    channelEffects.play(PopUps)

if Preferences["Show Pop-ups"] == 1:
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

    def close_all():
        for window in windows.values():
            try:
                window.destroy()
            except tkinter.TclError:
                pass

        main_window.destroy()

    main_window.protocol("WM_DELETE_WINDOW", close_all)
    main_window.mainloop()

text.edit(text="THANKS FOR USING THIS FAKE VIRUES")
AdditionalUi.RateUs()

# Playtime Seconds
exit_time = datetime.datetime.now()
time_played = (exit_time - start_time).total_seconds()
DataHandling.update_playtime(time_played)

# Save Database
DataHandling.save_database()

text.hide()

# Show windows crashed (Fake - Just an image)
bg_video.delete()

screen.screen.fill((255,255,255))

bg_image = splash.BackgroundImage(screen,"Assets/EndImage.png")
if Preferences["Sound Effects"] == 1:
    channelEffects.play(winCrash)
bg_image.set()


screen.wait(6)

screen.stop()

if (DataHandling.get_username() != "OWNER") and (Preferences["Restart PC"] == 1):

    # Restart System
    os.system("shutdown /r /t 0")




