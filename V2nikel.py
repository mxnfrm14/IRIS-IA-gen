import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from llama_cpp import Llama
import threading
import time

# Initialize CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class LoadingDots(ctk.CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dots = ""
        self.is_running = False
        
    def start(self):
        self.is_running = True
        self.update_dots()
        
    def stop(self):
        self.is_running = False
        self.configure(text="")
        
    def update_dots(self):
        if not self.is_running:
            return
            
        self.dots = self.dots + "." if len(self.dots) < 3 else ""
        self.configure(text=f"En train de réfléchir{self.dots}")
        self.after(500, self.update_dots)

class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Initialize the model at the start
        self.model = Llama(model_path="Models/qwen2.5-0.5b-instruct-q5_k_m.gguf")
        self.is_generating = False

        # Main window configuration
        self.title("IRIS Chatbot")
        self.geometry(f"{1100}x{580}")

        # Grid configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Sidebar components
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="IRIS", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="Question sur le fichier", 
                                            command=self.sidebar_button_event, 
                                            fg_color="#A075AD", hover_color="#88419D")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="Button 2", 
                                            command=self.sidebar_button_event, 
                                            fg_color="#A075AD", hover_color="#88419D")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, text="Réponses sécurisés", 
                                            command=self.sidebar_button_event, 
                                            fg_color="#A075AD", hover_color="#88419D")
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        # Appearance settings
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, 
                                                           values=["System", "Light", "Dark"],
                                                           fg_color="#A075AD",
                                                           button_color="#A075AD",
                                                           button_hover_color="#88419D",
                                                           command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # UI Scaling settings
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame,
                                                    values=["80%", "90%", "100%", "110%", "120%"],
                                                    fg_color="#A075AD",
                                                    button_color="#A075AD",
                                                    button_hover_color="#88419D",
                                                    command=self.change_scaling_event)
        self.scaling_optionemenu.set("100%")
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Chat display area
        self.chat_display = ctk.CTkTextbox(self, width=480, height=350)
        self.chat_display.grid(row=0, column=1, columnspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Loading indicator
        self.loading_indicator = LoadingDots(self, text="")
        self.loading_indicator.grid(row=2, column=1, padx=(20, 0), pady=(0, 0), sticky="w")

        try:
            # Load paperclip image
            self.trombone_image = Image.open("trombone.png")
            self.trombone_image = self.trombone_image.resize((20, 20), Image.LANCZOS)
            self.trombone_icon = ImageTk.PhotoImage(self.trombone_image)

            # Create file import button
            self.file_import_button = ctk.CTkButton(self, text="", image=self.trombone_icon, 
                                                  width=40, height=40,
                                                  fg_color="transparent", hover_color="#D3D3D3",
                                                  command=self.import_file)
            self.file_import_button.grid(row=3, column=2, padx=(10, 0), pady=(20, 20), sticky="ew")
        except FileNotFoundError:
            print("Warning: trombone.png not found. File import button will not have an icon.")
            self.file_import_button = ctk.CTkButton(self, text="📎", 
                                                  width=40, height=40,
                                                  fg_color="transparent", hover_color="#D3D3D3",
                                                  command=self.import_file)
            self.file_import_button.grid(row=3, column=2, padx=(10, 0), pady=(20, 20), sticky="ew")

        # User input field
        self.user_input = ctk.CTkEntry(self, placeholder_text="Entrez votre message ici...")
        self.user_input.grid(row=3, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # Send button
        self.send_button = ctk.CTkButton(self, text="Envoyer", 
                                       command=self.send_message, 
                                       fg_color="#A075AD", 
                                       hover_color="#88419D")
        self.send_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Bind Enter key to send message
        self.user_input.bind("<Return>", lambda event: self.send_message())

    def send_message(self):
        if self.is_generating:
            return

        user_message = self.user_input.get()
        if user_message:
            # Disable input and button while generating
            self.user_input.configure(state="disabled")
            self.send_button.configure(state="disabled")
            
            # Display user message
            self.chat_display.insert(ctk.END, f"Vous: {user_message}\n")
            self.chat_display.see(ctk.END)
            
            # Clear input field
            self.user_input.delete(0, ctk.END)
            
            # Start loading animation
            self.is_generating = True
            self.loading_indicator.start()
            
            # Start generation in separate thread
            threading.Thread(target=self.generate_response, args=(user_message,), daemon=True).start()

    def generate_response(self, message):
        try:
            # Generate response
            response = self.model(message, max_tokens=2048)
            bot_response = response["choices"][0]["text"].strip()
            
            # Schedule the response update in the main thread
            self.after(0, self.update_chat_with_response, bot_response)
            
        except Exception as e:
            self.after(0, self.update_chat_with_response, f"Erreur: {str(e)}")
        
        finally:
            # Re-enable input and button, stop loading animation
            self.after(0, self.finish_generation)

    def update_chat_with_response(self, response):
        self.chat_display.insert(ctk.END, f"Bot: {response}\n\n")
        self.chat_display.see(ctk.END)

    def finish_generation(self):
        self.is_generating = False
        self.loading_indicator.stop()
        self.user_input.configure(state="normal")
        self.send_button.configure(state="normal")
        self.user_input.focus()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def import_file(self):
        file_path = filedialog.askopenfilename(title="Sélectionner un fichier")
        if file_path:
            self.chat_display.insert(ctk.END, f"Fichier importé: {file_path}\n")
            self.chat_display.see(ctk.END)

if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()