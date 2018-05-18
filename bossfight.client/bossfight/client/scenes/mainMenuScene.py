# -*- coding: utf-8 -*-

import cocos
from cocos.director import director
from pyglet.window import NoSuchScreenModeException
import bossfight.client.config as config
from bossfight.client.scenes.gameLoopTestScene import GameLoopTestScene
from bossfight.client.scenes.serverTestScene import ServerTestScene

class MainMenuScene(cocos.scene.Scene):
    def __init__(self):
        super().__init__()
        self.open_main_menu()

    def open_options_menu(self):
        self.add(OptionsMenuLayer())

    def open_main_menu(self):
        self.add(MainMenuLayer())

class MainMenuLayer(cocos.menu.Menu):
    def __init__(self):
        super().__init__(title='BossFight')
        self.font_title.update({
            'font_size': 128,
            'bold': True
        })
        self.font_item.update({
            'font_size': 64
        })
        self.font_item_selected.update(self.font_item)
        self.font_item_selected.update({
            'color': (255, 255, 255, 255)
        })
        menu_items = [
            cocos.menu.MenuItem('Test Game Loop', self.on_test_loop),
            cocos.menu.MenuItem('Test Server', self.on_test_server),
            cocos.menu.MenuItem('Options', self.on_options),
            cocos.menu.MenuItem('Quit', self.on_quit)
        ]
        self.create_menu(
            items=menu_items,
            selected_effect=cocos.menu.zoom_in(),
            unselected_effect=cocos.menu.zoom_out()
        )
    
    def on_test_loop(self):
        director.push(GameLoopTestScene())

    def on_test_server(self):
        director.push(ServerTestScene())

    def on_options(self):
        self.parent.open_options_menu()
        self.kill()

    def on_quit(self):
        self.parent.end()

class OptionsMenuLayer(cocos.menu.Menu):
    def __init__(self):
        super().__init__(title='Options')
        self.font_title.update({
            'font_size': 64,
            'bold': True
        })
        self.font_item.update({
            'font_size': 32
        })
        self.font_item_selected.update(self.font_item)
        self.font_item_selected.update({
            'color': (255, 255, 255, 255)
        })
        self.resolutions = ['854x480', '1280x720', '1600x900', '1920x1080']
        current_resolution = [
            idx for idx, value in enumerate(self.resolutions) \
            if value == str(config.get.screen_mode['width']) + 'x' \
            + str(config.get.screen_mode['height'])
        ][0]
        menu_items = [
            cocos.menu.MultipleMenuItem(
                'Resolution: ', self.on_resolution, self.resolutions, current_resolution
            ),
            cocos.menu.ToggleMenuItem(
                'Fullscreen: ', self.on_fullscreen, config.get.screen_mode['fullscreen']
            ),
            cocos.menu.MenuItem('Revert to default', self.on_default),
            cocos.menu.MenuItem('Apply', self.on_apply),
            cocos.menu.MenuItem('Back', self.on_back)
        ]
        self.create_menu(
            items=menu_items,
            selected_effect=cocos.menu.zoom_in(),
            unselected_effect=cocos.menu.zoom_out()
        )

    def on_resolution(self, index):
        width_height = self.resolutions[index].split('x')
        config.get.screen_mode['width'] = int(width_height[0])
        config.get.screen_mode['height'] = int(width_height[1])

    def on_fullscreen(self, fullscreen):
        config.get.screen_mode['fullscreen'] = bool(fullscreen)

    def on_default(self):
        config.revert_to_default()
        self.parent.open_options_menu()
        self.kill()

    def on_apply(self):
        try:
            director.window.set_fullscreen(
                fullscreen=config.get.screen_mode['fullscreen'],
                width=config.get.screen_mode['width'],
                height=config.get.screen_mode['height']
            )
            config.save()
        except NoSuchScreenModeException:
            config.load()
            self.parent.open_options_menu()
            self.kill()

    def on_back(self):
        config.load()
        self.parent.open_main_menu()
        self.kill()

    def on_quit(self):
        self.on_back()
