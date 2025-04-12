# 🧬 Buscador de Archivos Duplicados por Contenido (SHA-256)

Este script detecta archivos duplicados en una carpeta (o disco completo) **comparando su contenido** mediante el algoritmo de hash **SHA-256**. La interfaz gráfica está construida con `Tkinter` y ha sido **optimizada para alto rendimiento** en carpetas grandes gracias a:

- Uso de **procesamiento en segundo plano** (`multithreading`)
- Barra de **progreso visual**
- Agrupación de archivos duplicados por contenido exacto

---

## 🚀 ¿Cómo funciona?

### 🔐 Hash SHA-256
El script calcula un resumen criptográfico (digest) del contenido de cada archivo utilizando el algoritmo **SHA-2 (SHA-256)**. Si dos archivos producen el mismo hash, **se garantiza que su contenido es idéntico** (bit a bit).

### 🔁 Multithreading
Para evitar que la interfaz gráfica se congele durante el análisis de muchos archivos, el script:

1. Inicia un **hilo en segundo plano** (`threading.Thread`) para escanear y calcular los hashes.
2. La interfaz sigue respondiendo mientras se actualiza la **barra de progreso** en tiempo real.
3. Al finalizar, se cargan los duplicados detectados en una tabla interactiva.

---

## ✅ Funcionalidades destacadas

- Selector de carpeta para escanear.
- Detección precisa de duplicados por **contenido exacto** (no solo por nombre).
- Agrupación por **Grupo (G1, G2, etc.)** para ver qué archivos son iguales entre sí.
- Barra de progreso con estado de avance.
- Botón "Eliminar seleccionados" con confirmación.
- Botón "Abrir Carpeta" para inspeccionar los archivos directamente.
- Interfaz que **no colapsa en carpetas grandes** gracias al uso de multihilo.

---

## 📦 Requisitos

- Python 3.6 o superior
- Librerías estándar (`tkinter`, `hashlib`, `os`, etc.)
- Librería adicional:
  
    pip install humanize

---

## ▶️ Uso

1. Ejecuta el script:

    python duplicados_por_hash.py

2. Selecciona la carpeta o disco que deseas escanear.
3. Espera mientras se escanean los archivos (verás la barra de progreso).
4. Revisa los resultados:
   - Usa `Ctrl + clic` o `Shift` para selección múltiple en la tabla.
   - Haz clic en "Eliminar seleccionados" o "Abrir carpeta" para inspección manual.

---

## ⚙️ ¿Qué es SHA-256?

SHA-256 es parte del estándar **SHA-2** desarrollado por el NIST. Es una función de hash criptográfica que genera un **valor único de 64 caracteres** (256 bits) para un archivo.

Ventajas:
- Alta precisión para detectar duplicados.
- Incluso archivos con el mismo nombre pero diferente contenido serán tratados como únicos.

---

## 📌 Ideas futuras

- Combinación con búsqueda por nombre en un mismo sistema.
- Opciones avanzadas para usar hashes parciales o ignorar archivos pequeños.
- Exportar resultados a CSV.
- Interfaz más moderna con `ttkbootstrap` o `PyQt`.

---

## 🧑‍💻 Autor

Este script fue desarrollado como una solución educativa-práctica para organización de archivos. ¡Sugerencias, mejoras y forks son bienvenidos!
