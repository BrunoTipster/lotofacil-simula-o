import random
import tkinter as tk
from tkinter import messagebox
import json

def generate_combination():
    """Gera uma combinação única de 15 números entre 1 e 25."""
    combination = random.sample(range(1, 26), 15)
    return combination

def generate_combinations(num_combinations=120):
    """Gera um número especificado de combinações únicas."""
    combinations = set()
    while len(combinations) < num_combinations:
        combination = tuple(sorted(generate_combination()))
        combinations.add(combination)
    return sorted(combinations)

def count_hits(user_numbers, combination):
    """Conta quantos números do usuário estão na combinação gerada."""
    return len(set(user_numbers) & set(combination))

class LotteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulação de Loteria")
        
        self.selected_numbers = []
        self.buttons = []
        self.combinations = []

        self.create_widgets()
    
    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        for i in range(1, 26):
            button = tk.Button(frame, text=f"{i:02}", width=5, height=2, command=lambda i=i: self.select_number(i))
            button.grid(row=(i-1)//5, column=(i-1)%5, padx=5, pady=5)
            self.buttons.append(button)
        
        self.label = tk.Label(self.root, text="Dezenas selecionadas: 0")
        self.label.pack(pady=10)

        self.check_button = tk.Button(self.root, text="Verificar", command=self.check_results)
        self.check_button.pack(pady=5)

        self.generate_label = tk.Label(self.root, text="Quantas combinações gerar?")
        self.generate_label.pack(pady=5)

        self.generate_entry = tk.Entry(self.root)
        self.generate_entry.pack(pady=5)

        self.generate_button = tk.Button(self.root, text="Gerar", command=self.generate_combinations_and_save)
        self.generate_button.pack(pady=10)
    
    def select_number(self, number):
        if number in self.selected_numbers:
            self.selected_numbers.remove(number)
        else:
            if len(self.selected_numbers) < 15:
                self.selected_numbers.append(number)
            else:
                messagebox.showwarning("Aviso", "Você só pode selecionar 15 números.")
        
        self.update_label()
        self.update_buttons()
    
    def update_label(self):
        self.label.config(text=f"Dezenas selecionadas: {len(self.selected_numbers)}")
    
    def update_buttons(self):
        for button in self.buttons:
            number = int(button.cget("text"))
            if number in self.selected_numbers:
                button.config(bg="lightblue")
            else:
                button.config(bg="SystemButtonFace")

    def check_results(self):
        if len(self.selected_numbers) != 15:
            messagebox.showwarning("Aviso", "Selecione exatamente 15 números.")
            return
        
        if not self.combinations:
            messagebox.showwarning("Aviso", "Gere as combinações primeiro.")
            return

        results = [count_hits(self.selected_numbers, comb) for comb in self.combinations]
        self.show_results(results)
    
    def show_results(self, results):
        result_window = tk.Toplevel(self.root)
        result_window.title("Resultados")

        canvas = tk.Canvas(result_window)
        scrollbar = tk.Scrollbar(result_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        filtered_results = [f"Combinação {i+1}: Acertos: {result}" for i, result in enumerate(results) if result >= 14]
        
        if not filtered_results:
            filtered_results.append("Nenhuma combinação teve 14 ou mais acertos.")

        for result in filtered_results:
            label = tk.Label(scrollable_frame, text=result, justify="left")
            label.pack(anchor="w")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def generate_combinations_and_save(self):
        try:
            num_combinations = int(self.generate_entry.get())
            if num_combinations <= 0:
                raise ValueError

            self.combinations = generate_combinations(num_combinations)
            with open("combinacoes.json", "w") as file:
                json.dump(self.combinations, file, indent=4)

            messagebox.showinfo("Sucesso", f"{num_combinations} combinações geradas e salvas em combinacoes.json.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LotteryApp(root)
    root.mainloop()
