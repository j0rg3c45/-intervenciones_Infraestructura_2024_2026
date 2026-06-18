"""
Generacion de graficos y tablas para el analisis de capas de infraestructura.
Exporta visualizaciones a output/ para mejorar la interpretacion del EDA.
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data_infraestructura"
OUTPUT_DIR = BASE_DIR / "output"

ARCHIVOS = {
    "2024": DATA_DIR / "2024" / "2024" / "Infraestructura_2024.shp",
    "2025": DATA_DIR / "2025" / "2025_Consolidado.shp",
    "2026": DATA_DIR / "2026" / "2026_Consolidado_proyect.shp",
}

# Colores consistentes por ano
COLORES = {"2024": "#2196F3", "2025": "#FF9800", "2026": "#4CAF50"}


def cargar_datos():
    """Carga los tres shapefiles."""
    datos = {}
    for anio, ruta in ARCHIVOS.items():
        if ruta.exists():
            datos[anio] = gpd.read_file(ruta)
    return datos


def grafico_registros_por_ano(datos):
    """Grafico de barras: total de registros por ano."""
    fig, ax = plt.subplots(figsize=(8, 5))
    anos = list(datos.keys())
    registros = [len(gdf) for gdf in datos.values()]
    colores = [COLORES[a] for a in anos]

    bars = ax.bar(anos, registros, color=colores, edgecolor="black", linewidth=0.5)
    for bar, val in zip(bars, registros):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                str(val), ha="center", va="bottom", fontsize=12, fontweight="bold")

    ax.set_xlabel("Ano", fontsize=11)
    ax.set_ylabel("Numero de registros", fontsize=11)
    ax.set_title("Total de Intervenciones por Ano", fontsize=13, fontweight="bold")
    ax.set_ylim(0, max(registros) * 1.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "grafico_registros_por_ano.png", dpi=150)
    plt.close()
    print("  [OK] grafico_registros_por_ano.png")


def grafico_tipo_intervencion(datos):
    """Grafico de barras horizontales: tipos de intervencion por ano."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 7))

    for idx, (anio, gdf) in enumerate(datos.items()):
        ax = axes[idx]
        conteo = gdf["tipo_inter"].value_counts().sort_values()
        conteo.plot(kind="barh", ax=ax, color=COLORES[anio], edgecolor="black", linewidth=0.3)
        ax.set_title(f"Tipo de Intervencion - {anio}", fontsize=11, fontweight="bold")
        ax.set_xlabel("Cantidad")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        for i, v in enumerate(conteo.values):
            ax.text(v + 1, i, str(v), va="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "grafico_tipo_intervencion.png", dpi=150)
    plt.close()
    print("  [OK] grafico_tipo_intervencion.png")


def grafico_estado_obras(datos):
    """Grafico de torta: estado de las obras por ano."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for idx, (anio, gdf) in enumerate(datos.items()):
        ax = axes[idx]
        conteo = gdf["estado"].value_counts()
        colores_estado = ["#4CAF50", "#FFC107", "#F44336"][:len(conteo)]
        wedges, texts, autotexts = ax.pie(
            conteo.values, labels=conteo.index, autopct="%1.1f%%",
            colors=colores_estado, startangle=90,
            textprops={"fontsize": 9}
        )
        ax.set_title(f"Estado - {anio}", fontsize=11, fontweight="bold")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "grafico_estado_obras.png", dpi=150)
    plt.close()
    print("  [OK] grafico_estado_obras.png")


def grafico_nulidad(datos):
    """Heatmap de nulidad: porcentaje de nulos por campo y ano."""
    # Campos comunes relevantes
    campos_comunes = [
        "referencia", "referenc_1", "fuente_fin", "nombre_up_",
        "fecha_inic", "fecha_fin", "fecha_inau", "lat", "lon",
        "plataforma", "url_proces", "clase_up", "descripcio", "Observacio"
    ]

    matriz = {}
    for anio, gdf in datos.items():
        nulidad = {}
        for campo in campos_comunes:
            if campo in gdf.columns:
                pct = (gdf[campo].isnull().sum() / len(gdf)) * 100
            else:
                pct = 100.0  # campo no existe = 100% nulo
            nulidad[campo] = round(pct, 1)
        matriz[anio] = nulidad

    df_nulidad = pd.DataFrame(matriz)

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(df_nulidad.values, cmap="RdYlGn_r", aspect="auto", vmin=0, vmax=100)

    ax.set_xticks(range(len(df_nulidad.columns)))
    ax.set_xticklabels(df_nulidad.columns, fontsize=11)
    ax.set_yticks(range(len(df_nulidad.index)))
    ax.set_yticklabels(df_nulidad.index, fontsize=10)

    # Anotar valores
    for i in range(len(df_nulidad.index)):
        for j in range(len(df_nulidad.columns)):
            val = df_nulidad.iloc[i, j]
            color = "white" if val > 60 else "black"
            ax.text(j, i, f"{val:.0f}%", ha="center", va="center",
                    fontsize=9, color=color, fontweight="bold")

    ax.set_title("Porcentaje de Nulidad por Campo y Ano", fontsize=13, fontweight="bold")
    plt.colorbar(im, ax=ax, label="% Nulos", shrink=0.8)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "grafico_nulidad_campos.png", dpi=150)
    plt.close()
    print("  [OK] grafico_nulidad_campos.png")


def grafico_comunas(datos):
    """Grafico de barras: top 10 comunas con mas intervenciones por ano."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    for idx, (anio, gdf) in enumerate(datos.items()):
        ax = axes[idx]
        conteo = gdf["comuna_cor"].value_counts().head(10).sort_values()
        conteo.plot(kind="barh", ax=ax, color=COLORES[anio], edgecolor="black", linewidth=0.3)
        ax.set_title(f"Top 10 Comunas - {anio}", fontsize=11, fontweight="bold")
        ax.set_xlabel("Intervenciones")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        for i, v in enumerate(conteo.values):
            ax.text(v + 0.3, i, str(v), va="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "grafico_top_comunas.png", dpi=150)
    plt.close()
    print("  [OK] grafico_top_comunas.png")


def grafico_grupo_normativo(datos):
    """Grafico de barras apiladas: distribucion por grupo normativo."""
    frames = []
    for anio, gdf in datos.items():
        if "GRUPO_NORM" in gdf.columns:
            conteo = gdf["GRUPO_NORM"].value_counts().reset_index()
            conteo.columns = ["grupo", "cantidad"]
            conteo["anio"] = anio
            frames.append(conteo)

    df = pd.concat(frames, ignore_index=True)
    pivot = df.pivot_table(index="grupo", columns="anio", values="cantidad", fill_value=0)

    fig, ax = plt.subplots(figsize=(10, 5))
    pivot.plot(kind="bar", ax=ax, color=[COLORES[c] for c in pivot.columns],
               edgecolor="black", linewidth=0.3)
    ax.set_title("Intervenciones por Grupo Normativo y Ano", fontsize=13, fontweight="bold")
    ax.set_xlabel("Grupo Normativo")
    ax.set_ylabel("Cantidad")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.xticks(rotation=25, ha="right")
    plt.legend(title="Ano")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "grafico_grupo_normativo.png", dpi=150)
    plt.close()
    print("  [OK] grafico_grupo_normativo.png")


def tabla_resumen_consolidada(datos):
    """Genera tabla resumen en formato texto y la guarda."""
    lineas = []
    lineas.append("=" * 90)
    lineas.append(" TABLA RESUMEN CONSOLIDADA - CAPAS DE INFRAESTRUCTURA")
    lineas.append("=" * 90)
    lineas.append("")
    lineas.append(f"{'Metrica':<40} {'2024':>12} {'2025':>12} {'2026':>12}")
    lineas.append(f"{'-'*40} {'-'*12} {'-'*12} {'-'*12}")

    metricas = {
        "Total registros": {a: len(g) for a, g in datos.items()},
        "Total columnas": {a: len(g.columns)-1 for a, g in datos.items()},
        "CRS (EPSG)": {a: str(g.crs.to_epsg()) for a, g in datos.items()},
        "Tipos de intervencion": {a: g["tipo_inter"].nunique() for a, g in datos.items()},
        "Comunas cubiertas": {a: g["comuna_cor"].nunique() for a, g in datos.items()},
        "Barrios/veredas unicos": {a: g["barrio_ver"].nunique() for a, g in datos.items()},
        "Nulos totales": {a: g.drop(columns="geometry").isnull().sum().sum() for a, g in datos.items()},
        "Campos 100% vacios": {a: sum(1 for c in g.columns if c != "geometry" and g[c].isnull().all()) for a, g in datos.items()},
    }

    for nombre, valores in metricas.items():
        lineas.append(f"{nombre:<40} {str(valores.get('2024','-')):>12} {str(valores.get('2025','-')):>12} {str(valores.get('2026','-')):>12}")

    lineas.append("")
    lineas.append("=" * 90)

    texto = "\n".join(lineas)
    with open(OUTPUT_DIR / "tabla_resumen_consolidada.txt", "w", encoding="utf-8") as f:
        f.write(texto)
    print(texto)
    print("\n  [OK] tabla_resumen_consolidada.txt")


def main():
    print("=" * 70)
    print(" GENERACION DE GRAFICOS - EDA INFRAESTRUCTURA 2024-2026")
    print("=" * 70)

    datos = cargar_datos()

    print("\nGenerando graficos...")
    grafico_registros_por_ano(datos)
    grafico_tipo_intervencion(datos)
    grafico_estado_obras(datos)
    grafico_nulidad(datos)
    grafico_comunas(datos)
    grafico_grupo_normativo(datos)

    print("\nGenerando tabla resumen...")
    tabla_resumen_consolidada(datos)

    print(f"\n[FIN] Todos los graficos exportados a: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
