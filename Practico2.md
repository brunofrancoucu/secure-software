# Practico 2

## Inicialización del PoC

Inicializacion comun de todos los ejercicios

1. Levantar la aplicacion

```bash
docker compose up -d --build
```

2. Ingresar a [http://localhost:5000](http://localhost:5000)

## 1. SQL Inyection

[**CWE-89**](https://cwe.mitre.org/data/definitions/89.html?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc): *Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')*

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

[**CWE-79**](https://cwe.mitre.org/data/definitions/79.html?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc): *Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')*

### PoC

**2.1.** Idem [Inicialización del PoC](#inicialización-del-poc)

**2.2.** Buscar una pelicula y hacer click en `Editar`

**2.3.** Reemplazar la descripcion del formulario por:

```html
<script>alert('Vulnerabilidad **CWE-79** explotada exitosamente');</script>
```

**2.4.** Guardar el Formulario

**2.5.** Buscar la pelicula y hacer click en `Editar`

> Resultado: El navegador interpreta y renderiza las etiquetas `<script>`

### Mitigación:


- Remover `| safe`: Esta directiva de confianza de Jinja2 anula el por defecto de escapar los caracteres peligrosos (ej. `<` o `>`).

## 3. Subida Insegura de Archivos

[**CWE-434**](https://cwe.mitre.org/data/definitions/434.html?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc): *Unrestricted Upload of File with Dangerous Type* y [**CWE-22**](https://cwe.mitre.org/data/definitions/22.html?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc): *Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')*

Nota (CWE-434): Spring Boot, no soporta la ejecucion dinamica de archivos (ej. .jsp) asi como la sobreescritura de archivos esta protegida al usar `Files.copy()`, los ejemplos Web Shell en cwe.mitre.org no aplican para este entorno. 

### PoC CWE-434 y CWE-22

**3.1.** Idem [Inicialización del PoC](#inicialización-del-poc)

**3.2.** Subir el archivo:

```bash
curl -X POST http://localhost:5000/upload/1 -F "afiche=@xss.svg;filename=xss.svg"
```

**3.3** Entrar a [http://localhost:5000/uploads/xss.svg](http://localhost:5000/uploads/xss.svg)

Al compartir el link a usuarios de la aplicacion este script se ejecuta dentro de la frontera de confianza (el dominio), permitiendo ejemplo robar credenciales.

### Mitigacion

- Checkear el tipo de archivo subido (evitando ejecutables, innecesarios para la caratula de una pelicula)
- Validar que la solicitud no escape del directorio base

## 4. Inyección al Servidor (SpEL/SSTI)

[CWE-917](https://cwe.mitre.org/data/definitions/917.html): Improper Neutralization of Special Elements used in an Expression Language Statement y [CWE-94](https://cwe.mitre.org/data/definitions/94.html): Improper Control of Generation of Code

### PoC CWE-917 y CWE-94

**4.1.** Idem [Inicialización del PoC](#inicialización-del-poc)

**4.2.** Solicitud maliciosa inyectando java en el buscador.

```bash
curl -X POST http://localhost:5000/upload/1 -F "afiche=@xss.svg;filename=xss.svg"
```

> Output: Un archivo creado en el sistema operativo del servidor.

**4.3.** Verificar la vulnerabilidad

```bash
docker exec cinebuscador4 ls -l /tmp/servidor_comprometido.txt
```

> Output: *-rw-r--r-- 1 root root 0 Sep  6 20:54 /tmp/servidor_comprometido2.txt*

La ejecución de comandos arbitrarios puede resultar en la conexión remota asi tomando control total de la infraestructura.

### Mitigacion
- Evtar introducir datos controlados por el usuario a un interprete de expresiones (usando `SimpleEvaluationContext`).
- Bloquear la ejecucion de metodos java, limitando a solo lectura (idealmente `buscar` no pasa por SpEL).
- Validacion de la entrada del usuario para que no se evalue como expresion (sanitizacion o whitelist).