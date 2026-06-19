# ⚽ BetStats · Mundial 2026 — Análisis estadístico de los 72 partidos

Sitio estático con análisis de los 72 partidos de la fase de grupos del
Mundial 2026, generado con un modelo propio (Elo derivado del ranking FIFA
real + Poisson bivariado + Monte Carlo 50.000 simulaciones por partido).

Se actualiza automáticamente cada 2 horas con los resultados reales desde
la API pública de [football-data.org](https://www.football-data.org/).

---

## ¿Cómo publicarlo en 10 minutos?

### Paso 1 — Subir el código a GitHub

1. Creá un repositorio nuevo en [github.com/new](https://github.com/new)
   - Nombre sugerido: `mundial2026`
   - Visibilidad: **Public** (necesario para GitHub Pages gratis)
2. Subí todos los archivos de esta carpeta al repositorio
   (podés arrastrarlos desde la interfaz web o usar `git push`)

### Paso 2 — Obtener clave de la API (gratuita, 2 minutos)

1. Registrate en [football-data.org/client/register](https://www.football-data.org/client/register)
2. Confirmá tu email
3. Copiá tu **API Token** (está en tu perfil, es una cadena de 32 caracteres)

### Paso 3 — Agregar la clave como Secret en GitHub

1. En tu repositorio: **Settings → Secrets and variables → Actions**
2. Clic en **New repository secret**
3. Nombre: `FOOTBALL_DATA_API_KEY`
4. Valor: pegá tu token de football-data.org
5. Clic en **Add secret**

### Paso 4 — Activar GitHub Pages

1. En tu repositorio: **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: **gh-pages** / **/ (root)**
4. Clic en **Save**

### Paso 5 — Primera ejecución manual

1. Andá a **Actions → Actualizar sitio Mundial 2026**
2. Clic en **Run workflow → Run workflow**
3. Esperá ~2 minutos a que termine
4. Tu sitio estará en: `https://TU_USUARIO.github.io/mundial2026/`

---

## ¿Cómo funciona la actualización automática?

```
Cada 2 horas:
  update_scores.py  →  consulta football-data.org
                    →  escribe src/scores_live.json
  generate.py       →  fusiona scores_live + datos estáticos
                    →  regenera los 73 HTMLs (index + 72 partidos)
  GitHub Actions    →  publica docs/ en la rama gh-pages
```

Los partidos ya jugados muestran el **resultado real oficial** en un banner
verde al inicio de cada página. Los partidos pendientes muestran el análisis
predictivo del modelo.

---

## Estructura del repositorio

```
├── .github/workflows/update.yml  # Workflow de actualización automática
├── src/
│   ├── model.py         # Motor estadístico (Elo + Poisson + Monte Carlo)
│   ├── teams_data.py    # Datos de los 48 equipos (ranking, historial, estilo)
│   ├── extra_data.py    # Clima, H2H y marcadores estáticos iniciales
│   └── matches.json     # Calendario oficial de los 72 partidos
├── docs/                # Sitio generado (GitHub Pages sirve desde aquí)
│   ├── index.html
│   └── partidos/        # 72 páginas HTML (una por partido)
├── generate.py          # Generador del sitio HTML completo
├── update_scores.py     # Actualización de marcadores desde la API
├── requirements.txt
└── README.md
```

---

## Ejecutar localmente

```bash
pip install numpy requests

# Opcional: setear la API key para actualizar marcadores
export FOOTBALL_DATA_API_KEY="tu_token_aqui"
python update_scores.py

# Generar el sitio en docs/
python generate.py

# Abrir en el navegador
open docs/index.html   # macOS
xdg-open docs/index.html  # Linux
```

---

## Metodología del modelo

- **Rating Elo** derivado del ranking FIFA real al 11-jun-2026:
  `R = 1900 − 9 × (posición − 1)` + 40 puntos de bonus para los anfitriones
- **xG por partido** varía según calidad promedio de los equipos y brecha de nivel, ajustado por perfiles de estilo (ataque/defensa/físico/corners) individuales por equipo
- **Poisson bivariado** dividido 45%/55% entre primera y segunda mitad
- **Monte Carlo** con 50.000 simulaciones (numpy) para derivar empíricamente todas las probabilidades

---

> Análisis estadístico de entretenimiento · No es asesoría financiera ni de apuestas · Jugá con responsabilidad
