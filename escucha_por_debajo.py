import speech_recognition as sr
import logging
import configparser
from main import Main
from conexion_ini import connIni

class EscuchaPorDebajo:
    def __init__(self):
        try:
            self.recognized_text = None
            self.r = sr.Recognizer()
            self.m = sr.Microphone()
            
            self.conn = connIni()
            self.config = self.conn.leer_ini()

            # Ajustar el ruido ambiental
            with self.m as source:
                print("Ajustando ruido ambiental... por favor, espera.")
                self.r.adjust_for_ambient_noise(source, duration=2)
                print(f"Umbral ajustado a: {self.r.energy_threshold}")
            
            self.iniciar_escucha()    
        
        except Exception as e:
            print(f"INIT Error: {e}")
            
              
    def grabar_pantalla(self):
        try:
            from capturar_pantalla import VideoEncoding
            from threading import Thread
            self.video = VideoEncoding()
            self.hilo_video = Thread(target=self.video.capturar_pantalla)
            self.hilo_video.start()
        except Exception as e:
            print(f"Grabacion Error: {e}")  

    def callback(self, recognizer, audio):
        try:
            lenguaje = self.config["status"]["languageRec"]
            self.recognized_text = str(recognizer.recognize_google(audio, language=lenguaje)).lower()
            print(f"\nDijiste: {self.recognized_text}")
            indice1 = self.recognized_text.find("jarvis")
            texto1 = self.recognized_text[indice1:]
            indice = texto1.find(" ") 
            texto_jarvis = texto1[:indice]
            comando_jarvis = texto1[indice:].strip()
            clip = comando_jarvis.find("clip")
            xbox = comando_jarvis.find("xbox")   
            jarvis = ["jarvis","yarbis","yarbiss","yarvis","yarviss","yarbis","yarbiss","yarviss"]   
            
            if texto_jarvis in jarvis:
                    
                # Create new instance without background listening
                if hasattr(self, 'stop_listening'):
                    self.stop_listening(wait_for_stop=False)
                    delattr(self, 'stop_listening')
                self.video.cerrar_captura()
                self.hilo_video.join()
                # Execute main flow
                main = Main()
                if clip >= 0:
                    comando = "clip"
                        
                elif xbox >= 0:
                    comando = "xbox"
                    
                else:
                    comando = ""

                main.verificar_texto_voz(comando)
                # Start new background listening with fresh context
                self.m = sr.Microphone()
                self.iniciar_escucha()
                
        except sr.UnknownValueError:
            print(".", end="", flush=True)
        except sr.RequestError as e:
            print(f"\nError de conexión: {e}")
        except Exception as e:
            print(f"\nError: {e}")
    
    def iniciar_escucha(self):
        try:
            print("\nIniciando escucha en segundo plano...")
            self.stop_listening = self.r.listen_in_background(self.m, self.callback)
            grabarPantalla = self.config["status"].getint("grabarPantalla")
            if grabarPantalla:
                self.grabar_pantalla()
            else:
                pass
        except Exception as e:
            
            print(f"Iniciar Escucha Error: {e}")

    def detener_escucha(self):
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
            self.video.cerrar_captura()
            print("Escucha en segundo plano detenida.")
                        
if __name__ == "__main__":
    try:
        escucha = EscuchaPorDebajo()
        input("Presiona Enter para detener la escucha.\n")
        escucha.detener_escucha()
    except Exception as e:
        print(f"Error en el módulo principal: {e}")
