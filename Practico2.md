# Practico 2

## Inicialización del PoC

Inicializacion comun de todos los ejercicios

1. Levantar la aplicacion

```bash
docker compose up -d --build
```

2. Ingresar a localhost:5000

## 1. SQL Inyection

CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')

### PoC

**1.1.** Idem [Inicialización del PoC](#inicialización-del-poc)

**1.2.** En el buscador ingresar: 

Usando `%'` para cerrar prematuramente la clausula `LIKE '%`:

Podemos obtener la version SQL (entre otras posiblidades):
```sql
%' UNION SELECT sqlite_version(), '2026-07-20 00:00:00', 999 --
```
> Output: Fila con version exacta `3.46.1`

En este caso las modificaciones no son posibles por usar sqlite3, el cual prevee un statement a la vez. Por lo que `;` si separa statements pero no se ejecuta.

```sql
%'; DROP TABLE peliculas; --
```
> Output: <i>sqlite3.ProgrammingError: You can only execute one statement at a time.</i>


### Mitigación:

- **Sanitacizacion** del query el por marcadores, tratando como valor literal y no como codigo ejecutable?
- Whitelist para columnas, sory_by y sort_dir no tienen sanitazacion disponible

## 2. Cross Site Scripting

CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')

### PoC

**2.1.** Idem [Inicialización del PoC](#inicialización-del-poc)

**2.2.** Buscar una pelicula y hacer click en `Editar`

**2.3.** Reemplazar la descripcion del formulario por:

```html
<script>alert('Vulnerabilidad CWE-79 explotada exitosamente');</script>
```

**2.4.** Guardar el Formulario

**2.5.** Buscar la pelicula y hacer click en `Editar`

> Resultado: El navegador interpreta y renderiza las etiquetas `<script>`

### Mitigación:


- Remover `| safe`: Esta directiva de confianza de Jinja2 anula el por defecto de escapar los caracteres peligrosos (ej. `<` o `>`).

## 3. 