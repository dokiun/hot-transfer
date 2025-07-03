# %%
import pandas as pd
import os
#%%
def load_dat_file(file_path):
    """
    Carga un archivo .dat de P.A.Hilton Logger en un DataFrame de pandas.
    
    Args:
        file_path (str): Ruta al archivo .dat
        
    Returns:
        pandas.DataFrame: DataFrame con los datos del archivo
    """
    try:
        # Leer el archivo línea por línea para encontrar donde comienzan los datos
        with open(file_path, 'r', encoding='latin-1') as f:
            lines = f.readlines()
        
        # Encontrar las líneas con los nombres de las columnas
        descriptive_names_line = None
        header_line = None
        data_start = None
        
        for i, line in enumerate(lines):
            # Buscar la línea con nombres descriptivos (T1, T2, etc.)
            if 'T1;T2;T3;T4;T5;Voltage;Amperios;DAT;' in line:
                descriptive_names_line = i
            # Buscar la línea con Sample;Date;Time; (línea de encabezados)
            elif line.strip().startswith('Sample;Date;Time;'):
                header_line = i
                data_start = i + 1
                break
        
        if header_line is None:
            raise ValueError("No se encontró la línea de encabezados en el archivo")
        
        # Extraer los nombres de columnas descriptivos si están disponibles
        if descriptive_names_line is not None:
            descriptive_names = lines[descriptive_names_line].strip().split(';')
            # Filtrar nombres vacíos y combinar con Sample, Date, Time
            descriptive_names = [name for name in descriptive_names if name.strip()]
            column_names = ['Sample', 'Date', 'Time'] + descriptive_names
        else:
            # Fallback: usar los nombres de la línea de encabezados
            column_names = lines[header_line].strip().split(';')
            # Renombrar columnas duplicadas
            seen = {}
            for i, name in enumerate(column_names):
                if name in seen:
                    seen[name] += 1
                    column_names[i] = f"{name}_{seen[name]}"
                else:
                    seen[name] = 1
        
        # Leer los datos usando pandas
        df = pd.read_csv(file_path, 
                        sep=';',
                        skiprows=data_start,
                        names=column_names,
                        encoding='latin-1',
                        decimal=',')  # Los archivos usan coma como separador decimal
        
        # Convertir la columna Date y Time en una sola columna datetime
        if 'Date' in df.columns and 'Time' in df.columns:
            # Manejar valores NaN correctamente
            df['Date'] = df['Date'].fillna('').astype(str)
            df['Time'] = df['Time'].fillna('').astype(str)
            
            # Filtrar filas donde Date o Time están vacíos o son 'nan'
            valid_rows = (df['Date'] != '') & (df['Time'] != '') & (df['Date'] != 'nan') & (df['Time'] != 'nan')
            
            # Inicializar columna DateTime para todas las filas
            df['DateTime'] = pd.NaT
            
            if valid_rows.any():
                df.loc[valid_rows, 'DateTime'] = pd.to_datetime(
                    df.loc[valid_rows, 'Date'] + ' ' + df.loc[valid_rows, 'Time'], 
                    format='%d/%m/%Y %H:%M:%S', 
                    errors='coerce'
                )
            
            # Reordenar columnas para que DateTime esté al principio
            cols = ['Sample', 'DateTime'] + [col for col in df.columns if col not in ['Sample', 'Date', 'Time', 'DateTime']]
            df = df[cols]
            
            # Las columnas Date y Time ya fueron eliminadas en el reordenamiento
        
        return df
        
    except Exception as e:
        print(f"Error al cargar el archivo {file_path}: {str(e)}")
        return None

def load_all_dat_files(directory_path='.'):
    """
    Carga todos los archivos .dat de un directorio en un diccionario de DataFrames.
    
    Args:
        directory_path (str): Ruta al directorio que contiene los archivos .dat
        
    Returns:
        dict: Diccionario donde las claves son los nombres de archivo y los valores son DataFrames
    """
    dat_files = {}
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.dat'):
            file_path = os.path.join(directory_path, filename)
            df = load_dat_file(file_path)
            if df is not None:
                dat_files[filename] = df
                print(f"Cargado: {filename} - {len(df)} filas")
            else:
                print(f"Error al cargar: {filename}")
    
    return dat_files

def show_dataframe_headers(dat_files_dict, max_rows=5):
    """
    Muestra los encabezados y las primeras filas de cada DataFrame en el diccionario.
    
    Args:
        dat_files_dict (dict): Diccionario con DataFrames (resultado de load_all_dat_files)
        max_rows (int): Número máximo de filas a mostrar para cada DataFrame (default: 5)
    """
    if not dat_files_dict:
        print("No hay archivos cargados para mostrar.")
        return
    
    for filename, df in dat_files_dict.items():
        print(f"\n{'='*60}")
        print(f"ARCHIVO: {filename}")
        print(f"{'='*60}")
        print(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
        print(f"\nColumnas:")
        for i, col in enumerate(df.columns):
            dtype = df[col].dtype
            print(f"  {i+1:2d}. {col:<15} ({dtype})")
        
        print(f"\nPrimeras {min(max_rows, len(df))} filas:")
        print(df.head(max_rows).to_string(index=False))
        
        if len(df) > max_rows:
            print(f"\n... y {len(df) - max_rows} filas más")

def show_single_dataframe_info(df, filename="DataFrame"):
    """
    Muestra información detallada de un solo DataFrame.
    
    Args:
        df (pandas.DataFrame): DataFrame a analizar
        filename (str): Nombre del archivo o identificador del DataFrame
    """
    print(f"\n{'='*60}")
    print(f"INFORMACIÓN DE: {filename}")
    print(f"{'='*60}")
    
    print(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
    
    print(f"\nTipos de datos:")
    print(df.dtypes.to_string())
    
    print(f"\nInformación estadística:")
    print(df.describe().to_string())
    
    print(f"\nValores nulos por columna:")
    null_counts = df.isnull().sum()
    for col, count in null_counts.items():
        if count > 0:
            print(f"  {col}: {count} valores nulos")
    if null_counts.sum() == 0:
        print("  No hay valores nulos")
    
    if 'DateTime' in df.columns:
        print(f"\nRango temporal:")
        print(f"  Inicio: {df['DateTime'].min()}")
        print(f"  Fin: {df['DateTime'].max()}")
        print(f"  Duración: {df['DateTime'].max() - df['DateTime'].min()}")

# %%
# Cargar todos los archivos
datos = load_all_dat_files()

# %%
datos['Radiacion_jul_01_11-1.dat']
# %%
