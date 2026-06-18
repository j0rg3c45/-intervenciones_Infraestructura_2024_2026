"""
Script de Auditoria, Diagnostico de Calidad y EDA Estructurado
para los archivos espaciales en data_infraestructura/ (2024, 2025, 2026).

Puntos de control:
1. Informacion general (nombre, CRS, tipo de geometria)
2. Inventario de atributos (columnas y tipos de datos)
3. Calidad alfanumerica (nulos, duplicados tabulares)
4. Duplicidad espacial y topologica
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path
import sys

# Rutas base
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data_infraestructura"
OUTPUT_DIR = BASE_DIR / "output"

# Definicion de archivos a analizar por ano
ARCHIVOS = {
    "2024": DATA_DIR / "2024" / "2024" / "Infraestructura_2024.shp",
    "2025": DATA_DIR / "2025" / "2025_Consolidado.shp",
    "2026": DATA_DIR / "2026" / "2026_Consolidado_proyect.shp",
}


def analizar_shapefile(anio, ruta):
    """Ejecuta el EDA completo para un shapefile dado."""
    print(f"\n{'='*70}")
    print(f" ANO: {anio}")
    print(f" Archivo: {ruta.name}")
    print(f"{'='*70}")

    if not ruta.exists():
        print(f"  [ERROR] El archivo no existe: {ruta}")
        return None

    # Lectura del shapefile
    gdf = gpd.read_file(ruta)

    # --- 1. Informacion General ---
    print(f"\n--- 1. INFORMACION GENERAL ---")
    print(f"  Nombre: {ruta.name}")
    print(f"  Registros (filas): {len(gdf)}")
    print(f"  CRS: {gdf.crs}")
    print(f"  EPSG: {gdf.crs.to_epsg() if gdf.crs else 'No definido'}")
    print(f"  Tipo de geometria: {gdf.geom_type.unique().tolist()}")

    # Validar CRS para Colombia (EPSG:4326 WGS84 o EPSG:3116 MAGNA-SIRGAS)
    epsg = gdf.crs.to_epsg() if gdf.crs else None
    crs_validos = [4326, 3116, 4686, 9377]
    if epsg in crs_validos:
        print(f"  CRS valido para Colombia: Si (EPSG:{epsg})")
    else:
        print(f"  CRS valido para Colombia: REVISAR (EPSG:{epsg})")

    # --- 2. Inventario de Atributos ---
    print(f"\n--- 2. INVENTARIO DE ATRIBUTOS ---")
    print(f"  Total columnas: {len(gdf.columns)}")
    print(f"  {'Columna':<30} {'Tipo de Dato':<20}")
    print(f"  {'-'*30} {'-'*20}")
    for col in gdf.columns:
        if col != "geometry":
            print(f"  {col:<30} {str(gdf[col].dtype):<20}")

    # --- 3. Calidad Alfanumerica ---
    print(f"\n--- 3. CALIDAD ALFANUMERICA ---")

    # Valores nulos
    nulos = gdf.drop(columns="geometry").isnull().sum()
    nulos_total = nulos.sum()
    print(f"  Total valores nulos en dataset: {nulos_total}")
    if nulos_total > 0:
        print(f"  Detalle de nulos por columna:")
        for col, count in nulos[nulos > 0].items():
            pct = (count / len(gdf)) * 100
            print(f"    - {col}: {count} ({pct:.1f}%)")

    # Valores vacios (strings vacios)
    cols_obj = gdf.select_dtypes(include=["object"]).columns.tolist()
    if "geometry" in cols_obj:
        cols_obj.remove("geometry")
    vacios = {col: (gdf[col] == "").sum() for col in cols_obj}
    vacios_total = sum(vacios.values())
    print(f"  Total valores vacios (string ''): {vacios_total}")
    if vacios_total > 0:
        for col, count in vacios.items():
            if count > 0:
                print(f"    - {col}: {count}")

    # Duplicados tabulares (sin geometria)
    cols_sin_geom = [c for c in gdf.columns if c != "geometry"]
    duplicados_tab = gdf.duplicated(subset=cols_sin_geom, keep=False).sum()
    print(f"  Registros duplicados (atributos): {duplicados_tab}")

    # --- 4. Duplicidad Espacial y Topologica ---
    print(f"\n--- 4. DUPLICIDAD ESPACIAL Y TOPOLOGICA ---")

    # Duplicados espaciales (misma geometria exacta)
    gdf["geom_wkt"] = gdf.geometry.apply(lambda g: g.wkt if g else None)
    duplicados_espaciales = gdf.duplicated(subset=["geom_wkt"], keep=False).sum()
    print(f"  Registros con geometria duplicada: {duplicados_espaciales}")

    # Duplicados espaciales + atributos (redundancia total)
    cols_completas = cols_sin_geom + ["geom_wkt"]
    duplicados_totales = gdf.duplicated(subset=cols_completas, keep=False).sum()
    print(f"  Registros con geometria + atributos duplicados (redundancia total): {duplicados_totales}")

    # Limpiar columna auxiliar
    gdf.drop(columns="geom_wkt", inplace=True)

    return gdf


def generar_resumen_csv(resultados):
    """Genera un CSV resumen con metricas clave por ano."""
    filas = []
    for anio, gdf in resultados.items():
        if gdf is None:
            continue
        cols_sin_geom = [c for c in gdf.columns if c != "geometry"]
        gdf_temp = gdf.copy()
        gdf_temp["geom_wkt"] = gdf_temp.geometry.apply(lambda g: g.wkt if g else None)

        fila = {
            "anio": anio,
            "archivo": ARCHIVOS[anio].name,
            "registros": len(gdf),
            "columnas": len(gdf.columns) - 1,
            "crs_epsg": gdf.crs.to_epsg() if gdf.crs else None,
            "tipo_geometria": gdf.geom_type.unique().tolist(),
            "nulos_totales": gdf.drop(columns="geometry").isnull().sum().sum(),
            "duplicados_tabulares": gdf.duplicated(subset=cols_sin_geom, keep=False).sum(),
            "duplicados_espaciales": gdf_temp.duplicated(subset=["geom_wkt"], keep=False).sum(),
            "redundancia_total": gdf_temp.duplicated(subset=cols_sin_geom + ["geom_wkt"], keep=False).sum(),
        }
        filas.append(fila)

    df_resumen = pd.DataFrame(filas)
    output_path = OUTPUT_DIR / "resumen_eda_infraestructura.csv"
    df_resumen.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n{'='*70}")
    print(f" RESUMEN EXPORTADO: {output_path}")
    print(f"{'='*70}")
    print(df_resumen.to_string(index=False))


def main():
    """Ejecuta el EDA para todos los anos."""
    print("=" * 70)
    print(" EDA - AUDITORIA DE CALIDAD: DATA INFRAESTRUCTURA 2024-2026")
    print("=" * 70)

    resultados = {}
    for anio, ruta in ARCHIVOS.items():
        resultados[anio] = analizar_shapefile(anio, ruta)

    # Generar resumen consolidado
    generar_resumen_csv(resultados)

    print("\n[FIN] Analisis completado.")


if __name__ == "__main__":
    main()
