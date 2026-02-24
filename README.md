# Generador de Firmas de Correo | IMB-CNM

Este proyecto es una herramienta interactiva diseñada para generar firmas de correo electrónico profesionales de alto impacto. Aunque está preconfigurado para el **IMB-CNM (CSIC)**, el sistema es totalmente flexible y puede ser adaptado para cualquier organización.

<img width="1216" height="856" alt="image" src="https://github.com/user-attachments/assets/c5a64067-5b5c-4ebb-804e-d20a4fa63587" />


## 🚀 Descripción

El proyecto consiste en un generador basado en web que permite a los usuarios personalizar sus datos personales (nombre, cargo, extensiones, imágenes de perfil) y descargar un archivo HTML listo para ser importado en clientes de correo como Outlook, Gmail o Thunderbird.

La principal ventaja es que utiliza **estilos en línea (inline CSS)** automáticos para asegurar que la firma se vea idéntica en todos los dispositivos y aplicaciones de correo, solucionando los problemas comunes de formato.

## ✨ Características Principales

- **Personalización en tiempo real**: Cambia nombre, cargo, enlaces y fotos con vista previa instantánea.
- **Barra de separación configurable**: Permite activar/desactivar la línea vertical divisora, ajustar su ancho y elegir el color corporativo.
- **Gestión de Redes Sociales**: Añade o quita redes sociales de forma dinámica.
- **Descarga Directa**: Genera un archivo `.html` autónomo que puedes abrir e importar fácilmente.
- **Arquitectura Robusta**: Diseñado con Vue.js para la interfaz y Python para la generación del generador.

## 📁 Estructura del Proyecto

- `build_app.py`: El "motor" del proyecto. Es un script de Python que procesa la plantilla base y genera la herramienta interactiva.
- `generador.html`: La aplicación interactiva final. Solo necesitas abrir este archivo en cualquier navegador para empezar a crear firmas.
- `firma.html`: Un ejemplo de firma ya generada para pruebas rápidas.
- `images/`: Carpeta que contiene los activos visuales (logos del centro en color/gris y los iconos de redes sociales).
- `firma_original.html`: Plantilla base utilizada por el script de construcción.

## 🛠️ Requisitos

Para **usar** el generador:
- Solo necesitas un navegador web moderno (Chrome, Firefox, Edge, Safari).

Para **ejecutar el build** (si deseas modificar el funcionamiento interno):
- **Python 3.x** instalado en tu sistema.

## 📖 Instrucciones de Uso

### 1. Generar la Firma
1. Abre `generador.html` en tu navegador.
2. Rellena tus datos en las pestañas **Personal**, **Empresa** y **Redes**.
3. Sube tu foto de perfil y, si lo deseas, un banner de cabecera.
4. Ajusta la barra de separación según tu preferencia.
5. Haz clic en **"Descargar HTML"**.

### 2. Instalar en tu Correo
1. Abre el archivo `firma.html` descargado en tu navegador.
2. Selecciona toda la firma (Ctrl+A / Cmd+A).
3. Cópiala (Ctrl+C / Cmd+C).
4. Pégala en la configuración de firmas de tu cliente de correo (Outlook, Gmail, etc.).

## 🔧 Desarrollo y Adaptación

Si deseas adaptar este generador a otra empresa:
1. Modifica la plantilla base `firma_original.html` con el nuevo diseño.
2. Ajusta las reglas de reemplazo en `build_app.py` para que coincidan con tus nuevas etiquetas.
3. Ejecuta el script para generar el nuevo generador:
   ```bash
   python build_app.py
   ```

---
*Desarrollado para el IMB-CNM (CSIC).*

