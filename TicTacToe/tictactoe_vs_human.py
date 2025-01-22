#made using the https://www.geeksforgeeks.org/tic-tac-toe-game-with-gui-using-tkinter-in-python/
#as base
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import pandas as pd
import random
from computer import Computer_Plays
import time

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.num_comp_plays = 0
        self.entrou_for = 0
        self.count_win = 0
        self.count_loss = 0
        self.count_tie = 0

        # Criar o Label para exibir o contador
        self.counter_label = tk.Label(self.root, text=self.get_score_text(), font=("Helvetica", 14))
        self.counter_label.pack()

        self.frame_game = tk.LabelFrame(self.frame,text="Jogo da Velha",width=50,height=50)
        self.frame_game.grid(row=1,column=0)

        # Sempre o X começa
        self.marker = 'X'
        self.stop_game = False
        self.ganhou = ""
        self.cols = ["Começou", "Jogada 1", "Jogada 2","Jogada 3", "Jogada 4", "Jogada 5", "Jogada 6",
                        "Jogada 7", "Jogada 8","Jogada 9",'M00','M01','M02','M10','M11','M12'
                        'M20','M21','M22',"Terminou na Rodada","Ganhou"]     

        self.jogadas_list_cols = ["Jogada 1", "Jogada 2","Jogada 3", "Jogada 4", "Jogada 5", "Jogada 6",
                        "Jogada 7", "Jogada 8","Jogada 9"]
        self.tabuleiro_cols = ['M00','M01','M02','M10','M11','M12','M20','M21','M22']

        self.file = pd.read_csv('jogadas.csv',names=self.cols)


        # Initialize the board (Buttons and states)
        self.b = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self.rodada = 0
        self.jogadas =['0', '0', '0', '0', '0', '0', '0', '0', '0']
        self.states = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]



        self.dict = {'Player': 0,'Computer':1}
        self.dict_inv = {0:'Player',1:'Computer'}

        self.start = random.randint(0,1)
        self.who_played = self.start
        
        # Create the buttons for the Tic Tac Toe board
        for i in range(3):
            for j in range(3):
                self.b[i][j] = Button(
                    self.frame_game, height=4, width=8, font=("Helvetica", "20"),
                    command=lambda r=i, c=j: self.clicked(r, c)
                )
                self.b[i][j].grid(row=i, column=j)

        self.info_game = tk.LabelFrame(self.frame,text="Game Info",width=50,height=50)
        self.info_game.grid(row=2,column=0)

        self.player = Button(self.info_game, text=f"Player : {'X' if  self.start == self.dict['Player'] else 'O'}", height=10, width=40, state=DISABLED)
        self.player.grid(row=0, column=1)
        self.computer = Button(self.info_game, text=f"Computer : {'X' if  self.start == self.dict['Computer'] else 'O'}", height=10, width=40, state=DISABLED)
        self.computer.grid(row=0,column=2)
        
        if self.dict['Computer'] == self.start:
            #self.computer_plays()
            #self.simulation_computer()
            self.computer_plays_algo()

        elif self.dict['Player'] == self.start:
            #self.simulation()
            pass

        self.root.mainloop()

    def minimax_algo(self,maximizing,ttt_matrix,rodada_minimax):
        ### Maximizing == True -> X Plays
        ### Maximizing == False -> O Plays

        if (self.check_if_win_minimax(ttt_matrix) == True) and (maximizing == True):
            ## se esta rodada de max, o X jogará, sendo assim, se o tubuleiro agora esta finalizado
            ## o O ganhou
            return -1*(9-rodada_minimax+1)
        
        if (self.check_if_win_minimax(ttt_matrix) == True) and (maximizing == False):
            ## se esta rodada de min, o O jogará, sendo assim, se o tubuleiro agora esta finalizado
            ## o X ganhou
            return 1*(9-rodada_minimax+1)
        
        if (self.check_if_win_minimax(ttt_matrix) == 'Tie'):
            return 0

        if (self.check_if_win_minimax(ttt_matrix) == 'Continua o Jogo'):
            pass

        ## Continuando o Jogo
        if maximizing == True:
            max_score  = float('-inf')
            marker = 'X'
            for row in range(3):
                for col in range(3):
                    ttt_matrix_copy = [row[:] for row in ttt_matrix]
                    if ttt_matrix_copy[row][col] == 0:
                        ttt_matrix_copy[row][col] = marker
                        algo_score = self.minimax_algo(maximizing=False,ttt_matrix=ttt_matrix_copy,rodada_minimax=rodada_minimax+1)
                        ttt_matrix_copy[row][col] = 0
                        ## pontuação maxima possivel para a rodada, para otimizar o processo de maximizacao
                        ## não precisando rodar todos os for, otimizando o codigo
                        max_score = max(max_score,algo_score)
                        max_score_possible = 1*(9-(rodada_minimax+1)+1)
                        if max_score == max_score_possible:
                            return max_score ## não deixa a branch continuar, não sentido testar outros resultados se este é o ótimo
                        
                        
                        
            return max_score


                
        if maximizing == False:
            min_score  = float('inf')
            marker = 'O'
            
            for row in range(3):
                for col in range(3):
                    ttt_matrix_copy = [row[:] for row in ttt_matrix]
                    if ttt_matrix_copy[row][col] == 0:
                        ttt_matrix_copy[row][col] = marker
                        algo_score = self.minimax_algo(maximizing=True,ttt_matrix=ttt_matrix_copy,rodada_minimax=rodada_minimax+1)
                        ttt_matrix_copy[row][col] = 0
                        ## pontuação minima possivel para a rodada, para otimizar o processo de minimização
                        ## não precisando rodar todos os for, otimizando o codigo
                        min_score = min(min_score,algo_score)
                        min_score_possible = -1*(9-(rodada_minimax+1)+1)
                        if min_score == min_score_possible:
                            return min_score ## não deixa a branch continuar, não sentido testar outros resultados se este é o ótimo
                        

            return min_score  

    def computer_plays_algo(self):
        time_start = time.time()
        maximization = None
        ## definir se é max ou min o computador, baseado em quem começou
        if self.dict_inv[self.start] == 'Computer':
            ## computer começou, então o proximo oponente deve minimizar
            maximization = False
            marker = 'X'
            score = float('-inf')
            optimun_score_possible = 1*(9-(self.rodada+1)+1)

        if self.dict_inv[self.start] != 'Computer':
            ## player começou, então o proximo oponente em relação ao computer deve maximizar
            maximization = True
            marker = 'O'
            score = float('inf')
            optimun_score_possible = -1*(9-(self.rodada+1)+1) 

        
        for row in range(3):
            for col in range(3):
                ttt_matrix = [row[:] for row in self.states]
                if ttt_matrix[row][col] == 0:
                    
                    ttt_matrix[row][col] = marker
                    algo_score = self.minimax_algo(maximizing=maximization,ttt_matrix=ttt_matrix,rodada_minimax=self.rodada+1)
                    ## pontuação otima possivel para a rodada, para otimizar o processo de max ou min
                    ## não precisando rodar todos os for, otimizando o codigo

                    
                    ##print(f'Optm score -> {optimun_score_possible} | score -> {score}')
                    ##print(f'Algo-Score na pos {row,col} = {algo_score}, matrix:\n{ttt_matrix}')
                    
                    if (maximization  == False) and (algo_score > score):
                        score = algo_score
                        position_to_play = [row,col]

                    elif (maximization  == True) and (algo_score < score):
                        score = algo_score
                        position_to_play = [row,col]
                        
                    if algo_score == optimun_score_possible:     
                        position_to_play = [row,col]
                        break ## não deixa a branch continuar, não sentido testar outros resultados se este é o ótimo
                    
                    

            if score == optimun_score_possible:
                break ## não deixa a branch continuar, não sentido testar outros resultados se este é o ótimo 
        time_end = time.time() - time_start



        
        self.states[position_to_play[0]][position_to_play[1]] = self.marker
        self.b[position_to_play[0]][position_to_play[1]].configure(text=self.marker)
        #print(f'Rodada : {self.rodada}\nMax Score: {score}\nPosição : {position_to_play}')
        self.num_comp_plays += 1
        self.marker = 'O' if self.marker == 'X' else 'X'
        self.jogadas[self.rodada] = f"Linha: {position_to_play[0]} Coluna: {position_to_play[1]}"
        self.rodada = self.rodada + 1
        self.who_played = self.dict['Computer']
        self.check_if_win()


    def computer_plays(self):
        data = {}
        data[self.cols[0]] = self.start
   
        for i,col in enumerate(self.jogadas_list_cols):
            data[col] = self.jogadas[i]
        

        p_tab = ['Computer Played', 'Opponent Played']
        map_dict = {}
        if self.start == self.dict['Computer']:
            map_dict['X'] = p_tab[0]
            map_dict['O'] = p_tab[1]
            map_dict[0] = 'Nobody Played'
            for line in range(3):
                for col in range(3):
                    data[f'M{line}{col}'] = map_dict[self.states[line][col]]

        elif self.start == self.dict['Player']:
            map_dict['X'] = p_tab[1]
            map_dict['O'] = p_tab[0]
            map_dict[0] = 'Nobody Played'
            for line in range(3):
                for col in range(3):
                    data[f'M{line}{col}'] = map_dict[self.states[line][col]]

        data['Terminou na Rodada'] = self.rodada + 1
        data[self.cols[-1]] = 'Ganhou'


        dataset = pd.DataFrame(data=[data],columns=self.cols)

        comp_plays = Computer_Plays(predict_col=f'Jogada {self.rodada+1}',dataset=dataset)
        y_pred,y_pred_pos=comp_plays.knn_model(n_neighbors=1)
        print('KNN',y_pred,y_pred_pos)
        try:
            c = int(y_pred_pos[0][-1])
            r = int(y_pred_pos[0][7])
            valid_num = True
        except:
            r=0
            c=0
            valid_num = False

        if (self.states[r][c] == 0) and (not self.stop_game) and (valid_num):
            # Update the button with the player's mark
            self.b[r][c].configure(text=self.marker)
            self.states[r][c] = self.marker
        
        ### SVM demora muito
        #else:
        #        y_pred,y_pred_pos=comp_plays.svm()
        #        print('SVM',y_pred,y_pred_pos)
#
        #        try:
        #            c = int(y_pred_pos[0][-1])
        #            r = int(y_pred_pos[0][7])
        #            valid_num = True
        #        except:
        #            c=0
        #            r=0
        #            valid_num = False
#
        #        if (self.states[r][c] == 0) and (not self.stop_game) and (valid_num):
        #            # Update the button with the player's mark
        #            self.b[r][c].configure(text=self.marker)
        #            self.states[r][c] = self.marker
        #            #print('SVM ENTROU',y_pred,y_pred_pos)
            
        else:
            found = False
            self.entrou_for += 1
            for r in range(3):
                for c in range(3):
                    if (self.states[r][c] == 0) and (not self.stop_game):
                        #print(f'ENTROU NO RANDOM {r} {c}')
                        self.b[r][c].configure(text=self.marker)
                        self.states[r][c] = self.marker
                        #print(self.states)
                        found = True
                        break
                if found:
                    break
        
                                
                    #print('Saiu do FOR')
        self.num_comp_plays += 1
        self.marker = 'O' if self.marker == 'X' else 'X'
        self.jogadas[self.rodada] = f"Linha: {r} Coluna: {c}"
        self.rodada = self.rodada + 1
        self.who_played = self.dict['Computer']
        #self.root.after(10000, self.check_if_win)
        self.check_if_win()

        
    def simulation(self):
        r = random.randint(0,2)
        c = random.randint(0,2)
        print(r,c)
        while(self.states[r][c] != 0):
            r = random.randint(0,2)
            c = random.randint(0,2)
            print(r,c)
        if (self.states[r][c] == 0) and (not self.stop_game):
            # Update the button with the player's mark
            self.b[r][c].configure(text=self.marker)
            self.states[r][c] = self.marker
            
            # Switch to the other player
            self.marker = 'O' if self.marker == 'X' else 'X'
            self.jogadas[self.rodada] = f"Linha: {r} Coluna: {c}"
            self.rodada = self.rodada + 1
            # Check if there's a winner
            self.who_played = self.dict['Player']
            print("Início do delay...")
            #self.root.after(10000, self.check_if_win)  # Pausa por 2 segundos
            print("Fim do delay.")
            self.check_if_win()

    def simulation_computer(self):
        r = random.randint(0,2)
        c = random.randint(0,2)
        print(r,c)
        while(self.states[r][c] != 0):
            r = random.randint(0,2)
            c = random.randint(0,2)
            print(r,c)
        if (self.states[r][c] == 0) and (not self.stop_game):
            # Update the button with the player's mark
            self.b[r][c].configure(text=self.marker)
            self.states[r][c] = self.marker
            
            # Switch to the other player
            self.marker = 'O' if self.marker == 'X' else 'X'
            self.jogadas[self.rodada] = f"Linha: {r} Coluna: {c}"
            self.rodada = self.rodada + 1
            # Check if there's a winner
            self.who_played = self.dict['Computer']
            print("Início do delay...")
            #self.root.after(10000, self.check_if_win)  # Pausa por 2 segundos
            print("Fim do delay.")
            self.check_if_win()

            
    def clicked(self, r, c):
        """Handle the player's move."""
        if self.states[r][c] == 0 and not self.stop_game:
            # Update the button with the player's mark
            self.b[r][c].configure(text=self.marker)
            self.states[r][c] = self.marker
            
            # Switch to the other player
            self.marker = 'O' if self.marker == 'X' else 'X'
            self.jogadas[self.rodada] = f"Linha: {r} Coluna: {c}"
            self.rodada = self.rodada + 1
            # Check if there's a winner
            self.who_played = self.dict['Player']
            self.check_if_win()
            

    
    def restart(self):
        


        print(f'Vitórias: {self.count_win} \nEmpates: {self.count_tie}\nDerrotas {self.count_loss}')
        self.update_score()
        data = {}
        data[self.cols[0]] = self.start

        for i,col in enumerate(self.jogadas_list_cols):
            data[col] = self.jogadas[i]
        

        p_tab = ['Computer Played', 'Opponent Played']
        map_dict = {}
        if self.start == self.dict['Computer']:
            map_dict['X'] = p_tab[0]
            map_dict['O'] = p_tab[1]
            map_dict[0] = 'Nobody Played'
            for line in range(3):
                for col in range(3):
                    data[f'M{line}{col}'] = map_dict[self.states[line][col]]

        elif self.start == self.dict['Player']:
            map_dict['X'] = p_tab[1]
            map_dict['O'] = p_tab[0]
            map_dict[0] = 'Nobody Played'
            for line in range(3):
                for col in range(3):
                    data[f'M{line}{col}'] = map_dict[self.states[line][col]]

        data['Venceu na Rodada'] = self.rodada + 1
        data[self.cols[-1]] = self.ganhou
        


        df = pd.DataFrame(data=[data])


        # In this game we can double our data, if we invert the Started columns and the Winerr Column. then change the positions columns
        # Double data
        # In case of tie, change the Started column and the position columns
        
        # map_quem_jogou = {'Computer Played':2, 'Nobody Played': 0, 'Opponent Played':1}
        map_quem_jogou_invert =  {'Computer Played':'Opponent Played', 'Nobody Played': 'Nobody Played', 'Opponent Played':'Computer Played'} 
        # quem comecou dict original
        ## self.dict = {'Player': 0,'Computer':1}
        who_started_invert = {1: 0,0:1}
        # map_column_ganhou = {'Ganhou': 2,'Perdeu': 0,'Empate': 1}
        map_column_ganhou_invert = {'Ganhou': 'Perdeu','Perdeu': 'Ganhou','Empate': 'Empate'}
        copy_to_double_data = df.copy()

        line_index = 0
        # Invert Winner Column
        quem_ganhou_value = copy_to_double_data.loc[line_index,'Ganhou']
        copy_to_double_data.loc[line_index,'Ganhou'] = map_column_ganhou_invert[quem_ganhou_value]
        # Invert the Started Column
        quem_comecou_value = copy_to_double_data.loc[line_index,'Começou']
        copy_to_double_data.loc[line_index,'Começou'] = who_started_invert[quem_comecou_value]
        # Invert Position Data
        for tab_col in self.tabuleiro_cols:
            position_value  = copy_to_double_data.loc[line_index,tab_col]
            copy_to_double_data.loc[line_index,tab_col] = map_quem_jogou_invert[position_value]

        print('Tamanho da DATA: ',len(df))
        
        to_csv_data = pd.concat([df,copy_to_double_data],axis=0)

        to_csv_data.to_csv('jogadas.csv',mode='a',index=False,header=False)

        self.rodada = 0
        self.jogadas =['0', '0', '0', '0', '0', '0', '0', '0', '0']
        self.ganhou = ""

        self.states = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        for i in range(3):
            for j in range(3):
                self.b[i][j].configure(text='')

        self.marker = 'X'
        self.stop_game = False

        self.start = random.randint(0,1)
        self.who_played = self.start

        self.player.config(text=f"Player : {'X' if  self.start == self.dict['Player'] else 'O'}")
        self.computer.config(text=f"Computer : {'X' if  self.start == self.dict['Computer'] else 'O'}")


        if self.dict['Computer'] == self.start:
            #self.computer_plays()
            self.computer_plays_algo() 
            pass
        elif self.dict['Player'] == self.start:
            #self.simulation()
            pass

    def check_if_win_minimax(self,ttt_matrix):
        """Check if there's a winner or a tie."""
        for i in range(3):
            # Check rows
            if ttt_matrix[i][0] == ttt_matrix[i][1] == ttt_matrix[i][2] != 0:
                return True 

            # Check columns
            if ttt_matrix[0][i] == ttt_matrix[1][i] == ttt_matrix[2][i] != 0:
                return True

        # Check diagonals
        if ttt_matrix[0][0] == ttt_matrix[1][1] == ttt_matrix[2][2] != 0:
            return True
        
        if ttt_matrix[0][2] == ttt_matrix[1][1] == ttt_matrix[2][0] != 0:
            return True

        # Check for tie (if all spots are filled and no winner)
        if all(cell != 0 for row in ttt_matrix for cell in row):
            return 'Tie'
        return 'Continua o Jogo'


    def check_if_win(self):
        """Check if there's a winner or a tie."""
        for i in range(3):
            # Check rows
            if self.states[i][0] == self.states[i][1] == self.states[i][2] != 0:
                self.stop_game = True
                #messagebox.showinfo("Winner", f"{self.states[i][0]} Won")
                self.ganhou = 'Ganhou' if self.who_played == self.dict['Computer'] else "Perdeu"
                print(f'Resultado -> \n{self.states}')
                self.root.after(1000,self.restart)
                return

            # Check columns
            if self.states[0][i] == self.states[1][i] == self.states[2][i] != 0:
                self.stop_game = True
                #messagebox.showinfo("Winner", f"{self.states[0][i]} Won!")
                self.ganhou = 'Ganhou' if self.who_played == self.dict['Computer'] else "Perdeu"
                print(f'Resultado -> \n{self.states}')
                self.root.after(1000,self.restart)
                return

        # Check diagonals
        if self.states[0][0] == self.states[1][1] == self.states[2][2] != 0:
            self.stop_game = True
            #messagebox.showinfo("Winner", f"{self.states[0][0]} Won!")
            self.ganhou = 'Ganhou' if self.who_played == self.dict['Computer'] else "Perdeu"
            self.root.after(1000,self.restart)
            return
        
        if self.states[0][2] == self.states[1][1] == self.states[2][0] != 0:
            self.stop_game = True
            #messagebox.showinfo("Winner", f"{self.states[0][2]} Won!")
            self.ganhou = 'Ganhou' if self.who_played == self.dict['Computer'] else "Perdeu"
            print(f'Resultado -> \n{self.states}')
            self.root.after(1000,self.restart)
            return

        # Check for tie (if all spots are filled and no winner)
        if all(cell != 0 for row in self.states for cell in row):
            self.stop_game = True
            #messagebox.showinfo("Tie", "It's a tie!")
            self.ganhou = 'Empate'
            print(f'Resultado -> \n{self.states}')
            self.root.after(2000,self.restart)
            
            return
        if self.stop_game==False and self.who_played == self.dict['Player']:
            #print('AAAAA')
            print("Inicio do Delay 1")
            #self.root.after(150, self.simulation_computer) 
            #self.root.after(150, self.computer_plays)
            #self.computer_plays()    
            self.computer_plays_algo()

        if self.stop_game==False and self.who_played == self.dict['Computer']:
            #print('BBBB')
            print("Inicio do Delay 2")
            #self.root.after(150, self.simulation)
            #self.simulation() 

    def update_score(self):
        # Atualiza os contadores de vitórias, derrotas e empates
        if self.ganhou == 'Ganhou':
            self.count_win += 1
        elif self.ganhou == 'Perdeu':
            self.count_loss += 1
        elif self.ganhou =='Empate':
            self.count_tie += 1

        self.counter_label.config(text=self.get_score_text())

    def get_score_text(self):
        # Gera o texto do contador

        try:
            result=round(self.entrou_for/self.num_comp_plays*100,2)
        except:
            result=0
        return f"Ganhou: {self.count_win} | Perdeu: {self.count_loss} | Empates: {self.count_tie} | Cont entrou for {result}%\n {self.entrou_for}/{self.num_comp_plays}"

if __name__ == '__main__':
    TicTacToe()
