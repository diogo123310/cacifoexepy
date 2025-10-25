#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FontAwesome Integration for Kivy
Mapeamento de emojis para códigos FontAwesome
"""

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle

# Mapeamento de emojis para códigos FontAwesome
EMOJI_TO_FONTAWESOME = {
    '📧': '\uf0e0',  # envelope (email)
    '🔢': '\uf292',  # hashtag (PIN/numbers)
    '🔓': '\uf09c',  # unlock
    '✅': '\uf00c',  # check
    '⚠️': '\uf071',  # exclamation-triangle (warning)
    '🔒': '\uf023',  # lock
    '🏠': '\uf015',  # home
    '🔄': '\uf021',  # refresh/sync
    '💰': '\uf155',  # dollar-sign
    '📋': '\uf0cb',  # list
    '🎯': '\uf140',  # bullseye/target
    '📱': '\uf10b',  # mobile phone
    '📬': '\uf01c',  # inbox
    '✓': '\uf00c',   # check mark
    '!': '\uf071',   # exclamation
    '@': '\uf0e0',   # email/at symbol
}

class FontAwesomeLabel(Label):
    """Label with FontAwesome icon support"""
    def __init__(self, emoji_text="", **kwargs):
        # Converter emoji para FontAwesome se existir no mapeamento
        if emoji_text in EMOJI_TO_FONTAWESOME:
            fontawesome_code = EMOJI_TO_FONTAWESOME[emoji_text]
            text = f'[font=FontAwesome]{fontawesome_code}[/font]'
        else:
            text = emoji_text
        
        super().__init__(
            text=text,
            markup=True,
            **kwargs
        )

class FontAwesomeButton(Button):
    """Button with FontAwesome icon support"""
    def __init__(self, emoji_text="", button_text="", **kwargs):
        # Converter emoji para FontAwesome se existir
        if emoji_text in EMOJI_TO_FONTAWESOME:
            fontawesome_code = EMOJI_TO_FONTAWESOME[emoji_text]
            text = f'[font=FontAwesome]{fontawesome_code}[/font] {button_text}'
        else:
            text = f'{emoji_text} {button_text}' if emoji_text else button_text
        
        super().__init__(
            text=text,
            markup=True,
            **kwargs
        )

class FontAwesomeIconTextField(BoxLayout):
    """Professional text field with FontAwesome icon"""
    def __init__(self, emoji_icon="", hint_text="", is_password=False, input_filter=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.spacing = dp(10)
        
        # FontAwesome icon container
        icon_container = BoxLayout(size_hint_x=None, width=dp(50))
        with icon_container.canvas.before:
            Color(0/255, 77/255, 122/255, 1)  # Blue background
            self.icon_bg = RoundedRectangle(pos=icon_container.pos, size=icon_container.size, radius=[dp(8)])
        icon_container.bind(pos=self._update_icon_bg, size=self._update_icon_bg)
        
        # Convert emoji to FontAwesome
        if emoji_icon in EMOJI_TO_FONTAWESOME:
            fontawesome_code = EMOJI_TO_FONTAWESOME[emoji_icon]
            icon_text = f'[font=FontAwesome]{fontawesome_code}[/font]'
        else:
            icon_text = f'[{emoji_icon}]'
        
        icon_label = Label(
            text=icon_text,
            markup=True,
            font_size=sp(20),
            color=(1, 1, 1, 1),  # White text
            halign='center',
            valign='middle'
        )
        icon_container.add_widget(icon_label)
        self.add_widget(icon_container)
        
        # Professional text input
        self.text_input = TextInput(
            hint_text=hint_text,
            multiline=False,
            password=is_password,
            font_size=sp(18),
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0/255, 77/255, 122/255, 1),
            cursor_color=(1, 204/255, 0, 1),
            selection_color=(1, 204/255, 0, 0.3),
            padding=[dp(15), dp(12)]
        )
        
        if input_filter:
            self.text_input.input_filter = input_filter
        
        # Add border to text input
        with self.text_input.canvas.before:
            Color(200/255, 200/255, 200/255, 1)
            self.text_input.border_rect = RoundedRectangle(
                pos=self.text_input.pos, 
                size=self.text_input.size, 
                radius=[dp(8)]
            )
        
        self.text_input.bind(pos=self._update_border, size=self._update_border)
        self.text_input.bind(focus=self._on_focus_change)
        self.add_widget(self.text_input)
    
    def _update_border(self, *args):
        self.text_input.border_rect.pos = self.text_input.pos
        self.text_input.border_rect.size = self.text_input.size
    
    def _update_icon_bg(self, instance, value):
        self.icon_bg.pos = instance.pos
        self.icon_bg.size = instance.size
    
    def _on_focus_change(self, instance, focus):
        """Change border color based on focus"""
        if focus:
            # Yellow border when focused
            with self.text_input.canvas.before:
                Color(1, 204/255, 0, 1)
                self.text_input.border_rect = RoundedRectangle(
                    pos=self.text_input.pos, 
                    size=self.text_input.size, 
                    radius=[dp(8)]
                )
        else:
            # Gray border when not focused
            with self.text_input.canvas.before:
                Color(200/255, 200/255, 200/255, 1)
                self.text_input.border_rect = RoundedRectangle(
                    pos=self.text_input.pos, 
                    size=self.text_input.size, 
                    radius=[dp(8)]
                )

# Function to convert text with emojis to FontAwesome
def convert_emoji_to_fontawesome(text):
    """Convert emojis in text to FontAwesome codes"""
    for emoji, fontawesome in EMOJI_TO_FONTAWESOME.items():
        if emoji in text:
            text = text.replace(emoji, f'[font=FontAwesome]{fontawesome}[/font]')
    return text