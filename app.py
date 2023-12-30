from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from datetime import datetime, timedelta
from kivy.clock import Clock

class TimerApp(MDApp):
    def build(self):
        self.subject_input = MDTextField(
            hint_text="Enter Subject",
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            size_hint=(None, None),
            width=200
        )
        self.start_button = MDRaisedButton(
            text="Start Timer",
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            on_press=self.start_timer,
            size_hint=(None, None),
            width=200
        )
        self.pause_button = MDRaisedButton(
            text="Pause Timer",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            on_press=self.pause_timer,
            size_hint=(None, None),
            width=200,
            disabled=True
        )
        self.stop_button = MDRaisedButton(
            text="Stop Timer",
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            on_press=self.stop_timer,
            size_hint=(None, None),
            width=200,
            disabled=True
        )
        self.running_time_label = MDTextField(
            text="",
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            size_hint=(None, None),
            width=200,
            readonly=True
        )
        self.root = Builder.load_string(
            '''
BoxLayout:
    orientation: 'vertical'
    spacing: '10dp'
    padding: '10dp'
    MDLabel:
        text: 'Timer App'
        theme_text_color: "Secondary"
        halign: 'center'
        font_style: 'H4'
    MDLabel:
        text: 'Record:'
        theme_text_color: "Primary"
        halign: 'left'
        font_style: 'Subtitle1'
    ScrollView:
        MDList:
            id: record_list
    '''
        )

        self.root.add_widget(self.subject_input)
        self.root.add_widget(self.start_button)
        self.root.add_widget(self.pause_button)
        self.root.add_widget(self.stop_button)
        self.root.add_widget(self.running_time_label)

        return self.root

    def start_timer(self, instance):
        if not hasattr(self, 'start_time'):
            self.start_time = datetime.now()
            self.subject = self.subject_input.text
            self.stop_button.disabled = False
            self.pause_button.disabled = False
            self.start_button.disabled = True
            self.running_time_label.text = "Running..."
            self.running_time_schedule = Clock.schedule_interval(self.update_running_time, 1)
        else:
            self.show_dialog("Error", "Timer already running.")

    def update_running_time(self, dt):
        if hasattr(self, 'start_time'):
            current_time = datetime.now()
            elapsed_time = current_time - self.start_time
            self.running_time_label.text = f"Running Time: {str(elapsed_time)}"

    def pause_timer(self, instance):
        if hasattr(self, 'start_time'):
            if not hasattr(self, 'pause_time'):
                self.pause_time = datetime.now()
                self.running_time_schedule.cancel()
                self.running_time_label.text = "Paused"
            else:
                self.start_time += (datetime.now() - self.pause_time)
                self.running_time_label.text = "Running..."
                self.running_time_schedule = Clock.schedule_interval(self.update_running_time, 1)
                delattr(self, 'pause_time')

    def stop_timer(self, instance):
        if hasattr(self, 'start_time'):
            end_time = datetime.now()
            elapsed_time = end_time - self.start_time
            self.show_dialog("Timer Stopped", f"Subject: {self.subject}\nStart Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\nElapsed Time: {str(elapsed_time)}")
            self.record_data(self.subject, self.start_time, elapsed_time)
            self.update_record()
            self.running_time_schedule.cancel()
            delattr(self, 'start_time')
            self.running_time_label.text = ""
            self.start_button.disabled = False
            self.pause_button.disabled = True
            self.stop_button.disabled = True
        else:
            self.show_dialog("Error", "No timer running.")

    def record_data(self, subject, start_time, elapsed_time):
        record = f"Subject: {subject}\nStart Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\nTime spent: {str(elapsed_time)}\n\n"
        try:
            with open("record.txt", "a") as file:
                file.write(record)
        except Exception as e:
            self.show_dialog("Error", f"Failed to record data: {str(e)}")

    def update_record(self):
        try:
            with open("record.txt", "r") as file:
                records = file.read()
        except Exception as e:
            self.show_dialog("Error", f"Failed to read records: {str(e)}")

        self.root.ids.record_list.clear_widgets()
        for record in records.split("\n\n")[:-1]:
            self.root.ids.record_list.add_widget(MDTextField(text=record, multiline=True, readonly=True))

    def show_dialog(self, title, text):
        dialog = MDDialog(title=title, text=text, size_hint=(0.9, 0.5))
        dialog.open()

if __name__ == '__main__':
    TimerApp().run()
