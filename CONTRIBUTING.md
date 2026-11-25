# Guía de Contribución

Proyecto individual de análisis de datos agrícolas. Por defecto se trabaja directamente sobre `main`; las ramas se usan solo cuando el cambio lo amerite.

## 1. Ramas

**Formato:**
```bash
tipo/descripcion-corta
```


**Tipos permitidos**

| Tipo | Cuándo usarlo |
|---|---|
| `feat` | Nueva funcionalidad o análisis |
| `fix` | Corrección de errores |
| `refactor` | Reestructuración sin cambiar comportamiento |
| `data` | Cambios en pipeline, limpieza o validación de datos |
| `docs` | Documentación o notebooks de EDA |
| `chore` | Configuración, dependencias, tooling |

**Ejemplos**
- `data/parse-dms-to-utm`
- `feat/consolidate-monthly-csvs`
- `fix/encoding-csvs-2020`
- `chore/add-shapely-dependency`

> Si el cambio es pequeño (un notebook de EDA, un ajuste de `.gitignore`),
> se hace directamente en `main`.

---

## 2. Commits

**Formato:**
```bash
tipo(alcance): descripción en imperativo
```

**Alcances típicos**
`data`, `pipeline`, `parcela`, `eda`, `configs`, `docs`

**Ejemplos**
- `docs(eda): initial exploration of Parcela.xlsx`
- `data(pipeline): convert DMS coordinates to UTM`
- `feat(pipeline): consolidate monthly CSVs into a single parquet`
- `fix(pipeline): parse elevation with thousands separator`
- `chore(configs): add chardet dependency`

**Reglas**
- Idioma: **inglés**
- Descripción en imperativo (`add`, no `added`)
- En minúscula
- Máximo 72 caracteres en la primera línea
- Si necesitas más detalle, añade un cuerpo separado por una línea en blanco

---

## 3. Nunca commitear

- `.env`, credenciales o tokens
- `.venv/`
- `data/raw/`, `data/interim/`, `data/processed/`
- `models/*` (artefactos entrenados)
- `*.parquet`, `*.pkl`, `*.joblib`, `*.h5`
- `__pycache__/`, `.pytest_cache/`
- `.ipynb_checkpoints/`

Todo lo anterior ya está cubierto por `.gitignore`.

---

## 4. Notas

- Los **notebooks solo observan**; toda transformación vive en `src/`.
- Nombrado de notebooks: `NN_descripcion.ipynb` (ej. `01_eda_parcela.ipynb`).
- Toda limpieza debe ser reproducible: si un dato se transforma, el código
  que lo hace debe estar en `src/`, no solo en el notebook.
- La documentación de instalación y ejecución vive en el `README.md`.
