import hashlib
import time
import itertools
import string
import sys

print("=== Demostración A04: Fuerza Bruta contra MD5 ===")

# Generamos el hash MD5 exacto para 'ucu3sep' dinámicamente para la demo
contrasena_objetivo = "ucu3s"
hash_objetivo = hashlib.md5(contrasena_objetivo.encode('utf-8')).hexdigest()

# Añadimos letras minúsculas porque la contraseña contiene "ucu" y "sep"
caracteres = string.ascii_lowercase + string.digits 
longitud_base = 5
longitud_maxima = 5

print(f"[*] Hash a romper: {hash_objetivo}")
print("[*] Iniciando ataque de fuerza bruta (calculando hashes al vuelo)...")

inicio = time.time()
intentos = 0

# Iteramos creando combinaciones
for longitud in range(longitud_base, longitud_maxima + 1):
    for combinacion in itertools.product(caracteres, repeat=longitud):
        intentos += 1
        intento_password = "".join(combinacion)
        
        # Indicador de progreso: actualiza la misma línea cada 500,000 intentos
        # Evitamos imprimir en cada intento porque el I/O de la terminal ralentizaría el ataque
        if intentos % 500000 == 0:
            sys.stdout.write(f"\r[*] Progreso: {intentos:,} hashes calculados... (Probando: {intento_password})")
            sys.stdout.flush()
            
        # Calculamos el MD5 de la combinación actual
        hash_calculado = hashlib.md5(intento_password.encode('utf-8')).hexdigest()
        
        # Comparamos si logramos romper el hash
        if hash_calculado == hash_objetivo:
            tiempo_total = time.time() - inicio
            # Limpiamos la línea de progreso con espacios antes de imprimir el resultado final
            sys.stdout.write("\r" + " " * 80 + "\r")
            
            print(f"[!] CRÍTICO -> ¡Contraseña rota!                     ")
            print(f"[*] Contraseña original: '{intento_password}'")
            print(f"[*] Hashes calculados: {intentos:,}")
            print(f"[*] Tiempo de ejecución: {tiempo_total:.4f} segundos")
            exit()

print("\n[-] Contraseña no encontrada en el espacio de búsqueda.")