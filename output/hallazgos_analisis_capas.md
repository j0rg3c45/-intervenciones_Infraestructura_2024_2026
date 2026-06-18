# Hallazgos - Analisis de Capas de Infraestructura 2024-2026

## 1. Descripcion General de los Insumos

Los shapes suministrados por la Secretaria de Infraestructura contienen una capa unica por ano con geometria tipo LineString (trazados de vias intervenidas).

| Ano  | Archivo                        | Registros | Columnas | CRS (EPSG) | CRS Nombre                    |
|------|--------------------------------|-----------|----------|------------|-------------------------------|
| 2024 | Infraestructura_2024.shp       | 323       | 35       | 4326       | WGS 84                        |
| 2025 | 2025_Consolidado.shp           | 677       | 34       | 6249       | MAGNA-SIRGAS / Cali urban grid|
| 2026 | 2026_Consolidado_proyect.shp   | 199       | 37       | 4326       | WGS 84                        |

---

## 2. Cubrimiento Espacial

El cubrimiento corresponde al municipio de Santiago de Cali (Comunas 01-22 y corregimientos rurales).

| Ano  | Min Lon      | Min Lat    | Max Lon      | Max Lat    |
|------|--------------|------------|--------------|------------|
| 2024 | -76.660017   | 3.306021   | -76.462219   | 3.520078   |
| 2025 | 1046369.83 (proyectado) | 857913.35 (proyectado) | 1068038.45 (proyectado) | 881949.38 (proyectado) |
| 2026 | -76.636141   | 3.336163   | -76.464416   | 3.493317   |

Nota: 2025 esta en coordenadas planas (EPSG:6249), no comparables directamente con 2024 y 2026 sin reproyeccion.

---

## 3. Temporalidad

| Ano  | Campo ano | Fecha inicio (rango)       | Fecha fin (rango)          | Registros con fecha |
|------|-----------|----------------------------|----------------------------|---------------------|
| 2024 | 2024      | 2024-02-09 a 2025-01-14    | 2024-02-09 a 2025-01-17    | 322 de 323          |
| 2025 | 2025      | 2025-01-02 a 2025-12-30    | 2025-01-03 a 2026-07-21    | 677 de 677          |
| 2026 | 2026      | 2026-01-06 a 2026-05-06    | 2026-01-12 a 2026-05-07    | 178 de 199          |

---

## 4. Datos Tematicos Disponibles

### 4.1 Tipo de intervencion (tipo_inter)

| Ano  | Valores |
|------|---------|
| 2024 | Bacheo, Cicloinfraestructura, Fresado, Mantenimiento Via Urbana, Nivelacion, Pavimento, Recarpeteo |
| 2025 | Adoquin, Bacheo, Conformacion Vial, Construccion De Cunetas, Construccion Huellas Vehiculares, Construccion Huellas Vehiculares Y Cunetas, Construccion Obras De Drenaje, Fresado, Mantenimiento Via Urbana, Pavimento, Recarpeteo |
| 2026 | Bacheo, Fresado, Nivelacion, Pavimento, Recarpeteo |

### 4.2 Estado de la obra (estado)

| Ano  | Valores |
|------|---------|
| 2024 | Finalizado |
| 2025 | En Ejecucion, Finalizado, No Iniciado |
| 2026 | Finalizado |

### 4.3 Tipo de via (nombre_up)

Valores comunes: Camino o sendero, Cicloinfraestructura, Via arteria principal, Via arteria secundaria, Via colectora, Via interregional, Via local, Via rural.

### 4.4 Grupo normativo (GRUPO_NORM)

| Ano  | Valores |
|------|---------|
| 2024 | Grupo Operativo, Tercerizado, Tercerizado (Presupuesto Participativo) |
| 2025 | Grupo Operativo, Grupo Operativo (Cuadrilla 2.0), Tercerizado, Tercerizado (Presupuesto Participativo) |
| 2026 | Grupo Operativo, Grupo Operativo (Cuadrilla 2.0) |

### 4.5 Cobertura administrativa

- Comunas identificadas: 01 a 22 (mas corregimientos rurales)
- Barrios/veredas unicos: 156 (2024), 216 (2025), 72 (2026)

---

## 5. Campos con Datos Utiles (presentes en los 3 anos)

| Campo        | Descripcion                          | Completitud |
|--------------|--------------------------------------|-------------|
| identifica   | Identificador del proyecto           | 100%        |
| bpin         | Codigo BPIN                          | 100%        |
| tipo_equip   | Tipo de equipamiento                 | 100%        |
| tipo_inter   | Tipo de intervencion                 | 100%        |
| nombre_up    | Clasificacion de la via              | 100%        |
| comuna_cor   | Comuna o corregimiento               | 100%        |
| barrio_ver   | Barrio o vereda                      | 100%        |
| direccion    | Direccion de la intervencion         | 100%        |
| estado       | Estado de la obra                    | 100%        |
| presupuest   | Presupuesto asignado                 | 100%        |
| avance_obr   | Porcentaje de avance                 | 100%        |
| cantidad     | Cantidad (metros carril)             | 100%        |
| unidad       | Unidad de medida (Metro carril)      | 100%        |
| fecha_inic   | Fecha de inicio                      | 89-100%     |
| fecha_fin    | Fecha de finalizacion                | 88-100%     |
| GRUPO_NORM   | Grupo normativo de ejecucion         | 100%        |

---

## 6. Campos con Problemas de Calidad

### 6.1 Campos 100% vacios en los tres anos (sin informacion)

- fuente_fin
- fecha_inau
- clase_up
- descripcio
- Observacio

### 6.2 Campos con alta nulidad (>70%)

| Campo       | 2024   | 2025   | 2026   |
|-------------|--------|--------|--------|
| referencia  | 70.3%  | 82.1%  | 100%   |
| referenc_1  | 70.3%  | 82.1%  | 100%   |
| plataforma  | 70.3%  | 82.1%  | 100%   |
| url_proces  | 70.3%  | 82.1%  | 100%   |
| lat         | 0%     | 100%   | 100%   |
| lon         | 0%     | 100%   | 100%   |

### 6.3 Duplicados

- 2025: 2 registros con atributos tabulares identicos.
- No se detectaron duplicados espaciales en ningun ano.

---

## 7. Problemas Detectados

1. **CRS no homogeneo:** 2024 y 2026 en EPSG:4326 (WGS84), 2025 en EPSG:6249 (MAGNA-SIRGAS Cali). Impide consolidacion directa.
2. **Esquema de columnas variable:** 35 columnas (2024), 34 (2025), 37 (2026). No hay un esquema fijo.
3. **Campos sin uso:** 5 campos estan completamente vacios en todas las entregas.
4. **Campos lat/lon redundantes:** La geometria ya existe en el shape; estos campos no se llenan en 2025 y 2026.
5. **Registros sin fecha:** 21 registros en 2026 sin fecha_inic, 23 sin fecha_fin.
6. **2 duplicados tabulares en 2025.**

---

## 8. Recomendaciones para Solicitud Formal

1. **Estandarizar CRS:** Solicitar todas las entregas en EPSG:4326 (WGS84) o EPSG:9377 (MAGNA-SIRGAS origen nacional).
2. **Esquema fijo de atributos:** Exigir un esquema unico y documentado que se mantenga constante entre entregas.
3. **Diccionario de datos:** Solicitar documento oficial con la definicion, dominio de valores y obligatoriedad de cada campo.
4. **Eliminar o llenar campos vacios:** Los 5 campos 100% nulos deben eliminarse del esquema o llenarse obligatoriamente.
5. **Eliminar campos redundantes:** lat/lon no son necesarios si la capa ya tiene geometria.
6. **Validacion previa a la entrega:** Sin registros duplicados, sin geometrias nulas, fechas obligatorias.
7. **Periodicidad de entrega:** Definir formalmente si es mensual, trimestral o semestral.
8. **Formato de entrega:** Mantener formato .zip con todos los componentes del Shapefile incluidos.
