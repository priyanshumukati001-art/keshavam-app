import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import requests
import threading
import sqlite3

class KeshavamApp(App):
    def build(self):
        self.title = "Keshavam - Your AI Brother"
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Header
        self.layout.add_widget(Label(text='केशवम्', font_size=45, size_hint_y=0.15, color=(0.2, 0.6, 1, 1)))
        
        # Chat Display
        self.chat_scroll = ScrollView(size_hint_y=0.6)
        self.chat_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_scroll.add_widget(self.chat_layout)
        self.layout.add_widget(self.chat_scroll)
        
        # Input Area
        input_box = BoxLayout(size_hint_y=0.1, spacing=10)
        self.user_input = TextInput(hint_text='Bhai se kuch pucho...', multiline=False, padding=[10, 10])
        send_btn = Button(text='Bhejo', size_hint_x=0.3, background_color=(0.2, 0.6, 1, 1))
        send_btn.bind(on_press=self.send_message)
        input_box.add_widget(self.user_input)
        input_box.add_widget(send_btn)
        self.layout.add_widget(input_box)
        
        self.init_db()
        return self.layout

    def init_db(self):
        self.conn = sqlite3.connect('keshavam.db')
        self.conn.execute('CREATE TABLE IF NOT EXISTS chat (sender TEXT, msg TEXT)')
        self.add_msg("Keshavam", "Ram Ram bhai! Main Keshavam hoon. Aaj kya help karun?")

    def add_msg(self, sender, msg):
        color = "3399FF" if sender == "Keshavam" else "33FF33"
        lbl = Label(text=f"[color={color}][b]{sender}:[/b][/color] {msg}", 
                    markup=True, size_hint_y=None, height=120, text_size=(500, None))
        self.chat_layout.add_widget(lbl)
        Clock.schedule_once(lambda dt: setattr(self.chat_scroll, 'scroll_y', 0))

    def send_message(self, instance):
        txt = self.user_input.text.strip()
        if txt:
            self.add_msg("You", txt)
            self.user_input.text = ""
            threading.Thread(target=self.get_ai_resp, args=(txt,)).start()

    def get_ai_resp(self, user_txt):
        # Hugging Face Free API का इस्तेमाल (या अपनी कोई भी Key यहाँ डालें)
        # API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
        # headers = {"Authorization": "Bearer YOUR_HF_TOKEN_HERE"}
        
        user_txt = user_txt.lower()
        
        # Smart Offline Logic (ताकि ऐप कभी फेल न हो)
        if "naam" in user_txt:
            resp = "Mera naam Keshavam hai bhai, aapka digital bhai!"
        elif "kaise ho" in user_txt:
            resp = "Main ek dum badiya! Aap batao ghar pe sab kaise hain?"
        elif "khana" in user_txt:
            resp = "Main to bijli pe chalta hoon bhai, aapne mast khana khaya?"
        elif "bye" in user_txt or "alvida" in user_txt:
            resp = "Ram Ram bhai! Phir milenge jaldi."
        else:
            # यहाँ असली API कॉल डाल सकते हैं
            resp = "Bhai, ye baat sun kar maza aa gaya! Main hamesha tumhare saath hoon."

        Clock.schedule_once(lambda dt: self.add_msg("Keshavam", resp))

if __name__ == '__main__':
    KeshavamApp().run()
