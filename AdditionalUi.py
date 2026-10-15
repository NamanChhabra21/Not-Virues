from customtkinter import *
import DataHandling
import webbrowser
import json
import textwrap


set_appearance_mode("default")



def center_window(window, width, height):
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate X and Y coordinates for the top-left corner
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

def delete(window):
    window.withdraw()
    window.quit()
    return

class RateUs:
    def __init__(self):

        root = CTk("gray50")
        root.attributes("-topmost",True)

        root.overrideredirect(True)
        center_window(root, 300, 340)
        x_button = CTkButton(root, text="X", font=("george", 20), command=lambda: delete(root), width=40, height=40,
                             corner_radius=0, fg_color="red", hover_color="red3")
        x_button.pack(anchor="ne")

        rateus = CTkLabel(root,text="Rate Us",text_color="white",font=("impact",40))
        rateus.pack(pady=(0,0),padx=(0,0))

        star_frame = CTkFrame(root,width=300,height=100,fg_color="gray50")
        star_frame.pack(pady=(30,0))

        stars = {}

        rating_messages = ["Poor","Not Good","Good !","Fantastic !!!","Loved it !!!!!!"]
        def fill_color(index):

            # Fill first `i` stars
            for star in range(0,index+1):
                stars[star].configure(text_color="yellow")

            # Fill remaining stars
            for star in range(index+1, 5):
                stars[star].configure(text_color="white")

            # Change rating message
            star_message.configure(text = rating_messages[index])

            # Show submit button
            submit.pack_forget()
            submit.configure(command=lambda x = index+1:self.submit(x,root))
            submit.pack()
        star_message = CTkLabel(star_frame,text="",font=("default",20),text_color="white")
        star_message.grid(row=1,columnspan=5,pady=(8,0))
        for i in range(0,5):
            stars[i] = CTkButton(star_frame,text="★",command=lambda x=i:fill_color(x),width=30,height=70,font=("Segoe UI Emoji",30),fg_color="black",hover_color="gray10")
            stars[i].grid(row=0,column=i,padx=2)

        message_text = """
Rating helps us to Improve !
                        """
        submit = CTkButton(root,text="Submit!",font=("default",20),fg_color="green",width=20,corner_radius=5,hover_color="green3")
        submit.pack_forget()

        message = CTkLabel(root,text=message_text,font=("default",20),text_color="white")
        message.pack()
        root.mainloop()
    @staticmethod
    def submit(rating,window):

        DataHandling.update_rating(rating)
        delete(window)
        return


class Feedback:
    def __init__(self):
        root = CTk()
        root.resizable(False,False)
        root.overrideredirect(True)

        center_window(root,300,450)
        root.title("Feedback")
        root.attributes("-topmost", True)
        root.configure(fg_color="gray60")
        root.iconbitmap("assets/icon.ico")
        x_button = CTkButton(root, text="X", font=("george", 20), command=lambda: delete(root), width=40, height=40,
                             corner_radius=0, fg_color="red", hover_color="red3")
        x_button.pack(anchor="ne")

        feedback_label = CTkLabel(root,text="Feedback",font=("impact",40))
        feedback_label.pack()

        feedback_entry = CTkTextbox(root,width=280,height=250,font=("default",18),wrap="word",activate_scrollbars=True)
        feedback_entry.pack(pady=(30,0))

        submit = CTkButton(root, text="Submit!", font=("default", 20), fg_color="green", width=40,height=20, corner_radius=5,
                           hover_color="green3", command=lambda : self.submit(root,str(feedback_entry.get("1.0", "end-1c") )))
        submit.pack(pady=(20,0))

        root.mainloop()

    @staticmethod
    def submit(root,feedback):
        DataHandling.add_feedback(feedback)
        delete(root)

class AskName:
    def __init__(self):
        root = CTk()
        root.resizable(False, False)
        center_window(root, 300, 200)
        root.wm_iconbitmap("Assets/icon.ico")
        root.title("Name")
        name_label = CTkLabel(root, text="Your Name", font=("impact", 30))
        name_label.pack(pady=(20,0))


        Name_entry = CTkEntry(root, width=250, height=20, font=("default", 20), placeholder_text="Optional")
        Name_entry.pack(pady=(30, 0))

        submit = CTkButton(root, text="Submit", font=("default", 20), fg_color="green", width=40, height=20,corner_radius=5,hover_color="green3",command=lambda: self.submit(root, str(Name_entry.get())))
        submit.pack(pady=(20, 0))
        root.mainloop()

    @staticmethod
    def submit(root, name):
        delete(root)
        DataHandling.Uid(name).make()

class Settings:
    def __init__(self):
        self.RUN = False
        self.root = CTk()
        self.root.resizable(False,False)
        self.root.geometry("300x515")
        self.root.configure(fg_color="black")
        self.root.title("Settings")

        center_window(self.root,300,515)

        self.root.iconbitmap("Assets/icon.ico")

        # Settings and Tagline Label
        CTkLabel(self.root,text="Settings",font=("Terminal",25)).pack(pady=(20,0))
        CTkLabel(self.root, text="Your Computer, Your Controls", font=("MV Boli", 15)).pack(pady=(1, 0))

        # Default Settings:
        self.settings = {
            "Restart PC":True,
            "Open Camera":True,
            "Sound Effects":True,
            "Show Pop-ups":True,
        }

        # Frame for showing settings
        self.settings_frame = CTkFrame(self.root,280,300,12,4,"black","gray10",border_color="gray20")
        self.settings_frame.pack()
        self.settings_frame.grid_propagate(False)

        self.setting_labels = {}
        self.settings_switches = {}
        for i,setting in enumerate(self.settings.keys()):
            self.setting_labels[f"{setting}_Label"] = CTkLabel(self.settings_frame,text=setting,font=("Arial Black", 20),text_color="white")
            self.setting_labels[f"{setting}_Label"].grid(row=i,column=0,pady=16,padx=20)
            self.settings_switches[f"{setting}_switch"] = CTkSwitch(self.settings_frame,text="",width=30,progress_color="green",fg_color="red")
            self.settings_switches[f"{setting}_switch"].select()
            self.settings_switches[f"{setting}_switch"].grid(row=i,column=1,pady=16,padx=20)

        def submit():
            self.submitbtn.configure(text="Saving...",state="disabled",text_color="yellow")
            # print()
            with open("Assets/UserData.json", "r") as datafile:
                df = json.load(datafile)
                df["Settings"]["Restart PC"] = self.settings_switches["Restart PC_switch"].get()
                df["Settings"]["Open Camera"] = self.settings_switches["Open Camera_switch"].get()
                df["Settings"]["Sound Effects"] = self.settings_switches["Sound Effects_switch"].get()
                df["Settings"]["Show Pop-ups"] = self.settings_switches["Show Pop-ups_switch"].get()
            with open("Assets/UserData.json", "w") as writedf:
                json.dump(df, writedf)
            self.settings_frame.destroy()
            msgLabel.destroy()
            msgbtn.destroy()
            self.root.geometry("400x320")
            center_window(self.root,400,320)
            SUCCESS_MESSAGE = "🎉 Your Setup Was Successful!\n\nYou can now share this application with your\nfriends and family.\n\nThe next time you open the application, it will\nstart the simulated virus experience based on\nthe settings you selected.\n\nOr, if you're ready...\n\nTry it now! 👀"
            CTkLabel(self.root, text=textwrap.fill(SUCCESS_MESSAGE,width=40), font=("Segoe UI Emoji", 18)).pack(pady=(20, 0))

            # Run Button
            def RunClicked():
                self.RUN = True
                delete(self.root)
            RunBtn = CTkButton(self.root,text="Run",font=("Terminal",16),fg_color="green",text_color="white",hover_color="green4", command=RunClicked)
            RunBtn.pack(pady=10)
        self.submitbtn = CTkButton(self.settings_frame,text="Save",font=("Impact",20),fg_color="green",text_color="white",hover_color="green4", command=submit)
        self.submitbtn.grid(row=len(self.settings_switches),columnspan=2,pady=(15,0))


        # Show Message
        MESSAGE = (
            "This application uses the selected features\n"
            "to create a simulated virus experience.\n"
            "Some features may access your camera or\n"
            "restart your computer. Review your choices\n"
            "before continuing. By clicking Save, you\n"
            "confirm your choices and agree to the"
        )
        msgLabel = CTkLabel(self.root,text=MESSAGE,font=("default",13))
        msgLabel.pack(pady=(12,0))

        # Privacy Policy Button
        def open_policy():
            webbrowser.open(r'https://github.com/NamanChhabra21/Not-Virues/blob/main/Privacy%20Policy.md')
        msgbtn = CTkButton(self.root,text="Privacy Policy",font=("default",13),text_color="deep sky blue",bg_color="black",fg_color="black",hover_color="black",command=open_policy)
        msgbtn.pack()


    def start(self):
        self.root.mainloop()
        print("MainEnd")

