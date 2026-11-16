
import math
import matplotlib.pyplot as plt
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

# ---------------------------------------------
# 1. Parámetros de la figura polar
# ---------------------------------------------

n, d = 1, 4
num_points = 720
A = 110

k = n / d

theta_max = math.pi * d if (n * d) % 2 == 1 else 2 * math.pi * d

# ---------------------------------------------
# 2. Transformaciones
# ---------------------------------------------

ANGULO = 0
ESPEJO_X = False

OFFSET_X = 0
OFFSET_Y = 0

_c = math.cos(math.radians(ANGULO))
_s = math.sin(math.radians(ANGULO))


def transformar(x, y):

    if ESPEJO_X:
        x = -x

    xr = x * _c - y * _s
    yr = x * _s + y * _c

    return xr + OFFSET_X, yr + OFFSET_Y


# ---------------------------------------------
# 3. Generar rosa polar
# ---------------------------------------------

rosa = []

for i in range(num_points + 1):

    theta = theta_max * i / num_points

    r = A * math.cos(k * theta)

    x = r * math.cos(theta)
    y = r * math.sin(theta)

    rosa.append(transformar(x, y))


y_min = min(p[1] for p in rosa)


# ---------------------------------------------
# 4. Generar texto
# ---------------------------------------------

nombre = "Tito & Juan"

tam_fuente = 40
margen = 25

fp = FontProperties(
    family="DejaVu Sans",
    weight="bold"
)

tp = TextPath(
    (0, 0),
    nombre,
    size=tam_fuente,
    prop=fp
)

contornos = tp.to_polygons(closed_only=False)

# Centrar texto horizontalmente
ext = tp.get_extents()

dx = -(ext.x0 + ext.x1) / 2

# Ubicar debajo de la rosa
dy = (y_min - margen) - ext.y1

texto_trazos = []

for c in contornos:

    pts = [
        (float(px) + dx, float(py) + dy)
        for px, py in c
    ]

    if pts[0] != pts[-1]:
        pts.append(pts[0])

    # Aplicar las mismas transformaciones
    pts = [
        transformar(x, y)
        for x, y in pts
    ]

    texto_trazos.append(pts)


# ---------------------------------------------
# 5. Dibujar figura
# ---------------------------------------------

fig, ax = plt.subplots(figsize=(10, 10))

# Dibujar rosa polar
x_rosa = [p[0] for p in rosa]
y_rosa = [p[1] for p in rosa]

ax.plot(
    x_rosa,
    y_rosa,
    color="blue",
    linewidth=1.5,
    label="Rosa polar"
)

# Dibujar contornos del texto
for pts in texto_trazos:

    x_texto = [p[0] for p in pts]
    y_texto = [p[1] for p in pts]

    ax.plot(
        x_texto,
        y_texto,
        color="red",
        linewidth=1.5
    )

# ---------------------------------------------
# 6. Configuración del cuadro
# ---------------------------------------------

ax.set_title("Rosa polar y texto", fontsize=15)

ax.set_xlabel("X (mm)")
ax.set_ylabel("Y (mm)")

ax.set_aspect("equal", adjustable="datalim")

ax.grid(True, linestyle="--", alpha=0.5)

ax.axhline(0, color="black", linewidth=0.7)
ax.axvline(0, color="black", linewidth=0.7)

# ax.legend()

plt.tight_layout()
plt.show()
