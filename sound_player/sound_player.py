import torch
from TTS.api import TTS
import os
from .utils import *
import pygame
from pygame.mixer import Sound
import re

    
class SoundPlayer:
    def __init__(self, language='zh'):
        pygame.mixer.init()
        self.language = language
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = parameters['model'][language]
        self.tts = TTS(self.model, progress_bar=False).to(self.device)
        self.output_path = parameters['out_path']
        self.speed = 1
        self.player = None
        self.channel = None
        self.text = ''

    def generate_speech(self, text, file_path=None):
        output_path = self.output_path
        if file_path is not None:
            output_path = file_path
        self.tts.tts_to_file(text, file_path=output_path)

    def _change_speed(self, speed):
        # TODO: 修改播放速度
        self.speed = speed
    
    def speed_up(self, d=0.25, upper=3):
        if self.speed + d <= upper:
            self._change_speed(d)

    def speed_down(self, d=0.25, lower=0.5):
        if self.speed - d >= lower:
            self._change_speed(-d)

    def _play(self, file_path=None):
        if file_path is None:
            file_path = self.output_path
        if not os.path.exists(file_path): return  # sound file not exist
        self.player = Sound(file_path)
        self.channel = self.player.play()

    def play_sound(self, text, remove_special_chars=True):
        # 去除特殊字符和英文字母
        if remove_special_chars:
            text = re.sub(r'[^\u4e00-\u9fa50-9]', '', text) + '。'
        if self.text != text:  # similar to save cache file
            self.generate_speech(text)
            self.text = text
        self._play()
    
    def stop_sound(self):
        if self.is_playing():
            self.player.stop()

    def is_playing(self):
        return self.channel.get_busy()