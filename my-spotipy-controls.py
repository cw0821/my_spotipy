import tkinter as tk

# Conversion: 1 inch = 96 pixels (at 96 DPI)
DPI = 96
rect_width = int(1 * DPI)      # 1 inch wide
rect_height = int(0.5 * DPI)   # 0.5 inch tall
rect2_width = int(2 * DPI)     # 2 inches wide
rect2_height = rect_height     # 0.5 inch tall

# Create main window
root = tk.Tk()
root.title("Three Rectangles")

# Padding around drawings
padding = 40

# Calculate canvas size based on shapes
canvas_width = rect2_width + padding
canvas_height = rect_height * 2 + rect2_height + padding

# Create canvas just large enough
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Calculate center coordinates
center_x = canvas_width // 2
center_y = canvas_height // 3   # move rectangles a bit up

# Left rectangle coordinates (blue)
left_x1 = center_x - rect_width
left_y1 = center_y - rect_height // 2
left_x2 = center_x
left_y2 = center_y + rect_height // 2

# Right rectangle coordinates (green)
right_x1 = center_x
right_y1 = center_y - rect_height // 2
right_x2 = center_x + rect_width
right_y2 = center_y + rect_height // 2

# Grey rectangle coordinates (hidden initially, placed below)
grey_x1 = center_x - rect2_width // 2
grey_y1 = center_y + rect_height // 2 + 20
grey_x2 = center_x + rect2_width // 2
grey_y2 = grey_y1 + rect2_height

# Draw rectangles
blue_rect = canvas.create_rectangle(left_x1, left_y1, left_x2, left_y2, fill="light blue", outline="black")
green_rect = canvas.create_rectangle(right_x1, right_y1, right_x2, right_y2, fill="light green", outline="black")
grey_rect = canvas.create_rectangle(grey_x1, grey_y1, grey_x2, grey_y2, fill="light grey", outline="black", state="hidden")

# Add texts (initially hidden)
blue_text = canvas.create_text((left_x1 + left_x2) // 2, (left_y1 + left_y2) // 2,
                               text="BLUE", fill="black", font=("Arial", 16, "bold"), state="hidden")
green_text = canvas.create_text((right_x1 + right_x2) // 2, (right_y1 + right_y2) // 2,
                                text="GREEN", fill="black", font=("Arial", 16, "bold"), state="hidden")

# Track hover state
hovering = {"blue": False, "green": False, "grey": False}

def update_visibility():
    if hovering["blue"] or hovering["green"] or hovering["grey"]:
        canvas.itemconfigure(grey_rect, state="normal")
    else:
        canvas.itemconfigure(grey_rect, state="hidden")

def show_blue(event):
    hovering["blue"] = True
    canvas.itemconfigure(blue_text, state="normal")
    update_visibility()

def hide_blue(event):
    hovering["blue"] = False
    canvas.itemconfigure(blue_text, state="hidden")
    update_visibility()

def show_green(event):
    hovering["green"] = True
    canvas.itemconfigure(green_text, state="normal")
    update_visibility()

def hide_green(event):
    hovering["green"] = False
    canvas.itemconfigure(green_text, state="hidden")
    update_visibility()

def enter_grey(event):
    hovering["grey"] = True
    update_visibility()

def leave_grey(event):
    hovering["grey"] = False
    update_visibility()

# Bind hover events
canvas.tag_bind(blue_rect, "<Enter>", show_blue)
canvas.tag_bind(blue_rect, "<Leave>", hide_blue)
canvas.tag_bind(green_rect, "<Enter>", show_green)
canvas.tag_bind(green_rect, "<Leave>", hide_green)
canvas.tag_bind(grey_rect, "<Enter>", enter_grey)
canvas.tag_bind(grey_rect, "<Leave>", leave_grey)

root.mainloop()
