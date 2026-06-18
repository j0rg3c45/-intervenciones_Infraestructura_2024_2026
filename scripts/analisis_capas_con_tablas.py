"""
Genera el reporte analisis_capas_infraestructura.txt con tablas formateadas
para facilitar la interpretacion de los datos.
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


def formato_tabla(headers, rows, col_widths=None):
    """Genera una tabla formateada con bordes de texto."""
    if col_widths is None:
        col_widths = []
        for i, h in enumerate(headers):
            max_w = len(str(h))
            for row in rows:
                if i < len(row):
                    max_w = max(max_w, len(str(row[i])))
            col_widths.append(max_w + 2)

    separador = "+" + "+".join("-" * w for w in col_widths) + "+"
    lineas = []
    lineas.append(separador)

    # Header
    header_line = "|"
    for i, h in enumerate(headers):
        header_line += f" {str(h):<{col_widths[i]-2}} |"
    lineas.append(header_line)
    lineas.append(separador)

    # Rows
    for row in rows:
        row_line = "|"
        for i, cell in enumerate(row):
            row_line += f" {str(cell):<{col_widths[i]-2}} |"
        lineas.append(row_line)

    lineas.append(separador)
    return "\n".join(lineas)


def main():
    # Cargar datos
    datos = {}
    for anio, ruta in ARCHIVOS.items():
        if ruta.exists():
            datos[anio] = gpd.read_file(ruta)

    lineas = []

    # =========================================================================
    # ENCABEZADO
    # =========================================================================
    lineas.append("=" * 90)
    lineas.append(" ANALISIS DE CAPAS - INFRAESTRUCTURA 2024-2026")
    lineas.append(" Objetivo: Identificar datos, temporalidad y cubrimiento")
    lineas.append(" para definir requerimientos formales de suministro")
    lineas.append("=" * 90)

    # =========================================================================
    # TABLA 1: INFORMACION GENERAL
    # =========================================================================
    lineas.append("\n\n1. INFORMACION GENERAL DE LAS CAPAS")
    lineas.append("-" * 50)

    headers = ["Metrica", "2024", "2025", "2026"]
    rows = [
        ["Archivo", "Infraestructura_2024.shp", "2025_Consolidado.shp", "2026_Consolidado_proyect.shp"],
        ["Registros", len(datos["2024"]), len(datos["2025"]), len(datos["2026"])],
        ["Columnas", len(datos["2024"].columns)-1, len(datos["2025"].columns)-1, len(datos["2026"].columns)-1],
        ["CRS (EPSG)", datos["2024"].crs.to_epsg(), datos["2025"].crs.to_epsg(), datos["2026"].crs.to_epsg()],
        ["CRS Nombre", "WGS 84", "MAGNA-SIRGAS/Cali", "WGS 84"],
        ["Geometria", "LineString", "LineString", "LineString"],
        ["CRS Valido", "Si", "REVISAR", "Si"],
    ]
    lineas.append(formato_tabla(headers, rows))

    # =========================================================================
    # TABLA 2: CUBRIMIENTO ESPACIAL
    # =========================================================================
    lineas.append("\n\n2. CUBRIMIENTO ESPACIAL (Bounding Box)")
    lineas.append("-" * 50)

    headers = ["Coordenada", "2024", "2025 (proyectado)", "2026"]
    rows_bbox = []
    for anio, gdf in datos.items():
        bounds = gdf.total_bounds
        if anio == "2024":
            rows_bbox = [
                ["Min X (Lon)", f"{bounds[0]:.6f}", "", ""],
                ["Min Y (Lat)", f"{bounds[1]:.6f}", "", ""],
                ["Max X (Lon)", f"{bounds[2]:.6f}", "", ""],
                ["Max Y (Lat)", f"{bounds[3]:.6f}", "", ""],
            ]

    # Completar las demas columnas
    for anio in ["2025", "2026"]:
        bounds = datos[anio].total_bounds
        col_idx = 2 if anio == "2025" else 3
        for i, val in enumerate(bounds):
            if anio == "2025":
                rows_bbox[i][2] = f"{val:.2f}"
            else:
                rows_bbox[i][3] = f"{val:.6f}"

    lineas.append(formato_tabla(headers, rows_bbox))
    lineas.append("\n  Nota: 2025 esta en coordenadas planas (EPSG:6249). Requiere reproyeccion")
    lineas.append("  para comparar con 2024 y 2026 que estan en geograficas (EPSG:4326).")

    # =========================================================================
    # TABLA 3: TEMPORALIDAD
    # =========================================================================
    lineas.append("\n\n3. TEMPORALIDAD")
    lineas.append("-" * 50)

    headers = ["Campo", "2024", "2025", "2026"]
    rows_temp = [["Valor campo 'ano'", "2024", "2025", "2026"]]

    for campo in ["fecha_inic", "fecha_fin"]:
        row = [campo]
        for anio, gdf in datos.items():
            if campo in gdf.columns:
                fechas = pd.to_datetime(gdf[campo], errors="coerce").dropna()
                if len(fechas) > 0:
                    row.append(f"{fechas.min().strftime('%Y-%m-%d')} a {fechas.max().strftime('%Y-%m-%d')}")
                else:
                    row.append("Sin datos")
            else:
                row.append("Campo no existe")
        rows_temp.append(row)

    # Registros con fecha
    row_count = ["Registros con fecha"]
    for anio, gdf in datos.items():
        if "fecha_inic" in gdf.columns:
            count = gdf["fecha_inic"].notna().sum()
            row_count.append(f"{count} de {len(gdf)}")
        else:
            row_count.append("-")
    rows_temp.append(row_count)

    lineas.append(formato_tabla(headers, rows_temp))

    # =========================================================================
    # TABLA 4: TIPOS DE INTERVENCION
    # =========================================================================
    lineas.append("\n\n4. TIPOS DE INTERVENCION (tipo_inter)")
    lineas.append("-" * 50)

    # Obtener todos los tipos unicos
    todos_tipos = set()
    for gdf in datos.values():
        todos_tipos.update(gdf["tipo_inter"].dropna().unique())

    headers = ["Tipo de Intervencion", "2024", "2025", "2026"]
    rows_tipos = []
    for tipo in sorted(todos_tipos):
        row = [tipo]
        for anio, gdf in datos.items():
            count = (gdf["tipo_inter"] == tipo).sum()
            row.append(str(count) if count > 0 else "-")
        rows_tipos.append(row)

    # Totales
    rows_tipos.append(["TOTAL", str(len(datos["2024"])), str(len(datos["2025"])), str(len(datos["2026"]))])
    lineas.append(formato_tabla(headers, rows_tipos))

    # =========================================================================
    # TABLA 5: ESTADO DE LAS OBRAS
    # =========================================================================
    lineas.append("\n\n5. ESTADO DE LAS OBRAS")
    lineas.append("-" * 50)

    todos_estados = set()
    for gdf in datos.values():
        todos_estados.update(gdf["estado"].dropna().unique())

    headers = ["Estado", "2024", "2025", "2026"]
    rows_estado = []
    for estado in sorted(todos_estados):
        row = [estado]
        for anio, gdf in datos.items():
            count = (gdf["estado"] == estado).sum()
            pct = (count / len(gdf)) * 100 if count > 0 else 0
            row.append(f"{count} ({pct:.1f}%)" if count > 0 else "-")
        rows_estado.append(row)
    lineas.append(formato_tabla(headers, rows_estado))

    # =========================================================================
    # TABLA 6: TOP 10 COMUNAS
    # =========================================================================
    lineas.append("\n\n6. TOP 10 COMUNAS CON MAS INTERVENCIONES")
    lineas.append("-" * 50)

    for anio, gdf in datos.items():
        lineas.append(f"\n  Ano {anio}:")
        top = gdf["comuna_cor"].value_counts().head(10)
        headers_c = ["Comuna", "Intervenciones", "% del total"]
        rows_c = []
        for comuna, count in top.items():
            pct = (count / len(gdf)) * 100
            rows_c.append([comuna, count, f"{pct:.1f}%"])
        lineas.append(formato_tabla(headers_c, rows_c))

    # =========================================================================
    # TABLA 7: GRUPO NORMATIVO
    # =========================================================================
    lineas.append("\n\n7. GRUPO NORMATIVO (GRUPO_NORM)")
    lineas.append("-" * 50)

    todos_grupos = set()
    for gdf in datos.values():
        if "GRUPO_NORM" in gdf.columns:
            todos_grupos.update(gdf["GRUPO_NORM"].dropna().unique())

    headers = ["Grupo Normativo", "2024", "2025", "2026"]
    rows_grupo = []
    for grupo in sorted(todos_grupos):
        row = [grupo]
        for anio, gdf in datos.items():
            if "GRUPO_NORM" in gdf.columns:
                count = (gdf["GRUPO_NORM"] == grupo).sum()
                row.append(str(count) if count > 0 else "-")
            else:
                row.append("-")
        rows_grupo.append(row)
    lineas.append(formato_tabla(headers, rows_grupo))

    # =========================================================================
    # TABLA 8: CALIDAD - NULIDAD
    # =========================================================================
    lineas.append("\n\n8. CALIDAD DE DATOS - PORCENTAJE DE NULIDAD POR CAMPO")
    lineas.append("-" * 50)

    campos_eval = [
        "referencia", "referenc_1", "fuente_fin", "nombre_up_",
        "fecha_inic", "fecha_fin", "fecha_inau", "lat", "lon",
        "plataforma", "url_proces", "clase_up", "descripcio", "Observacio"
    ]

    headers = ["Campo", "% Nulo 2024", "% Nulo 2025", "% Nulo 2026", "Diagnostico"]
    rows_nul = []
    for campo in campos_eval:
        row = [campo]
        valores = []
        for anio, gdf in datos.items():
            if campo in gdf.columns:
                pct = (gdf[campo].isnull().sum() / len(gdf)) * 100
            else:
                pct = 100.0
            row.append(f"{pct:.1f}%")
            valores.append(pct)
        # Diagnostico
        if all(v == 100.0 for v in valores):
            row.append("ELIMINAR")
        elif any(v > 70 for v in valores):
            row.append("REVISAR")
        else:
            row.append("OK")
        rows_nul.append(row)
    lineas.append(formato_tabla(headers, rows_nul))

    # =========================================================================
    # TABLA 9: DUPLICADOS
    # =========================================================================
    lineas.append("\n\n9. DUPLICIDAD")
    lineas.append("-" * 50)

    headers = ["Tipo de Duplicado", "2024", "2025", "2026"]
    rows_dup = []

    # Tabulares
    row_tab = ["Duplicados tabulares"]
    for anio, gdf in datos.items():
        cols_sin_geom = [c for c in gdf.columns if c != "geometry"]
        count = gdf.duplicated(subset=cols_sin_geom, keep=False).sum()
        row_tab.append(str(count))
    rows_dup.append(row_tab)

    # Espaciales
    row_esp = ["Duplicados espaciales"]
    for anio, gdf in datos.items():
        gdf_temp = gdf.copy()
        gdf_temp["_wkt"] = gdf_temp.geometry.apply(lambda g: g.wkt if g else None)
        count = gdf_temp.duplicated(subset=["_wkt"], keep=False).sum()
        row_esp.append(str(count))
    rows_dup.append(row_esp)

    # Redundancia total
    row_red = ["Redundancia total (geom+atrib)"]
    for anio, gdf in datos.items():
        gdf_temp = gdf.copy()
        gdf_temp["_wkt"] = gdf_temp.geometry.apply(lambda g: g.wkt if g else None)
        cols_all = [c for c in gdf.columns if c != "geometry"] + ["_wkt"]
        count = gdf_temp.duplicated(subset=cols_all, keep=False).sum()
        row_red.append(str(count))
    rows_dup.append(row_red)

    lineas.append(formato_tabla(headers, rows_dup))

    # =========================================================================
    # TABLA 10: ESQUEMA COMPARATIVO DE COLUMNAS
    # =========================================================================
    lineas.append("\n\n10. ESQUEMA COMPARATIVO DE COLUMNAS")
    lineas.append("-" * 50)

    todas_cols = set()
    for gdf in datos.values():
        todas_cols.update([c for c in gdf.columns if c != "geometry"])

    headers = ["Columna", "2024", "2025", "2026"]
    rows_cols = []
    for col in sorted(todas_cols):
        row = [col]
        for anio, gdf in datos.items():
            if col in gdf.columns:
                row.append("Si")
            else:
                row.append("-")
        rows_cols.append(row)
    lineas.append(formato_tabla(headers, rows_cols))

    # =========================================================================
    # SINTESIS FINAL
    # =========================================================================
    lineas.append("\n\n" + "=" * 90)
    lineas.append(" SINTESIS Y RECOMENDACIONES PARA SOLICITUD FORMAL")
    lineas.append("=" * 90)

    lineas.append("""
PROBLEMAS DETECTADOS:
+----+------------------------------------------------------------------+
| #  | Problema                                                         |
+----+------------------------------------------------------------------+
| 1  | CRS no homogeneo: 2025 en EPSG:6249, resto en EPSG:4326         |
| 2  | Esquema de columnas variable entre anos (35, 34, 37 columnas)    |
| 3  | 5 campos 100% vacios en todos los anos (sin informacion)         |
| 4  | Campos lat/lon vacios en 2025 y 2026 (redundantes con geometria) |
| 5  | Campos referencia/plataforma/url con >70% nulidad                |
| 6  | 2 registros duplicados tabulares en 2025                         |
| 7  | 21 registros sin fecha de inicio en 2026                         |
+----+------------------------------------------------------------------+

RECOMENDACIONES:
+----+------------------------------------------------------------------+
| #  | Requerimiento para solicitud formal                              |
+----+------------------------------------------------------------------+
| 1  | Entregar todas las capas en CRS unico: EPSG:4326 o EPSG:9377    |
| 2  | Definir y mantener esquema fijo de atributos para todos los anos |
| 3  | Entregar diccionario de datos oficial con definicion de campos   |
| 4  | Eliminar campos sin uso o llenarlos obligatoriamente             |
| 5  | Eliminar campos lat/lon si la geometria ya contiene la posicion  |
| 6  | Validar datos antes de entrega: sin duplicados, fechas completas |
| 7  | Definir periodicidad de entrega (mensual, trimestral, semestral) |
| 8  | Entregar en formato .zip con todos los componentes del Shapefile |
+----+------------------------------------------------------------------+
""")

    # Guardar
    output_path = OUTPUT_DIR / "analisis_capas_infraestructura.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print("\n".join(lineas))
    print(f"\n\nReporte exportado a: {output_path}")


if __name__ == "__main__":
    main()
