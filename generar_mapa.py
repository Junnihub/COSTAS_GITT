"""
COSTAS_GITT – Generador de Mapa Interactivo de Peligros Costeros
================================================================
Extensión académica de CoastSat aplicada a Puerto Colombia, Atlántico, Colombia.

Genera un mapa HTML interactivo con folium que muestra zonas de peligro costero
derivadas del análisis satelital de la línea costera.

Basado en: https://github.com/kvos/CoastSat
Área de estudio: Puerto Colombia (10.9856°N, 74.9731°O), Mar Caribe, Colombia.

Uso:
    python generar_mapa.py

El mapa se guarda en: output/mapa_peligros_costeros.html
"""

import json
import os

import folium
from folium.plugins import Fullscreen, MeasureControl, MousePosition


# ── Configuración ─────────────────────────────────────────────────────────────
CENTRO_PUERTO_COLOMBIA = [10.9856, -74.9731]
ZOOM_INICIAL = 15
ARCHIVO_SALIDA = os.path.join("output", "mapa_peligros_costeros.html")
ARCHIVO_GEOJSON = os.path.join("data", "peligros_costeros.geojson")


# ── Datos de peligros costeros ────────────────────────────────────────────────
PELIGROS = {
    "erosion_alta": {
        "nombre": "Erosión Activa (Alta)",
        "color": "#d73027",
        "geojson": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "tipo": "Erosión Activa",
                        "nivel": "Alto",
                        "descripcion": (
                            "Zona de retroceso costero documentado por imágenes "
                            "satelitales. Pérdida estimada de 1–3 m/año."
                        ),
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-74.9870, 10.9880],
                            [-74.9820, 10.9880],
                            [-74.9820, 10.9865],
                            [-74.9870, 10.9865],
                            [-74.9870, 10.9880],
                        ]],
                    },
                }
            ],
        },
    },
    "erosion_media": {
        "nombre": "Erosión Moderada",
        "color": "#fc8d59",
        "geojson": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "tipo": "Erosión Moderada",
                        "nivel": "Medio",
                        "descripcion": (
                            "Zona con tendencia de retroceso costero moderado. "
                            "Requiere monitoreo continuo."
                        ),
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-74.9820, 10.9880],
                            [-74.9770, 10.9880],
                            [-74.9770, 10.9865],
                            [-74.9820, 10.9865],
                            [-74.9820, 10.9880],
                        ]],
                    },
                }
            ],
        },
    },
    "inundacion_alta": {
        "nombre": "Inundación por Marejadas (Alta)",
        "color": "#fee090",
        "geojson": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "tipo": "Riesgo de Inundación por Marejadas",
                        "nivel": "Alto",
                        "descripcion": (
                            "Área susceptible a inundaciones costeras durante "
                            "eventos de marejada ciclónica y oleaje extremo."
                        ),
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-74.9900, 10.9895],
                            [-74.9750, 10.9895],
                            [-74.9750, 10.9878],
                            [-74.9900, 10.9878],
                            [-74.9900, 10.9895],
                        ]],
                    },
                }
            ],
        },
    },
    "inundacion_media": {
        "nombre": "Inundación por Marejadas (Media)",
        "color": "#ffffbf",
        "geojson": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "tipo": "Riesgo de Inundación por Marejadas",
                        "nivel": "Medio",
                        "descripcion": (
                            "Zona con riesgo moderado de inundación en "
                            "eventos extremos de marejada."
                        ),
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-74.9900, 10.9915],
                            [-74.9750, 10.9915],
                            [-74.9750, 10.9895],
                            [-74.9900, 10.9895],
                            [-74.9900, 10.9915],
                        ]],
                    },
                }
            ],
        },
    },
    "contaminacion": {
        "nombre": "Contaminación Costera",
        "color": "#4d9221",
        "geojson": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "tipo": "Contaminación Costera",
                        "nivel": "Medio",
                        "descripcion": (
                            "Zona afectada por descarga de residuos sólidos "
                            "y aguas residuales."
                        ),
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-74.9760, 10.9890],
                            [-74.9720, 10.9890],
                            [-74.9720, 10.9870],
                            [-74.9760, 10.9870],
                            [-74.9760, 10.9890],
                        ]],
                    },
                }
            ],
        },
    },
    "acrecion": {
        "nombre": "Acreción Costera",
        "color": "#1a9641",
        "geojson": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "tipo": "Acreción Costera",
                        "nivel": "Informativo",
                        "descripcion": (
                            "Zona con tendencia de acumulación de sedimentos "
                            "(avance de la línea costera)."
                        ),
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-74.9700, 10.9880],
                            [-74.9660, 10.9880],
                            [-74.9660, 10.9865],
                            [-74.9700, 10.9865],
                            [-74.9700, 10.9880],
                        ]],
                    },
                }
            ],
        },
    },
}

LINEAS = {
    "linea_costera": {
        "nombre": "Línea Costera (CoastSat)",
        "color": "#2171b5",
        "coordinates": [
            [10.9875, -74.9950],
            [10.9873, -74.9900],
            [10.9871, -74.9850],
            [10.9870, -74.9800],
            [10.9869, -74.9750],
            [10.9868, -74.9700],
        ],
        "descripcion": (
            "Posición de la línea costera detectada por análisis satelital "
            "con metodología CoastSat (Landsat/Sentinel-2, 1984–presente)."
        ),
    },
    "muelle": {
        "nombre": "Muelle Histórico",
        "color": "#7b2d8b",
        "coordinates": [
            [10.9876, -74.9843],
            [10.9845, -74.9843],
            [10.9815, -74.9843],
            [10.9785, -74.9843],
        ],
        "descripcion": (
            "Muelle Histórico de Puerto Colombia (1888–1893). "
            "Patrimonio cultural en riesgo por erosión y deterioro estructural."
        ),
    },
}

PUNTOS = [
    {
        "nombre": "Muelle de Puerto Colombia",
        "coords": [10.9876, -74.9843],
        "color": "#7b2d8b",
        "icono": "anchor",
        "descripcion": (
            "Muelle histórico (1888–1893). Fue el muelle de concreto más "
            "largo del mundo. En riesgo por erosión costera."
        ),
    },
    {
        "nombre": "Playa Puerto Colombia",
        "coords": [10.9872, -74.9830],
        "color": "#2171b5",
        "icono": "tint",
        "descripcion": (
            "Playa principal con procesos activos de erosión costera que "
            "amenazan la franja de arena y la infraestructura cercana."
        ),
    },
    {
        "nombre": "Desembocadura Arroyo Salado",
        "coords": [10.9868, -74.9780],
        "color": "#fc8d59",
        "icono": "exclamation-triangle",
        "descripcion": (
            "Zona de dinámica sedimentaria compleja. Riesgo de contaminación "
            "por escorrentía urbana durante lluvias intensas."
        ),
    },
]


# ── Funciones ─────────────────────────────────────────────────────────────────
def crear_mapa():
    """Genera el mapa interactivo de peligros costeros de Puerto Colombia."""
    m = folium.Map(
        location=CENTRO_PUERTO_COLOMBIA,
        zoom_start=ZOOM_INICIAL,
        tiles=None,
    )

    # Capas base
    folium.TileLayer(
        tiles=(
            "https://server.arcgisonline.com/ArcGIS/rest/services/"
            "World_Imagery/MapServer/tile/{z}/{y}/{x}"
        ),
        attr="Esri World Imagery",
        name="Satélite (Esri)",
        overlay=False,
        control=True,
    ).add_to(m)

    folium.TileLayer(
        tiles="OpenStreetMap",
        name="OpenStreetMap",
        overlay=False,
        control=True,
    ).add_to(m)

    folium.TileLayer(
        tiles="CartoDB dark_matter",
        name="CartoDB Oscuro",
        overlay=False,
        control=True,
    ).add_to(m)

    # Capas de peligros (polígonos)
    for key, datos in PELIGROS.items():
        fg = folium.FeatureGroup(name=datos["nombre"], show=True)
        color = datos["color"]
        for feature in datos["geojson"]["features"]:
            props = feature["properties"]
            popup_html = (
                f"<b>{props['tipo']}</b><br>"
                f"<span style='color:{color};font-weight:600'>"
                f"Nivel: {props['nivel']}</span><br><br>"
                f"{props['descripcion']}"
            )
            folium.GeoJson(
                feature,
                style_function=lambda _, c=color: {
                    "fillColor": c,
                    "color": c,
                    "weight": 1.5,
                    "fillOpacity": 0.4,
                    "opacity": 0.85,
                },
                highlight_function=lambda _: {
                    "fillOpacity": 0.65,
                    "weight": 2.5,
                },
                tooltip=folium.Tooltip(props["tipo"]),
                popup=folium.Popup(popup_html, max_width=280),
            ).add_to(fg)
        fg.add_to(m)

    # Líneas (línea costera y muelle)
    for key, linea in LINEAS.items():
        fg = folium.FeatureGroup(name=linea["nombre"], show=True)
        folium.PolyLine(
            locations=linea["coordinates"],
            color=linea["color"],
            weight=3,
            opacity=0.9,
            dash_array="8 4",
            tooltip=folium.Tooltip(linea["nombre"]),
            popup=folium.Popup(
                f"<b>{linea['nombre']}</b><br>{linea['descripcion']}",
                max_width=280,
            ),
        ).add_to(fg)
        fg.add_to(m)

    # Marcadores de puntos de interés
    fg_puntos = folium.FeatureGroup(name="Puntos de Interés", show=True)
    for punto in PUNTOS:
        folium.Marker(
            location=punto["coords"],
            popup=folium.Popup(
                f"<b>{punto['nombre']}</b><br>{punto['descripcion']}",
                max_width=280,
            ),
            tooltip=punto["nombre"],
            icon=folium.Icon(
                color="purple" if punto["color"] == "#7b2d8b" else "blue",
                icon=punto["icono"],
                prefix="fa",
            ),
        ).add_to(fg_puntos)
    fg_puntos.add_to(m)

    # Controles adicionales
    folium.LayerControl(position="topright", collapsed=False).add_to(m)
    Fullscreen(position="topleft").add_to(m)
    MeasureControl(
        position="topleft",
        primary_length_unit="meters",
        secondary_length_unit="kilometers",
        primary_area_unit="sqmeters",
    ).add_to(m)
    MousePosition(
        position="bottomleft",
        separator=" | Lon: ",
        prefix="Lat: ",
        num_digits=5,
    ).add_to(m)

    # Título HTML personalizado
    titulo_html = """
    <div style="
        position: fixed;
        top: 10px; left: 50px; z-index: 1000;
        background: rgba(13, 33, 55, 0.92);
        border: 1px solid #2a5298;
        border-radius: 8px;
        padding: 10px 16px;
        color: #e0e6f0;
        font-family: 'Segoe UI', sans-serif;
        max-width: 360px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    ">
        <h4 style="margin:0 0 4px 0; color:#4fc3f7; font-size:1rem;">
            🌊 COSTAS_GITT
        </h4>
        <p style="margin:0; font-size:0.78rem; color:#90b4ce;">
            Peligros Costeros · Puerto Colombia, Atlántico, Colombia<br>
            <em style="font-size:0.7rem; color:#4a6b8a;">
                Extensión académica de CoastSat
            </em>
        </p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(titulo_html))

    return m


def main():
    """Punto de entrada principal."""
    os.makedirs("output", exist_ok=True)

    print("🌊 COSTAS_GITT – Generando mapa de peligros costeros...")
    print(f"   Área de estudio: Puerto Colombia ({CENTRO_PUERTO_COLOMBIA})")

    mapa = crear_mapa()
    mapa.save(ARCHIVO_SALIDA)

    print(f"✅ Mapa guardado en: {ARCHIVO_SALIDA}")
    print("   Abre el archivo en tu navegador para visualizarlo.")


if __name__ == "__main__":
    main()
