import random
import matplotlib.pyplot as plt
import numpy as np

class TicTacToeGame:
    def __init__(self):
        self.trainings = []
        self.board = [['-' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.scores = {'X': 0, 'O': 0, 'draw': 0}

    def read_training_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

            current_move = None
            current_board = []
            for line in lines:
                line = line.strip()

                if line == '':
                    continue

                if line[0].isdigit():
                    if current_board:
                        self.trainings.append((current_move, current_board))
                        current_board = []

                    parts = line.split()
                    if len(parts) == 2:
                        current_move = (int(parts[0]), int(parts[1]))
                    else:
                        print(f"Error: formato incorrecto en la línea '{line}'")
                else:
                    current_board.append(list(line))

            if current_move is not None and current_board:
                self.trainings.append((current_move, current_board))

        except FileNotFoundError:
            print(f"Error: No se puede encontrar el archivo '{filename}'")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")

    def print_trainings(self):
        if not self.trainings:
            print("No se encontraron datos de entrenamiento.")
            return

        for i, (move, board) in enumerate(self.trainings):
            print(f"\nEntrenamiento {i + 1}:")
            print(f"Siguiente movimiento: {move}")
            for row in board:
                print(' '.join(row))
        print(f"\nTotal de entrenamientos: {len(self.trainings)}")

    def print_board(self):
        for row in self.board:
            print(' '.join(row))
        print()

    def check_winner(self):
        for row in self.board:
            if row.count(row[0]) == 3 and row[0] != '-':
                return row[0]

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != '-':
                return self.board[0][col]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != '-':
            return self.board[0][0]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != '-':
            return self.board[0][2]

        return None

    def play_game(self):
        self.board = [['-' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        while True:
            row, col = self.get_random_move()

            if self.board[row][col] == '-':
                self.board[row][col] = self.current_player
            else:
                continue

            winner = self.check_winner()
            if winner:
                self.scores[winner] += 1
                return winner

            if all(cell != '-' for row in self.board for cell in row):
                self.scores['draw'] += 1
                return 'draw'

            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def get_random_move(self):
        empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == '-']
        return random.choice(empty_cells) if empty_cells else (0, 0)

    def plot_results(self, iterations):
        print(f"\nResultados después de {iterations} partidas:")
        print(f"Victorias de X: {self.scores['X']}")
        print(f"Victorias de O: {self.scores['O']}")
        print(f"Empates: {self.scores['draw']}\n")

        x_values = list(range(1, iterations + 1))
        plt.figure(figsize=(14, 6))

        plt.subplot(1, 2, 1)
        plt.bar(['X', 'O', 'Draw'], [self.scores['X'], self.scores['O'], self.scores['draw']])
        plt.xlabel('Jugadores')
        plt.ylabel('Victorias')
        plt.title('Victorias por Jugador')

        plt.subplot(1, 2, 2)
        x_learning = np.convolve([self.scores['X'] / (i + 1) for i in range(iterations)], np.ones(10)/10, mode='valid')
        o_learning = np.convolve([self.scores['O'] / (i + 1) for i in range(iterations)], np.ones(10)/10, mode='valid')
        plt.plot(x_values[9:], x_learning, label='Aprendizaje X', color='blue')
        plt.plot(x_values[9:], o_learning, label='Aprendizaje O', color='orange')
        plt.xlabel('Partidas')
        plt.ylabel('Tasa de Aprendizaje (Promedio Móvil)')
        plt.title('Tasa de Aprendizaje de Jugadores')
        plt.legend()
        plt.tight_layout()
        plt.show()


def main():
    game = TicTacToeGame()
    game.read_training_file('C:/Users/Andres Gordillo/Desktop/Compi/Class300924/RedNeuroTriqui/Entregable/board_train_data.txt')
    game.print_trainings()

    iterations = 0
    max_iterations = 1000
    consecutive_draws = 0

    while iterations < max_iterations and consecutive_draws < 10:
        winner = game.play_game()
        iterations += 1

        if winner == 'draw':
            consecutive_draws += 1
            # Aquí puedes implementar un cambio en el comportamiento de los jugadores si es necesario
        else:
            consecutive_draws = 0

    game.plot_results(iterations)

if __name__ == "__main__":
    main()
