from tiktoken import get_encoding, encoding_for_model
from typing import List, Dict
from cell import Cell

def assume_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = get_encoding("cl100k_base")

        
    if model == "gpt-3.5-turbo":
        # print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return assume_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        # print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return assume_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

class ChatMessages:
    def __init__(self, max_tokens: int, model: str):
        self._max_tokens = max_tokens
        # Messages are stored to fit within max_token or less.
        # When actually sent, the message is truncated to meet the max_token, including the system message which is added to the end of the message.
        self._messages = []   
        self._system_message = ""
        self._model: str = model

    @property
    def max_tokens(self):
        return self._max_tokens

    @max_tokens.setter
    def max_tokens(self, value):
        if value < 1:
            raise ValueError("Max tokens must be greater than 0.")
        self._max_tokens = value

    @staticmethod
    def _validate_message_structure(message: Dict):
        return True if set(message.keys()) == {"role", "content"} else False

    def _add_message(self, role: str, content: str):
        # validate message
        if not role in ("user", "assistant"):
            raise ValueError(f"not appropriate role: {role}")
        
        message = {"role": role, "content": content}

        if self._validate_message_structure(message=message):
            self._messages.append(message)
            self._truncate_self_messages()        
    
    def get_latest_assistant_message_if_exists(self):
        if self._messages:
            latest_message = self._messages[-1]        
            if latest_message["role"] == "assistant":
                return latest_message["content"]
        return       

    
    def create_sending_messages(self, system_message: str):
        self._truncate_self_messages()
        messages = self._messages.copy()
        messages.append({"role":"system", "content":system_message})

        truncated_messages = self.truncate_messages_to_max_tokens(messages=messages, max_tokens=self.max_tokens, model=self._model)
        return truncated_messages
      
    def create_system_message(self, persona: str, game_status, mines_locations: List[Cell], false_flagged_cells: List[Cell], progression_rate: float):
        mines_locations_string = ",".join(mines_locations)
        false_flagged_cells_string = ",".join(false_flagged_cells)

        message = f"You are {persona}, reply user based on your persona. You must always reply in the same language as the language spoken."

        # self._system_message = \
        # f"""The User is playing the Minesweeper game. You are {persona} and watching the user is playing the game.
        # You must play a role as a {persona}. Do and say things appropriate to your persona.
        # The current status of the game will be communicated in a later section ##GameStatus.
        # Based on your character, if GAMESTATUS is "won", congratulate the user; if it "lose", comfort him as.
        # If GAMESTATUS is "ongoing" or "starting", encourage the user based on your persona and the situation explained in the ##GameStatus section.
        # If user ask you to tell where the mines are located, the strict persona will never tell it. On the contrary, they will be angry with you for the fact that user asked you to tell it.
        # However, a persona with a weak personality, a kind persona, or a persona with a weakness toward the user may tell you.
        # Your relationship with the user, as inferred from the conversation, is also important.
        # Any persona may teach it if the persona is persuaded to do so by the conversation the persona have had with them. 
        # However, the difficulty a user has in convincing a persona depends on the nature of that persona.
        # When a user is not specifically talking about a game, there is no need to specifically mention the game. Converse with the user according to the flow of the conversation and your persona.
        # You must always reply in the same language as the language spoken.
        
        # # GameStatus
        # GAMESTATUS: {game_status}
        # Location of mines: {mines_locations_string}
        # Cells that are incorrectly flagged by the user: {false_flagged_cells_string}
        # Rate of Progression: {progression_rate}
        # """
        return message

    @staticmethod
    def truncate_messages_to_max_tokens(messages: List[Dict], max_tokens: int, model: str):
        while True:
            token_usage = assume_tokens_from_messages(messages=messages, model=model)
            if token_usage < max_tokens:
                break
            messages.pop(0)
        return messages


    def _truncate_self_messages(self):
        truncate_messages = self.truncate_messages_to_max_tokens(messages=self._messages, max_tokens=self.max_tokens, model=self._model)
        self._messages = truncate_messages
        return


    def send_message(self, openai_api, prompt):
        """
        Sends a message to the OpenAI API and returns the response.
        Args:
            openai_api: An instance of the OpenAI API client.
            prompt: The user's message to send to the OpenAI API.
        Returns:
            The assistant's response as a string.
        """
        self._add_message(role="user", content=prompt)
        system_message = self.create_system_message(persona="user's younger sister", game_status="",mines_locations=[], false_flagged_cells=[], progression_rate=0.0)
        sending_messages = self.create_sending_messages(system_message=system_message)

        response = openai_api.ChatCompletion.create(
            model=self._model,
            messages=sending_messages,
            max_tokens=self.max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )

        assistant_response = response.choices[0].message["content"]
        self._add_message("assistant", assistant_response)
        return assistant_response
