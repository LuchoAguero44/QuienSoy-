import random
import time
import streamlit as st

st.set_page_config(page_title="¿Quién Soy?", page_icon="🎭", layout="centered")

# Estilos CSS para la tarjeta en pantalla completa y la cuenta regresiva
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .full-screen-card {
        height: 68vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #111111;
        color: #FFFFFF;
        font-size: 10vw;
        font-weight: 900;
        text-align: center;
        border-radius: 20px;
        border: 4px solid #FF4B4B;
        padding: 20px;
        margin-bottom: 15px;
        word-break: break-word;
    }
    .countdown-card {
        height: 75vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #1E1E1E;
        color: #FF4B4B;
        font-size: 25vw;
        font-weight: bold;
        border-radius: 20px;
        text-align: center;
    }
    .countdown-text {
        font-size: 22px;
        color: #FFFFFF;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

LISTA_PERSONAJES_BASE = [
    # Mitología y Leyendas
    "Zeus",
    "Hércules",
    "Poseidón",
    "Atenea",
    "Odiseo",
    "Thor",
    "Loki",
    "Odín",
    "Anubis",
    "Rey Arturo",
    "Merlín",
    "Medusa",
    "Aquiles",
    "Gilgamesh",
    "Quetzalcóatl",
    # Historia Universal
    "Julio César",
    "Cleopatra",
    "Alejandro Magno",
    "Napoleón Bonaparte",
    "Juana de Arco",
    "Leonardo da Vinci",
    "Gengis Kan",
    "Albert Einstein",
    "Marie Curie",
    "Abraham Lincoln",
    "Winston Churchill",
    "Moctezuma",
    "Simón Bolívar",
    "Marco Polo",
    "Cristóbal Colón",
    # Literatura Clásica
    "Don Quijote",
    "Sancho Panza",
    "Sherlock Holmes",
    "Conde Drácula",
    "Victor Frankenstein",
    "Edmond Dantès",
    "Hamlet",
    "Romeo",
    "Julieta",
    "Elizabeth Bennet",
    "Capitán Ahab",
    "D'Artagnan",
    "Ebenezer Scrooge",
    "Alicia",
    "Tom Sawyer",
    # Cine y Cómics
    "Darth Vader",
    "Luke Skywalker",
    "Indiana Jones",
    "Harry Potter",
    "Gandalf",
    "Frodo Bolsón",
    "Jack Sparrow",
    "James Bond",
    "Batman",
    "Joker",
    "Superman",
    "Spider-Man",
    "Iron Man",
    "Ellen Ripley",
    "Forrest Gump",
    # Anime y Manga
    "Son Goku",
    "Naruto Uzumaki",
    "Monkey D. Luffy",
    "Sailor Moon",
    "Edward Elric",
    "Light Yagami",
    "Spike Spiegel",
    "Eren Yeager",
    "Saitama",
    "Pikachu",
    "Ash Ketchum",
    # Videojuegos
    "Mario",
    "Luigi",
    "Link",
    "Princesa Zelda",
    "Kratos",
    "Lara Croft",
    "Master Chief",
    "Geralt de Rivia",
    "Pac-Man",
    "Sonic",
    "Solid Snake",
    "Arthur Morgan",
    "Cloud Strife",
    "Gordon Freeman",
]

@st.cache_resource
def get_game_state():
  return {
      "players": {},
      "used_characters": [],  # Pa que no se repita bro
      "game_started": False,
      "finished_count": 0,
      "round_id": 0,  # Control para la cuenta regresiva
  }


game = get_game_state()

if "my_name" not in st.session_state:
  st.session_state.my_name = ""
if "last_seen_round" not in st.session_state:
  st.session_state.last_seen_round = -1

st.title("🎭 ¿Quién Soy?")

# formulario para ingresar los nombres
if not st.session_state.my_name or st.session_state.my_name not in game["players"]:
  st.subheader("Ingresa tu nombre para jugar kp")
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
              "rank": None,
          }
        st.session_state.my_name = clean_name
        st.rerun()
      else:
        st.warning("Por favor ingresa un nombre válido.")

  with col_clear:
    if st.button("🗑️ Borrar la lista de jogadores muito bem menino"):
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
  if st.button("❌ Me piché y me voy"):
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
      if st.button(
          "🚀 Iniciar Ronda", type="primary", use_container_width=True
      ):
        if len(game["players"]) < 1:
          st.error("Se necesita al menos 1 jugador para iniciar.")
        else:
          # Seleccionar personajes no usados recientemente
          available = [
              c
              for c in LISTA_PERSONAJES_BASE
              if c not in game["used_characters"]
          ]
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
          game["round_id"] += 1  # Incrementa el id de ronda
          game["game_started"] = True
          st.rerun()

    with col2:
      if st.button(
          "🗑️ Soy thanos y borro a todo el mundo", use_container_width=True
      ):
        game["players"] = {}
        game["game_started"] = False
        game["finished_count"] = 0
        game["used_characters"] = []
        st.session_state.my_name = ""
        st.rerun()

  else:
    my_data = game["players"].get(player_name)

    if not my_data:
      st.warning(
          "Te uniste después de iniciar la ronda. Espera a la siguiente."
      )
      return

    # 1. CUENTA REGRESIVA DE 3 SEGUNDOS
    if st.session_state.last_seen_round != game["round_id"]:
      countdown_box = st.empty()

      for sec in range(3, 0, -1):
        countdown_box.markdown(
            f"""
                    <div class="countdown-card">
                        <div class="countdown-text">📱 ¡PÓNTELO EN TU SYVA!</div>
                        {sec}
                    </div>
                    """,
            unsafe_allow_html=True,
        )
        time.sleep(1)

      countdown_box.markdown(
          """
                <div class="countdown-card">
                    <div class="countdown-text">📱 ¡PÓNTELO EN TU SYVA!</div>
                    ¡YA!
                </div>
                """,
          unsafe_allow_html=True,
      )
      time.sleep(0.5)
      countdown_box.empty()

      st.session_state.last_seen_round = game["round_id"]
      st.rerun()

    # 2. MOSTRAR PERSONAJE EN PANTALLA COMPLETA
    if not my_data["guessed"]:
      st.markdown(
          f"""
            <div class="full-screen-card">
                {my_data['character']}
            </div>
            """,
          unsafe_allow_html=True,
      )

      # Botón para declarar adivinanza justo abajo
      if st.button(
          "🎉 ¡ADIVINÉ MI PERSONAJE, SOY UN/A CRACK!", type="primary", use_container_width=True
      ):
        game["finished_count"] += 1
        rank = game["finished_count"]

        # Asignación de puntos
        points = max(6 - rank, 1)

        my_data["guessed"] = True
        my_data["rank"] = rank
        my_data["score"] += points
        st.rerun()
    else:
      st.success(
          f"¡Adivinaste! Quedaste en el puesto #{my_data['rank']} (+{max(6 - my_data['rank'], 1)} pts)"
      )

      st.divider()

      # Tabla de posiciones y estado actual
      st.write("### 🏆 Posiciones de la ronda")

      leaderboard = []
      for name, info in game["players"].items():
        status = (
            f"✅ Puesto #{info['rank']}" if info["guessed"] else "⏳ Jugando..."
        )
        leaderboard.append(
            {"Jugador": name, "Estado": status, "Puntos Totales": info["score"]}
        )

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
