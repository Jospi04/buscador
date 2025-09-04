import streamlit as st
import difflib

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(
    page_title="🛍️ Buscador de Productos",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- BASE DE DATOS DE EJEMPLO ---
productos = [
    {"nombre": "Polo Nike DryFit", "descripcion": "Polo deportivo transpirable", "precio": 79.90, "categoria": "polo", "imagen": "img/polo1.png"},
    {"nombre": "Polo Adidas Training", "descripcion": "Ideal para entrenamientos", "precio": 69.90, "categoria": "polo", "imagen": "img/polo1.png"},
    {"nombre": "Camiseta Oversize", "descripcion": "Estilo urbano y moderno", "precio": 55.00, "categoria": "camiseta", "imagen": "img/polo1.png"},
    {"nombre": "Jean Slim Fit", "descripcion": "Jean azul corte moderno", "precio": 120.00, "categoria": "jean", "imagen": "img/polo1.png"},
    {"nombre": "Jean Roto Urbano", "descripcion": "Estilo callejero con roturas", "precio": 135.00, "categoria": "jean", "imagen": "img/polo1.png"},
    {"nombre": "Zapatillas Nike Air", "descripcion": "Comodidad y estilo", "precio": 250.00, "categoria": "zapatillas", "imagen": "img/polo1.png"},
    {"nombre": "Zapatillas Adidas Classic", "descripcion": "Casuales y resistentes", "precio": 210.00, "categoria": "zapatillas", "imagen": "img/polo1.png"},
    {"nombre": "Vestido Floral", "descripcion": "Vestido veraniego con estampado floral", "precio": 150.00, "categoria": "vestido", "imagen": "img/polo1.png"},
    {"nombre": "Casaca Deportiva Puma", "descripcion": "Abrigo ligero para entrenar", "precio": 180.00, "categoria": "casaca", "imagen": "img/polo2.png"},
    {"nombre": "Short Deportivo Nike", "descripcion": "Short ligero para running", "precio": 89.90, "categoria": "short", "imagen": "img/polo2.png"},
    {"nombre": "Short Adidas ClimaCool", "descripcion": "Short fresco para entrenar", "precio": 95.00, "categoria": "short", "imagen": "img/polo2.png"},
    {"nombre": "Short Cargo Urbano", "descripcion": "Short casual con bolsillos", "precio": 110.00, "categoria": "short", "imagen": "img/polo3.png"},
    {"nombre": "Polo Lacoste Original", "descripcion": "Polo elegante de algodón", "precio": 150.00, "categoria": "polo", "imagen": "img/polo3.png"},
    {"nombre": "Polo Básico Unicolor", "descripcion": "Polo casual de algodón", "precio": 39.90, "categoria": "polo", "imagen": "img/polo3.png"},
    {"nombre": "Camiseta Marvel", "descripcion": "Camiseta con estampado de superhéroes", "precio": 65.00, "categoria": "camiseta", "imagen": "img/polo2.png"},
    {"nombre": "Camiseta Anime", "descripcion": "Diseño inspirado en anime japonés", "precio": 70.00, "categoria": "camiseta", "imagen": "img/polo2.png"},
    {"nombre": "Jean Mom Fit", "descripcion": "Jean corte relajado estilo vintage", "precio": 140.00, "categoria": "jean", "imagen": "img/polo2.png"},
    {"nombre": "Jean Negro Skinny", "descripcion": "Ajustado y versátil", "precio": 130.00, "categoria": "jean", "imagen": "img/polo3.png"},
    {"nombre": "Casaca de Cuero", "descripcion": "Casaca clásica estilo motero", "precio": 350.00, "categoria": "casaca", "imagen": "img/polo3.png"},
    {"nombre": "Vestido Elegante Noche", "descripcion": "Vestido largo para eventos", "precio": 280.00, "categoria": "vestido", "imagen": "img/polo2.png"},
    {"nombre": "Vestido Casual Denim", "descripcion": "Vestido de jean para el día a día", "precio": 160.00, "categoria": "vestido", "imagen": "img/polo2.png"},
    {"nombre": "Zapatillas Converse Chuck", "descripcion": "Clásicas e informales", "precio": 200.00, "categoria": "zapatillas", "imagen": "img/polo3.png"},
    {"nombre": "Zapatillas Vans Old Skool", "descripcion": "Estilo urbano skater", "precio": 190.00, "categoria": "zapatillas", "imagen": "img/polo2.png"},
    {"nombre": "Short Playero", "descripcion": "Perfecto para verano", "precio": 75.00, "categoria": "short", "imagen": "img/polo3.png"},
    {"nombre": "Short Elegante Beige", "descripcion": "Para ocasiones casuales", "precio": 105.00, "categoria": "short", "imagen": "img/polo3.png"},
    {"nombre": "Polo Perú Selección", "descripcion": "Oficial blanquirroja", "precio": 120.00, "categoria": "polo", "imagen": "img/polo1.png"},
    {"nombre": "Camiseta Retro 90s", "descripcion": "Estilo vintage", "precio": 80.00, "categoria": "camiseta", "imagen": "img/polo2.png"},
    {"nombre": "Jean Azul Claro", "descripcion": "Jean casual de verano", "precio": 125.00, "categoria": "jean", "imagen": "img/polo1.png"},
    {"nombre": "Casaca Rompeviento", "descripcion": "Protección ligera contra el viento", "precio": 160.00, "categoria": "casaca", "imagen": "img/polo1.png"},
]

# --- DICCIONARIO DE SINÓNIMOS ---
sinonimos = {
    "pol": "polo",
    "playera": "polo",
    "zapa": "zapatillas",
    "tenis": "zapatillas",
    "camisa": "camiseta",
    "chompa": "casaca"
}

# --- SIDEBAR ---
st.sidebar.title("📌 Opciones de Búsqueda")
st.sidebar.markdown("Filtra y encuentra tu producto más rápido.")

# Buscador por texto
busqueda = st.sidebar.text_input("🔎 Buscar producto")

# Normalizar búsqueda con sinónimos
busqueda_normalizada = busqueda.lower().strip()
if busqueda_normalizada in sinonimos:
    busqueda_normalizada = sinonimos[busqueda_normalizada]

# Filtro por categoría
categorias = sorted(list(set([p["categoria"] for p in productos])))
categoria_filtro = st.sidebar.multiselect("📂 Filtrar por categoría", categorias, default=categorias)

# Filtro por precio
precio_min = st.sidebar.slider("💵 Precio mínimo (S/.)", 0, 1000, 0)
precio_max = st.sidebar.slider("💵 Precio máximo (S/.)", 0, 1000, 1000)

# --- FILTRADO DE PRODUCTOS ---
resultados = []
for p in productos:
    # fuzzy match para nombres y categorías
    if (busqueda_normalizada in p["nombre"].lower() or
        busqueda_normalizada in p["categoria"].lower() or
        difflib.get_close_matches(busqueda_normalizada, [p["nombre"].lower(), p["categoria"].lower()], cutoff=0.6)) \
        and (p["categoria"] in categoria_filtro) \
        and (precio_min <= p["precio"] <= precio_max):
        resultados.append(p)

# --- PANEL PRINCIPAL ---
st.title("🛍️ Buscador de Productos")
st.markdown("Encuentra lo que quieras con **estilo profesional** 💎")

if resultados:
    cols = st.columns(3)  # Mostrar 3 productos por fila
    for i, producto in enumerate(resultados):
        with cols[i % 3]:
            st.image(producto["imagen"], width=200)
            st.subheader(producto["nombre"])
            st.write(producto["descripcion"])
            st.write(f"💵 **Precio:** S/. {producto['precio']}")
            st.caption(f"Categoría: {producto['categoria']}")
            st.markdown("---")
else:
    st.warning("⚠️ No se encontraron productos con esos filtros.")
    st.image("https://media.giphy.com/media/14uQ3cOFteDaU/giphy.gif", width=250)
