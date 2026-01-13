import customtkinter as ctk
import time 
ctk.set_appearance_mode("dark")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tecnica de Estudio Pomodoro")
        self.geometry("600x400")

        # ----- Contenedor principal -----
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.modo="pomodoro"
        self.corriendo = False
        self.tiempo_inicial = 0
        self.tiempo_estudio = 25 * 60
        self.tiempo_descanso = 5 * 60
        self.ciclos_completados = 0
        self.tiempo_transcurrido = 0
        self.after_id = None

        # ----- Título -----
        self.titulo = ctk.CTkLabel(
            self.container,
            text="Modo Pomodoro",
            font=("Arial", 22)
        )
        self.titulo.pack(pady=10)

        # ----- Tiempo -----
        self.label_tiempo = ctk.CTkLabel(
            self.container,
            text="00:00:00",
            font=("Arial", 36)
        )
        self.label_tiempo.pack(pady=20)

        # ----- Botones -----
        botones_frame = ctk.CTkFrame(self.container)
        botones_frame.pack(pady=10)

        self.btn_iniciar = ctk.CTkButton(botones_frame, text="Iniciar", command=self.iniciar_pomodoro)
        self.btn_iniciar.grid(row=0, column=0, padx=5)

        self.btn_pausar = ctk.CTkButton(botones_frame, text="Pausar" , command=self.pausar)
        self.btn_pausar.grid(row=0, column=1, padx=5)

        self.btn_continuar = ctk.CTkButton(botones_frame, text="Continuar", command=self.continuar)
        self.btn_continuar.grid(row=0, column=1, padx=5)
        self.btn_continuar.grid_remove()

        self.btn_siguiente = ctk.CTkButton(botones_frame, text="Siguiente", command=self.siguiente)
        self.btn_siguiente.grid(row=0, column=2, padx=5)

        # ----- Ciclos -----
        ciclo_frame = ctk.CTkFrame(self.container)
        ciclo_frame.pack(pady=10)

        self.label_ciclo = ctk.CTkLabel(
            ciclo_frame,
            text="0/3",
            font=("Arial", 16)
        )
        self.label_ciclo.pack()
    def iniciar_pomodoro(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        self.titulo.configure(text="Modo Pomodoro")
        self.btn_continuar.grid_remove()
        self.btn_pausar.grid()
        if not self.corriendo:
            self.corriendo = True
            self.tiempo_inicial = time.time() - self.tiempo_transcurrido
            self.actualizar_pomodoro()
    def actualizar_pomodoro(self):
        self.titulo.configure(text="Modo Pomodoro")
        self.modo="pomodoro"
        
        if self.corriendo:
            self.tiempo_transcurrido = time.time() - self.tiempo_inicial
            tiempo_restante = self.tiempo_estudio - int(self.tiempo_transcurrido)
            horas, rem = divmod(tiempo_restante, 3600)
            minutos, segundos = divmod(rem, 60)
            self.label_tiempo.configure(text=f"{int(horas):02}:{int(minutos):02}:{int(segundos):02}")

            self.after_id = self.after(1000, self.actualizar_pomodoro)
            if tiempo_restante <= 0:
                self.corriendo = False
                self.tiempo_transcurrido = 0
                self.ciclos_completados += 1
                self.label_ciclo.configure(text=f"{self.ciclos_completados}/3")
                self.label_tiempo.configure(text="00:25:00")
                self.iniciar_descanso()
    def pausar(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        self.corriendo = False
        self.btn_pausar.grid_remove()
        self.btn_continuar.grid()


    def iniciar_descanso(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        self.titulo.configure(text="Modo Descanso")

        self.modo="descanso"
        self.tiempo_inicial = time.time()
        self.tiempo_transcurrido = 0
        self.corriendo = True
        self.actualizar_descanso()
    def actualizar_descanso(self):
        self.titulo.configure(text="Modo Descanso")
        self.modo="descanso"
        if self.corriendo:
            self.tiempo_transcurrido = time.time() - self.tiempo_inicial
            tiempo_restante = self.tiempo_descanso - int(self.tiempo_transcurrido)
            horas, rem = divmod(tiempo_restante, 3600)
            minutos, segundos = divmod(rem, 60)
            self.label_tiempo.configure(text=f"{int(horas):02}:{int(minutos):02}:{int(segundos):02}")

            self.after_id = self.after(1000, self.actualizar_descanso)
            if tiempo_restante <= 0:
                self.corriendo = False
                self.tiempo_transcurrido = 0
                self.label_tiempo.configure(text="00:05:00")
                self.siguiente()
    def continuar(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        self.corriendo = True
        self.tiempo_inicial = time.time() - self.tiempo_transcurrido
        if self.modo == "pomodoro":
            self.actualizar_pomodoro()
        else:
            self.actualizar_descanso()
            
    def siguiente(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        
        self.corriendo = False
        self.tiempo_transcurrido = 0
        self.btn_pausar.grid()
        if self.modo == "pomodoro":
            self.ciclos_completados += 1
            self.label_ciclo.configure(text=f"{self.ciclos_completados}/3")
            self.iniciar_descanso()
        else:
            self.iniciar_pomodoro()
    


        



if __name__ == "__main__":
    app = App()
    app.mainloop()
