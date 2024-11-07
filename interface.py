import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

import torch
from llama_cpp import Llama

# Initialiser CustomTkinter
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Thèmes: "blue" (standard), "green", "dark-blue"

class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.title("IRIS Chatbot")  # Titre de la fenêtre   
        self.geometry(f"{1100}x{580}")

        # Configuration de la disposition de la fenêtre
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Créer la sidebar (menu de gauche)
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="IRIS", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="Question sur le fichier", command=self.sidebar_button_event, fg_color="#A075AD", hover_color="#88419D")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="Button 2", command=self.sidebar_button_event , fg_color="#A075AD", hover_color="#88419D")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, text="Réponses sécurisés", command=self.sidebar_button_event , fg_color="#A075AD", hover_color="#88419D")
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["System","Light", "Dark"],
                                                            fg_color="#A075AD",           # Couleur du fond
                                                            button_color="#A075AD",       # Couleur du bouton
                                                            button_hover_color="#88419D", # Couleur du bouton au survol
                                                            command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        default_scaling_value = tk.StringVar(value="100%")
        self.scaling_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            fg_color="#A075AD",           # Couleur du fond
            button_color="#A075AD",       # Couleur du bouton
            button_hover_color="#88419D", # Couleur du bouton au survol
            command=self.change_scaling_event,
            variable=default_scaling_value
        )
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Créer la zone d'affichage pour les messages
        self.chat_display = ctk.CTkTextbox(self, width=480, height=350)
        self.chat_display.grid(row=0, column=1, columnspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Charger l'image du trombone
        self.trombone_image = Image.open("trombone.png")
        self.trombone_image = self.trombone_image.resize((20, 20), Image.LANCZOS)  # Utiliser LANCZOS à la place de ANTIALIAS
        self.trombone_icon = ImageTk.PhotoImage(self.trombone_image)

        # Créer un bouton rond pour importer des fichiers à gauche du champ de saisie
        self.file_import_button = ctk.CTkButton(self, text="", image=self.trombone_icon, width=40, height=40,
                                                fg_color="transparent", hover_color="#D3D3D3",
                                                command=self.import_file)
        self.file_import_button.grid(row=3, column=2, padx=(10, 0), pady=(20, 20), sticky="ew")

        # Créer un champ d'entrée pour les messages de l'utilisateur
        self.user_input = ctk.CTkEntry(self, placeholder_text="Entrez votre message ici...")
        self.user_input.grid(row=3, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # Créer un bouton pour envoyer le message
        self.send_button = ctk.CTkButton(self, text="Envoyer", command=self.send_message, fg_color="#A075AD", bg_color="#88419D")
        self.send_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def send_message(self):
        user_message = self.user_input.get()
        if user_message:
            self.chat_display.insert(ctk.END, f"Vous: {user_message}\n")
            bot_response = self.get_bot_response(user_message)
            self.chat_display.insert(ctk.END, f"Bot: {bot_response}\n")
            self.user_input.delete(0, ctk.END)


    # Charger le modèle GGUF localement
    self.model = Llama(model_path="Models/qwen2.5-0.5b-instruct-q5_k_m.gguf")

    def get_bot_response(self, message):
        # if "bonjour" in message.lower():
        #     return "Bonjour! Comment puis-je vous aider?"
        # elif "comment ça va" in message.lower():
        #     return "Je suis un bot, donc je ne ressens pas d'émotions, mais merci de demander!"
        # else:
        #     return "Je ne suis pas sûr de comprendre. Pouvez-vous reformuler?"
        response = self.model(message)
        return response["choices"][0]["text"].strip()
        

    def get_bot_response(self, message):
        # Générer la réponse en utilisant le modèle Qwen
        response = self.model(message)
        return response["choices"][0]["text"].strip()

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

# Lancer l'application
if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
