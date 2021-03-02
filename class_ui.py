# class_ui.py

# UI
import tkinter as tk
from tkinter import messagebox as tkMessagebox
from tkinter import filedialog as tkFiledialog


class App():

    # CLASS VARIABLE - ls_mapping_options
    #   {"rb_display_text": "rb_value"} || {"display_text": "module_to_run"}
    # Option to dynamically add mapping options for future additions.
    # ls_mapping_options = [
    #     ("Dissertation", "dissertations"),
    #     ("Maps", "maps")
    #     ]

    def __init__(self, ls_mapping_options=None):
        self.ls_mapping_options = ls_mapping_options

        self.root = tk.Tk()

        # Setting Title
        self.root.title("MARC-to-CSV")

        # Setting Window Size
        width=300
        height=120

        # Centering window on screen
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=True, height=True)
        
        # Create Frames/Widgets
        self.create_input_widgets()
        self.create_mapping_widgets()
        self.create_action_widgets()
        
        # Start mainloop
        self.root.mainloop()

    # Collect input via:
    #   ENTRY - source file & BUTTON - filedialog
    #   ENTRY - output file
    def create_input_widgets(self):
        
        # FRAME - entry_frame1
        #   Containing (1) Lbl (2) Entry (3) Btn
        self.entry_frame1 = tk.Frame(self.root)
        self.entry_frame1.pack(padx=1, pady=1, anchor="w")
        
        # LABLE-ENTRY - lbl_source
        #   For entry_source_path
        self.lbl_source = tk.Label(
            self.entry_frame1,
            justify = "left",
            text = "Input source path:"
            )
        self.lbl_source.pack(side="left")

        # ENTRY - source_path_text
        #   User provided input for path the input file
        self.source_path_text = tk.StringVar()
        self.entry_source_path = tk.Entry(
            self.entry_frame1,
            justify = "left",
            textvariable = self.source_path_text,
            borderwidth = "1px"
            )
        self.entry_source_path.pack(side="left")

        # BUTTON - btn_select_source
        #   Open up filedialog to ask for file
        self.btn_select_source=tk.Button(
            self.entry_frame1,
            justify = "center",
            text = "Dialog",
            command = self.command_btn_select_source
            )
        self.btn_select_source.pack(side="right", padx=5)

        # FRAME - entry_frame2
        #   Containing (1) Lbl (2) Entry
        self.entry_frame2 = tk.Frame(self.root)
        self.entry_frame2.pack(padx=1, pady=1, anchor="w")

        # LABLE-ENTRY - lbl_output
        #   For entry_output_path
        self.lbl_output=tk.Label(
            self.entry_frame2,
            justify = "center",
            text = "Output Name:"
            )
        self.lbl_output.pack(side="left", padx=10)

        # ENTRY - entry_output_path
        #   User provided input for output path/name
        self.entry_output_path=tk.Entry(
            self.entry_frame2,
            justify = "left",
            text = "input_destination",
            borderwidth = "1px"
            )
        self.entry_output_path.pack(side="left")


    # Collect input via:
    #   RADIOBUTTON - mapping options
    def create_mapping_widgets(self):
        
        # FRAME - rad_frame
        #   containing (1) radiobutton(s)
        self.rad_frame = tk.Frame(self.root)
        self.rad_frame.pack(padx=1, pady=1, anchor="s")

        # Radiobutton - ()Dissertations, ()Maps
        self.var_rb_option = tk.StringVar()

        # Dynamically build RadioButton(s) based on class variable for mapping options.
        for display_text, rb_value in self.ls_mapping_options:
            self.rb = tk.Radiobutton(
                self.rad_frame,
                variable=self.var_rb_option,
                text = display_text,
                value = rb_value
                )
            self.rb.pack(side="left")
            self.var_rb_option.set(rb_value)


    # Wait for user interaction via:
    #   BUTTON - btn_start
    def create_action_widgets(self):
        # Frame - btn_frame
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(padx=1, pady=1, anchor="s")
        
        # Button - btn_start
        # Starts the process for running the appropriate mapping.
        self.btn_start=tk.Button(
            self.btn_frame,
            justify = "center",
            text = "START",
            command = self.command_btn_start
            )
        self.btn_start.pack(side="bottom", padx=10, pady=10)


    # COMMAND - command_btn_select_source
    #   Attached - btn_select_source
    #   What to do when btn is pressed.
    def command_btn_select_source(self):
        
        # FILEDIALOG - fd_source_path
        fd_source_path = tk.filedialog.askopenfilename(
            initialdir="/",
            title="Select a file",
            filetypes=(("MARC Files","*.bib;*.mrc"),("All Files","*.*")))
        # Update Entry Source Path Text
        self.source_path_text.set(fd_source_path)


    # COMMAND - command_btn_start
    #   Attached - btn_start
    #   What to do when btn is pressed.
    def command_btn_start(self):
        
        print("btn START clicked.")


        # TODO: Add in error checking before continuing with processing.
        #   -Check if file is already exists, ask if want to append or cancel.
        
        # TODO: Create dynamic 'kick-off' based on the CLASS VARIABLE.


        # # Capture user provide input and save to variables.
        self.input_path = self.entry_source_path.get()
        self.output_path = self.entry_output_path.get()

        # # Choose which mapping to use based on RADIOBOX.
        self.mapping = self.var_rb_option.get()

        # # HACK: Dynamically execute method based on ls_mapping_options to run
        # if selected_option is not None:
        #     exec(
        #         """{mapping_to_run}(extract_from=r"{input_path}", save_name="{output_path}")
        #         """.format(mapping_to_run=selected_option, input_path=input_path, output_path=output_path)
        #         )
        #     tk.messagebox.showinfo(
        #     'Complete',
        #     "Mapping: '{mapping_text}' ran.".format(mapping_text=selected_option)
        #     )
        # else:
        #     tk.messagebox.showinfo(
        #     'Error',
        #     "Please select a process from the radiobox"
        #     )
        self.root.destroy()
        self.root.quit()
