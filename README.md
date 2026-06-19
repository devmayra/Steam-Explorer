# 🎮 Steam Explorer



Buscador interactivo de juegos de Steam. Muestra precio, descripción, imagen, géneros y estadísticas de jugadores en tiempo real.



## Tecnologías



- Python + Streamlit

- Steam Store API + SteamSpy API (sin API key)



## Instalación local



```bash

git clone https://github.com/tuusuario/steam-explorer.git

cd steam-explorer

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

streamlit run app.py

```



## Estructura



```

steam-explorer/

├── app.py          # Interfaz

├── steam\_api.py    # Conexión con las APIs

├── requirements.txt

└── .gitignore

```


## Notas

- SteamSpy puede no tener estadísticas de juegos AAA recientes o de publishers grandes
- Si un juego no muestra estadísticas, es normal — no es un error
