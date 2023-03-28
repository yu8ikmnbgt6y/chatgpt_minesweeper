import copy
from typing import Dict, List

from tiktoken import encoding_for_model, get_encoding

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
    def __init__(self):
        self._messages = []
        self._previous_game_status = None

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
    
    def get_latest_assistant_message_if_exists(self):
        if self._messages:
            latest_message = self._messages[-1]        
            if latest_message["role"] == "assistant":
                return latest_message["content"]
        return       

    
    def create_sending_messages(self, model: str, max_tokens: int, system_message: str):
        self._truncate_self_messages(model=model, max_tokens=max_tokens)

        messages = self._messages.copy()
        # messages.insert(0, {"role":"system", "content":system_message})
        messages.append({"role":"system", "content":system_message})

        truncated_messages = self.truncate_messages_to_max_tokens(
            messages=messages,
            max_tokens=max_tokens,
            model=model
            )
        return truncated_messages
      
    def create_system_message(self, game_status_dict: Dict, chat_settings_dict: Dict):
        persona = chat_settings_dict["persona"]
        character = chat_settings_dict["character"]
        relationship = chat_settings_dict["relationship"]
        chat_language = chat_settings_dict["chat_language"]

        message = \
        f"""
        ##Setup: you are {persona}, and you have a {character} disposition.
        Your relationship with the user is {relationship}.
        Reply to the user based on the above settings.
        ## NOTE
        You must always speak in a single language.
        You must reply in a single language, {chat_language} at all times.
        Respond in ***{chat_language}***, even if spoken to in another language.
        """
        if game_status_dict == {}:
            game_status_dict = self._previous_game_status
        else:
            self._previous_game_status = copy.deepcopy(game_status_dict)

        if game_status_dict != {}:
            game_status = game_status_dict["game_status"]
            mines_remaining: List[Cell] = game_status_dict["mines_remaining"]
            false_flagged_cells: List[Cell] = game_status_dict["false_flagged_cells"]
            progression_rate: float = game_status_dict["progression_rate"]
            mines_remaining_string = ",".join([str(x) for x in mines_remaining])
            if false_flagged_cells:
                false_flagged_cells_string = ",".join([str(x) for x in false_flagged_cells])
            else:
                false_flagged_cells_string = "None"

            message += \
            f"""The User is playing the Minesweeper game. You are watching the user is playing the game.
            You must play a role as a {persona}. Do and say things appropriate to your persona.
            The current status of the game will be communicated in a later section ##GameStatus.
            Based on your character, if GAMESTATUS is "won", congratulate the user; if it "lose", comfort him as.
            If GAMESTATUS is "ongoing" or "starting", encourage the user based on your persona and the situation explained in the ##GameStatus section.
            It is not prohibited to tell users the location of mines. However, Decide whether to teach based on your persona, personality, relationship with the user, and game situation.
            Any persona may teach it if the persona is persuaded to do so by the conversation the persona have had with them. 
            However, the difficulty a user has in convincing a persona depends on the nature of that persona.
            When a user is not specifically talking about a game, there is no need to specifically mention the game. Converse with the user according to the flow of the conversation and your persona.
            Don't tell them where the mines are by yourself, even if they don't ask.
            Telling people the location of many mines should be avoided in favor of telling them the location of a small number of mines.
            Do not continue to talk about the same things you have talked about before.
            Please answer in one sentences or less unless otherwise required. Do not add translations.

            # GameStatus
            GAMESTATUS: {game_status}
            Location of mines: {mines_remaining_string}
            Cells that are incorrectly flagged by the user: {false_flagged_cells_string}
            Rate of Progression which represent the ratio opened cells against closed cells: {progression_rate * 100:.2f}%
            """
        message += \
        f"""## NOTE
        You must always speak in a single language.
        You must reply in a single language, {chat_language} at all times.
        Respond in ***{chat_language}***, even if spoken to in another language.
        """

        print(message)
        return message

    @staticmethod
    def truncate_messages_to_max_tokens(messages: List[Dict], max_tokens: int, model: str):
        while True:
            token_usage = assume_tokens_from_messages(messages=messages, model=model)
            if token_usage < max_tokens:
                break
            messages.pop(0)
        return messages


    def _truncate_self_messages(self, model: str, max_tokens: int):
        truncate_messages = self.truncate_messages_to_max_tokens(
            messages=self._messages,
            max_tokens=max_tokens,
            model=model
            )
        self._messages = truncate_messages
        return


    def send_message(self, openai_api, prompt, game_status_dict: Dict, chat_settings_dict: Dict):
        """
        Sends a message to the OpenAI API and returns the response.
        Args:
            openai_api: An instance of the OpenAI API client.
            prompt: The user's message to send to the OpenAI API.
        Returns:
            The assistant's response as a string.
        """
        model = chat_settings_dict["model"]
        max_tokens = chat_settings_dict["max_tokens"]
        temperature = chat_settings_dict["temperature"]

        if prompt:
            self._add_message(role="user", content=prompt)

        system_message = self.create_system_message(
            game_status_dict=game_status_dict,
            chat_settings_dict=chat_settings_dict
        )

        sending_messages = self.create_sending_messages(
            model=model,
            max_tokens=max_tokens,
            system_message=system_message
            )

        response = openai_api.ChatCompletion.create(
            model=model,
            messages=sending_messages,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=temperature,
        )

        assistant_response = response.choices[0].message["content"]
        self._add_message("assistant", assistant_response)
        return assistant_response
