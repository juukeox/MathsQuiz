import tkinter as tk
import random
from tkinter import messagebox

class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz App")

        self.score = 0
        self.timer_seconds = 30  # Initial timer value in seconds
        self.current_question = None
        self.questions_answered = 0

        self.problem_label = tk.Label(root, text="", font=("Arial", 24))
        self.problem_label.pack(pady=20)

        self.answer_entry = tk.Entry(root, font=("Arial", 24))
        self.answer_entry.pack(pady=10)

        self.check_button = tk.Button(root, text="Check Answer", command=self.check_answer)
        self.check_button.pack(pady=10)
        self.root.bind("<Return>", lambda event=None: self.check_answer())


        self.timer_label = tk.Label(root, text="0", font=("Arial", 18))
        self.timer_label.pack()

        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 18))
        self.score_label.pack()

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=20)

        self.high_scores_button = tk.Button(root, text="High Scores", command=self.show_high_scores)
        self.high_scores_button.pack()

        self.high_scores = []  # List to store high scores (e.g., (score, player_name))

        self.load_high_scores()  # Load high scores from a file if available

        self.timer = None  # Timer object
        self.game_in_progress = False

    def start_game(self):
        self.reset_game()
        self.start_button.config(state=tk.DISABLED)
        self.next_question()
        self.update_timer()

    def update_timer(self):
        if self.timer_seconds > 0 and self.game_in_progress:
            self.timer_seconds -= 1
            self.update_timer_label()
            self.root.after(1000, self.update_timer)
        elif self.timer_seconds == 0 and self.game_in_progress:
            
            self.end_game()

    def reset_game(self):
        self.score = 0
        self.questions_answered = 0
        self.timer_seconds = 30
        self.update_score_label()
        self.update_timer_label()
        self.load_high_scores()
        self.game_in_progress = True

    def next_question(self):
        if self.timer_seconds <= 0:
            self.end_game()
            return

        self.current_question = self.generate_problem()
        self.problem_label.config(text=self.current_question)
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
        self.update_timer_label()
        self.update_score_label()

    def generate_problem(self):
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operator = random.choice(["+", "-", "*", "/"])
        problem = f"{num1} {operator} {num2}"
        return problem

    def check_answer(self):
        user_answer = self.answer_entry.get()
        try:
            correct_answer = eval(self.current_question)
            if float(user_answer) == correct_answer:
                self.score += 1
                self.update_score_label()
                self.questions_answered += 1
                if self.questions_answered < 10:
                    self.next_question()
                else:
                    self.end_game()
            else:
                self.next_question()
        except:
            messagebox.showerror("Invalid Input", "Please enter a valid numerical answer.")

    def update_score_label(self):
        self.score_label.config(text=f"Score: {self.score}")

    def update_timer_label(self):
        self.timer_label.config(text=f"Time Left: {self.timer_seconds} seconds")

    def end_game(self):
        self.game_in_progress = False
        self.start_button.config(state=tk.NORMAL)
        messagebox.showinfo("Game Over", f"Your final score: {self.score}")
        self.save_high_score()
        self.load_high_scores()

    def save_high_score(self):
        player_name = messagebox.askstring("High Score", "Enter your name:")
        if player_name:
            self.high_scores.append((self.score, player_name))
            self.high_scores.sort(reverse=True)
            with open("high_scores.txt", "w") as file:
                for score, name in self.high_scores[:10]:  # Save the top 10 high scores
                    file.write(f"{score}: {name}\n")

    def load_high_scores(self):
        try:
            with open("high_scores.txt", "r") as file:
                high_scores = file.readlines()
                self.high_scores = [(int(score.split(":")[0].strip()), score.split(":")[1].strip()) for score in high_scores]
                self.high_scores.sort(reverse=True)
        except FileNotFoundError:
            self.high_scores = []

    def show_high_scores(self):
        high_scores_str = "High Scores:\n"
        for i, (score, name) in enumerate(self.high_scores[:10]):
            high_scores_str += f"{i+1}. {name}: {score}\n"
        messagebox.showinfo("High Scores", high_scores_str)


if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()


    # edit problem function so no questions have 2+ decimal places. Can answer to 1 decimal place?
    #timer doesn't go down
    #layout