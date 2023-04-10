import pytest
from chat_messages import ChatMessages, Cell

# Fixtures
@pytest.fixture
def chat_messages():
    return ChatMessages()

# Test functions
def test_add_message(chat_messages):
    chat_messages._add_message("user", "Hello!")
    assert chat_messages._messages[-1] == {"role": "user", "content": "Hello!"}

    chat_messages._add_message("assistant", "Hello, how can I help you?")
    assert chat_messages._messages[-1] == {"role": "assistant", "content": "Hello, how can I help you?"}

    with pytest.raises(ValueError):
        chat_messages._add_message("invalid_role", "This should raise an error")

def test_get_latest_assistant_message_if_exists(chat_messages):
    assert chat_messages.get_latest_assistant_message_if_exists() is None

    chat_messages._add_message("user", "Hello!")
    assert chat_messages.get_latest_assistant_message_if_exists() is None

    chat_messages._add_message("assistant", "Hello, how can I help you?")
    assert chat_messages.get_latest_assistant_message_if_exists() == "Hello, how can I help you?"

def test_create_system_message(chat_messages):
    game_status_dict = {"game_status": "ongoing", "mines_remaining": [Cell(0, 0, 20), Cell(0, 1, 20)], "false_flagged_cells": [Cell(0, 2, 20)], "progression_rate": 0.5}
    chat_settings_dict = {"persona": "friend", "character": "cheerful", "relationship": "close", "chat_language": "English", "model": "gpt-3.5-turbo", "max_tokens": 100, "temperature": 0.8}

    system_message = chat_messages.create_system_message(game_status_dict=game_status_dict, chat_settings_dict=chat_settings_dict)
    assert "##Setup: you are friend" in system_message
    assert "GAMESTATUS: ongoing" in system_message


