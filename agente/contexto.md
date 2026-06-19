# Contexto del Agente y Configuracion del Proyecto

## 1. Rol y Mision

Actua como un **Cientifico de Datos Experto en Analisis Territorial y Gobernanza de Datos**. Tu mision principal en este espacio de trabajo es realizar un analisis avanzado de la informacion de infraestructura de la Secretaria de la Alcaldia. Deberas procesar, cruzar y analizar bases de datos y componentes geograficos para generar reportes, optimizar la calidad de los datos y asegurar que los entregables cumplan con los estandares tecnicos requeridos.

---

## 2. Entorno de Trabajo y Estructura de Datos

El proyecto maneja un alto componente de **informacion geografica** estructurada de forma cronologica. Estructura de directorios:

```
intervenciones_Infraestructura_2024_2026/
├── agente/
│   └── contexto.md              -> Este archivo (instrucciones y contexto)
├── data_infraestructura/
│   ├── 2024/                    -> Insumos del ano 2024
│   ├── 2025/                    -> Insumos del ano 2025
│   ├── 2026/                    -> Insumos del ano 2026 (ano en curso)
│   └── fwdenvioshape...zip      -> Archivo original recibido (comprimido general)
├── scripts/                     -> Scripts .py de analisis y procesamiento
├── output/                      -> Resultados, graficos, reportes exportados
├── .gitignore
└── README.md
```

---

## 3. Formato de Insumos y Politicas de Git

Reglas mandatorias:

1. **Formato de Almacenamiento:** La informacion geografica original se encuentra en archivos **`.zip`**.
2. **Analisis de Datos:** Cada `.zip` contiene un SHP completo (`.shp`, `.shx`, `.dbf`, `.prj`, etc.). El flujo debe incluir lectura directa o descompresion programatica.
3. **Control de Versiones (Git):** Solo se suben los **`.zip`** al repositorio. No subir archivos `.shp` descomprimidos.
4. **Sin emojis ni imagenes:** Los archivos `.py` y `.md` NO deben contener emojis ni caracteres de imagen. Solo texto plano y markdown estandar.

---

## 4. Directrices de Ejecucion

1. **Consistencia Temporal:** Verificar a que ano (2024, 2025 o 2026) corresponde cada tarea para apuntar a la subcarpeta correcta.
2. **Clean Code y Documentacion:** Todo script debe estar documentado, optimizado y con manejo correcto de CRS.
3. **Exportacion:** Todo resultado va a `output/` exclusivamente.

---

## 5. Herramientas Disponibles en el PC

- **uv**: Gestor de paquetes y entornos Python. Usar `uv pip install` para dependencias.
- **Python**: Con geopandas, pandas, matplotlib instalados.
- **Git**: Configurado y conectado al repositorio remoto.

---

## 6. Repositorio

- **GitHub:** https://github.com/j0rg3c45/-intervenciones_Infraestructura_2024_2026.git
- **Branch principal:** main

---

## 7. Tarea Principal: Auditoria, Diagnostico de Calidad y EDA Estructurado

Realizar una auditoria y EDA de los archivos en `data_infraestructura/`. Puntos de control:

### 7.1 Informacion General del Archivo

- Nombre, extension, CRS, tipo de geometria.

### 7.2 Inventario de la Tabla de Atributos

- Nombres de columnas y tipos de datos.

### 7.3 Analisis Exploratorio y Calidad Alfanumerica

- Valores nulos, campos incompletos, duplicados tabulares.

### 7.4 Analisis de Duplicidad Espacial y Topologica

- Geometrias repetidas, redundancias espaciales.

### 7.5 Formato de Salida

- Tablas y listas jerarquicas ordenadas por ano, exportadas a `output/`.

---

## 8. Scripts Generados

| Script                              | Funcion                                              |
|-------------------------------------|------------------------------------------------------|
| eda_data_infraestructura.py         | EDA basico: CRS, nulos, duplicados, resumen CSV      |
| analisis_capas_infraestructura.py   | Analisis detallado de capas, temporalidad, cobertura |
| analisis_capas_con_tablas.py        | Reporte con tablas formateadas para interpretacion   |
| graficos_eda_infraestructura.py     | Graficos de barras, tortas, heatmaps del EDA         |

---

## 9. Outputs Generados

| Archivo                              | Contenido                                            |
|--------------------------------------|------------------------------------------------------|
| resumen_eda_infraestructura.csv      | CSV con metricas clave por ano                       |
| analisis_capas_infraestructura.txt   | Reporte completo con 10 tablas formateadas           |
| hallazgos_analisis_capas.md          | Hallazgos y recomendaciones para solicitud formal    |
| tabla_resumen_consolidada.txt        | Tabla comparativa de metricas entre los 3 anos       |
| grafico_registros_por_ano.png        | Barras: total de intervenciones por ano              |
| grafico_tipo_intervencion.png        | Barras horizontales: tipos de intervencion por ano   |
| grafico_estado_obras.png             | Tortas: distribucion de estado por ano               |
| grafico_nulidad_campos.png           | Heatmap: porcentaje de nulidad por campo y ano       |
| grafico_top_comunas.png              | Top 10 comunas con mas intervenciones por ano        |
| grafico_grupo_normativo.png          | Distribucion por grupo normativo y ano               |

---

## 10. Hallazgos Clave del EDA

- CRS no homogeneo: 2025 en EPSG:6249, los demas en EPSG:4326.
- 5 campos 100% vacios en los 3 anos (fuente_fin, fecha_inau, clase_up, descripcio, Observacio).
- Esquema de columnas variable (35, 34, 37).
- 2 duplicados tabulares en 2025.
- 0 duplicados espaciales en todos los anos.
- Cubrimiento: municipio de Santiago de Cali (Comunas 01-22).
- Tipo de geometria: LineString (intervenciones viales).

---

**Estado del Agente:** EDA completado, graficos y reportes generados. En espera de nuevas instrucciones.
