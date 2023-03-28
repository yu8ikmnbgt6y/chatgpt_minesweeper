import os
import json
import tkinter as tk
from tkinter import messagebox

DARK_GRAY = "#282828"
CHAT_BOARD_BG_COLOR = DARK_GRAY


CHAT_SETTINGS_FILE = "chat_settings.json"

DEFAULT_SETTINGS = {
    "max_tokens": "2048",
    "model": "gpt-3.5-turbo",
    "persona": "father",
    "persona_candidates": ["father", "mother", "teacher"],
    "character": "friendly",
    "character_candidates": ["friendly", "strict", "funny", "wise"]
}

MODEL_OPTIONS = [
    "gpt-4",
    "gpt-3.5-turbo"
]


def save_settings(settings):
    with open(CHAT_SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


def load_settings() -> dict:
    if os.path.exists(CHAT_SETTINGS_FILE):
        with open(CHAT_SETTINGS_FILE, "r") as f:
            settings = json.load(f)
    else:
        settings = DEFAULT_SETTINGS.copy()
    return settings


class  ChatSettingsWindow:
    def __init__(self, root):
        self._root = root
        self._chat_setting_window = None
        self.settings: dict = load_settings()
    
    @property
    def model(self):
        return str(self.settings["model"])

    @property
    def max_tokens(self):
        return int(self.settings["max_tokens"])
    
    @property
    def character(self):
        return str(self.settings["character"])
    
    @property
    def persona(self):
        return str(self.settings["persona"])

    
    @property
    def character_candidates(self):
        return self.settings["character_candidates"]


    def show_chat_settings_window(self):
        if self._chat_setting_window is not None:
            self._chat_setting_window.destroy()

        self._chat_settings_window = tk.Toplevel(self._root)
        self._chat_settings_window.title("Chat Settings")
        # self._chat_settings_window.resizable(False, False)

        frame_option_model = self._create_frame_option_model()
        frame_option_max_tokens = self._create_frame_option_max_tokens()
        frame_option_persona_settings = self._create_frame_option_persona_settings()
        frame_option_character_settings = self._create_frame_option_character_settings()
        frame_option_save_button = self._create_frame_option_save_button()
        

        frame_option_model.grid             (row=0, column=0, padx=10, pady=10, sticky="nsew")
        frame_option_max_tokens.grid        (row=1, column=0, padx=10, pady=10, sticky="nsew")
        frame_option_persona_settings.grid  (row=2, column=0, padx=10, pady=10, sticky="nsew")
        frame_option_character_settings.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        frame_option_save_button.grid       (row=4, column=0, padx=10, pady=10, sticky="nsew")


    def _create_frame_option_model(self):
        frame = tk.Frame(self._chat_settings_window)

        self.model_var = tk.StringVar()
        self.model_var.set(self.settings['model'])
        model_options = MODEL_OPTIONS

        model_option_label = tk.Label(frame, text="Model:")
        model_option_label.pack()
        model_option_menu = tk.OptionMenu(frame, self.model_var, *model_options)
        model_option_menu.pack()

        return frame

    def _create_frame_option_max_tokens(self):
        frame = tk.Frame(self._chat_settings_window)

        self.max_tokens_var = tk.StringVar()
        self.max_tokens_var.set(self.settings['max_tokens'])

        max_token_label = tk.Label(frame, text="Max Tokens:")
        max_token_label.pack()
        max_token_entry = tk.Entry(frame, textvariable=self.max_tokens_var)
        max_token_entry.pack()

        return frame

    def _create_frame_option_character_settings(self):
        frame = tk.Frame(self._chat_settings_window,)

        self.character_var = tk.StringVar()
        self.character_var.set(self.settings['character'])

        character_options = self.settings['character_candidates']

        character_option_label = tk.Label(frame, text="Character:")
        character_option_label.pack()
        character_option_menu = tk.OptionMenu(frame, self.character_var, *character_options)
        character_option_menu.pack()

        return frame
    
    def _create_frame_option_persona_settings(self):
        frame = tk.Frame(self._chat_settings_window)

        self.persona_var = tk.StringVar()
        self.persona_var.set(self.settings['persona'])
        persona_options = self.settings['persona_candidates']

        persona_option_label = tk.Label(frame, text="Persona:")
        persona_option_label.pack()
        persona_option_menu = tk.OptionMenu(frame, self.persona_var, *persona_options)
        persona_option_menu.pack()
        return frame

    def _create_frame_option_save_button(self):
        frame = tk.Frame(self._chat_settings_window)
        setting_save_button = tk.Button(frame, text="Save", command=self.save_settings)
        setting_save_button.pack()

        return frame

    def save_settings(self):
        try:
            max_tokens = int(self.max_tokens_var.get())
        except ValueError:
            messagebox.showerror("Error", "Max Tokens should be a number.")
            return

        if 50 <= max_tokens <= 4096:
            self.settings['max_tokens'] = max_tokens
        else:
            messagebox.showerror("Error", "Max Tokens should be between 50 and 4096.")
            return

        self.settings['model'] = self.model_var.get()
        self.settings['character'] = self.character_var.get()

        save_settings(self.settings)
