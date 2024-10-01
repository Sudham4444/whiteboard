from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab

# Initialize root window
root = Tk()
root.title("whiteboard | sudham")
root.geometry("1100x700")
root.configure(bg="#f2f3f5")
root.resizable(True, True)

current_x = 0
current_y = 0
color = 'black'
image_objects = []  # List to store image objects for movement
current_mode = "draw"  # Current mode (draw or move)

# Define functions
def locate_xy(event):
    global current_x, current_y
    current_x = event.x
    current_y = event.y

def add_line(event):
    if current_mode == "draw":
        global current_x, current_y
        canvas.create_line((current_x, current_y, event.x, event.y), width=get_current_value(), fill=color,
                           capstyle=ROUND, smooth=TRUE)
        current_x, current_y = event.x, event.y

def show_color(new_color):
    global color
    color = new_color

def new_canvas():
    canvas.delete('all')
    display_palette()

def save_canvas():
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    if file_path:
        x = root.winfo_rootx() + canvas.winfo_x()
        y = root.winfo_rooty() + canvas.winfo_y()
        x1 = x + canvas.winfo_width()
        y1 = y + canvas.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)

# Color palette setup
colors = ['black', 'gray', 'brown4', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink']

def display_palette():
    color_palette.delete("all")  # Clear previous colors
    for idx, col in enumerate(colors):
        id = color_palette.create_rectangle((10, 10 + idx*30, 30, 30 + idx*30), fill=col)
        color_palette.tag_bind(id, '<Button-1>', lambda x, col=col: show_color(col))

color_palette = Canvas(root, bg="#ffffff", width=40, height=330, bd=0)
color_palette.grid(row=0, column=0, padx=10, pady=20, sticky='n')

# Display the initial palette
display_palette()

# Canvas for drawing
canvas = Canvas(root, width=900, height=500, background="white", cursor="hand2")
canvas.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')

canvas.bind('<Button-1>', locate_xy)
canvas.bind('<B1-Motion>', add_line)

# Ensure the canvas expands when resizing
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Thickness slider
current_value = DoubleVar()

def get_current_value():
    return '{:.2f}'.format(current_value.get())

def slider_changed(event):
    value_label.configure(text=get_current_value())

slider = ttk.Scale(root, from_=1, to=10, orient='horizontal', command=slider_changed, variable=current_value)
slider.grid(row=1, column=1, sticky='w', padx=20, pady=10)

value_label = ttk.Label(root, text=get_current_value())
value_label.grid(row=1, column=1, sticky='w', padx=150, pady=10)

# Save Button
save_btn = ttk.Button(root, text="Save", command=save_canvas)
save_btn.grid(row=2, column=0, padx=10, pady=10, sticky='w')

# New Canvas (Eraser) Button
eraser = PhotoImage(file="eraser.png")
clear_btn = ttk.Button(root, image=eraser, command=new_canvas)
clear_btn.grid(row=2, column=1, padx=10, pady=10, sticky='w')

# Color Picker Button
color_picker_btn = ttk.Button(root, text="Choose Color", command=lambda: show_color(askcolor()[1]))
color_picker_btn.grid(row=1, column=0, padx=10, pady=10)

# Add Image Button
def add_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((300, 300))  # Resize the image
        img_tk = ImageTk.PhotoImage(img)
        img_id = canvas.create_image(current_x, current_y, image=img_tk, anchor='nw')
        image_objects.append((img_tk, img_id))  # Store the reference to avoid garbage collection

def move_image(event):
    if current_mode == "move":
        img_id = canvas.find_withtag(CURRENT)[0]  # Get the ID of the currently selected image
        canvas.move(img_id, event.x - current_x, event.y - current_y)  # Move the image
        locate_xy(event)  # Update the current_x and current_y for movement

# Bind the move_image function to the canvas if in move mode
canvas.bind('<B1-Motion>', move_image)

# Mode Toggle Button
def toggle_mode():
    global current_mode
    if current_mode == "draw":
        current_mode = "move"
        toggle_btn.config(text="Switch to Draw Mode")
        canvas.bind('<B1-Motion>', move_image)  # Bind move_image when in move mode
    else:
        current_mode = "draw"
        toggle_btn.config(text="Switch to Move Mode")
        canvas.bind('<B1-Motion>', add_line)  # Bind add_line when in draw mode

toggle_btn = ttk.Button(root, text="Switch to Move Mode", command=toggle_mode)
toggle_btn.grid(row=1, column=1, padx=10, pady=10)

# Add Image Button
add_image_btn = ttk.Button(root, text="Add Image", command=add_image)
add_image_btn.grid(row=2, column=1, padx=10, pady=10, sticky='e')

# Make window elements resizable
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

root.mainloop()
