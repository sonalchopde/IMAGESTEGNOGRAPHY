import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image


# Function to encode a message into an image
from PIL import Image
from tkinter import messagebox

def encode_message(img_path, message):
    img = Image.open(img_path)
    width, height = img.size

    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Check if the image can hold the message
    max_chars = (width * height * 3) // 8
    if len(binary_message) > max_chars:
        messagebox.showerror("Error", "Message too long for the selected image.")
        return

    data_index = 0
    for y in range(height):
        for x in range(width):
            if data_index < len(binary_message):
                r, g, b = img.getpixel((x, y))

                # Modify red, green, and blue values only if there are enough bits left in the binary message
                r = r & ~1 | int(binary_message[data_index]) if data_index < len(binary_message) else r
                g = g & ~1 | int(binary_message[data_index + 1]) if data_index + 1 < len(binary_message) else g
                b = b & ~1 | int(binary_message[data_index + 2]) if data_index + 2 < len(binary_message) else b

                img.putpixel((x, y), (r, g, b))
                data_index += 3
            else:
                img.save("encoded_image.png")
                messagebox.showinfo("Success", "Message encoded successfully.")
                return

    # Save image if message was encoded in the entire image
    img.save("encoded_image.png")
    messagebox.showinfo("Success", "Message encoded successfully.")


# Function to decode a message from an image
def decode_message(img_path):
    img = Image.open(img_path)
    width, height = img.size

    binary_message = ''
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            binary_message += str(r & 1)
            binary_message += str(g & 1)
            binary_message += str(b & 1)

    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte:
            message += chr(int(byte, 2))
        else:
            break

    messagebox.showinfo("Decoded Message", message)

# GUI
root = tk.Tk()
root.title("Image Steganography")

# Function to open file dialog for selecting image
def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)

# Function to encode message
def encode():
    img_path = entry_path.get()
    message = entry_message.get("1.0", tk.END)
    if img_path and message:
        encode_message(img_path, message.strip())
    else:
        messagebox.showerror("Error", "Please select an image and enter a message.")

# Function to decode message
def decode():
    img_path = entry_path.get()
    if img_path:
        decode_message(img_path)
    else:
        messagebox.showerror("Error", "Please select an image.")

# Widgets
label_path = tk.Label(root, text="Image Path:")
label_path.grid(row=0, column=0, padx=5, pady=5)

entry_path = tk.Entry(root, width=50)
entry_path.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

button_browse = tk.Button(root, text="Browse", command=select_image)
button_browse.grid(row=0, column=3, padx=5, pady=5)

label_message = tk.Label(root, text="Message:")
label_message.grid(row=1, column=0, padx=5, pady=5)

entry_message = tk.Text(root, width=50, height=10)
entry_message.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

button_encode = tk.Button(root, text="Encode", command=encode)
button_encode.grid(row=2, column=1, padx=5, pady=5)

button_decode = tk.Button(root, text="Decode", command=decode)
button_decode.grid(row=2, column=2, padx=5, pady=5)

root.mainloop()
