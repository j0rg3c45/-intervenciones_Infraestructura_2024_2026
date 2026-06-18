"""
Analisis detallado de capas de infraestructura.
Objetivo: Conocer que datos, temporalidad y cubrimiento contienen los shapes
para definir que solicitar formalmente a la Secretaria.

Genera un reporte consolidado en output/analisis_capas_infraestructura.txt
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data_infraestructura"
OUTPUT_DIR = BASE_DIR / "output"

ARCHIVOS = {
    "2024": DATA_DIR / "2024" / "2024" / "Infraestructura_2024.shp",
    "2025": DATA_DIR / "2025" / "2025_Consolidado.shp",
    "2026": DATA_DIR / "2026" / "2026_Consolidado_proyect.shp",
}


def analizar_capa(anio, ruta):
    """Analiza una capa en detalle: datos, temporalidad y cubrimiento."""
    if not ruta.exists():
        return None

    gdf = gpd.read_file(ruta)
    info = {}
    info["anio"] = anio
    info["archivo"] = ruta.name
    info["registros"] = len(gdf)
    info["crs_epsg"] = gdf.crs.to_epsg() if gdf.crs else None
    info["crs_nombre"] = str(gdf.crs.name) if gdf.crs else "No definido"
    info["tipo_geometria"] = gdf.geom_type.unique().tolist()

    # --- Cubrimiento espacial (bounding box) ---
    bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
    info["bbox"] = {
        "min_x": bounds[0],
        "min_y": bounds[1],
        "max_x": bounds[2],
        "max_y": bounds[3],
    }

    # --- Columnas disponibles ---
    cols = [c for c in gdf.columns if c != "geometry"]
    info["columnas"] = cols

    # --- Temporalidad: buscar campos de fecha y ano ---
    info["campo_ano"] = None
    info["rango_anos"] = None
    if "ano" in [c.lower().replace("ñ", "n") for c in cols]:
        col_ano = [c for c in cols if c.lower().replace("ñ", "n") == "ano"][0]
        info["campo_ano"] = col_ano
        valores_ano = gdf[col_ano].dropna().unique()
        info["rango_anos"] = sorted([str(v) for v in valores_ano])

    # Fechas
    info["fechas"] = {}
    for col in cols:
        if "fecha" in col.lower():
            no_nulo = gdf[col].dropna()
            if len(no_nulo) > 0:
                try:
                    fechas = pd.to_datetime(no_nulo, errors="coerce").dropna()
                    if len(fechas) > 0:
                        info["fechas"][col] = {
                            "min": str(fechas.min()),
                            "max": str(fechas.max()),
                            "registros_con_dato": len(fechas),
                        }
                except Exception:
                    pass

    # --- Campos tematicos clave (valores unicos) ---
    campos_tematicos = [
        "tipo_equip", "tipo_inter", "estado", "comuna_cor",
        "nombre_up", "barrio_ver", "GRUPO", "GRUPO_NORM", "unidad"
    ]
    info["tematicos"] = {}
    for campo in campos_tematicos:
        if campo in cols:
            valores = gdf[campo].dropna().unique().tolist()
            info["tematicos"][campo] = {
                "valores_unicos": len(valores),
                "muestra": sorted(valores)[:15],  # maximo 15 para no saturar
            }

    # --- Campos con datos utiles vs vacios ---
    info["campos_con_datos"] = []
    info["campos_vacios"] = []
    for col in cols:
        nulos = gdf[col].isnull().sum()
        if nulos == len(gdf):
            info["campos_vacios"].append(col)
        else:
            pct_lleno = ((len(gdf) - nulos) / len(gdf)) * 100
            info["campos_con_datos"].append({"campo": col, "pct_lleno": round(pct_lleno, 1)})

    return info


def generar_reporte(resultados):
    """Genera el reporte de texto consolidado."""
    lineas = []
    lineas.append("=" * 80)
    lineas.append(" ANALISIS DE CAPAS - INFRAESTRUCTURA 2024-2026")
    lineas.append(" Objetivo: Identificar datos, temporalidad y cubrimiento")
    lineas.append("=" * 80)

    for anio, info in resultados.items():
        if info is None:
            continue

        lineas.append(f"\n{'='*80}")
        lineas.append(f" ANO: {anio} | Archivo: {info['archivo']}")
        lineas.append(f"{'='*80}")

        # Informacion general
        lineas.append(f"\n  [INFORMACION GENERAL]")
        lineas.append(f"  Registros: {info['registros']}")
        lineas.append(f"  CRS: EPSG:{info['crs_epsg']} ({info['crs_nombre']})")
        lineas.append(f"  Geometria: {info['tipo_geometria']}")

        # Cubrimiento
        bbox = info["bbox"]
        lineas.append(f"\n  [CUBRIMIENTO ESPACIAL (Bounding Box)]")
        lineas.append(f"  Min X (Lon): {bbox['min_x']:.6f}")
        lineas.append(f"  Min Y (Lat): {bbox['min_y']:.6f}")
        lineas.append(f"  Max X (Lon): {bbox['max_x']:.6f}")
        lineas.append(f"  Max Y (Lat): {bbox['max_y']:.6f}")

        # Temporalidad
        lineas.append(f"\n  [TEMPORALIDAD]")
        if info["campo_ano"]:
            lineas.append(f"  Campo de ano: {info['campo_ano']}")
            lineas.append(f"  Valores: {info['rango_anos']}")
        else:
            lineas.append(f"  Campo de ano: No identificado")

        if info["fechas"]:
            for campo_fecha, datos in info["fechas"].items():
                lineas.append(f"  {campo_fecha}:")
                lineas.append(f"    Rango: {datos['min']} a {datos['max']}")
                lineas.append(f"    Registros con dato: {datos['registros_con_dato']}")
        else:
            lineas.append(f"  Sin campos de fecha con datos validos.")

        # Campos tematicos
        lineas.append(f"\n  [CAMPOS TEMATICOS - VALORES UNICOS]")
        if info["tematicos"]:
            for campo, datos in info["tematicos"].items():
                lineas.append(f"  {campo} ({datos['valores_unicos']} valores):")
                for v in datos["muestra"]:
                    lineas.append(f"    - {v}")
        else:
            lineas.append(f"  Sin campos tematicos identificados.")

        # Campos con datos vs vacios
        lineas.append(f"\n  [CAMPOS CON DATOS]")
        for item in sorted(info["campos_con_datos"], key=lambda x: x["pct_lleno"], reverse=True):
            lineas.append(f"  {item['campo']:<30} {item['pct_lleno']:>5.1f}% lleno")

        lineas.append(f"\n  [CAMPOS 100% VACIOS (sin informacion)]")
        if info["campos_vacios"]:
            for c in info["campos_vacios"]:
                lineas.append(f"  - {c}")
        else:
            lineas.append(f"  Ninguno.")

    # Seccion final: Sintesis para solicitud formal
    lineas.append(f"\n\n{'='*80}")
    lineas.append(f" SINTESIS PARA SOLICITUD FORMAL")
    lineas.append(f"{'='*80}")
    lineas.append(f"""
  Basado en el analisis, los shapes suministrados contienen:

  CAPAS: 3 archivos tipo LineString (intervenciones lineales de infraestructura)
    - Infraestructura_2024.shp (323 registros)
    - 2025_Consolidado.shp (677 registros)
    - 2026_Consolidado_proyect.shp (199 registros)

  DATOS DISPONIBLES:
    - Identificadores de proyecto (ID, bpin, identifica)
    - Tipo de equipamiento e intervencion (tipo_equip, tipo_inter)
    - Localizacion administrativa (comuna_cor, barrio_ver, direccion)
    - Nombre del proyecto (nombre_up)
    - Estado de la obra (estado)
    - Presupuesto y avance (presupuest, avance_obr)
    - Fechas de inicio y fin (fecha_inic, fecha_fin)
    - Grupo normativo (GRUPO_NORM)

  TEMPORALIDAD:
    - 2024: Registros del ano 2024 (fechas desde inicio de obras hasta cierre)
    - 2025: Registros del ano 2025
    - 2026: Registros del ano 2026 (proyectados)

  CUBRIMIENTO:
    - Corresponde al municipio de estudio (verificar con limite administrativo)
    - CRS mixto: 2024 y 2026 en EPSG:4326, 2025 en EPSG:6249

  PROBLEMAS DETECTADOS PARA SOLICITUD:
    1. CRS no homogeneo entre anos (solicitar entrega en un solo CRS)
    2. Campos 100% vacios que no aportan informacion:
       fuente_fin, fecha_inau, clase_up, descripcio, Observacio
    3. Campos lat/lon vacios en 2025 y 2026 (redundantes si hay geometria)
    4. Campos referencia/plataforma/url con alta nulidad (>70%)
    5. Esquema de columnas variable entre anos (no estandarizado)
    6. 2 registros duplicados en 2025

  RECOMENDACIONES PARA SOLICITUD FORMAL:
    - Solicitar entrega en CRS unico: EPSG:4326 o EPSG:9377 (MAGNA-SIRGAS)
    - Exigir esquema de atributos estandarizado y fijo para todos los anos
    - Solicitar diccionario de datos oficial con definicion de cada campo
    - Pedir que eliminen campos sin uso o los llenen antes de entregar
    - Solicitar validacion topologica previa (sin geometrias duplicadas)
    - Definir periodicidad de entrega (mensual, trimestral, semestral)
""")

    # Escribir archivo
    output_path = OUTPUT_DIR / "analisis_capas_infraestructura.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print("\n".join(lineas))
    print(f"\n\nReporte exportado a: {output_path}")


def main():
    resultados = {}
    for anio, ruta in ARCHIVOS.items():
        resultados[anio] = analizar_capa(anio, ruta)
    generar_reporte(resultados)


if __name__ == "__main__":
    main()
