import math
from tkinter import *
from tkinter import messagebox, ttk
from plyer import notification

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
mark = "✔"
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    label.config(text="Timer")
    tick.config(text="")
    global reps
    reps = 0

# ---------------------------- NOTIFICATION MECHANISM ------------------------------- #
def show_popup(message):
    popup = Toplevel(window)
    popup.title("Time's Up!")
    popup.geometry("300x150")
    popup.config(padx=20, pady=20, bg=YELLOW)

    label = Label(popup, text=message, font=(FONT_NAME, 18, "bold"), bg=YELLOW, fg=RED)
    label.pack(expand=True)

    ok_button = Button(popup, text="OK", command=popup.destroy)
    ok_button.pack()
    popup.attributes("-topmost", True)  # Keep the window on top

def notify(message):
    notification.notify(
        title="Pomodoro Timer",
        message=message,
        app_name="Pomodoro",
        timeout=10  # Notification lasts for 10 seconds
    )

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    global mark
    reps += 1
    work_seconds = WORK_MIN * 60
    short_break_seconds = SHORT_BREAK_MIN * 60
    long_break_seconds = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_seconds)
        label.config(text="Break", fg=PINK)

    elif reps % 2 == 0:
        count_down(short_break_seconds)
        label.config(text="Break", fg=RED)

    else:
        count_down(work_seconds)
        label.config(text="Work", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_min < 10:
        count_min = f"0{count_min}"

    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0:
        global timer
        timer = window.after(10, count_down, count - 1)
    else:
        # Use either pop-up or system notification
        if reps % 8 == 0:
            show_popup("Take a Long Break!")  # Or replace with notify("Take a Long Break!")
        elif reps % 2 == 0:
            show_popup("Take a Short Break!")  # Or replace with notify("Take a Short Break!")
        else:
            show_popup("Get Back to Work!")  # Or replace with notify("Get Back to Work!")

        start_timer()
        mark = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            mark += "✔"
        tick.config(text=mark)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(103, 133, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 50))
label.grid(row=0, column=1)

start = Button(text="Start", highlightthickness=0, bd=0, command=start_timer)
start.grid(row=2, column=0)

reset = Button(text="Reset", highlightthickness=0, relief="flat", bd=0, command=reset_timer)
reset.grid(row=2, column=2)

tick = Label(bg=YELLOW, fg=GREEN)
tick.grid(row=3, column=1)

window.mainloop()