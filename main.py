from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle
from PIL import Image, ImageDraw, ImageFont
import os

# فونت کنار فایل پروژه
font_path = "Vazir.ttf"

if os.path.exists(font_path):
    LabelBase.register(name="Vazir", fn_regular=font_path)
else:
    print(f"⚠️ فونت پیدا نشد: {font_path}. از فونت پیش فرض استفاده می‌شود.")
    font_path = None

class ColoredBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.92, 0.95, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class DigApp(App):
    def build(self):
        self.distances = []
        self.readings = []
        self.depths = []
        self.total_distance = 0
        self.slope_sign = 1
        self.distance_mode = "step"

        self.save_dir = "/storage/emulated/0/Pictures/masoudad7"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        self.root = ColoredBoxLayout()
        self.show_guide()
        return self.root

    # ------------------------------
    # صفحه راهنما
    # ------------------------------
    def show_guide(self):
        guide_text = (
            "سلام خدمت کاربر گرامی\n\n"
            "به مثبت و منفی بودن شیب دقت کنید.\n"
            "اگر عمق حفاری‌ها به سطح زمین نزدیک شوند شیب مثبت و در غیر اینصورت منفی است.\n\n"
            "فاصله‌ها می‌توانند مرحله‌ای یا تجمعی باشند.\n"
            "با دکمه «محاسبه عمق» مراحل بعدی پیش می‌رود.\n\n"
            f"⚠️ خروجی برنامه به صورت تصویر (PNG) ذخیره می‌شود.\n"
            f"مسیر ذخیره: {self.save_dir}\n"
            "می‌توانید تصاویر ذخیره شده را در گالری مشاهده کنید.\n\n"
            "خدمت‌گزار شما، مهندس مسعود احمدی دارانی"
        )
        layout = ColoredBoxLayout(orientation='vertical', padding=20, spacing=20)
        label = Label(
            text=guide_text,
            font_name="Vazir" if font_path else None,
            halign="center",
            valign="middle",
            font_size=45,
            size_hint_y=None,
            color=(0, 0, 0, 1)
        )
        label.bind(width=lambda *x: label.setter("text_size")(label, (label.width, None)))
        label.bind(texture_size=label.setter("size"))
        layout.add_widget(label)

        ok_btn = Button(
            text="✅ تایید و ادامه",
            size_hint=(1, 0),
            font_name="Vazir" if font_path else None,
            font_size=40,
            background_color=(0.1, 0.6, 0.1, 1),
            color=(0, 1, 1, 1)
        )
        ok_btn.bind(on_press=lambda x: self.show_form())
        layout.add_widget(ok_btn)

        self.root.clear_widgets()
        self.root.add_widget(layout)

    # ------------------------------
    # فرم اصلی
    # ------------------------------
    def show_form(self):
        self.root.clear_widgets()
        self.layout = ColoredBoxLayout(orientation='vertical', padding=10, spacing=10)

        self.place_input = TextInput(hint_text="نام محل", font_name="Vazir" if font_path else None, font_size=45)
        self.height_input = TextInput(hint_text="ارتفاع مبدا", input_type='number', input_filter='float', font_name="Vazir" if font_path else None, font_size=45)
        self.slope_input = TextInput(hint_text="شیب (بدون علامت)", input_type='number', input_filter='float', font_name="Vazir" if font_path else None, font_size=45)
        self.slope_btn = Button(text="+", size_hint=(0.2, 1), font_size=32, background_color=(1, 0.5, 0.8, 1), color=(0,0,0,1))
        self.slope_btn.bind(on_press=self.toggle_slope_sign)
        self.sand_input = TextInput(hint_text="شن خور (متر)", input_type='number', input_filter='float', font_name="Vazir" if font_path else None, font_size=45)
        self.benchmark_input = TextInput(hint_text="قرائت مبدا", input_type='number', input_filter='float', font_name="Vazir" if font_path else None, font_size=45)

        self.distance_input = TextInput(hint_text="فاصله", input_type='number', input_filter='float', font_name="Vazir" if font_path else None, font_size=45)
        self.distance_mode_btn = Button(text="مرحله‌ای", size_hint=(0.3, 1), font_name="Vazir" if font_path else None, font_size=45, background_color=(1, 0.5, 0.9, 1), color=(0,0,0,1))
        self.distance_mode_btn.bind(on_press=self.toggle_distance_mode)

        self.reading_next_input = TextInput(hint_text="قرائت بعدی", input_type='number', input_filter='float', font_name="Vazir" if font_path else None, font_size=45)

        self.layout.add_widget(self.place_input)
        self.layout.add_widget(self.height_input)

        slope_box = ColoredBoxLayout(orientation='horizontal', spacing=5)
        slope_box.add_widget(self.slope_input)
        slope_box.add_widget(self.slope_btn)
        self.layout.add_widget(slope_box)

        self.layout.add_widget(self.sand_input)
        self.layout.add_widget(self.benchmark_input)

        distance_box = ColoredBoxLayout(orientation='horizontal', spacing=5)
        distance_box.add_widget(self.distance_input)
        distance_box.add_widget(self.distance_mode_btn)
        self.layout.add_widget(distance_box)

        self.layout.add_widget(self.reading_next_input)

        self.calc_btn = Button(
            text="📐 محاسبه عمق",
            font_name="Vazir" if font_path else None,
            font_size=45,
            background_color=(0.2, 0.4, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        self.calc_btn.bind(on_press=self.calc_depth)
        self.layout.add_widget(self.calc_btn)

        self.end_btn = Button(
            text="💾 پایان و ذخیره جدول",
            font_name="Vazir" if font_path else None,
            font_size=40,
            background_color=(0.2, 0.4,0.8, 1),
            color=(1,1, 1, 1)
        )
        self.end_btn.bind(on_press=self.show_save_table)
        self.end_btn.disabled = True
        self.layout.add_widget(self.end_btn)

        self.result_label = Label(
            text="",
            halign='center',
            valign='middle',
            font_name="Vazir" if font_path else None,
            font_size=45,
            color=(0, 0, 0, 1),
            size_hint_y=None
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.layout.add_widget(self.result_label)

        self.new_form_btn = Button(
            text="🆕 فرم جدید",
            font_name="Vazir" if font_path else None,
            font_size=45,
            background_color=(0.6, 0.6, 0.6, 1),
            color=(1, 1, 1, 1)
        )
        self.new_form_btn.bind(on_press=self.reset_form)
        self.layout.add_widget(self.new_form_btn)

        self.exit_btn = Button(
            text="❌ خروج از برنامه",
            font_name="Vazir" if font_path else None,
            font_size=45,
            background_color=(0.8, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        self.exit_btn.bind(on_press=self.exit_app)
        self.layout.add_widget(self.exit_btn)

        self.root.add_widget(self.layout)

    # ------------------------------
    # توابع کمکی
    # ------------------------------
    def toggle_slope_sign(self, instance):
        self.slope_sign *= -1
        self.slope_btn.text = "+" if self.slope_sign > 0 else "-"

    def toggle_distance_mode(self, instance):
        if self.distance_mode == "step":
            self.distance_mode = "cumulative"
            self.distance_mode_btn.text = "تجمعی"
        else:
            self.distance_mode = "step"
            self.distance_mode_btn.text = "مرحله‌ای"

    def safe_float(self, text, default=0.0):
        try:
            return float(text)
        except:
            return default

    def calc_depth(self, instance):
        height = self.safe_float(self.height_input.text)
        slope = self.safe_float(self.slope_input.text) * self.slope_sign
        sand = self.safe_float(self.sand_input.text)
        benchmark = self.safe_float(self.benchmark_input.text)
        distance = self.safe_float(self.distance_input.text)
        reading = self.safe_float(self.reading_next_input.text)

        if self.distance_mode == "step":
            self.total_distance += distance
        else:
            self.total_distance = distance

        depth = benchmark + height - slope * self.total_distance - reading + sand

        self.distances.append(self.total_distance)
        self.readings.append(reading)
        self.depths.append(depth)

        self.result_label.text = f"عمق حفاری: {depth:.3f} متر"
        self.end_btn.disabled = False

        self.distance_input.text = ""
        self.reading_next_input.text = ""

    # ------------------------------
    # ذخیره جدول
    # ------------------------------
    def show_save_table(self, instance):
        content = ColoredBoxLayout(orientation="vertical", spacing=10, padding=10)
        self.popup_input = TextInput(hint_text="نام محل", multiline=False, font_name="Vazir" if font_path else None, font_size=28)
        content.add_widget(self.popup_input)

        btn_layout = ColoredBoxLayout(orientation="horizontal", spacing=10)
        btn_ok = Button(text="تأیید", font_name="Vazir" if font_path else None, font_size=28, background_color=(0.2,0.6,0.3,1), color=(1,1,1,1))
        btn_cancel = Button(text="انصراف", font_name="Vazir" if font_path else None, font_size=28, background_color=(0.8,0.3,0.3,1), color=(1,1,1,1))
        btn_layout.add_widget(btn_ok)
        btn_layout.add_widget(btn_cancel)
        content.add_widget(btn_layout)

        self.popup = Popup(title="نام محل را وارد کنید",
                           content=content,
                           size_hint=(0.8, 0.4))
        btn_ok.bind(on_press=self.save_with_place)
        btn_cancel.bind(on_press=self.popup.dismiss)
        self.popup.open()

    def save_with_place(self, instance):
        place = self.popup_input.text.strip()
        self.popup.dismiss()
        if not place:
            self.result_label.text = "⚠️ لطفاً نام محل را وارد کنید."
            return

        col_headers = ["شماره", "فاصله", "قرائت بعدی", "عمق حفاری"]
        col_widths = [100, 150, 150, 150]
        row_height = 40
        total_width = sum(col_widths) + 40
        total_height = 280 + len(self.depths) * row_height

        img = Image.new("RGB", (total_width, total_height), color="white")
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype(font_path, 22) if font_path else ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        first_slope = self.safe_float(self.slope_input.text) * self.slope_sign
        first_benchmark = self.safe_float(self.benchmark_input.text)
        draw.text((20, 20), f"📍 محل حفاری: {place}", fill="black", font=font)
        draw.text((20, 60), f"شیب: {first_slope:.3f} | قرائت مبدا: {first_benchmark:.3f}", fill="black", font=font)

        start_y = 100
        x_positions = [20]
        for w in col_widths:
            x_positions.append(x_positions[-1] + w)

        # رسم سرستون
        for i, header in enumerate(col_headers):
            bbox = draw.textbbox((0, 0), header, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            draw.text(
                (x_positions[i] + (col_widths[i]-text_width)/2, start_y + (row_height-text_height)/2),
                header,
                fill="black",
                font=font
            )

        # رسم جدول و پر کردن داده‌ها
        for y in range(start_y, start_y + (len(self.depths)+1)*row_height + 1, row_height):
            draw.line((20, y, total_width-20, y), fill="black", width=2)
        for x in x_positions:
            draw.line((x, start_y, x, start_y + row_height*(len(self.depths)+1)), fill="black", width=2)

        for idx, depth in enumerate(self.depths):
            y = start_y + (idx+1)*row_height
            values = [
                str(idx+1),
                f"{self.distances[idx]:.3f}",
                f"{self.readings[idx]:.3f}",
                f"{depth:.3f}"
            ]
            for i, val in enumerate(values):
                bbox = draw.textbbox((0,0), val, font=font)
                text_width = bbox[2]-bbox[0]
                text_height = bbox[3]-bbox[1]
                draw.text(
                    (x_positions[i] + (col_widths[i]-text_width)/2, y + (row_height-text_height)/2),
                    val,
                    fill="black",
                    font=font
                )

        safe_place = place.replace(" ", "_")
        filename = os.path.join(self.save_dir, f"{safe_place}.png")
        img.save(filename)
        self.result_label.text = f"✅ جدول ذخیره شد: {filename}"

    def reset_form(self, instance):
        self.place_input.text = ""
        self.height_input.text = ""
        self.slope_input.text = ""
        self.distance_input.text = ""
        self.sand_input.text = ""
        self.benchmark_input.text = ""
        self.reading_next_input.text = ""
        self.result_label.text = ""

        self.distances.clear()
        self.readings.clear()
        self.depths.clear()
        self.total_distance = 0
        self.distance_mode = "step"
        self.distance_mode_btn.text = "مرحله‌ای"

        self.end_btn.disabled = True

    def exit_app(self, instance):
        App.get_running_app().stop()

if __name__ == "__main__":
    DigApp().run()
