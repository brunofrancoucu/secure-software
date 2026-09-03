import csv
import hashlib
import time

print("=== Demostración A04: Fallos Criptográficos ===")

# 1. Simulación de la creación de la Tabla Precomputada
diccionario = ["qwerty", "123456", "admin", "password", "peñarol2026", "seguridad2025"]
tabla_precomputada = {}

print("[*] Generando tabla precomputada en memoria...")
inicio_calc = time.time()

for palabra in diccionario:
    # Aseguramos utf-8 para que la "ñ" se procese bien
    hash_md5 = hashlib.md5(palabra.encode('utf-8')).hexdigest()
    tabla_precomputada[hash_md5] = palabra

print(f"[*] ¡Tabla lista en {time.time() - inicio_calc:.5f} segundos!\n")

# 2. Análisis de la base de datos robada
print("[*] Analizando usuarios.csv filtrado...")
# Aseguramos utf-8 al leer el archivo CSV
with open('usuarios.csv', mode='r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    
    for fila in lector:
        usuario = fila['Usuario']
        # .strip() elimina espacios y saltos de línea invisibles (\n, \r)
        hash_bd = fila['Hash_MD5'].strip()
        
        # 3. Explotación: Búsqueda en la tabla
        if hash_bd in tabla_precomputada:
            contrasena_original = tabla_precomputada[hash_bd]
            print(f"[!] CRÍTICO -> Usuario: '{usuario}' | Contraseña original expuesta: '{contrasena_original}'")
        else:
            print(f"[-] Seguro -> Usuario: '{usuario}' | Hash no encontrado.")