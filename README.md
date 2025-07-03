# 📊 Cargador de Archivos .dat de P.A.Hilton Logger

Este proyecto proporciona herramientas para cargar y analizar archivos de datos `.dat` generados por equipos P.A.Hilton Logger, específicamente diseñado para datos de radiación térmica.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso Rápido](#-uso-rápido)
- [Documentación de Funciones](#-documentación-de-funciones)
- [Estructura de Datos](#-estructura-de-datos)
- [Ejemplos](#-ejemplos)
- [Solución de Problemas](#-solución-de-problemas)
- [Contribuir](#-contribuir)

## ✨ Características

- ✅ **Carga automática** de archivos `.dat` de P.A.Hilton Logger
- ✅ **Detección inteligente** de estructura de archivos y nombres de columnas
- ✅ **Manejo robusto** de valores faltantes y formatos inconsistentes
- ✅ **Conversión automática** de fecha y hora a formato datetime
- ✅ **Análisis estadístico** integrado de los datos cargados
- ✅ **Visualización** clara de encabezados y primeras filas
- ✅ **Soporte para múltiples archivos** con carga en lote
- ✅ **Codificación Latin-1** para caracteres especiales

## 📦 Requisitos

- Python 3.7+
- pandas >= 1.0.0

## 🚀 Instalación

1. **Clona o descarga** este repositorio:
```bash
git clone <repository-url>
cd TRANSFER
```

2. **Instala las dependencias**:
```bash
pip install pandas
```

3. **Coloca tus archivos .dat** en el mismo directorio que `radiacion.py`

## ⚡ Uso Rápido

```python
# Importar el módulo
from radiacion import load_all_dat_files, show_dataframe_headers

# Cargar todos los archivos .dat del directorio actual
datos = load_all_dat_files()

# Mostrar resumen de todos los archivos cargados
show_dataframe_headers(datos)

# Acceder a un archivo específico
df = datos['nombre_archivo.dat']
```

## 📖 Documentación de Funciones

### `load_dat_file(file_path)`

Carga un archivo `.dat` individual en un DataFrame de pandas.

**Parámetros:**
- `file_path` (str): Ruta al archivo .dat

**Retorna:**
- `pandas.DataFrame`: DataFrame con los datos del archivo, o `None` si hay error

**Ejemplo:**
```python
df = load_dat_file('Radiacion_jul_01_11-1.dat')
if df is not None:
    print(f"Archivo cargado con {len(df)} filas")
```

### `load_all_dat_files(directory_path='.')`

Carga todos los archivos `.dat` de un directorio en un diccionario de DataFrames.

**Parámetros:**
- `directory_path` (str, opcional): Ruta al directorio. Por defecto es el directorio actual

**Retorna:**
- `dict`: Diccionario donde las claves son nombres de archivo y los valores son DataFrames

**Ejemplo:**
```python
# Cargar del directorio actual
datos = load_all_dat_files()

# Cargar de un directorio específico
datos = load_all_dat_files('/ruta/a/mis/datos')
```

### `show_dataframe_headers(dat_files_dict, max_rows=5)`

Muestra los encabezados y primeras filas de cada DataFrame.

**Parámetros:**
- `dat_files_dict` (dict): Diccionario con DataFrames (resultado de `load_all_dat_files`)
- `max_rows` (int, opcional): Número máximo de filas a mostrar. Por defecto 5

**Ejemplo:**
```python
datos = load_all_dat_files()
show_dataframe_headers(datos, max_rows=10)
```

### `show_single_dataframe_info(df, filename="DataFrame")`

Muestra información estadística detallada de un DataFrame individual.

**Parámetros:**
- `df` (pandas.DataFrame): DataFrame a analizar
- `filename` (str, opcional): Nombre identificativo del DataFrame

**Ejemplo:**
```python
df = datos['mi_archivo.dat']
show_single_dataframe_info(df, 'mi_archivo.dat')
```

## 📊 Estructura de Datos

Los archivos `.dat` de P.A.Hilton Logger tienen la siguiente estructura que es procesada automáticamente:

### Formato de Archivo Original
```
P.A.Hilton Logger Data File
C:\Users\Admin\Desktop\...
1/07/2025 11:27:14 a. m.

;;;0001;0011;0021;0031;0041;0051;0113;0123;
Graph Display;;;-10 | 100;-10 | 100;0 | 70;...
Lower limit | Upper Limit;;;- | -;- | -;...
;;;T1;T2;T3;T4;T5;Radiometer;Input Voltage;Input Current;
Sample;Date;Time;°C;°C;°C;°C;°C;W/m2;V;A;
0;1/07/2025;11:27:53;21,86623;24,61388;...
```

### DataFrame Resultante

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `Sample` | object | Número de muestra |
| `DateTime` | datetime64[ns] | Fecha y hora combinadas |
| `T1` | float64 | Temperatura 1 (°C) |
| `T2` | float64 | Temperatura 2 (°C) |
| `T3` | float64 | Temperatura 3 (°C) |
| `T4` | float64 | Temperatura 4 (°C) |
| `T5` | float64 | Temperatura 5 (°C) |
| `Radiometer` | float64 | Radiación térmica (W/m²) |
| `Input Voltage` | float64 | Voltaje de entrada (V) |
| `Input Current` | float64 | Corriente de entrada (A) |

## 💡 Ejemplos

### Ejemplo 1: Análisis Básico
```python
import pandas as pd
from radiacion import load_all_dat_files, show_dataframe_headers

# Cargar datos
datos = load_all_dat_files()

# Mostrar información general
show_dataframe_headers(datos)

# Acceder a un archivo específico
df = datos['Radiacion_jul_01_11-1.dat']

# Análisis básico
print(f"Promedio T1: {df['T1'].mean():.2f} °C")
print(f"Máxima radiación: {df['Radiometer'].max():.2f} W/m²")
```

### Ejemplo 2: Filtrado y Análisis Temporal
```python
# Cargar datos
datos = load_all_dat_files()
df = datos['Radiacion_jul_01_11-1.dat']

# Filtrar datos válidos (sin NaT en DateTime)
df_validos = df[df['DateTime'].notna()]

if not df_validos.empty:
    # Análisis temporal
    duracion = df_validos['DateTime'].max() - df_validos['DateTime'].min()
    print(f"Duración del experimento: {duracion}")
    
    # Estadísticas por columna
    columnas_temp = ['T1', 'T2', 'T3', 'T4', 'T5']
    temp_stats = df_validos[columnas_temp].describe()
    print(temp_stats)
```

### Ejemplo 3: Combinación de Múltiples Archivos
```python
import pandas as pd

# Cargar todos los archivos
datos = load_all_dat_files()

# Combinar todos los DataFrames
dfs_combinados = []
for nombre_archivo, df in datos.items():
    df_copia = df.copy()
    df_copia['archivo_origen'] = nombre_archivo
    dfs_combinados.append(df_copia)

# Crear DataFrame combinado
df_total = pd.concat(dfs_combinados, ignore_index=True)
print(f"Total de registros combinados: {len(df_total)}")
```

### Ejemplo 4: Exportar a Excel
```python
# Cargar datos
datos = load_all_dat_files()

# Exportar cada archivo a una hoja de Excel
with pd.ExcelWriter('datos_radiacion.xlsx') as writer:
    for nombre_archivo, df in datos.items():
        # Usar nombre de archivo sin extensión como nombre de hoja
        nombre_hoja = nombre_archivo.replace('.dat', '')
        df.to_excel(writer, sheet_name=nombre_hoja, index=False)

print("Datos exportados a 'datos_radiacion.xlsx'")
```

## 🔧 Solución de Problemas

### Error: "No se encontró la línea de encabezados"
**Causa:** El archivo no tiene el formato esperado de P.A.Hilton Logger.
**Solución:** Verifica que el archivo sea genuino y contenga la línea `Sample;Date;Time;`.

### Error: "can only concatenate str (not float) to str"
**Causa:** Este error fue corregido en la versión actual.
**Solución:** Asegúrate de usar la versión más reciente del código.

### Columnas DateTime aparecen como NaT
**Causa:** Formato de fecha/hora no reconocido.
**Solución:** Verifica que las fechas estén en formato `dd/mm/yyyy` y horas en `HH:MM:SS`.

### Archivos no se cargan
**Posibles causas:**
- Archivos no tienen extensión `.dat`
- Problemas de codificación
- Archivos corruptos

**Solución:**
```python
# Verificar archivos en directorio
import os
archivos_dat = [f for f in os.listdir('.') if f.endswith('.dat')]
print("Archivos .dat encontrados:", archivos_dat)
```

### Valores faltantes en columnas numéricas
**Es normal:** Algunos equipos pueden no registrar todos los sensores.
**Manejo:**
```python
# Contar valores faltantes
print(df.isnull().sum())

# Eliminar filas con valores faltantes en columnas críticas
df_limpio = df.dropna(subset=['T1', 'T2', 'Radiometer'])
```

## 🤝 Contribuir

1. **Fork** el repositorio
2. **Crea** una rama para tu función (`git checkout -b feature/nueva-funcion`)
3. **Confirma** tus cambios (`git commit -am 'Añadir nueva función'`)
4. **Push** a la rama (`git push origin feature/nueva-funcion`)
5. **Crea** un Pull Request

### Reportar Problemas

Si encuentras un problema:
1. Verifica que no esté ya reportado en Issues
2. Incluye un ejemplo de archivo `.dat` problemático (si es posible)
3. Describe los pasos para reproducir el error
4. Incluye la versión de Python y pandas que usas

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 📞 Contacto

Para preguntas o soporte, contacta al desarrollador o crea un issue en el repositorio.

---

**Desarrollado para análisis de datos de radiación térmica con equipos P.A.Hilton Logger** 🌡️📊
