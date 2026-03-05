import re
import os

input_file = 'firma_original.html'
output_file = 'generador.html'

with open(input_file, 'r', encoding='utf-8') as f:
    html = f.read()


# 1. Extract default images
def extract_img(pattern):
    m = re.search(pattern, html, re.IGNORECASE)
    return m.group(1) if m else ""

default_image = extract_img(r'<img[^>]*alt=""[^>]*src="(data:image/jpeg;base64,[^"]+)"[^>]*>')
default_header_image = extract_img(r'<img[^>]*alt="Institute of Microelectronics[^>]*src="(data:image/jpeg;base64,[^"]+)"[^>]*>')

img_fb = extract_img(r'<img[^>]*alt="Facebook"[^>]*src="(data:image/[^;]+;base64,[^"]+)"')
img_x = extract_img(r'<img[^>]*alt="X"[^>]*src="(data:image/[^;]+;base64,[^"]+)"')
img_yt = extract_img(r'<img[^>]*alt="Youtube"[^>]*src="(data:image/[^;]+;base64,[^"]+)"')
img_link = extract_img(r'<img[^>]*alt="Linkedin"[^>]*src="(data:image/[^;]+;base64,[^"]+)"')
img_insta = extract_img(r'<img[^>]*alt="Instagram"[^>]*src="(data:image/[^;]+;base64,[^"]+)"')


# 2. Replace Left Side (User info)
html = html.replace('Sergi Sànchez Romero', '<span v-html="formattedFullName"></span>')

# Inline styles for paragraphs and links to ensure better copy-paste
html = html.replace('<p style="font-family: Arial, Helvetica; font-size: 13px; color:#000; font-style:italic; vertical-align: text-top;">', 
                   '<p style="margin: 0 0 10px 0; font-family: Arial, Helvetica; font-size: 13px; color:#000; font-style:italic; vertical-align: text-top; line-height: 1.15;">')

title_html = """<a href="https://www.imb-cnm.csic.es/en/laboratories/wafer-electrical-characterisation-service" target="_blank" style="color: #000;">Head of the Electrical</a><br />
<a href="https://www.imb-cnm.csic.es/en/laboratories/wafer-electrical-characterisation-service" target="_blank" style="color: #000;">Characterisation Laboratory</a>"""
new_title_html = """<a :href="form.website || '#'" target="_blank" style="color: #000; text-decoration: underline;" v-html="formattedJobTitle"></a>"""
html = html.replace(title_html, new_title_html)

html = html.replace('<p style="font-family: Arial, Helvetica; font-size: 10px; color:#000; font-style:italic;">',
                   '<p style="margin: 5px 0 10px 0; font-family: Arial, Helvetica; font-size: 10px; color:#000; font-style:italic; line-height: 1.15;">')

# Clean up website and email
html = html.replace('<p style="font-family: Arial, Helvetica; font-size: 9px; color:#000;">',
                   '<p style="margin: 5px 0 10px 0; font-family: Arial, Helvetica; font-size: 9px; color:#000; line-height: 1.15;">')
html = html.replace('https://www.imb-cnm.csic.es/en/laboratories/wafer-electrical-characterisation-service', '{{ form.website }}')
# Fixed mailto replacement to be more robust
html = re.sub(r'href="mailto:[^"]+"', ':href="\'mailto:\' + (form.email || \'correo@imb-cnm.csic.es\')"', html)
html = html.replace('sergi.sanchez@imb-cnm.csic.es', '{{ form.email || "correo@imb-cnm.csic.es" }}')

# Inline underlines for links
html = html.replace('style="color: #000;"', 'style="color: #000; text-decoration: underline;"')
html = html.replace('style="color: #000"', 'style="color: #000; text-decoration: underline;"')

# Replace phone extensions
new_ext_html = """<span v-if="form.ext1 || form.ext2">
Ext. <a v-if="form.ext1" :href="'tel:+34935947700p' + form.ext1" style="color: #000; text-decoration: underline;">{{ form.ext1 }}</a>
<span v-if="form.ext1 && form.ext2"> - </span>
<a v-if="form.ext2" :href="'tel:+34935947700p' + form.ext2" style="color: #000; text-decoration: underline;">{{ form.ext2 }}</a>
</span><br />"""
html = re.sub(r'Ext\..*?</a>.*?(?:<br\s*/>|</p>)', new_ext_html, html, flags=re.DOTALL)

# Modify profile image to add transform (closer to the line)
html = re.sub(
    r'<img style="border-radius: 45px;" alt="" title="" src="data:image/jpeg;base64,[^"]+" />',
    r'<img style="border-radius: 45px; width: 55px; height: 55px; object-fit: cover; transform: translateX(3px);" alt="Profile" title="Profile" :src="form.image || defaultImage" />', 
    html
)

# Replace Header Image - use dynamic width binding
html = re.sub(
    r'<img border="0" style="width: 385px" alt="Institute of Microelectronics of Barcelona \(CSIC\)" title="Institute of Microelectronics of Barcelona \(CSIC\)" src="data:image/jpeg;base64,[^"]+" >',
    '<img border="0" :style="{ width: headerImageWidth + \'px\', maxHeight: \'150px\', objectFit: \'contain\' }" alt="Header" title="Header" :src="form.headerImage || defaultHeaderImage" >', 
    html
)

# Replace outer div width with dynamic binding
html = html.replace(
    '<div style="border: 1px solid #CCC; padding:2px; width: 390px; z-index:999;',
    '<div :style="{ border: \'1px solid #CCC\', padding: \'2px\', width: form.cardWidth + \'px\', zIndex: 999,'
)
html = html.replace(
    "-webkit-box-shadow: 5px 5px 5px 0px rgba(0,0,0,0.75);\n-moz-box-shadow: 5px 5px 5px 0px rgba(0,0,0,0.75);\nbox-shadow: 5px 5px 5px 0px rgba(0,0,0,0.75);\"",
    "WebkitBoxShadow: '5px 5px 5px 0px rgba(0,0,0,0.75)', MozBoxShadow: '5px 5px 5px 0px rgba(0,0,0,0.75)', boxShadow: '5px 5px 5px 0px rgba(0,0,0,0.75)' }\""
)

# Inline table styles - use dynamic width bindings
html = html.replace('<table width="390" border="0" style="padding-top: 10px;">',
                   '<table :width="form.cardWidth" border="0" style="margin-top: 10px; border-collapse: separate; border-spacing: 2px;">')
html = html.replace('<table width="250" border="0" style="padding: 0px;">',
                   '<table :width="form.leftWidth" border="0" style="padding: 0px; border-collapse: separate; border-spacing: 2px;">')

# Replace left section td width
html = html.replace('<td width="250" style="vertical-align:top;">',
                   '<td :width="form.leftWidth" style="vertical-align:top;">')

# Replace name/info column td width (193 = 250 - 55 - 2)
html = html.replace('<td width="193" style="vertical-align:top;">',
                   '<td :width="nameColumnWidth" style="vertical-align:top;">')

# Replace right section td width
html = html.replace('<td width="125" style="vertical-align:top;">',
                   '<td :width="rightWidth" style="vertical-align:top;">')


# Replace separator
# Use both width attribute and style width + min-width. Also reduce font-size/line-height to allow < 5px
separator_html = '<td v-if="form.showSeparator" :width="form.separatorWidth" :style="{ backgroundColor: form.separatorColor, width: form.separatorWidth + \'px\', minWidth: form.separatorWidth + \'px\', fontSize: \'1px\', lineHeight: \'1px\' }">&nbsp;</td>'
html = html.replace('<td with="5" style="background-color: #EBEBEB;">&nbsp;</td>', separator_html)

# 3. Replace Right Side (Company info and socials)
right_html = """<p style="margin: 0; font-family: Arial, Helvetica; font-size: 9px; color:#000; text-align:right; line-height: 1.15;">
{{ form.companyName }}<br />
{{ form.companyLine2 }}<br />
<a :href="form.companyAddressUrl" target="_blank" style="color: #000; text-decoration: underline;">{{ form.companyAddress }}</a><br />
{{ form.companyPostalCode }}<br />
{{ form.companyCity }}<br />
Tel. <a :href="'tel:' + form.companyPhone.replace(/\\s+/g, '')" style="color: #000; text-decoration: underline;">{{ form.companyPhone }}</a><br />
<a :href="form.companyWebsiteUrl" target="_blank" style="color: #000; text-decoration: underline;">{{ form.companyWebsiteDisplay }}</a><br />
<template v-for="(social, index) in form.socials" :key="index">
<a :href="social.url" target="_blank"><img style="margin-top:5px; max-height: 16px; margin-left: 2px; display: inline-block;" border="0" :alt="social.name" :title="social.name" :src="social.image || social.defaultImage" /></a>
</template>
</p>"""
html = re.sub(r'<p style="font-family: Arial, Helvetica; font-size: 9px; color:#000; text-align:right">.*?</p>', right_html.replace('\\', '\\\\'), html, flags=re.DOTALL)

html = html.replace('v-pre', '')

# Construct output
app_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generador de Firma de Correo | IMB-CNM</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <style>
        body {{ background-color: #f3f4f6; }}
        .glass {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        }}
        .preview-container img {{
            display: inline-block !important;
        }}
        .preview-container a {{
            text-decoration: underline !important;
        }}
        .preview-container p {{
            margin-top: 5px !important;
            margin-bottom: 10px !important;
            line-height: 1.15 !important;
        }}
        .preview-container p:first-child {{
            margin-top: 0 !important;
        }}
        .preview-container > div > table {{
            margin-top: 10px !important;
        }}
        .preview-container table {{
            border-collapse: separate !important;
            border-spacing: 2px !important;
        }}
        .preview-container a img {{
            margin-left: 2px !important;
        }}
    </style>
</head>
<body class="min-h-screen text-gray-800 font-sans p-4 md:p-8">

<div id="app" class="max-w-6xl mx-auto flex flex-col md:flex-row gap-8">
    
    <!-- Formulario con Tabs -->
    <div class="glass p-6 md:p-8 rounded-2xl w-full md:w-1/2 flex flex-col gap-4">
        <h1 class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 mb-2">Generador de Firma</h1>
        
        <!-- Navegación Tabs -->
        <div class="flex border-b border-gray-200 mb-2">
            <button @click="activeTab = 'user'" :class="['py-2 px-4 font-semibold text-sm', activeTab === 'user' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500 hover:text-gray-700']">Personal</button>
            <button @click="activeTab = 'company'" :class="['py-2 px-4 font-semibold text-sm', activeTab === 'company' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500 hover:text-gray-700']">Empresa</button>
            <button @click="activeTab = 'social'" :class="['py-2 px-4 font-semibold text-sm', activeTab === 'social' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500 hover:text-gray-700']">Redes</button>
        </div>

        <!-- Tab 1: Personal -->
        <div v-show="activeTab === 'user'" class="flex flex-col gap-4">
            <div>
                <label class="block text-sm font-semibold mb-1 text-gray-700">Nombre Completo</label>
                <input v-model="form.fullName" type="text" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition" placeholder="Ej. Ana García López"/>
                <p class="text-xs text-gray-400 mt-1">Usa la barra vertical (|) para dividir en dos líneas si es muy largo.</p>
            </div>
            
            <div>
                <label class="block text-sm font-semibold mb-1 text-gray-700">Puesto de trabajo</label>
                <input v-model="form.jobTitle" type="text" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition" placeholder="Ej. Investigadora Principal"/>
                <p class="text-xs text-gray-400 mt-1">Usa la barra vertical (|) para dividir en dos líneas.</p>
            </div>
            
            <div>
                <label class="block text-sm font-semibold mb-1 text-gray-700">Enlace web (Opcional)</label>
                <input v-model="form.website" type="text" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition" placeholder="https://..."/>
            </div>
            
            <div>
                <label class="block text-sm font-semibold mb-1 text-gray-700">Correo Electrónico</label>
                <input v-model="form.email" type="email" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition" placeholder="correo@imb-cnm.csic.es"/>
            </div>
            
            <div class="flex gap-4">
                <div class="w-1/2">
                    <label class="block text-sm font-semibold mb-1 text-gray-700">Extensión 1</label>
                    <input v-model="form.ext1" type="text" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition" placeholder="Ej. 435558"/>
                </div>
                <div class="w-1/2">
                    <label class="block text-sm font-semibold mb-1 text-gray-700">Extensión 2 (Opcional)</label>
                    <input v-model="form.ext2" type="text" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition" placeholder="Ej. 435583"/>
                </div>
            </div>

            <div>
                <label class="block text-sm font-semibold mb-1 text-gray-700">Imagen de Perfil</label>
                <input type="file" @change="handleImageUpload" accept="image/*" class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 transition"/>
            </div>

            <div class="mt-2 border-t pt-4">
                <label class="block text-sm font-semibold mb-1 text-gray-700">Imagen de Cabecera (Banner)</label>
                <input type="file" @change="handleHeaderUpload" accept="image/*" class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100 transition"/>
                <p class="text-xs text-red-500 mt-1">Cuidado con la altura: la imagen debe ocupar el mismo ancho siempre. Procura usar banners estrechos.</p>
            </div>
        </div>

        <!-- Tab 2: Empresa -->
        <div v-show="activeTab === 'company'" class="flex flex-col gap-4">
            <div>
                <label class="block text-sm font-semibold mb-1 text-gray-700">Nombre Organización</label>
                <input v-model="form.companyName" type="text" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"/>
            </div>
            <div>
                <label class="block text-sm font-semibold mb-1 text-gray-700">Segunda Línea (Campus)</label>
                <input v-model="form.companyLine2" type="text" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"/>
            </div>
            <div>
                <label class="block text-sm font-semibold mb-1 text-gray-700">Dirección</label>
                <input v-model="form.companyAddress" type="text" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"/>
                <input v-model="form.companyAddressUrl" type="text" class="w-full px-4 py-2 mt-1 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition cursor-pointer text-blue-600 text-xs" placeholder="URL Google Maps"/>
            </div>
            <div class="flex gap-4">
                <div class="w-1/2">
                    <label class="block text-sm font-semibold mb-1 text-gray-700">Código Postal</label>
                    <input v-model="form.companyPostalCode" type="text" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"/>
                </div>
                <div class="w-1/2">
                    <label class="block text-sm font-semibold mb-1 text-gray-700">Ciudad/País</label>
                    <input v-model="form.companyCity" type="text" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"/>
                </div>
            </div>
            <div>
                <label class="block text-sm font-semibold mb-1 text-gray-700">Teléfono General</label>
                <input v-model="form.companyPhone" type="text" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"/>
            </div>
            <div>
                <label class="block text-sm font-semibold mb-1 text-gray-700">Sitio Web</label>
                <input v-model="form.companyWebsiteDisplay" type="text" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition" placeholder="Texto a mostrar (ej. www.org.es)"/>
                <input v-model="form.companyWebsiteUrl" type="text" class="w-full px-4 py-2 mt-1 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition text-xs text-blue-600" placeholder="URL Destino (ej. https://www.org.es)"/>
            </div>

            <div class="border-t pt-4 mt-2">
                <label class="block text-sm font-semibold mb-2 text-gray-700">Dimensiones de la tarjeta</label>
                <div class="flex gap-4 mb-3">
                    <div class="w-1/3">
                        <label class="block text-xs font-semibold mb-1 text-gray-500">Ancho total (px)</label>
                        <input v-model.number="form.cardWidth" type="number" min="300" max="800" class="w-full px-3 py-1 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"/>
                    </div>
                    <div class="w-1/3">
                        <label class="block text-xs font-semibold mb-1 text-gray-500">Ancho izquierda (px)</label>
                        <input v-model.number="form.leftWidth" type="number" min="150" max="500" class="w-full px-3 py-1 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"/>
                    </div>
                    <div class="w-1/3">
                        <label class="block text-xs font-semibold mb-1 text-gray-500">Ancho derecha (auto)</label>
                        <input :value="rightWidth" type="number" disabled class="w-full px-3 py-1 text-sm border border-gray-200 rounded-lg bg-gray-100 text-gray-500 cursor-not-allowed"/>
                    </div>
                </div>
            </div>

            <div class="border-t pt-4 mt-2">
                <label class="flex items-center gap-2 text-sm font-semibold mb-2 text-gray-700 cursor-pointer">
                    <input type="checkbox" v-model="form.showSeparator" class="w-4 h-4 rounded text-blue-600 focus:ring-blue-500 border-gray-300 transition">
                    Mostrar barra de separación
                </label>
                <div v-if="form.showSeparator" class="flex gap-4">
                    <div class="w-1/2">
                        <label class="block text-xs font-semibold mb-1 text-gray-500">Ancho (px)</label>
                        <input v-model.number="form.separatorWidth" type="number" class="w-full px-3 py-1 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"/>
                    </div>
                    <div class="w-1/2">
                        <label class="block text-xs font-semibold mb-1 text-gray-500">Color</label>
                        <div class="flex gap-2">
                            <input v-model="form.separatorColor" type="color" class="h-9 w-12 p-0.5 border border-gray-200 rounded-lg cursor-pointer flex-shrink-0"/>
                            <input v-model="form.separatorColor" type="text" class="flex-1 px-3 py-1 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition uppercase" placeholder="#EBEBEB"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 3: Redes Sociales -->
        <div v-show="activeTab === 'social'" class="flex flex-col gap-2">
            <p class="text-xs text-gray-500 mb-2">Para añadir tu propio icono de red social, usa una imagen cuadrada que se escalará a 16px.</p>
            
            <div v-for="(social, index) in form.socials" :key="index" class="p-4 border rounded-xl bg-gray-50 mb-2 shadow-sm">
                <div class="flex justify-between items-center mb-2">
                    <span class="font-bold text-sm text-gray-700">Red Social {{{{ index + 1 }}}}</span>
                    <button @click="removeSocial(index)" class="text-red-500 text-xs font-semibold hover:underline">X Eliminar</button>
                </div>
                <div class="flex flex-col gap-2">
                    <input v-model="social.name" type="text" class="text-sm w-full px-3 py-2 border rounded-lg" placeholder="Nombre (ej. Instagram)"/>
                    <input v-model="social.url" type="text" class="text-sm w-full px-3 py-2 border rounded-lg text-blue-600" placeholder="URL del perfil (https://...)"/>
                    
                    <div class="flex items-center gap-3 mt-1">
                        <img v-if="social.image || social.defaultImage" :src="social.image || social.defaultImage" class="w-6 h-6 object-contain" />
                        <input type="file" @change="e => handleSocialUpload(e, index)" accept="image/*" class="text-xs text-gray-500 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:text-xs file:font-semibold file:bg-gray-200 file:text-gray-700 hover:file:bg-gray-300"/>
                    </div>
                </div>
            </div>
            
            <button @click="addSocial" class="text-blue-600 text-sm font-bold mt-2 hover:underline w-fit">+ Añadir red social</button>
        </div>

    </div>

    <!-- Vista Previa -->
    <div class="w-full md:w-1/2 flex flex-col gap-4">
        <div class="glass p-6 md:p-8 rounded-2xl flex-1 flex flex-col">
            <h2 class="text-xl font-bold text-gray-800 mb-6">Vista Previa</h2>
            
            <div class="bg-white p-4 rounded-xl border border-gray-100 shadow-sm overflow-x-auto flex-1 flex items-center justify-center">
                <div ref="signatureNode" class="preview-container">
                    {html}
                </div>
            </div>
            
            <div class="mt-6 flex flex-col gap-4">
                <button @click="downloadSignature" class="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl shadow-lg transform transition hover:-translate-y-0.5 active:translate-y-0 flex items-center justify-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    Descargar HTML
                </button>
            </div>
        </div>
    </div>

</div>

<script>
    const {{ createApp, ref, computed }} = Vue;

    createApp({{
        setup() {{
            const defaultImage = "{default_image}";
            const defaultHeaderImage = "{default_header_image}";
            
            const activeTab = ref('user');
            
            const form = ref({{
                fullName: "Sergi Sànchez Romero",
                jobTitle: "Head of the Electrical|Characterisation Laboratory",
                website: "https://www.imb-cnm.csic.es/en/laboratories/wafer-electrical-characterisation-service",
                email: "sergi.sanchez@imb-cnm.csic.es",
                ext1: "435558",
                ext2: "435583",
                image: null,
                headerImage: null,
                
                companyName: "IMB-CNM",
                companyLine2: "Campus UAB",
                companyAddress: "Carrer dels Til·lers, s/n",
                companyAddressUrl: "https://goo.gl/maps/m4e7gKaLXKn",
                companyPostalCode: "08193 Bellaterra",
                companyCity: "Barcelona (Spain)",
                companyPhone: "+34 93 594 77 00",
                companyWebsiteDisplay: "www.imb-cnm.csic.es",
                companyWebsiteUrl: "https://www.imb-cnm.csic.es/en",
                
                cardWidth: 390,
                leftWidth: 250,
                
                showSeparator: true,
                separatorWidth: 5,
                separatorColor: "#EBEBEB",
                
                socials: [
                    {{ name: "Facebook", url: "https://www.facebook.com/Institute-of-Microelectronics-of-Barcelona-CNM-700005623436396", image: null, defaultImage: "{img_fb}" }},
                    {{ name: "X", url: "https://x.com/imb_cnm", image: null, defaultImage: "{img_x}" }},
                    {{ name: "Youtube", url: "https://www.youtube.com/user/imbcnm", image: null, defaultImage: "{img_yt}" }},
                    {{ name: "Linkedin", url: "http://www.linkedin.com/company/imb-cnm-csic", image: null, defaultImage: "{img_link}" }},
                    {{ name: "Instagram", url: "https://www.instagram.com/imb_cnm/", image: null, defaultImage: "{img_insta}" }}
                ]
            }});

            const signatureNode = ref(null);

            const formattedFullName = computed(() => {{
                if (!form.value.fullName) return "Nombre Completo";
                return form.value.fullName.split('|').join('<br />');
            }});

            const formattedJobTitle = computed(() => {{
                if (!form.value.jobTitle) return "Puesto de trabajo";
                return form.value.jobTitle.split('|').join('<br />');
            }});

            const rightWidth = computed(() => {{
                const sep = form.value.showSeparator ? form.value.separatorWidth : 0;
                return form.value.cardWidth - form.value.leftWidth - sep - 10;
            }});

            const headerImageWidth = computed(() => form.value.cardWidth - 5);
            const nameColumnWidth = computed(() => form.value.leftWidth - 55 - 2);

            // Functions for Tab 1
            const handleImageUpload = (event) => {{
                const file = event.target.files[0];
                if (!file) return;
                const reader = new FileReader();
                reader.onload = (e) => form.value.image = e.target.result;
                reader.readAsDataURL(file);
            }};

            const handleHeaderUpload = (event) => {{
                const file = event.target.files[0];
                if (!file) return;
                const reader = new FileReader();
                reader.onload = (e) => form.value.headerImage = e.target.result;
                reader.readAsDataURL(file);
            }};

            // Functions for Tab 3
            const handleSocialUpload = (event, index) => {{
                const file = event.target.files[0];
                if (!file) return;
                const reader = new FileReader();
                reader.onload = (e) => form.value.socials[index].image = e.target.result;
                reader.readAsDataURL(file);
            }};
            
            const addSocial = () => {{
                form.value.socials.push({{ name: "Nueva Red", url: "#", image: null, defaultImage: null }});
            }};
            
            const removeSocial = (index) => {{
                form.value.socials.splice(index, 1);
            }};

            const downloadSignature = () => {{
                if (!signatureNode.value) return;

                const htmlContent = signatureNode.value.innerHTML;
                const fullHtml = `<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Firma de Correo</title>
    <style>
        body {{ font-family: Arial, Helvetica, sans-serif; }}
        /* Ensure images and tables keep their structure when viewed as a file */
        img {{ display: inline-block !important; }}
    </style>
</head>
<body>
    <div style="width: ${{form.value.cardWidth}}px;">
        ${{htmlContent}}
    </div>
</body>
</html>`;

                const blob = new Blob([fullHtml], {{ type: "text/html;charset=utf-8" }});
                const url = URL.createObjectURL(blob);
                const link = document.createElement("a");
                link.href = url;
                link.download = "firma.html";
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
            }};

            return {{
                activeTab,
                form,
                defaultImage,
                defaultHeaderImage,
                formattedFullName,
                formattedJobTitle,
                rightWidth,
                headerImageWidth,
                nameColumnWidth,
                handleImageUpload,
                handleHeaderUpload,
                handleSocialUpload,
                addSocial,
                removeSocial,
                downloadSignature,
                signatureNode
            }}
        }}
    }}).mount('#app');
</script>
</body>
</html>
"""

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(app_html)

print("Generado con éxito:", output_file)
