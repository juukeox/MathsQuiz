import tkinter as tk
import random
from tkinter import messagebox
from datetime import datetime

class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz App")

        self.score = 0
        self.final_score = 0
        self.timer_seconds = 30  # Initial timer value in seconds
        self.current_question = None
        self.questions_attempted = 0


        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("Medium")

        self.problem_label = tk.Label(root, text="", font=("Arial", 24))
        self.problem_label.pack(pady=20)

        self.answer_entry = tk.Entry(root, font=("Arial", 24))
        self.answer_entry.pack(pady=10)

        self.check_button = tk.Button(root, text="Check Answer", command=self.check_answer)
        self.check_button.pack(pady=10)
        self.root.bind("<Return>", lambda event=None: self.check_answer())


        self.timer_label = tk.Label(root, text="", font=("Arial", 18))
        self.timer_label.pack()

        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 18))
        self.score_label.pack()

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=20)

        self.high_scores_button = tk.Button(root, text="High Scores", command=self.show_high_scores)
        self.high_scores_button.pack()

        self.high_scores = []  # List to store high scores (e.g., (score, player_name))

        self.settings_button = tk.Button(root, text="⚙️ Settings", command=self.open_settings)
        self.settings_button.pack(side=tk.BOTTOM, pady =10)

        # Add a label for the username entry
        self.username_label = tk.Label(root, text="Enter Your Name:", font=("Arial", 18))
        self.username_label.pack(pady=10)

        # Add an entry widget for the username
        self.username_entry = tk.Entry(root, font=("Arial", 18))
        self.username_entry.pack(pady=5)

        # Add a button to submit the username
        self.submit_button = tk.Button(root, text="Submit", command=self.submit_username)
        self.submit_button.pack(pady=10)

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
        self.final_score = 0
        self.questions_attempted = 0
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
        if self.difficulty_var.get() == "Hard":
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 20)
            num3 = random.randint(1, 20)
            operator1 = random.choice(["+", "-", "*", "/"])
            operator2 = random.choice(["+", "-", "*", "/"])
            problem = f"{num1} {operator1} {num2} {operator2} {num3}"
        elif self.difficulty_var.get() == "Easy":
            while True:
                num1 = random.randint(1, 10)
                num2 = random.randint(1, 10)
                operator1 = random.choice(["+", "-", "*", "/"])
                problem = f"{num1} {operator1} {num2}"
                try:
                    if int(eval(problem)) == eval(problem):
                        return problem
                except ZeroDivisionError:
                    pass
        else:
            while True:
                num1 = random.randint(1, 20)
                num2 = random.randint(1, 20)
                operator = random.choice(["+", "-", "*", "/"])
                problem = f"{num1} {operator} {num2}"

                # Check if the answer is an integer or has one decimal place
                try:
                    result = eval(problem)
                    if int(result) == result or round(result, 1) == result or (result * 4) % 1 == 0.0:
                        return problem
                except ZeroDivisionError:
                    pass
        return problem

    def check_answer(self):
        user_answer = self.answer_entry.get()
        try:
            correct_answer = eval(self.current_question)
            if float(user_answer) == correct_answer:
                self.score += 1
                self.update_score_label()
                self.questions_attempted += 1
                self.next_question() 
            else:
                self.next_question()
                self.questions_attempted += 1
        except:
            messagebox.showerror("Invalid Input", "Please enter a valid numerical answer.")

    def update_score_label(self):
        self.score_label.config(text=f"Score: {self.score}")

    def update_timer_label(self):
        self.timer_label.config(text=f"Time Left: {self.timer_seconds} seconds")

    def end_game(self):  #not being activated
        self.game_in_progress = False
        self.start_button.config(state=tk.NORMAL)
        self.high_score()
        messagebox.showinfo("Game Over", f"Your final score: {self.final_score}")
        self.save_high_score()
        self.load_high_scores()
        self.timer_seconds = 30 #!!! whatever it was set to before?
        self.update_timer_label
    #    self.update_score_label
    
    def submit_username(self):
        player_name = self.username_entry.get()
        if player_name:
            self.save_high_score(player_name)

    def high_score(self):
        difficulty_scores = {"Hard":2, "Medium":1.3, "Easy":1}
        multiplier = difficulty_scores.get(self.difficulty_var.get(), 1)
        self.final_score = round((self.score - (self.questions_attempted - self.score)) * multiplier, 1) 

    def save_high_score(self, player_name="Unknown"): 
            current_date = datetime.now().strftime("%Y-%m-%d")
            self.high_scores.append((self.final_score, player_name or "Unknown", current_date))
            self.high_scores.sort(reverse=True)
            if len(self.high_scores) > 10:
                self.high_scores = self.high_scores[:10]
            
            with open("high_scores.txt", "w") as file:
                for score, name, date in self.high_scores:
                    file.write(f"{score:.1f}: {name} ({date})\n")

    def load_high_scores(self):
        try:
            with open("high_scores.txt", "r") as file:
                high_scores = file.readlines()
                self.high_scores = [(float(score.split(":")[0].strip()), score.split(":")[1].strip()) for score in high_scores]
                self.high_scores.sort(reverse=True)
        except FileNotFoundError:
            self.high_scores = []

    def show_high_scores(self):
        high_scores_str = "High Scores:\n"
        for i, score_info in enumerate(self.high_scores[:10]):
            if len(score_info) == 3:
                name, score, date = score_info
                high_scores_str += f"{i+1}. {name}: {score} ({date})\n"
            elif len(score_info) == 2:
                score, name = score_info
                high_scores_str += f"{i+1}. {name}: {score}\n"
        messagebox.showinfo("High Scores", high_scores_str)
    
    def open_settings(self):
        # Create a new settings window
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
    
        # Add label and entry widget for setting the number of seconds
        seconds_label = tk.Label(settings_window, text="Time Duration (seconds):")
        seconds_label.pack(pady=10)
    
        seconds_entry = tk.Entry(settings_window, font=("Arial", 18))
        seconds_entry.insert(0, str(self.timer_seconds))  # Display the current value
        seconds_entry.pack(pady=5)
    
        # Add label and option menu for selecting difficulty level
        difficulty_label = tk.Label(settings_window, text="Difficulty Level:")
        difficulty_label.pack(pady=10)
    
        difficulty_options = ["Easy", "Medium", "Hard"]
        difficulty_var = tk.StringVar()
        difficulty_var.set("Medium")  # Default difficulty level
        difficulty_menu = tk.OptionMenu(settings_window, difficulty_var, *difficulty_options)
        difficulty_menu.pack(pady=5)
    
        # Save settings button
        save_button = tk.Button(settings_window, text="Save Settings", command=lambda: self.save_settings(settings_window, seconds_entry, difficulty_var))
        save_button.pack(pady=20)

    def save_settings(self, settings_window, seconds_entry, difficulty_var):
        try:
            # Get and validate user inputs
            new_seconds = int(seconds_entry.get())
            if new_seconds <= 0:   #!!! Add error handling for letters
                messagebox.showerror("Invalid Input", "Please enter a positive number of seconds.")
                return
            
            new_difficulty = difficulty_var.get()
            
            # Update app settings
            self.timer_seconds = new_seconds  # Update the timer value based on user input
            self.difficulty_var = difficulty_var
            self.root.after(0, self.update_timer_label)
            # Handle difficulty level settings here (e.g., adjust question generation logic)
            
            # Update timer label in the main window
            self.update_timer_label()
            
            # Close the settings window
            settings_window.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of seconds.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()

    #layout
    # scoreboard is an average BUT correct answers are more valuable on longer runs