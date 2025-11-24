import random
import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk

try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False


def user_win(player, opponent):
    return (player == 'plant' and opponent == 'sun') or \
           (player == 'sun' and opponent == 'pests') or \
           (player == 'pests' and opponent == 'plant')


def compute_result(user_choice, win_sound_path, lose_sound_path):
    choices = ['sun', 'plant', 'pests']
    computer_choice = random.choice(choices)

    if user_choice == computer_choice:
        result = f"It's a tie! Both chose {user_choice}."
        sound = lose_sound_path
    elif user_win(user_choice, computer_choice):
        sound = win_sound_path
        if user_choice == "plant":
            result = "YOU WIN!\n Your Plant will grow against opponent's Sun"
        elif user_choice == "sun":
            result = "YOU WIN!\n Your Sun will dry out the opponent's Pests"
        else:
            result = "YOU WIN! \n Your Pests will eat all of the opponent's Plant"

    else:
        sound = lose_sound_path
        if user_choice == "plant":
            result = "YOU LOSE!\n Opponent's Pests ate your Plant"
        elif user_choice == "sun":
            result = "YOU LOSE!\n Your Sun makes your Opponent's Plant grow"
        else:
            result = "YOU LOSE! \n Your Pests was dried out by opponent's Sun"

    if PYGAME_AVAILABLE and sound and os.path.exists(sound):
        try:
            pygame.mixer.Sound(sound).play()
        except Exception:
            pass

    return result


root = tk.Tk()
root.title("Sun Plant Pests")
root.geometry("520x380")
root.configure(bg="#4AFF4A")


base_path = os.path.dirname(__file__)
sun_img_path = os.path.join(base_path, "image", "sun.png")
plant_img_path = os.path.join(base_path, "image", "plant.png")
pests_img_path = os.path.join(base_path, "image", "pests.png")
win_sound_path = os.path.join(base_path, "sounds", "win_sound.mp3")
lose_sound_path = os.path.join(base_path, "sounds", "lose_sound.mp3")


def load_images():
    size = (80, 80)
    imgs = {}
    try:
        imgs['sun'] = ImageTk.PhotoImage(Image.open(sun_img_path).resize(size, Image.LANCZOS))
        imgs['plant'] = ImageTk.PhotoImage(Image.open(plant_img_path).resize(size, Image.LANCZOS))
        imgs['pests'] = ImageTk.PhotoImage(Image.open(pests_img_path).resize(size, Image.LANCZOS))
    except Exception:
        imgs['sun'] = imgs['plant'] = imgs['pests'] = None
    return imgs


images = load_images()

saved_users = []

main_frame = tk.Frame(root, bg="#4AFF4A")
main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

outer = tk.Frame(main_frame, bg="black")
outer.place(relx=0.5, rely=0.03, anchor='n', relwidth=0.9, relheight=0.25)

inner = tk.Frame(outer, bg="#FFFFFF")
inner.place(relx=0.02, rely=0.06, relwidth=0.96, relheight=0.88)

title = tk.Label(inner, text="Sun, Plant, Pests", bg="#FFFFFF", fg="#111111",
                 font=("Impact", 28))
title.pack(expand=True)

subtitle = tk.Label(main_frame, text="Presented by\nSDG 15: Life On Land", font=("Impact", 12), fg="black", bg="#4AFF4A")
subtitle.pack(pady=(0, 10))
subtitle.place(relx=0.37, rely=0.3)

btn_row = tk.Frame(main_frame, bg="#4AFF4A")
btn_row.place(relx=0.5, rely=0.66, anchor='n', relwidth=0.9, relheight=0.24)


def make_bordered_button(parent, text, cmd): #DONE
    shadow_color = "#2f2f2f"
    border_color = "#000000"
    face_color = "#DCDCDC"

    outer = tk.Frame(parent, bg=shadow_color, bd=0)

    border = tk.Frame(outer, bg=border_color)
    border.place(relx=0, rely=0, relwidth=0.96, relheight=0.96)

    btn = tk.Button(border, text=text, bg=face_color, fg="#000000",
                    relief='raised', bd=3, activebackground=face_color,
                    highlightthickness=0, command=cmd)
    btn.place(relx=0, rely=0, relwidth=1, relheight=1)

    return outer

def show_add_user(): #TAPOS
    user_options_frame.place_forget()
    add_user_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    refresh_user_list()

def update_username_display(): # DONEE
    """Update the username display label with the current user"""
    if current_user:
        username_display.config(text=f"Playing as: {current_user}")
    else:
        username_display.config(text="Playing as: None")

def set_current_user(username): # DONEE
    """Set the active user and refresh UI"""
    global current_user
    if username in saved_users:
        current_user = username
        update_username_display()
        messagebox.showinfo("Current User Updated", f"Username changed!\nNow playing as '{username}'.")

def save_user(): # DONEE
    global current_user
    username = username_entry.get().strip()
    if username:
        if username not in saved_users:
            saved_users.append(username)
            current_user = username
            username_entry.delete(0, tk.END)
            refresh_user_list()
            update_username_display()
            messagebox.showinfo("Success", f"User '{username}' saved and set as current user!")
        else:
            messagebox.showwarning("Warning", "Username already exists!")
    else:
        messagebox.showwarning("Warning", "Please enter a username!")

def delete_user(username): #TAPOS
    global current_user
    if username in saved_users:
        saved_users.remove(username)
        if current_user == username:
            current_user = None
        refresh_user_list()
        update_username_display()

def refresh_user_list(): # TAPOSSSA
    for widget in list_scrollable_frame.winfo_children():
        widget.destroy()
    for widget in user_list_scrollable_frame.winfo_children():
        widget.destroy()
    
    for username in saved_users:
        user_row = tk.Frame(list_scrollable_frame, bg="#FFFFFF")
        user_row.pack(fill="x", padx=10, pady=3)
        
        user_label = tk.Label(user_row, text=username, font=("Arial", 11), bg="#FFFFFF", fg="black", anchor='w', cursor="hand2")
        user_label.pack(side="left", fill="x", expand=True)
        user_label.bind("<Button-1>", lambda e, u=username: set_current_user(u))
        
        delete_btn = tk.Button(user_row, text="X", font=("Arial", 10, "bold"), 
                              bg="#FFFFFF", fg="red", relief="flat", 
                              command=lambda u=username: delete_user(u),
                              width=3, cursor="hand2", bd=0)
        delete_btn.pack(side="right")
        
        user_row2 = tk.Frame(user_list_scrollable_frame, bg="#FFFFFF")
        user_row2.pack(fill="x", padx=10, pady=3)
        
        user_label2 = tk.Label(user_row2, text=username, font=("Arial", 11), bg="#FFFFFF", fg="black", anchor='w', cursor="hand2")
        user_label2.pack(side="left", fill="x", expand=True)
        user_label2.bind("<Button-1>", lambda e, u=username: set_current_user(u))
        
        delete_btn2 = tk.Button(user_row2, text="X", font=("Arial", 10, "bold"), 
                               bg="#FFFFFF", fg="red", relief="flat", 
                               command=lambda u=username: delete_user(u),
                               width=3, cursor="hand2", bd=0)
        delete_btn2.pack(side="right", padx=(5, 0))

def show_game(): # TAPOSS
    update_username_display()
    main_frame.place_forget()
    game_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

def show_main(): #TAPOSS
    options_frame.place_forget()
    about_frame.place_forget()
    user_options_frame.place_forget()
    add_user_frame.place_forget()
    game_frame.place_forget()
    main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

def show_options(): #TAPOS
    user_options_frame.place_forget()
    add_user_frame.place_forget()
    about_frame.place_forget()
    options_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

def show_user_options(): #TAPOS
    options_frame.place_forget()
    add_user_frame.place_forget()
    user_options_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    refresh_user_list()

def show_about(): #NEED SOME MODIFICATION
    options_frame.place_forget()
    about_frame.place(relx=0, rely=0, relwidth=1, relheight=1)



#------ MAIN CODES FOR INTERFACE

if not saved_users:
    current_user = None
else:
    current_user = saved_users[0]

start_btn = make_bordered_button(btn_row, "Start", show_game)
start_btn.place(relx=0.05, rely=0.15, relwidth=0.28, relheight=0.6)

opt_btn = make_bordered_button(btn_row, "Option", show_options)
opt_btn.place(relx=0.36, rely=0.15, relwidth=0.28, relheight=0.6)

exit_btn = make_bordered_button(btn_row, "Exit", lambda: root.quit())
exit_btn.place(relx=0.67, rely=0.15, relwidth=0.28, relheight=0.6)

game_frame = tk.Frame(root, bg="#EFEFEF")

username_display = tk.Label(game_frame, text=f"Playing as: {current_user}", font=("Impact", 8), bg="#EFEFEF")
username_display.place(relx=0.1, rely=0.03, anchor='n')

game_title = tk.Label(game_frame, text="Choose one:", font=("Arial", 14), bg="#EFEFEF")
game_title.pack(pady=(12, 6))

game_result_label = tk.Label(game_frame, text="", font=("Arial", 12), bg="#EFEFEF", wraplength=380)
game_result_label.pack(pady=(6, 8))

game_btn_frame = tk.Frame(game_frame, bg="#EFEFEF")
game_btn_frame.pack(pady=8)

def on_choice(choice):
    res = compute_result(choice, win_sound_path, lose_sound_path)
    game_result_label.config(text=res)

rb = tk.Button(game_btn_frame, image=images['sun'], text='Sun', compound='top', width=100, height=110,
               relief='raised', bd=4, bg='#FFFFFF', command=lambda: on_choice('sun'))
rb.grid(row=0, column=0, padx=10)

pb = tk.Button(game_btn_frame, image=images['plant'], text='Plant', compound='top', width=100, height=110,
               relief='raised', bd=4, bg='#FFFFFF', command=lambda: on_choice('plant'))
pb.grid(row=0, column=1, padx=10)

sb = tk.Button(game_btn_frame, image=images['pests'], text='Pests', compound='top', width=100, height=110,
               relief='raised', bd=4, bg='#FFFFFF', command=lambda: on_choice('pests'))
sb.grid(row=0, column=2, padx=10)

back_container = make_bordered_button(game_frame, "Back", show_main)
back_container.place(relx=0.5, rely=0.78, anchor='n', relwidth=0.18, relheight=0.10)


options_frame = tk.Frame(root, bg="#4AFF4A")

opt1 = make_bordered_button(options_frame, "User Option", show_user_options)
opt1.place(relx=0.5, rely=0.22, anchor='n', relwidth=0.35, relheight=0.12)

opt2 = make_bordered_button(options_frame, "About Game", show_about)
opt2.place(relx=0.5, rely=0.44, anchor='n', relwidth=0.35, relheight=0.12)

opt_back = make_bordered_button(options_frame, "Back", show_main)
opt_back.place(relx=0.5, rely=0.66, anchor='n', relwidth=0.35, relheight=0.12)


about_frame = tk.Frame(root, bg="#F2F2F2")

about_title = tk.Label(about_frame, text="About Sun, Plant, Pests", font=("Impact", 18), bg="#F2F2F2", fg="#111111")
about_title.pack(pady=(20, 10))

about_outer = tk.Frame(about_frame, bg="black", bd=2)
about_outer.pack(padx=40, pady=(0, 20), fill="both", expand=True)

about_inner = tk.Frame(about_outer, bg="#FFFFFF")
about_inner.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

about_canvas = tk.Canvas(about_inner, bg="#FFFFFF", highlightthickness=0)
about_scrollbar = tk.Scrollbar(about_inner, orient="vertical", command=about_canvas.yview)
about_scrollable_frame = tk.Frame(about_canvas, bg="#FFFFFF")

about_scrollable_frame.bind(
    "<Configure>",
    lambda e: about_canvas.configure(scrollregion=about_canvas.bbox("all"))
)

about_canvas.create_window((0, 0), window=about_scrollable_frame, anchor="nw")
about_canvas.configure(yscrollcommand=about_scrollbar.set)

about_canvas.pack(side="left", fill="both", expand=True)
about_scrollbar.pack(side="right", fill="y")

placeholder_text = (
    """   
   Developer:
     - John Andrei E. Chan

   Subject/s:
     - Advance Computer Programming

   Professor/s:
     - Mr. Edbert Ocampo

   Tools:
     - Visual Studio Code (IDE)
     - Python (Programming Language)
     - Claude 4.5 Sonnet (LLM)

   Description:
     This educational game is designed
     for users of all ages to learn about
     Sustainable Development Goal 15: Life
     on Land. It demonstrates the cyclical
     relationships within land ecosystems.

     The game is inspired by the classic
     game Rock, Paper, Scissors, hence the
     name Sun, Plant, Pests. This familiar
     foundation allows users to quickly
     understand the gameplay mechanics, as
     it follows the same core logic as the
     original game.

   DISCLAIMER: 
   The Game developed with AI
   assistance, using Claude 4.5 Sonnet.

   DATE CREATED: November 2025
   """
)

about_text_label = tk.Label(
    about_scrollable_frame,
    text=placeholder_text,
    font=("Arial", 11),
    bg="#FFFFFF",
    fg="#111111",
    wraplength=360,
    justify="left"
)
about_text_label.pack(fill="both", expand=True, padx=10, pady=10)

about_back_btn = make_bordered_button(about_frame, "Back", show_options)
about_back_btn.pack(pady=(0, 30))


user_options_frame = tk.Frame(root, bg="#F2F2F2")

user_op1 = make_bordered_button(user_options_frame, "Add User", show_add_user)
user_op1.place(relx=0.07, rely=0.40, anchor='w', relwidth=0.2, relheight=0.1)

user_back = make_bordered_button(user_options_frame, "Back", show_options)
user_back.place(relx=0.07, rely=0.55, anchor='w', relwidth=0.2, relheight=0.1)

user_list_label = tk.Label(user_options_frame, text="Saved Users:", font=("Impact", 12), bg="#F2F2F2", fg="black")
user_list_label.place(relx=0.55, rely=0.15, anchor='w')

user_list_outer = tk.Frame(user_options_frame, bg="black", bd=2)
user_list_outer.place(relx=0.55, rely=0.22, anchor='nw', relwidth=0.4, relheight=0.6)

user_list_inner = tk.Frame(user_list_outer, bg="#FFFFFF")
user_list_inner.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

user_list_canvas = tk.Canvas(user_list_inner, bg="#FFFFFF", highlightthickness=0)
user_list_scrollbar = tk.Scrollbar(user_list_inner, orient="vertical", command=user_list_canvas.yview)
user_list_scrollable_frame = tk.Frame(user_list_canvas, bg="#FFFFFF")

user_list_scrollable_frame.bind(
    "<Configure>",
    lambda e: user_list_canvas.configure(scrollregion=user_list_canvas.bbox("all"))
)

user_list_canvas.create_window((0, 0), window=user_list_scrollable_frame, anchor="nw")
user_list_canvas.configure(yscrollcommand=user_list_scrollbar.set)

user_list_canvas.pack(side="left", fill="both", expand=True)
user_list_scrollbar.pack(side="right", fill="y")


add_user_frame = tk.Frame(root, bg="#F2F2F2")

entry_label = tk.Label(add_user_frame, text="Username:", font=("Arial", 12), bg="#F2F2F2", fg="black")
entry_label.place(relx=0.07, rely=0.20, anchor='w')

username_entry = tk.Entry(add_user_frame, font=("Arial", 12), width=20)
username_entry.place(relx=0.25, rely=0.25, anchor='n')

save_btn = make_bordered_button(add_user_frame, "Save", save_user)
save_btn.place(relx=0.07, rely=0.40, anchor='w', relwidth=0.15, relheight=0.08)

add_back_btn = make_bordered_button(add_user_frame, "Back", show_user_options)
add_back_btn.place(relx=0.07, rely=0.50, anchor='w', relwidth=0.15, relheight=0.08)

list_label = tk.Label(add_user_frame, text="Saved Users:", font=("Arial", 12), bg="#F2F2F2", fg="black")
list_label.place(relx=0.55, rely=0.15, anchor='w')

list_outer = tk.Frame(add_user_frame, bg="black", bd=2)
list_outer.place(relx=0.55, rely=0.22, anchor='nw', relwidth=0.4, relheight=0.6)

list_inner = tk.Frame(list_outer, bg="#FFFFFF")
list_inner.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

list_canvas = tk.Canvas(list_inner, bg="#FFFFFF", highlightthickness=0)
list_scrollbar = tk.Scrollbar(list_inner, orient="vertical", command=list_canvas.yview)
list_scrollable_frame = tk.Frame(list_canvas, bg="#FFFFFF")

list_scrollable_frame.bind(
    "<Configure>",
    lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
)

list_canvas.create_window((0, 0), window=list_scrollable_frame, anchor="nw")
list_canvas.configure(yscrollcommand=list_scrollbar.set)

list_canvas.pack(side="left", fill="both", expand=True)
list_scrollbar.pack(side="right", fill="y")



root.mainloop()