# UI
import tkinter as tk
from tkinter import messagebox as tkMessagebox

# Custom local libraries
from Crosswalk_Dissertations import process_marc as dissertation
# from Crosswalk_Maps


class App:
    def __init__(self):
        self.root = tk.Tk()
        # Setting title
        self.root.title("MARC-to-CSV")
        # Setting window size
        width=700
        height=350
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=True, height=True)

        # Entry - User provided input for INPUT FILE
        self.entry_source_path=tk.Entry(
            self.root,
            justify = "left",
            text = "input_source",
            borderwidth = "1px"
            )
        self.entry_source_path.place(x=150,y=40,width=430,height=25)
        
        lbl_source=tk.Label(
            self.root,
            justify = "center",
            text = "Source Path:"
            )
        lbl_source.place(x=50,y=40,width=100,height=25)

        # Entry - User provided input for OUTPUT FILE
        self.entry_output_path=tk.Entry(
            self.root,
            justify = "left",
            text = "input_destination",
            borderwidth = "1px"
            )
        self.entry_output_path.place(x=150,y=80,width=430,height=25)

        lbl_output=tk.Label(
            self.root,
            justify = "center",
            text = "Output Name:"
            )
        lbl_output.place(x=50,y=80,width=100,height=25)

        # Radio Button - ()Dissertations, ()Maps
        self.rad_option = tk.StringVar()
        self.rad_option.set("dissertation")
        self.ra=tk.Radiobutton(
            self.root,
            text="Dissertations",
            variable=self.rad_option,
            value="dissertation",
            justify="left"
            )
        self.ra.place(x=150,y=150,width=150,height=50)
        self.rb=tk.Radiobutton(
            self.root,
            text="Maps",
            variable=self.rad_option,
            value="map",
            justify="left"
            )
        self.rb.place(x=150,y=200,width=150,height=50)

        # Button - Start
        self.btn_start=tk.Button(
            self.root,
            justify = "center",
            text = "START",
            command = self.btn_start_command
            )
        self.btn_start.place(x=150,y=270,width=150,height=45)

        # Button - Exit
        self.btn_Exit=tk.Button(
            self.root,
            justify = "center",
            text = "EXIT",
            command = self.btn_Exit_command
            )
        self.btn_Exit.place(x=420,y=270,width=124,height=44)

        # Start Mainloop
        self.root.mainloop()


    def btn_start_command(self):
        print("btn START clicked.")

        input_path = self.entry_source_path.get()
        output_path = self.entry_output_path.get()

        # Choose which instructions to use based on RADIO BOX
        selected_option = self.rad_option.get()

        if selected_option == "dissertation":
            dissertation(extract_from=input_path, save_name=output_path)
            tkMessagebox.showinfo('Complete', "Operation finished running.")
        elif selected_option == "map":
            # TO-DO

            tkMessagebox.showinfo('Complete', "Operation finished running.")
        else:
            tkMessagebox.showinfo('Error', "Please select a process from the radiobox")


    def btn_Exit_command(self):
        print("Exiting Application.")
        self.root.destroy()