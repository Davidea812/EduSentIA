import nltk
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from unidecode import unidecode
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
import tkinter as tk
from tkinter import messagebox, scrolledtext
import customtkinter as ctk
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext

# Descargar recursos necesarios de NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Inicializar herramientas NLP
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
analyzer = SentimentIntensityAnalyzer()


# Cargar modelo de emociones
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)

# Función de limpieza y lematización
def limpiar_comentario(texto):
    texto = str(texto).lower()
    texto = unidecode(texto)
    texto = re.sub(r'[^\w\s]', '', texto)
    tokens = word_tokenize(texto)
    tokens = [t for t in tokens if t not in stop_words]
    lemas = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(lemas)

# Función de análisis de sentimiento
def obtener_sentimiento(texto):
    puntuacion = analyzer.polarity_scores(texto)
    if puntuacion['compound'] >= 0.05:
        return 'positivo'
    elif puntuacion['compound'] <= -0.05:
        return 'negativo'
    else:
        return 'neutral'

# Función para traducir
from deep_translator import GoogleTranslator

def traducir_texto(texto, src='es', dest='en'):
    try:
        traduccion = GoogleTranslator(source=src, target=dest).translate(texto)
        return traduccion
    except Exception as e:
        print(f"Error al traducir: {e}")
        return texto

# Función principal de análisis para la interfaz
def analizar_comentario():
    comentario_original = entrada_comentario.get("1.0", tk.END).strip()

    if not comentario_original:
        messagebox.showwarning("Campo vacío", "Por favor, ingresa un comentario.")
        return

    comentario_traducido = traducir_texto(comentario_original)
    comentario_limpio = limpiar_comentario(comentario_traducido)
    sentimiento = obtener_sentimiento(comentario_limpio)
    emocion = emotion_model(comentario_limpio)[0]['label']
    resultado = f"Original (ES): {comentario_original}\n\n" \
                f"Traducido (EN): {comentario_traducido}\n\n" \
                f"Comentario limpio: {comentario_limpio}\n\n" \
                f"Sentimiento: {sentimiento.capitalize()}\n" \
                f"Emoción: {emocion.capitalize()}\n" \
                f"Combinado: {sentimiento.capitalize()} + {emocion.capitalize()}"

    salida_resultado.config(state='normal')
    salida_resultado.delete("1.0", tk.END)
    salida_resultado.insert(tk.END, resultado)
    salida_resultado.config(state='disabled')


#import customtkinter as ctk
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext

import customtkinter as ctk
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext

# Configurar tema y colores
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

COLOR_FONDO = "#e0e0e0"
COLOR_TEXTO = "#222222"
COLOR_SALIDA_BG = "#f5f5f5"
COLOR_SALIDA_TEXTO = "#333333"

# Crear ventana
ventana = ctk.CTk()
ventana.title("Analizador de Comentarios")
ventana.geometry("720x560")
ventana.configure(bg=COLOR_FONDO)

# Título
titulo = ctk.CTkLabel(
    master=ventana,
    text="INGRESA TU COMENTARIO",
    font=ctk.CTkFont(size=18, weight="bold"),
    text_color=COLOR_TEXTO
)
titulo.pack(pady=18)

# Entrada de comentario (más pequeña)
entrada_comentario = scrolledtext.ScrolledText(
    ventana,
    width=70,
    height=4,
    font=("Helvetica", 11),
    wrap="word"
)
entrada_comentario.pack(pady=10)

# Función de análisis
def analizar_comentario():
    comentario_original = entrada_comentario.get("1.0", "end").strip()

    if not comentario_original:
        messagebox.showwarning("⚠️ Campo vacío", "Por favor, ingresa un comentario.")
        return

    # Aquí deberías usar tus propias funciones:
    comentario_traducido = traducir_texto(comentario_original)
    comentario_limpio = limpiar_comentario(comentario_traducido)
    sentimiento = obtener_sentimiento(comentario_limpio)
    emocion = emotion_model(comentario_limpio)[0]['label']

    # Estilo bonito del resultado
    resultado = (
        f"📌  COMENTARIO ORIGINAL:\n» {comentario_original}\n\n"
        f"🔁  TRADUCIDO AL INGLÉS:\n» {comentario_traducido}\n\n"
        f"🧹  TEXTO LIMPIO:\n» {comentario_limpio}\n\n"
        f"📊  SENTIMIENTO: {sentimiento.upper()}\n"
        f"🎭  EMOCIÓN: {emocion.upper()}\n"
        f"🎯  RESULTADO FINAL: {sentimiento.upper()} + {emocion.upper()}"
    )

    salida_resultado.configure(state='normal')
    salida_resultado.delete("1.0", "end")
    salida_resultado.insert("end", resultado)
    salida_resultado.configure(state='disabled')

# Botón de análisis
boton_analizar = ctk.CTkButton(
    master=ventana,
    text="ANALIZAR COMENTARIO",
    font=ctk.CTkFont(size=13, weight="bold"),
    command=analizar_comentario
)
boton_analizar.pack(pady=15)

# Área de salida más estética
salida_resultado = scrolledtext.ScrolledText(
    ventana,
    width=70,
    height=12,
    font=("Consolas", 11),  # Fuente monoespaciada para estilo "terminal"
    wrap="word",
    state='disabled',
    background=COLOR_SALIDA_BG,
    foreground=COLOR_SALIDA_TEXTO
)
salida_resultado.pack(pady=10)

ventana.mainloop()
