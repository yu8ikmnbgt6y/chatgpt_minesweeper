import os
import tkinter as tk
from typing import Dict
from tkinter import messagebox
import openai
from openai.error import AuthenticationError
from window_chat_settings import ChatSettingsWindow, CHAT_BOARD_BG_COLOR
from chat_messages import ChatMessages


CHAT_FONT_FAMILY = "Helvetica"
CHAT_FONT_SIZE = 12
OPEN_AI_KEY_FILE = "open-ai-key.txt"


def get_api_key():
    if not os.path.exists(OPEN_AI_KEY_FILE):
        return None
    with open(OPEN_AI_KEY_FILE, "r") as f:
        api_key = f.read().strip()
    return api_key if api_key else None


class ChatWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatGPT")
        self.api_key = get_api_key()

        if not self.api_key:
            self.chat_history.insert(tk.END, "Error: API key file 'open-ai-key.txt' not found or is empty.")
            return
        openai.api_key = self.api_key

        self.settings_window = ChatSettingsWindow(root=self.root)
        self.message_manager = ChatMessages()
        self._create_ui()
        
        
    def _create_ui(self):
        _frame = tk.Frame(self.root)

        frame = tk.Frame(_frame, bg='gray')
        frame.pack(padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_history = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, bg=CHAT_BOARD_BG_COLOR, fg='white', font=(CHAT_FONT_FAMILY, CHAT_FONT_SIZE))
        self.chat_history.pack()

        self.chat_history.tag_configure('user', foreground='green')
        self.chat_history.tag_configure('gpt', foreground='orange')
        scrollbar.config(command=self.chat_history.yview)

        def handle_return(event):
            if not event.state & 0x1:  # If the Shift key is not pressed, consume the event without inserting a newline
                self.handle_input()
                return "break"
            
        self.input_text = tk.Text(_frame, height=4, width=50, bg='white', fg='gray')
        self.input_text.pack(padx=10, pady=(0, 10))
        self.input_text.bind("<Return>", self.handle_input)
        self.input_text.bind("<Shift-Return>", lambda event: self.input_text.insert(tk.INSERT, '\n'))
        self.input_text.bind("<KeyPress-Return>", handle_return)

        settings_button = tk.Button(_frame, text="Settings", command=self.settings_window.show_chat_settings_window)
        settings_button.pack(padx=(0, 10), pady=(0, 10), side=tk.RIGHT)
        _frame.grid(row=0,column=0)

    
    def send_message_from_game_screen(self, game_status_dict: Dict):

        try:
            ans = ""
            gpt_res = self.message_manager.send_message(
                openai_api=openai,
                game_status_dict=game_status_dict,
                prompt="",
                chat_settings_dict=self.settings_window.get_settings()
                )
            ans = gpt_res
        except AuthenticationError as e:
            print("Authentication error:", e)
            ans = "Failed to get a response. Please check if the API key is valid."
        except Exception as e:
            print("Error:", e)
            ans = "Failed to get a response. Please try again."
        finally:
            self.chat_history.insert(tk.END, f"\nChatGPT: ", 'gpt')
            self.chat_history.insert(tk.END, ans, 'gpt')

        pass


    def handle_input(self, event=None):
        user_text = self.input_text.get("1.0", tk.END).strip()
        if user_text == "":
            return

        self.input_text.delete("1.0", tk.END)

        self.chat_history.insert(tk.END, "\nYou: ", 'user')
        self.chat_history.insert(tk.END, user_text, 'user')
        
        try:
            ans = ""
            gpt_res = self.message_manager.send_message(
                openai_api=openai,
                game_status_dict={},
                prompt=user_text,
                chat_settings_dict=self.settings_window.get_settings()
                )
            ans = gpt_res
        except AuthenticationError as e:
            print("Authentication error:", e)
            ans = "Failed to get a response. Please check if the API key is valid."
        except Exception as e:
            print("Error:", e)
            ans = "Failed to get a response. Please try again."
        finally:
            self.chat_history.insert(tk.END, f"\nChatGPT: ", 'gpt')
            self.chat_history.insert(tk.END, ans, 'gpt')

        self.chat_history.see(tk.END)
        return "break"


def main():
    root = tk.Tk()
    app = ChatWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
