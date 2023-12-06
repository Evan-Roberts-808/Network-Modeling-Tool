import tkinter as tk
from resources.visualize import NetworkApp

def main():
    root = tk.Tk()
    app = NetworkApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()