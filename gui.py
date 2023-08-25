import customtkinter
import os
from PIL import Image


class Gui(customtkinter.CTk):
    def __init__(app):
        super().__init__()

        app.title("Fortigate Programming")
        app.geometry("700x570")

        # set grid layout 1x2
        app.grid_rowconfigure(0, weight=1)
        app.grid_columnconfigure(1, weight=1)

        # create navigation frame
        app.navigation_frame = customtkinter.CTkFrame(app, corner_radius=0)
        app.navigation_frame.grid(row=0, column=0, sticky="nsew")
        app.navigation_frame.grid_rowconfigure(4, weight=1)

        app.navigation_frame_label = customtkinter.CTkLabel(app.navigation_frame, text="  Fortigate Programming", compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        app.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        app.ip_information_button = customtkinter.CTkButton(app.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="IP Information",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=app.ip_information_button_event)
        app.ip_information_button.grid(row=1, column=0, sticky="ew")

        app.frame_2_button = customtkinter.CTkButton(app.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=app.frame_2_button_event)
        app.frame_2_button.grid(row=2, column=0, sticky="ew")

        app.frame_3_button = customtkinter.CTkButton(app.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=app.frame_3_button_event)
        app.frame_3_button.grid(row=3, column=0, sticky="ew")

        app.appearance_mode_menu = customtkinter.CTkOptionMenu(app.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=app.change_appearance_mode_event)
        app.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create ip_information frame
        app.ip_information_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="transparent")
        app.ip_information_frame.grid_columnconfigure(0, weight=1)

        app.ip_information_entry1 = customtkinter.CTkEntry(app.ip_information_frame, placeholder_text="Fortigate Hostname ex Entre-60F")
        app.ip_information_entry1.grid(row=1, column=0, columnspan=2, padx=(40, 40), pady=(20, 0), sticky="nsew")

        app.ip_information_entry2 = customtkinter.CTkEntry(app.ip_information_frame, placeholder_text="Usable Public IP Address for Fortigate")
        app.ip_information_entry2.grid(row=2, column=0, columnspan=2, padx=(40, 40), pady=(10, 0), sticky="nsew")

        app.ip_information_entry3 = customtkinter.CTkEntry(app.ip_information_frame, placeholder_text="Public Gateway for the Modem")
        app.ip_information_entry3.grid(row=3, column=0, columnspan=2, padx=(40, 40), pady=(10, 0), sticky="nsew")

        app.ip_information_entry4 = customtkinter.CTkEntry(app.ip_information_frame, placeholder_text="Public Subnet Mask ex 255.255.255.252")
        app.ip_information_entry4.grid(row=4, column=0, columnspan=2, padx=(40, 40), pady=(10, 0), sticky="nsew")

        app.ip_information_entry5 = customtkinter.CTkEntry(app.ip_information_frame, placeholder_text="LAN IP for Fortigate ex 192.168.1.254")
        app.ip_information_entry5.grid(row=5, column=0, columnspan=2, padx=(40, 40), pady=(10, 0), sticky="nsew")

        app.ip_information_entry6 = customtkinter.CTkEntry(app.ip_information_frame, placeholder_text="LAN Subnet ex 255.255.255.0")
        app.ip_information_entry6.grid(row=6, column=0, columnspan=2, padx=(40, 40), pady=(10, 0), sticky="nsew")

        app.ip_information_entry7 = customtkinter.CTkEntry(app.ip_information_frame, placeholder_text="DHCP First IP ex 192.168.1.100")
        app.ip_information_entry7.grid(row=7, column=0, columnspan=2, padx=(40, 40), pady=(10, 0), sticky="nsew")

        app.ip_information_entry8 = customtkinter.CTkEntry(app.ip_information_frame, placeholder_text="DHCP Last IP ex 192.168.1.199")
        app.ip_information_entry8.grid(row=8, column=0, columnspan=2, padx=(40, 40), pady=(10, 0), sticky="nsew")

        app.ip_information_entry9 = customtkinter.CTkEntry(app.ip_information_frame, placeholder_text="DHCP First IP ex 192.168.1.100")
        app.ip_information_entry9.grid(row=9, column=0, columnspan=2, padx=(40, 40), pady=(10, 0), sticky="nsew")

        app.ip_information_entry10 = customtkinter.CTkEntry(app.ip_information_frame, placeholder_text="Primary DNS IP ex 192.168.1.254")
        app.ip_information_entry10.grid(row=10, column=0, columnspan=2, padx=(40, 40), pady=(10, 0), sticky="nsew")

        app.ip_information_entry11 = customtkinter.CTkEntry(app.ip_information_frame, placeholder_text="Second DNS IP ex 192.168.1.254")
        app.ip_information_entry11.grid(row=11, column=0, columnspan=2, padx=(40, 40), pady=(10, 0), sticky="nsew")

        app.ip_information_entry12 = customtkinter.CTkEntry(app.ip_information_frame, placeholder_text="Third DNS IP ex 192.168.1.254")
        app.ip_information_entry12.grid(row=12, column=0, columnspan=2, padx=(40, 40), pady=(10, 0), sticky="nsew")

        app.ip_information_entry13 = customtkinter.CTkEntry(app.ip_information_frame, placeholder_text="Local domain ex entre.local")
        app.ip_information_entry13.grid(row=13, column=0, columnspan=2, padx=(40, 40), pady=(10, 0), sticky="nsew")

        app.ip_information_button01 = customtkinter.CTkButton(app.ip_information_frame, text="Load Defaults")
        app.ip_information_button01.grid(row=15, column=0, padx=(0,0), pady=(20,0))
        
        # create Port Forward frame
        app.port_forward_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="transparent")

        # create third frame
        app.third_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="transparent")

        # select default frame
        app.select_frame_by_name("ip_information")

    def select_frame_by_name(app, name):
        # set button color for selected button
        app.ip_information_button.configure(fg_color=("gray75", "gray25") if name == "ip_information" else "transparent")
        app.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        app.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "ip_information":
            app.ip_information_frame.grid(row=0, column=1, sticky="nsew")
        else:
            app.ip_information_frame.grid_forget()
        if name == "frame_2":
            app.port_forward_frame.grid(row=0, column=1, sticky="nsew")
        else:
            app.port_forward_frame.grid_forget()
        if name == "frame_3":
            app.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            app.third_frame.grid_forget()

    def ip_information_button_event(app):
        app.select_frame_by_name("ip_information")

    def frame_2_button_event(app):
        app.select_frame_by_name("frame_2")

    def frame_3_button_event(app):
        app.select_frame_by_name("frame_3")

    def change_appearance_mode_event(app, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = Gui()
    app.mainloop()

