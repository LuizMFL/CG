import tkinter as tk
from PIL import Image, ImageTk

# create the main window
root = tk.Tk()

# create a canvas
canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()
img = Image.new('RGB', (100, 100), 'black')
img = img.resize((300,300))
img = ImageTk.PhotoImage(img)
# load the image

# add the image to the canvas
canvas.create_image(0, 0, anchor="nw", image=img)

# add a button on top of the image
button = tk.Button(root, text="Click Me!", command=lambda: root.quit())
button_window = canvas.create_window(50, 50, anchor="nw", window=button)

# run the main loop
root.mainloop()