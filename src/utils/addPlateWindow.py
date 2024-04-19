import customtkinter as ctk
from utils import text_utils


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        x = (1024 - 300) // 2
        y = (720 - 600) // 2
        self.geometry(f"300x600+{x}+{y}")
        self.title("Placas")
        self.resizable(False, False)
        self.radiobutton_variable = ctk.StringVar()
        self.button_list = []
        self.checkbox_list = []
        self.components()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.load_data()

    def on_closing(self):
        self.save_data()
        self.destroy()

    def add_plate_code(self):
        string = self.plate_input.get().upper()
        self.plate_input.delete(first_index=0, last_index=100)
        if textUtils.is_valid_license_plate(string):
            self.add_item(string)
            self.alert_label.configure(text="Adicionado")
            self.alert_label.configure(text_color="#44fa41")
            self.alert_label.place(in_=self, x=80, y=500)
            self.after(3000, self.alert_label.place_forget)
        else:
            self.alert_label.configure(text="Formato incorreto")
            self.alert_label.configure(text_color="#ff554f")
            self.alert_label.place(in_=self, x=80, y=500)
            self.after(3000, self.alert_label.place_forget)

    def upper_text(self, event):
        self.entry_text.set(self.entry_text.get().upper())

    def components(self):
        self.entry_text = ctk.StringVar()
        self.title = ctk.CTkLabel(self, text="Status\t Codigo ")
        self.scrollable_list = ctk.CTkScrollableFrame(
            master=self, width=265, height=480
        )
        self.plate_input = ctk.CTkEntry(
            self,
            placeholder_text="Codigo da placa",
            width=190,
            height=40,
            font=ctk.CTkFont(size=20),
            textvariable=self.entry_text,
        )
        self.plate_input.bind("<KeyRelease>", self.upper_text)

        self.add_button = ctk.CTkButton(
            self, text="Adicionar", width=90, height=40, command=self.add_plate_code
        )
        self.alert_label = ctk.CTkLabel(
            self,
            text="",
            width=140,
            font=ctk.CTkFont(size=16),
            text_color="#3d3c3c",
            corner_radius=10,
            fg_color="#3d3c3c",
        )

        self.title.place(in_=self, x=10, y=10)
        self.scrollable_list.grid_columnconfigure(0, weight=1)
        self.scrollable_list.grid(
            row=0, column=2, padx=10, pady=(40, 10), sticky="nsew"
        )
        self.plate_input.place(in_=self, x=10, y=540)
        self.add_button.place(in_=self, x=200, y=540)

    def load_data(self):
        try:
            with open("data.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    data = line.split(":")
                    self.add_item(data[1], data[0])
        except FileNotFoundError as e:
            print("Erro ao abrir o arquivo: ", e)

    def save_data(self):
        try:
            plate_code_list = []
            with open("data.txt", "w") as file:
                for checkbox in self.checkbox_list:
                    file.write(f"{checkbox.get()}:{checkbox.cget('text')}\n")
                    if checkbox.get() == 1:
                        plate_code_list.append(checkbox.cget("text"))
            return plate_code_list

        except FileNotFoundError as e:
            print("Erro ao gravar o arquivo: ", e)

    def add_item(self, item, state=1):
        checkbox = ctk.CTkCheckBox(
            self.scrollable_list,
            text=item,
            font=ctk.CTkFont(size=20),
            text_color_disabled="#707070",
        )
        button = ctk.CTkButton(
            self.scrollable_list,
            text="Remover",
            width=100,
            font=ctk.CTkFont(size=16),
            height=30,
            fg_color="#f5503d",
            hover_color="#fc270f",
        )
        button.configure(command=lambda: self.remove_item(item))
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)

        if state == "1":
            checkbox.select()

        self.checkbox_list.append(checkbox)
        self.button_list.append(button)

    def remove_item(self, item):
        for checkbox, button in zip(self.checkbox_list, self.button_list):
            if item == checkbox.cget("text"):
                checkbox.destroy()
                button.destroy()
                self.checkbox_list.remove(checkbox)
                self.button_list.remove(button)
                return
