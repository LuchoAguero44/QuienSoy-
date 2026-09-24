import streamlit as st
import random


st.set_page_config(page_title="¿Quién Soy?", page_icon="🎭", layout="centered")

LISTA_PERSONAJES_BASE = [
    # Antiguo Testamento
    "Adán", "Eva", "Caín", "Abel", "Set", "Matusalén", "Noé", "Abraham", "Sara", "Isaac",
    "Rebeca", "Jacob", "Esaú", "Raquel", "Lea", "José", "Moisés", "Aarón", "Miriam", "Josué",
    "Caleb", "Débora", "Gedeón", "Sansón", "Dalila", "Rut", "Noemí", "Samuel", "Saúl", "David",
    "Goliat", "Salomón", "Elías", "Eliseo", "Jonás", "Job", "Isaías", "Jeremías", "Ezequiel", "Daniel",
    "Sadrac", "Mesac", "Abed-nego", "Ester", "Mardoqueo", "Nehemías", "Esdras", "Balaam", "Rahab", "Melquisedec",
    
    # Nuevo Testamento
    "Jesús", "María", "José", "Juan el Bautista", "Pedro", "Andrés", "Santiago el Mayor", "Juan el Apóstol", "Felipe", "Bartolomé",
    "Tomás", "Mateo", "Santiago el Menor", "Tadeo", "Simón el Zelote", "Judas Iscariote", "Matías", "Pablo de Tarso", "Bernabé", "Esteban",
    "María Magdalena", "Marta", "Lázaro", "Zacarías", "Elisabet", "Simeón", "Ana", "Nicodemo", "José de Arimatea", "Zaqueo",
    "Bartimeo", "Jairo", "Tabita", "Cornelio", "Apolos", "Priscila", "Aquila", "Timoteo", "Tito", "Filemón",
    "Lucas", "Marcos", "Poncio Pilato", "Herodes Antipas", "Caifás", "Anás", "Barrabás", "Felipe el Diácono", "Silas", "Agabo"
]

@st.cache_resource
def get_game_state():
    return {
        "players": {},         
        "used_characters": [],  #Pa que no se repita bro
        "game_started": False,
        "finished_count": 0
    }

game = get_game_state()

if "my_name" not in st.session_state:
    st.session_state.my_name = ""

st.title("🎭 ¿Quién Soy? - Juego en Grupo")

# formulario para ingresar los nombres
if not st.session_state.my_name or st.session_state.my_name not in game["players"]:
    st.subheader("Ingresa tu nombre para unirte a la sala")
    name_input = st.text_input("Tu Nombre:")
    
    col_join, col_clear = st.columns(2)
    with col_join:
        if st.button("🚪 Unirse al Juego", type="primary"):
            clean_name = name_input.strip()
            if clean_name:
                if clean_name not in game["players"]:
                    game["players"][clean_name] = {
                        "character": None,
                        "guessed": False,
                        "score": 0,
                        "rank": None
                    }
                st.session_state.my_name = clean_name
                st.rerun()
            else:
                st.warning("Por favor ingresa un nombre válido.")

    with col_clear:
        if st.button("🗑️ Borrar lista de jugadores (Reiniciar Sala)"):
            game["players"] = {}
            game["game_started"] = False
            game["finished_count"] = 0
            game["used_characters"] = []
            st.session_state.my_name = ""
            st.success("Lista de jugadores borrada.")
            st.rerun()
            
    # Mostrar la lista actual de participantes registrados
    if game["players"]:
        st.write("---")
        st.write("### Jugadores actualmente en la sala:")
        for p in game["players"].keys():
            st.write(f"• **{p}**")

    st.stop()

player_name = st.session_state.my_name

col_user, col_exit = st.columns([3, 1])
with col_user:
    st.caption(f"Jugando como: **{player_name}**")
with col_exit:
    if st.button("❌ Salir de la sala"):
        if player_name in game["players"]:
            del game["players"][player_name]
        st.session_state.my_name = ""
        st.rerun()

st.fragment(run_every="3s")
def render_game():
    if not game["game_started"]:
        st.info("Esperando a que todos se unan para iniciar la ronda...")
        st.write("### 👥 Jugadores en la sala:")
        
        for p, data in game["players"].items():
            st.write(f"• **{p}** (Puntos acumulados: {data['score']})")

        st.write("---")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Iniciar Ronda", type="primary", use_container_width=True):
                if len(game["players"]) < 1:
                    st.error("Se necesita al menos 1 jugador para iniciar.")
                else:
                    # Seleccionar personajes no usados recientemente
                    available = [c for c in LISTA_PERSONAJES_BASE if c not in game["used_characters"]]
                    if len(available) < len(game["players"]):
                        # Si no alcanzan, reiniciamos el historial de usados
                        game["used_characters"] = []
                        available = LISTA_PERSONAJES_BASE.copy()

                    random.shuffle(available)

                    for p in game["players"]:
                        char = available.pop()
                        game["players"][p]["character"] = char
                        game["players"][p]["guessed"] = False
                        game["players"][p]["rank"] = None
                        game["used_characters"].append(char)

                    game["finished_count"] = 0
                    game["game_started"] = True
                    st.rerun()

        with col2:
            if st.button("🗑️ Borrar lista de jugadores", use_container_width=True):
                game["players"] = {}
                game["game_started"] = False
                game["finished_count"] = 0
                game["used_characters"] = []
                st.session_state.my_name = ""
                st.rerun()

    else:
        my_data = game["players"].get(player_name)

        if not my_data:
            st.warning("Te uniste después de iniciar la ronda. Espera a la siguiente.")
            return

        st.subheader("📱 Pega el celular a tu frente o muéstralo al grupo")

        # Tarjeta gigante con el personaje
        st.markdown(
            f"""
            <div style="
                background-color: #1E1E1E;
                color: #FFFFFF;
                padding: 35px 20px;
                border-radius: 15px;
                text-align: center;
                font-size: 38px;
                font-weight: bold;
                border: 3px solid #FF4B4B;
                margin-bottom: 20px;">
                {my_data['character']}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Botón para declarar adivinanza
        if not my_data["guessed"]:
            if st.button("🎉 ¡ADIVINÉ MI PERSONAJE!", type="primary", use_container_width=True):
                game["finished_count"] += 1
                rank = game["finished_count"]
                
                # Asignación de puntos
                points = max(6 - rank, 1)

                my_data["guessed"] = True
                my_data["rank"] = rank
                my_data["score"] += points
                st.rerun()
        else:
            st.success(f"¡Adivinaste! Quedaste en el puesto #{my_data['rank']} (+{max(6 - my_data['rank'], 1)} pts)")

        st.divider()

        # Tabla de posiciones y estado actual
        st.write("### 🏆 Posiciones de la ronda")

        leaderboard = []
        for name, info in game["players"].items():
            status = f"✅ Puesto #{info['rank']}" if info["guessed"] else "⏳ Jugando..."
            leaderboard.append({
                "Jugador": name,
                "Estado": status,
                "Puntos Totales": info["score"]
            })

        st.table(leaderboard)

        # Botones para continuar o resetear
        col_next, col_reset_all = st.columns(2)
        with col_next:
            if st.button("🔄 Siguiente Ronda"):
                game["game_started"] = False
                st.rerun()
                
        with col_reset_all:
            if st.button("🗑️ Borrar Jugadores"):
                game["players"] = {}
                game["game_started"] = False
                game["finished_count"] = 0
                game["used_characters"] = []
                st.session_state.my_name = ""
                st.rerun()

render_game()