from subclass.pop_up_panel import PopupPanel
from scripts.path_utils import get_resource_path
import random
import json
from pathlib import Path

# Load NPC dialogs at module initialization
def _load_npc_dialogs():
    """Load NPC dialog data from JSON file."""
    dialog_path = Path(get_resource_path("data/dialogs/npc_dialogs.json"))
    try:
        with open(dialog_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: NPC dialogs file not found at {dialog_path}")
        return {"npcs": {}}
    except json.JSONDecodeError:
        print(f"Warning: NPC dialogs JSON is malformed at {dialog_path}")
        return {"npcs": {}}

_NPC_DIALOGS = _load_npc_dialogs()

def _get_npc_dialog(npc_id, is_night=False, is_early_game=False):
    """Get a random dialog for an NPC, with preference for context."""
    npc_id_str = str(npc_id)
    
    if npc_id_str not in _NPC_DIALOGS.get("npcs", {}):
        return None
    
    npc_data = _NPC_DIALOGS["npcs"][npc_id_str]
    
    # Check for early game special dialogs
    if is_early_game and npc_data.get("special_dialogs", {}).get("early_game"):
        return random.choice(npc_data["special_dialogs"]["early_game"])
    
    # Select based on day/night
    if is_night:
        dialogs = npc_data.get("night_dialogs", [])
    else:
        dialogs = npc_data.get("day_dialogs", [])
    
    if dialogs:
        return random.choice(dialogs)
    
    return None

def _get_npc_name(npc_id):
    """Get the name of an NPC."""
    npc_id_str = str(npc_id)
    return _NPC_DIALOGS.get("npcs", {}).get(npc_id_str, {}).get("name", f"NPC {npc_id}")

def npc_dialog(game, npc_id):
    """
    Display NPC dialog based on their ID and game state.
    Dialogs are loaded from npc_dialogs.json and selected randomly.
    """
    npc_name = _get_npc_name(npc_id)
    is_night = game.is_night
    is_early_game = game.player.day in (1, 2, 3)
    
    # Get appropriate dialog based on NPC ID and game state
    dialog_text = _get_npc_dialog(npc_id, is_night, is_early_game)
    
    if dialog_text:
        PopupPanel.show_message(
            manager=game.manager,
            text=f"{npc_name}(NPC): {dialog_text}",
            screen_size=game.screen.get_size()
        )
    else:
        # Fallback if no dialog found
        PopupPanel.show_message(
            manager=game.manager,
            text=f"{npc_name}(NPC): ...",
            screen_size=game.screen.get_size()
        )


