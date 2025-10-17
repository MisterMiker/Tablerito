import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import base64

# --- Configuración de la página ---
st.set_page_config(page_title="Tablero de dibujo", layout="centered")

st.title("🎨 Tablero Interactivo de Dibujo")

# --- Barra lateral con controles ---
with st.sidebar:
    st.header("⚙️ Propiedades del Tablero")

    # Dimensiones
    st.subheader("Tamaño del lienzo")
    canvas_width = st.slider("Ancho", 300, 1000, 600, 50)
    canvas_height = st.slider("Alto", 200, 700, 400, 50)

    # Herramienta
    drawing_mode = st.selectbox(
        "Herramienta de dibujo",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )

    # Propiedades de trazo
    stroke_width = st.slider("Grosor del trazo", 1, 30, 5)
    stroke_color = st.color_picker("🎨 Color del trazo", "#FFFFFF")

    # Fondo
    bg_color = st.color_picker("🖼️ Color de fondo", "#000000")

    # Botón para limpiar
    clear_canvas = st.button("🧹 Limpiar tablero")

# --- Lienzo principal ---
st.markdown("---")

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key="canvas" if not clear_canvas else f"canvas_{st.session_state.get('reset', 0)}",
)

# --- Botón para guardar dibujo ---
if canvas_result.image_data is not None:
    img = Image.fromarray((canvas_result.image_data).astype("uint8"), "RGBA")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    b64 = base64.b64encode(byte_im).decode()

    st.download_button(
        label="💾 Descargar dibujo",
        data=byte_im,
        file_name="mi_dibujo.png",
        mime="image/png",
    )

# --- Pie de página ---
st.markdown(
    "<p style='text-align:center; color:gray;'>Hecho con ❤️ usando Streamlit</p>",
    unsafe_allow_html=True,
)
