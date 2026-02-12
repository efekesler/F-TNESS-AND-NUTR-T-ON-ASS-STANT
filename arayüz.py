import tkinter as tk
from tkinter import scrolledtext
from nlp_model import ask_fitness_assistant, ask_nutrition_assistant


class FitnessApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Fitness Assistant")
        self.geometry("650x750")
        self.configure(bg="#121212")

        container = tk.Frame(self, bg="#121212")
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, FitnessPage, NutritionPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, page):
        self.frames[page].tkraise()


# =========================
# HOME PAGE
# =========================

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")

        main_container = tk.Frame(self, bg="#121212")
        main_container.pack(expand=True)

        tk.Label(
            main_container,
            text="Fitness Assistant",
            font=("Segoe UI", 34, "bold"),
            bg="#121212",
            fg="white"
        ).pack(pady=(40, 10))

        tk.Label(
            main_container,
            text="Antrenman ve beslenme için kişisel dijital koçun",
            font=("Segoe UI", 14),
            bg="#121212",
            fg="#aaaaaa"
        ).pack(pady=(0, 50))

        card_container = tk.Frame(main_container, bg="#121212")
        card_container.pack()

        # FITNESS CARD
        fitness_card = tk.Frame(card_container, bg="#1f1f1f",
                                width=320, height=130,
                                highlightbackground="#2e2e2e",
                                highlightthickness=1)
        fitness_card.pack(pady=15)
        fitness_card.pack_propagate(False)

        fitness_title = tk.Label(
            fitness_card,
            text="Fitness Chat",
            font=("Segoe UI", 18, "bold"),
            bg="#1f1f1f",
            fg="white"
        )
        fitness_title.pack(pady=(25, 5))

        fitness_desc = tk.Label(
            fitness_card,
            text="Antrenman programı ve performans geliştirme",
            font=("Segoe UI", 11),
            bg="#1f1f1f",
            fg="#bbbbbb"
        )
        fitness_desc.pack()

        def go_fitness(event):
            controller.show_frame(FitnessPage)

        for widget in (fitness_card, fitness_title, fitness_desc):
            widget.bind("<Button-1>", go_fitness)
            widget.bind("<Enter>", lambda e, w=fitness_card: w.config(bg="#2a2a2a"))
            widget.bind("<Leave>", lambda e, w=fitness_card: w.config(bg="#1f1f1f"))

        # NUTRITION CARD
        nutrition_card = tk.Frame(card_container, bg="#1f1f1f",
                                  width=320, height=130,
                                  highlightbackground="#2e2e2e",
                                  highlightthickness=1)
        nutrition_card.pack(pady=15)
        nutrition_card.pack_propagate(False)

        nutrition_title = tk.Label(
            nutrition_card,
            text="Nutrition Chat",
            font=("Segoe UI", 18, "bold"),
            bg="#1f1f1f",
            fg="white"
        )
        nutrition_title.pack(pady=(25, 5))

        nutrition_desc = tk.Label(
            nutrition_card,
            text="Diyet planı ve sporcu beslenmesi",
            font=("Segoe UI", 11),
            bg="#1f1f1f",
            fg="#bbbbbb"
        )
        nutrition_desc.pack()

        def go_nutrition(event):
            controller.show_frame(NutritionPage)

        for widget in (nutrition_card, nutrition_title, nutrition_desc):
            widget.bind("<Button-1>", go_nutrition)
            widget.bind("<Enter>", lambda e, w=nutrition_card: w.config(bg="#2a2a2a"))
            widget.bind("<Leave>", lambda e, w=nutrition_card: w.config(bg="#1f1f1f"))


# =========================
# FITNESS PAGE
# =========================

class FitnessPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")

        top = tk.Frame(self, bg="#121212")
        top.pack(fill="x", pady=10)

        tk.Button(
            top, text="←",
            font=("Segoe UI", 14, "bold"),
            bg="#1f1f1f", fg="white", bd=0,
            command=lambda: controller.show_frame(HomePage)
        ).pack(side="left", padx=15)

        tk.Label(
            top, text="Fitness Chat",
            font=("Segoe UI", 20, "bold"),
            bg="#121212", fg="white"
        ).pack(side="left", padx=10)

        chat_card = tk.Frame(self, bg="#1f1f1f")
        chat_card.pack(fill="both", expand=True, padx=25, pady=10)

        self.chat = scrolledtext.ScrolledText(
            chat_card,
            bg="#1f1f1f",
            fg="white",
            font=("Segoe UI", 11),
            wrap="word",
            bd=0,
            highlightthickness=0,
            state="disabled"
        )
        self.chat.pack(fill="both", expand=True, padx=15, pady=15)

        self.chat.tag_config("user", foreground="#3fa9f5")
        self.chat.tag_config("coach", foreground="#00c853")

        bottom = tk.Frame(self, bg="#121212")
        bottom.pack(fill="x", padx=25, pady=15)

        self.entry = tk.Text(
            bottom, height=2,
            bg="#1f1f1f", fg="white",
            insertbackground="white",
            font=("Segoe UI", 11),
            bd=0
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        tk.Button(
            bottom, text="Gönder",
            font=("Segoe UI", 11, "bold"),
            bg="#00c853", fg="white",
            bd=0, padx=15, pady=5,
            command=self.send
        ).pack(side="right")

    def send(self):
        text = self.entry.get("1.0", tk.END).strip()
        if not text:
            return

        self.entry.delete("1.0", tk.END)
        reply = ask_fitness_assistant(text)

        self.chat.config(state="normal")
        self.chat.insert(tk.END, "Sen: " + text + "\n", "user")
        self.chat.insert(tk.END, "Koç: " + reply + "\n\n", "coach")
        self.chat.yview(tk.END)
        self.chat.config(state="disabled")


# =========================
# NUTRITION PAGE
# =========================

class NutritionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")

        top = tk.Frame(self, bg="#121212")
        top.pack(fill="x", pady=10)

        tk.Button(
            top, text="←",
            font=("Segoe UI", 14, "bold"),
            bg="#1f1f1f", fg="white", bd=0,
            command=lambda: controller.show_frame(HomePage)
        ).pack(side="left", padx=15)

        tk.Label(
            top, text="Nutrition Chat",
            font=("Segoe UI", 20, "bold"),
            bg="#121212", fg="white"
        ).pack(side="left", padx=10)

        chat_card = tk.Frame(self, bg="#1f1f1f")
        chat_card.pack(fill="both", expand=True, padx=25, pady=10)

        self.chat = scrolledtext.ScrolledText(
            chat_card,
            bg="#1f1f1f",
            fg="white",
            font=("Segoe UI", 11),
            wrap="word",
            bd=0,
            highlightthickness=0,
            state="disabled"
        )
        self.chat.pack(fill="both", expand=True, padx=15, pady=15)

        self.chat.tag_config("user", foreground="#3fa9f5")
        self.chat.tag_config("coach", foreground="#00c853")

        bottom = tk.Frame(self, bg="#121212")
        bottom.pack(fill="x", padx=25, pady=15)

        self.entry = tk.Text(
            bottom, height=2,
            bg="#1f1f1f", fg="white",
            insertbackground="white",
            font=("Segoe UI", 11),
            bd=0
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        tk.Button(
            bottom, text="Gönder",
            font=("Segoe UI", 11, "bold"),
            bg="#00c853", fg="white",
            bd=0, padx=15, pady=5,
            command=self.send
        ).pack(side="right")

    def send(self):
        text = self.entry.get("1.0", tk.END).strip()
        if not text:
            return

        self.entry.delete("1.0", tk.END)
        reply = ask_nutrition_assistant(text)

        self.chat.config(state="normal")
        self.chat.insert(tk.END, "Sen: " + text + "\n", "user")
        self.chat.insert(tk.END, "Beslenme Uzmanı: " + reply + "\n\n", "coach")
        self.chat.yview(tk.END)
        self.chat.config(state="disabled")


# =========================

if __name__ == "__main__":
    app = FitnessApp()
    app.mainloop()
