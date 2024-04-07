# Ported by brostos to api 8
# Tool used to make porting easier.(https://github.com/bombsquad-community/baport)
"""Hydra

The best CHEAT for BombSquad!
by @imnezy on Discord.
"""
from _future_ import annotations

_author_ = 'nezy'
_version_ = 1.0
_name_ = __name__

import babase
import bauiv1 as bui
import bascenev1 as bs
import _babase

from baenv import TARGET_BALLISTICA_BUILD as build_number
from bauiv1lib.settings.allsettings import AllSettingsWindow
from bascenev1lib.actor.spaz import Spaz
from bascenev1lib.actor.scoreboard import Scoreboard
from bascenev1lib.gameutils import SharedObjects

from typing import (
    Text,
    Tuple,
    Optional,
    Union,
    get_args
)
type

# Default Confings/Settings
CONFIG = "CheatMenu"
APPCONFIG = babase.app.config
Configs = {
    "Host": False,
    "God Mod": False,
    "Speed Modded": False,
    "Fly": False,
    "Invisible": False,
    "Glitch Player": False,
    "Super Punch": False,
    "IceBombs": False,
    "StickyBombs": False,
    "MineBombs": False,
    "ImpactBombs": False,
    "All Bombs": False,
    "Infinite Bombs": False,
    "Credits": False,
}


def setconfigs() -> None:
    """Set required defualt configs for mod"""
    if CONFIG not in APPCONFIG:
        APPCONFIG[str(CONFIG)] = Configs

    for c in Configs:
        if c not in APPCONFIG[str(CONFIG)]:
            APPCONFIG[str(CONFIG)][str(c)] = Configs[str(c)]
        else:
            pass
    APPCONFIG.apply_and_commit()


def update_config(config: str, change: any):
    """update's given value in json config file of pluguin"""
    APPCONFIG[str(CONFIG)][str(config)] = change
    APPCONFIG.apply_and_commit()


# ba_meta require api 8
# ba_meta export plugin
class Plugin(babase.Plugin):
    def on_app_running(self) -> None:
        if babase.app.build_number if build_number < 21282 else babase.app.env.build_number:
            setconfigs()
            self.overwrite()

        else:
            babase.screenmessage(f'{_name_} only works on api 8')

    def overwrite(self) -> None:
        AllSettingsWindow.init = AllSettingsWindow._init_
        AllSettingsWindow._init_ = AllSettingsWindowInit


# creating Cheat button, start button
def AllSettingsWindowInit(self, transition: str = 'in_right', origin_widget: bui.Widget = None):
    self.init(transition)

    uiscale = bui.app.ui_v1.uiscale
    btn_width = 825 if uiscale is babase.UIScale.SMALL else 400
    btn_height = 355

    self.cheat_menu_btn = bui.buttonwidget(
        parent=self._root_widget,
        autoselect=True,
        position=(btn_width, btn_height),
        size=(105, 10),
       
        label='Hydra Menu',
        button_type='square',
        text_scale=1.4,
        on_activate_call=babase.Call(
            on_cheat_menu_btn_press, self))


# on cheat button press call Window
def on_cheat_menu_btn_press(self):
    bui.containerwidget(edit=self._root_widget,
                        transition='out_scale')
    bui.app.ui_v1.set_main_menu_window(
        PsychoMenuWindow(
            transition='in_right').get_root_widget(), from_window=self._root_widget)


class PsychoMenuWindow(bui.Window):
    def _init_(self,
                 transition: Optional[str] = 'in_right') -> None:

        # background window, main widget parameters
        uiscale = bui.app.ui_v1.uiscale
        self._width = 870.0 if uiscale is babase.UIScale.SMALL else 670.0
        self._height = (390.0 if uiscale is babase.UIScale.SMALL else
                        450.0 if uiscale is babase.UIScale.MEDIUM else 520.0)
        extra_x = 150 if uiscale is babase.UIScale.SMALL else 0
        self.extra_x = extra_x
        top_extra = 20 if uiscale is babase.UIScale.SMALL else 0

        # scroll widget parameters
        self._scroll_width = self._width - (150 + 2 * extra_x)
        self._scroll_height = self._height - 115.0
        self._sub_width = self._scroll_width * 0.115
        self._sub_height = 980.0
        self._spacing = 15
        self._extra_button_spacing = self._spacing * 4.5

        super()._init_(
            root_widget=bui.containerwidget(
                size=(self._width, self._height),
                transition=transition,
                scale=(2.06 if uiscale is babase.UIScale.SMALL else
                       1.4 if uiscale is babase.UIScale.MEDIUM else 1.0)))

        # back button widget
        self._back_button = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(52 + self.extra_x,
                      self._height - 60 - top_extra),
            size=(50, 50),
            scale=0.8,
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            on_activate_call=self._back)
        bui.containerwidget(edit=self._root_widget,
                            cancel_button=self._back_button)

        # window title, apears in top center of window
        self._title_text = bui.textwidget(
            parent=self._root_widget,
            position=(0, self._height - 40 - top_extra),
            size=(self._width, 25),
            text='Hydra VIP (1.0)',
            color=bui.app.ui_v1.title_color,
            scale=1.5,
            h_align='center',
            v_align='top')

        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            position=(50 + extra_x, 50 - top_extra),
            simple_culling_v=20.0,
            highlight=False,
            size=(self._scroll_width,
                  self._scroll_height),
            selection_loops_to_parent=True)
        bui.widget(edit=self._scrollwidget,
                   right_widget=self._scrollwidget)

        # subcontainer represents scroll widget and used as parent
        self._subcontainer = bui.containerwidget(
            parent=self._scrollwidget,
            size=(self._sub_width,
                  self._sub_height),
            background=False,
            selection_loops_to_parent=True)

        v = self._sub_height - 50
        v -= self._spacing * 1.2
        conf = APPCONFIG[str(CONFIG)]

        for checkbox in Configs:
            bui.checkboxwidget(
                parent=self._subcontainer,
                autoselect=True,
                position=(25.0, v),
                size=(30, 30),
                text=checkbox,
                textcolor=(0.8, 0.8, 0.8),
                value=APPCONFIG[CONFIG][checkbox],
                on_value_change_call=babase.Call(
                    self.update, checkbox),
                scale=1.4,
                maxwidth=430)
            v -= 70

    def update(self, config: str, change) -> None:
        """Change config and get our sounds

        Args:
            config: str
            change: any
        """
        try:
            if change == True and config == "Fly":
                bui.screenmessage("Fly Activated",
                                  color=(1, 0, 0))
            update_config(config, change)
            bui.getsound('gunCocking').play()
        except Exception:
            bui.screenmessage("error", color=(1, 0, 0))
            bui.getsound('error').play()

        try:
            if change == True and config == "Super Punch":
                bui.screenmessage("SuperPunch Activated",
                                  color=(1, 0, 0))
            elif change == False and config == "Super Punch":
                bui.screenmessage("Super Punch Deactivated",
                                  color=(0.5, 0, 0))
            update_config(config, change)
            bui.getsound('gunCocking').play()
        except Exception:
            bui.screenmessage("error", color=(1, 0, 0))
            bui.getsound('spazOw').play()

        try:
            if change == True and config == "IceBombs":
                bui.screenmessage("Ice Bombs Activated",
                                  color=(0.1, 1, 1))
            elif change == False and config == "IceBombs":
                bui.screenmessage("Ice Bombs Deactivated",
                                  color=(1, 0, 0))
            update_config(config, change)
            bui.getsound('gunCocking').play()
        except Exception:
            bui.screenmessage("error", color=(1, 0, 0))
            bui.getsound('spazOw').play()
        try:
            if change == True and config == "StickyBombs":
                bui.screenmessage("Sticky Bombs Activated",
                                  color=(0, 1, 0))
            elif change == False and config == "StickyBombs":
                bui.screenmessage("Sticky Bombs Deactivated",
                                  color=(1, 0, 0))
            update_config(config, change)
            bui.getsound('gunCocking').play()
        except Exception:
            bui.screenmessage("error", color=(1, 0, 0))
            bui.getsound('spazOw').play()

        try:
            if change == True and config == "ImpactBombs":
                bui.screenmessage("Impact Bombs Activated",
                                  color=(0.5, 0.5, 0.5))
            elif change == False and config == "ImpactBombs":
                bui.screenmessage("Impact Bombs Deactivated",
                                  color=(1, 0, 0))
            update_config(config, change)
            bui.getsound('gunCocking').play()
        except Exception:
            bui.screenmessage("error", color=(1, 0, 0))
            bui.getsound('spazOw').play()

        try:
            if change == True and config == "More Are Coming":
                bui.screenmessage("Is Coming...",
                                  color=(4, 9, 2))
            update_config(config, change)
            bui.getsound('gunCocking').play()
        except Exception:
            bui.screenmessage("error", color=(1, 0, 0))
            bui.getsound('cheer').play()

        try:
            if change == True and config == "Credits":
                bui.screenmessage("The Creator of Hydra: @7mt21, on Discord.",
                                  color=(4, 9, 2))
            update_config(config, change)
            bui.getsound('gunCocking').play()
        except Exception:
            bui.screenmessage("error", color=(1, 0, 0))
            bui.getsound('cheer').play()

    def _back(self) -> None:
        """Kill the window and get back to previous one
        """
        bui.containerwidget(edit=self._root_widget,
                            transition='out_scale')
        bui.app.ui_v1.set_main_menu_window(
            AllSettingsWindow(
                transition='in_left').get_root_widget(), from_window=self._root_widget)


def ishost():
    session = bs.get_foreground_host_session()
    with session.context:
        for player in session.sessionplayers:
            if player.inputdevice.client_id >= -1:
                return True


def activity_loop():
    if bs.get_foreground_host_activity() is None:
        return
    
    activity = bs.get_foreground_host_activity()
    with activity.context:
        for player in activity.players:
            if not ishost() or not player.actor:
                return
            
            config = APPCONFIG[CONFIG]
            actor_node = player.actor.node
            
            actor_node.invincible = config["God Mod"]
            actor_node.fly = config["Fly"]
            actor_node.hockey = config["Speed Modded"]
            actor_node._punch_power_scale = 7 if config["Super Punch"] else 1.2
            
            if config["Host"]:
                with bs.get_foreground_host_session:
                    player.inputdevice.client_id = -1
            else:
                with bs.get_foreground_host_session:
                    player.inputdevice.client_id = 0
            
            if config["IceBombs"]:
                player.actor.bomb_type = 'ice'
                player.actor.bomb_count = 1
            elif config["MineBombs"]:
                player.actor.bomb_type = 'land_mine'
            else:
                player.actor.bomb_type = 'normal'
            
            if config["Invisible"]:
                if player.is_alive() and player.actor:
                    actor_node.color_mask_texture = None
                    actor_node.color_texture = None
                    actor_node.head_mesh = None
                    actor_node.torso_mesh = None
                    actor_node.upper_arm_mesh = None
                    actor_node.forearm_mesh = None
                    actor_node.pelvis_mesh = None
                    actor_node.toes_mesh = None
                    actor_node.upper_leg_mesh = None
                    actor_node.lower_leg_mesh = None
                    actor_node.hand_mesh = None
                    actor_node.name = ''
            else:
                player.actor.node.name = 'HydraVIP'
            
            if config["ImpactBombs"]:
                player.actor.bomb_type = 'impact'
                player.actor.bomb_count = 1
            
            if config["StickyBombs"]:
                player.actor.bomb_type = 'sticky'
                player.actor.bomb_count = 1
            
            if config["InfiniteBombs"]:
                player.actor.bomb_count = 100

timer = babase.AppTimer(2, activity_loop, repeat=True)