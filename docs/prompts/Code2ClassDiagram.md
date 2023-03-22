# ClassDiagram
Please create a class diagram from the code field below.
You may also use information obtained during the discussion.
The output of this class diagram must focus on a single class.
The class of interest is specified in the ##Class field.

## Format
Markdown, Mermaid

## Classes
Output Class diagram must include this class
* "StartScreen"

## Include
* all members the class of interest have.
* Classes the class of interest relates directly.
* Classes which is not the class of interest does not have information of members.

## Exclude
* Classes the class of interest does not relate directly.


## CODE
```
class StartScreen():
    def __init__(self, root, create_game_callback):
        self._root: tk.Tk = root
        self._initialize_game_callback = create_game_callback

        # Components
        self.start_frame: tk.Frame = tk.Frame(self._root)

        ## Title label
        #self.game_title_label = tk.Label(frame, text="Minesweeper",font=("Helvetica", 24), bg="gray", width=20, height=5)
        self.game_title_label = tk.Label(self.start_frame, text="Minesweeper",font=("Helvetica", 24), width=20, height=5)

        ## Difficulty Menu
        self.difficulty_var = tk.StringVar()
        self.difficulty_menu = ttk.Combobox(self.start_frame, textvariable=self.difficulty_var, state="readonly")

        ## Start Button
        self.start_button = tk.Button(self.start_frame, text="Start Game", command=self._start_game)

        self._setup_ui()

    def _setup_ui(self):           
        self.game_title_label.pack()
        self.difficulty_menu["values"] = ("beginner", "intermediate", "advanced")
        self.difficulty_menu.current(0)
        
        self.difficulty_menu.pack()

        # Start button
        self.start_button.pack()

        self.start_frame.grid(column=1, row=1)
    
    def release_ui(self):
        if self.game_title_label:
            self.game_title_label.pack_forget()
            self.game_title_label = None
        if self.difficulty_menu:
            self.difficulty_menu.pack_forget()
            self.difficulty_menu = None
        if self.start_button:
            self.start_button.pack_forget()
            self.start_button = None
        if self.start_frame:
            self.start_frame.grid_forget()
            self.start_frame = None

    def _start_game(self):
        difficulty = self.difficulty_var.get()
        self.release_ui()
        self._initialize_game_callback(difficulty)


```