from client import main
import tkinter as tk


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.bind("<F11>", lambda event: root.attributes("-fullscreen",
                                                     not root.attributes("-fullscreen")))
    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
    buttonframe = tk.Frame(root)
    container = tk.Frame(root)
    buttonframe.pack(side="top", anchor="center")
    container.pack(side="top", fill="both", expand=True)
    main.create_page(container, buttonframe)
    root.wm_geometry("1700x1000")
    root.title("Pizza Store")
    root.iconbitmap('src/icons/pizza.ico')
    root.mainloop()
