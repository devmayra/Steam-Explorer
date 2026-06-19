import streamlit as st
from steam_api import buscar_juegos, obtener_detalle, obtener_steamspy

st.set_page_config(page_title="Steam Explorer", page_icon="🎮", layout="wide")
st.title("🎮 Steam Explorer")
st.caption("Buscá y comparé juegos de Steam")

# --- BUSCADOR ---
query = st.text_input("Buscar juego", placeholder="Ej: Counter-Strike, Elden Ring...")

if query:
    with st.spinner("Buscando..."):
        resultados = buscar_juegos(query)

    if not resultados:
        st.warning("No se encontraron resultados.")
    else:
        # Selector de juego
        nombres = {j["name"]: j["id"] for j in resultados if "name" in j}
        seleccion = st.selectbox("Seleccioná un juego", list(nombres.keys()))

        if seleccion:
            appid = nombres[seleccion]

            col1, col2 = st.columns(2)

            with st.spinner("Cargando datos..."):
                detalle = obtener_detalle(appid)
                spy = obtener_steamspy(appid)

            # --- COLUMNA 1: info de Steam ---
            with col1:
                st.subheader("📋 Info general")

                if detalle.get("header_image"):
                    st.image(detalle["header_image"])

                if detalle.get("short_description"):
                    st.write(detalle["short_description"])

                precio = detalle.get("price_overview", {})
                if precio:
                    st.metric("💲 Precio", precio.get("final_formatted", "N/A"))
                else:
                    st.metric("💲 Precio", "Gratis")

                if detalle.get("genres"):
                    generos = ", ".join(g["description"] for g in detalle["genres"])
                    st.write(f"**Géneros:** {generos}")

                if detalle.get("release_date"):
                    st.write(f"**Lanzamiento:** {detalle['release_date'].get('date', 'N/A')}")

            # --- COLUMNA 2: info de SteamSpy ---
            with col2:
                st.subheader("📊 Estadísticas")

                ccu = spy.get("ccu", 0)
                owners = spy.get("owners", "")
                horas = spy.get("average_forever", 0)

                if not spy or (ccu == 0 and not owners):
                    st.info("SteamSpy no tiene estadísticas para este juego. Puede ser un DLC, un juego muy nuevo, o hubo demasiadas consultas seguidas. Esperá 1 minuto y reintentá.")
                else:
                    st.metric("👥 Jugadores ahora", f"{ccu:,}" if ccu else "No disponible")
                    st.metric("📦 Copias vendidas (aprox)", owners if owners else "No disponible")

                    if horas and horas > 0:
                        st.metric("⏱️ Horas promedio jugadas", f"{horas:,} hs")
                    else:
                        st.metric("⏱️ Horas promedio jugadas", "No disponible")

                if spy.get("tags"):
                    st.write("**Tags populares:**")
                    tags = list(spy["tags"].keys())[:8]
                    st.write(" · ".join(f"`{t}`" for t in tags))