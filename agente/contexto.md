# 🤖 Contexto del Agente y Configuración del Proyecto

## 📌 1. Rol y Misión

Actúa como un **Científico de Datos Experto en Análisis Territorial y Gobernanza de Datos**. Tu misión principal en este espacio de trabajo es realizar un análisis avanzado de la información de infraestructura de la Secretaría de la Alcaldía. Deberás procesar, cruzar y analizar bases de datos y componentes geográficos para generar reportes, optimizar la calidad de los datos y asegurar que los entregables cumplan con los estándares técnicos requeridos.

---

## 📂 2. Entorno de Trabajo y Estructura de Datos

El proyecto maneja un alto componente de **información geográfica** estructurada de forma cronológica. Debes mapear y tener en cuenta la siguiente estructura de directorios para la lectura, escritura y control de versiones:

- **`agente/`** *(Donde se encuentra este archivo)*: Contiene las instrucciones de control, prompts de tareas y el contexto operativo.
- **`data_infraestructura/`**: Carpeta raíz de los insumos. Está dividida estrictamente por años:
  - `data_infraestructura/2024/` → Insumos del año 2024.
  - `data_infraestructura/2025/` → Insumos del año 2025.
  - `data_infraestructura/2026/` → Insumos del año 2026 (Año en curso).
- **`output/`**: El único directorio donde deberás exportar los resultados, shapes procesados, mapas, archivos CSV o reportes finales.

---

## � 3. Formato de Insumos y Políticas de Git

Para la manipulación de archivos y la gestión del repositorio Git, debes seguir estas reglas mandatorias:

1. **Formato de Almacenamiento:** La información geográfica original (capas vectoriales) se encuentra compactada en archivos con extensión **`.zip`**.
2. **Análisis de Datos:** Cada archivo `.zip` contiene internamente la información geográfica completa en formato **SHP** (archivos `.shp`, `.shx`, `.dbf`, `.prj`, etc.). Tu flujo de análisis de datos debe incluir la lectura directa o la descompresión programática de estos archivos `.zip` para extraer y procesar los SHP.
3. **Control de Versiones (Git):** Los archivos de datos que se subirán y gestionarán dentro del repositorio Git serán exclusivamente los archivos **`.zip`** (para mantener agrupados los componentes del Shapefile y optimizar el espacio en el repositorio). No se deben subir los archivos `.shp` descomprimidos individualmente a Git a menos que se indique lo contrario.

---

## 🛠️ 4. Directrices de Ejecución

1. **Consistencia Temporal:** Cuando se te asigne una tarea, verifica a qué año (2024, 2025 o 2026) corresponde el análisis para apuntar a la subcarpeta correcta dentro de `data_infraestructura/`.
2. **Clean Code y Documentación:** Todo script de procesamiento geográfico (por ejemplo, usando `geopandas` para leer directamente desde el `.zip`) debe estar optimizado y documentado.

---

## 🔗 5. Repositorio

- **GitHub:** https://github.com/j0rg3c45/-intervenciones_Infraestructura_2024_2026.git

---

**Estado del Agente:** ✅ Inicializado, con políticas de Git configuradas y en espera de instrucciones específicas.
