import os
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt

# load the .env file variables
load_dotenv()

# Variables de entorno
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

# Configurar Spotipy con credenciales
auth_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp = Spotify(auth_manager=auth_manager)

# Artista Favorito
artist_id = "711MCceyCBcFnzjGY4Q7Un"

# Información del artista completa
artist_info = sp.artist(artist_id)
# print(artist_info)

# Top 10 canciones de Artista Favorito
top_tracks = sp.artist_top_tracks(artist_id)

# Código para acceder y mostrar los nombres de las tracks, popularidad y duración en minutos# Obtener las canciones más populares del artista
top_tracks = sp.artist_top_tracks(artist_id)

# Extraer los detalles de las canciones más populares
tracks_info = []
for track in top_tracks["tracks"]:
    # Convertir la duración de milisegundos a minutos
    duration_minutes = track['duration_ms'] / 60000

    # Almacenar la información relevante (nombre, popularidad, duración)
    track_details = {
        'name': track['name'],
        'popularity': track['popularity'],
        # Redondeamos a 2 decimales
        'duration_minutes': round(duration_minutes, 2)
    }

    tracks_info.append(track_details)

# Mostrar los resultados
for idx, track in enumerate(tracks_info, 1):
    print(
        f"{idx}. {track['name']} - Popularidad: {track['popularity']} - Duración: {track['duration_minutes']} minutos")

# Convertir datos en pd.Dataframe para posterior visualización
df_tracks = pd.DataFrame(tracks_info)

# Ordenamos por popularidad creciente
df_sorted = df_tracks.sort_values(by='popularity', ascending=True)

# Mostramos el top 3 de canciones con menor popularidad
top_3_tracks = df_sorted.head(3)
print(top_3_tracks)

# Analizamos la relación estadística
# Crear el gráfico de dispersión (scatter plot)
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df_tracks, x='duration_minutes', y='popularity')

# Añadir títulos y etiquetas
plt.title('Relación entre la duración y la popularidad de las canciones')
plt.xlabel('Duración (minutos)')
plt.ylabel('Popularidad')
plt.grid(True)

for i in range(len(df_tracks)):
    plt.annotate(
        df_tracks['name'].iloc[i],  # Nombre de la canción
        (df_tracks['duration_minutes'].iloc[i], df_tracks['popularity'].iloc[i]),  # Posición del texto
        fontsize=5,  # Tamaño de la fuente
    )

# Mostrar el gráfico
plt.show()

print(f'Analizando el gráfico, no podemos concluir que una canción que dure menos tienda a ser más popular que otra que dure más.')
print(f'Si es cierto que las 3 canciones más cortas tienden a ser más populares que las 3 úñtimas que duran más, por lo tanto podemos confirmar una tendencia aquí.')
print(f'Si bien es una tendencia no puede ser tratada como conclusión ya que las dos canciones (2nda y 3era) en el ranking de popularidad\ntienen una duración intermedia (2nda) y larga (3era)')