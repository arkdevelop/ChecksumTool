from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import hashlib

import os

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        BUF_SIZE = 65536
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        sha256 = hashlib.sha256()
        sha512 = hashlib.sha512()

        with open(os.path.join(path, filename[0]), 'rb') as stream:
            while True:
                data = stream.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
                sha1.update(data)
                sha256.update(data)
                sha512.update(data)

            self.text_input.text = "MD5: {0}".format(md5.hexdigest()) + "\nSHA-1: {0}".format(sha1.hexdigest()) + "\nSHA-256: {0}".format(sha256.hexdigest()) + "\nSHA-512: {0}".format(sha512.hexdigest())

        self.dismiss_popup()


class Editor(App):
    title = "Checksum"
    icon = ""
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)


if __name__ == '__main__':
    Editor().run()