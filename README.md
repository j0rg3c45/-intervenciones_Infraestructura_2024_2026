# Intervenciones Infraestructura 2024-2026

Proyecto de analisis territorial y gobernanza de datos para las intervenciones de infraestructura de la Secretaria de la Alcaldia. Comprende la auditoria de calidad, diagnostico y procesamiento de capas geograficas correspondientes a los anos 2024, 2025 y 2026.

---

## Estructura del Proyecto

```
intervenciones_Infraestructura_2024_2026/
├── agente/                     -> Contexto operativo e instrucciones del agente
├── data_infraestructura/       -> Insumos geograficos organizados por ano
│   ├── 2024/
│   ├── 2025/
│   └── 2026/
├── scripts/                    -> Scripts Python de analisis y procesamiento
├── output/                     -> Resultados, reportes y archivos exportados
├── .gitignore
└── README.md
```

---

## Datos

Los insumos son capas vectoriales en formato Shapefile (LineString) que registran intervenciones de infraestructura vial y equipamientos. Se almacenan comprimidos en `.zip` dentro del repositorio.

| Ano  | Archivo                        | Registros | Columnas | CRS (EPSG) |
|------|--------------------------------|-----------|----------|------------|
| 2024 | Infraestructura_2024.shp       | 323       | 35       | 4326       |
| 2025 | 2025_Consolidado.shp           | 677       | 34       | 6249       |
| 2026 | 2026_Consolidado_proyect.shp   | 199       | 37       | 4326       |

---

## EDA - Diagnostico de Calidad

Se ejecuto un Analisis Exploratorio de Datos (EDA) sobre los tres shapefiles. Los puntos de control evaluados fueron:

1. Informacion general (CRS, tipo de geometria, total de registros).
2. Inventario de atributos (columnas y tipos de datos).
3. Calidad alfanumerica (nulos, vacios, duplicados tabulares).
4. Duplicidad espacial y topologica.

### Hallazgos Principales

**CRS inconsistente:**
- 2024 y 2026 usan EPSG:4326 (WGS84 geografico).
- 2025 usa EPSG:6249 (MAGNA-SIRGAS / Colombia Bogota zone). Requiere reproyeccion para homologar.

**Campos con 100% de nulidad (en los tres anos):**
- fuente_fin
- fecha_inau
- clase_up
- descripcio
- Observacio

**Campos con alta nulidad (70-100%):**
- referencia, referenc_1, plataforma, url_proces
- lat, lon (en 2025 y 2026)

**Duplicados:**
- Tabulares: 2 registros en 2025.
- Espaciales: 0 en todos los anos.

**Esquema no homogeneo:**
- Las columnas varian entre anos (35, 34, 37). Se requiere normalizacion para consolidaciones temporales.

### Resumen Numerico

| Metrica                  | 2024  | 2025  | 2026  |
|--------------------------|-------|-------|-------|
| Nulos totales            | 2,621 | 7,084 | 2,233 |
| Duplicados tabulares     | 0     | 2     | 0     |
| Duplicados espaciales    | 0     | 0     | 0     |
| Redundancia total        | 0     | 0     | 0     |

---

## Scripts

| Script                           | Descripcion                                         |
|----------------------------------|-----------------------------------------------------|
| `scripts/eda_data_infraestructura.py` | Auditoria de calidad y EDA de los 3 shapefiles |

---

## Tecnologias

- Python 3.x
- geopandas
- pandas
- uv (gestor de paquetes)

---

## Repositorio

https://github.com/j0rg3c45/-intervenciones_Infraestructura_2024_2026.git
