"""Dos ilustraciones del sitio redibujadas en SVG para poder animarlas.

- chica_con_telefono(): la ilustración de "Te damos la bienvenida" (Inicio).
  Al entrar en pantalla (y al pasar el puntero): parpadea, la cabeza se
  inclina apenas, la pantalla del teléfono se enciende y suben tres avisos
  (un corazón, un "me gusta" y un mensaje) que se desvanecen. El estado final
  es el mismo dibujo quieto de siempre.
- persona_con_tablet(): la ilustración que estaba junto al formulario de
  Contacto. Al entrar: aparecen las seis burbujas una por una, el dedo toca
  la pantalla y deja una onda, la red del cerebro se enciende, la curva del
  gráfico se dibuja y el candado se cierra.

Las dos son decorativas (aria-hidden), igual que las imágenes originales
(alt vacío). Sin JavaScript o con movimiento reducido se ven completas y quietas.
"""

AZUL = '#4b5fd1'
PIEL = '#f19ac1'
TINTA = '#1b2233'


AVISOS = {
    # Inicio: redes (un corazón, un "me gusta" y un mensaje).
    'redes': ('<g class="calma-chica__aviso" style="--i:0"><circle cx="262" cy="196" r="15"/><path d="M262 203c-6-4-9-7-9-10a4 4 0 0 1 9-2 4 4 0 0 1 9 2c0 3-3 6-9 10Z"/></g>'
              '<g class="calma-chica__aviso" style="--i:1"><circle cx="292" cy="160" r="15"/><path d="M285 166v-8h4l4-7c2 0 3 1 3 3l-1 4h5c1 0 2 1 2 2l-2 6c0 1-1 2-2 2h-9"/></g>'
              '<g class="calma-chica__aviso" style="--i:2"><circle cx="252" cy="130" r="15"/><path d="M245 124h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-8l-5 4v-4h-1a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2Z"/></g>'),
    # Contacto: escribe un mensaje (burbuja con puntos que saltan) y lo envía:
    # un avión de papel sale del teléfono, vuela dejando una estela y llega el tilde de enviado.
    'contacto': ('<g class="calma-chica__escribe"><path d="M252 170h48a8 8 0 0 1 8 8v14a8 8 0 0 1-8 8h-38l-10 8v-8a8 8 0 0 1-8-8v-14a8 8 0 0 1 8-8Z"/>'
                 '<circle class="calma-chica__punto" style="--i:0" cx="266" cy="185" r="3.2"/><circle class="calma-chica__punto" style="--i:1" cx="278" cy="185" r="3.2"/>'
                 '<circle class="calma-chica__punto" style="--i:2" cx="290" cy="185" r="3.2"/></g>'
                 '<path class="calma-chica__estela" pathLength="1" d="M240 226C272 222 300 210 312 180S320 130 332 118"/>'
                 '<g class="calma-chica__avion"><path d="M-14 2 16-10 4 14 0 4Z"/><path d="M0 4 16-10"/></g>'
                 '<g class="calma-chica__enviado"><circle cx="332" cy="118" r="15"/><path d="M325 118l5 5 10-10"/></g>'),
}


def chica_con_telefono(avisos='redes'):
    avisos = AVISOS[avisos]
    motas = ''.join(f'<circle cx="{x}" cy="{y}" r="1.4"/>' for x, y in (
        (104, 318), (110, 330), (98, 334), (116, 342), (106, 350), (122, 326), (100, 346), (114, 356),
        (296, 318), (290, 332), (302, 336), (284, 344), (294, 350), (280, 326), (300, 348), (288, 356)))
    return f'''<svg class="calma-chica" viewBox="-10 40 420 420" width="420" height="420" aria-hidden="true" focusable="false">
<g class="calma-chica__cuerpo">
<path d="M84 372c20-34 70-50 116-50s96 16 116 50c-10 30-60 44-116 44s-106-14-116-44Z" fill="#2f2b33"/>
<path d="M150 360l100 40" stroke="#1b1920" stroke-width="2" fill="none"/>
<path d="M96 262c4-46 50-70 104-70s100 24 104 70l8 70c2 24-12 36-36 38H124c-24-2-38-14-36-38Z" fill="{AZUL}"/>
<g fill="#2c3a9c" opacity=".55">{motas}</g>
<path d="M126 300l52-8M274 250l4 44M204 316l76-8" stroke="{TINTA}" stroke-width="2" stroke-linecap="round" fill="none"/>
<path d="M170 300c14-6 30-2 36 8 4 8-2 16-14 16h-22c-10 0-14-8-10-14Z" fill="{PIEL}"/>
<path d="M176 312h22" stroke="{TINTA}" stroke-width="1.6" stroke-linecap="round"/>
</g>
<rect x="186" y="168" width="28" height="30" fill="{PIEL}"/>
<g class="calma-chica__cabeza">
<path d="M150 150c-4-44 22-66 50-66s54 22 50 66l2 34h-26l-2-44c-8-4-14-10-18-20-6 14-18 22-34 24l-2 40h-24Z" fill="#111"/>
<ellipse cx="200" cy="148" rx="32" ry="34" fill="{PIEL}"/>
<circle cx="166" cy="152" r="7" fill="{PIEL}"/><circle cx="234" cy="152" r="7" fill="{PIEL}"/>
<path d="M170 138c-2-14 4-24 14-30 4 12 12 20 24 22 8-6 12-14 14-22 8 8 10 18 8 30-4-10-10-16-18-20-4 8-10 14-18 16-10 0-18-2-24-8Z" fill="#111"/>
<g class="calma-chica__ojos"><circle cx="188" cy="150" r="3" fill="{TINTA}"/><circle cx="212" cy="150" r="3" fill="{TINTA}"/></g>
<path d="M200 152v7h-3M192 166q8 6 16 0" stroke="{TINTA}" stroke-width="1.8" stroke-linecap="round" fill="none"/>
</g>
<g class="calma-chica__telefono">
<rect x="198" y="222" width="42" height="70" rx="7" fill="#b8c5dc" stroke="{TINTA}" stroke-width="2"/>
<rect class="calma-chica__pantalla" x="202" y="228" width="34" height="58" rx="4" fill="#dff1ee"/>
<circle cx="230" cy="232" r="3" fill="none" stroke="{TINTA}" stroke-width="1.6"/>
<path d="M200 258c10-6 26-8 38-2 6 4 6 12 2 16l-8 12c-4 6-14 8-22 4l-10-6c-6-4-6-16 0-24Z" fill="{PIEL}"/>
<path d="M214 260l18-4M216 270l18-4M218 280l14-3" stroke="{TINTA}" stroke-width="1.6" stroke-linecap="round" fill="none"/>
</g>
<g class="calma-chica__avisos">
{avisos}</g>
</svg>'''


NAVY = '#1f2a6b'


def persona_con_tablet():
    return f'''<svg class="calma-tablet" viewBox="0 0 460 520" width="460" height="520" aria-hidden="true" focusable="false">
<circle cx="230" cy="280" r="205" fill="#fff"/>
<g fill="none" stroke="{NAVY}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
<!-- Persona -->
<g class="calma-tablet__persona">
<path d="M190 300c-14-72 6-122 46-122s60 50 46 122" fill="{NAVY}" stroke="none"/>
<rect x="224" y="284" width="24" height="30" fill="#fff"/>
<path d="M160 420c0-70 30-110 76-110s76 40 76 110Z" fill="{NAVY}" stroke="none"/>
<ellipse cx="236" cy="250" rx="34" ry="40" fill="#fff"/>
<path d="M202 236c16-2 30-12 38-28 8 14 18 24 30 28" fill="{NAVY}" stroke="none"/>
<circle cx="224" cy="254" r="2.6" fill="{NAVY}" stroke="none"/><circle cx="248" cy="254" r="2.6" fill="{NAVY}" stroke="none"/>
<path d="M230 272q6 5 12 0"/>
</g>
<!-- Pantalla flotante con el cerebro -->
<g class="calma-tablet__panel">
<rect x="188" y="296" width="178" height="112" rx="8" stroke="#fff" fill="rgb(255 255 255 / .06)"/>
<path d="M200 312h34M200 322h22M322 312h32M330 322h24" stroke="#fff" stroke-width="2"/>
<path d="M258 336c-14 0-24 10-22 22 2 10 12 14 20 12 2 8 12 12 20 8 10 2 18-6 16-16 6-8 0-20-10-20-4-8-16-10-24-6Z" stroke="#fff" stroke-width="2"/>
<path d="M270 372v18M286 360h30M330 392h24" stroke="#fff" stroke-width="2"/>
<circle class="calma-tablet__toque" cx="292" cy="348" r="7" stroke="#fff" stroke-width="2.4"/>
<circle class="calma-tablet__onda" cx="292" cy="348" r="7" stroke="#fff" stroke-width="2"/>
</g>
<!-- Tablet y manos -->
<g class="calma-tablet__tableta" transform="rotate(-12 196 380)">
<rect x="150" y="322" width="84" height="110" rx="10" fill="#fff"/><circle cx="192" cy="377" r="7" fill="{NAVY}" stroke="none"/>
</g>
<path d="M146 362c-8 4-10 16-4 22 6 6 14 4 16-2" fill="#fff"/>
<path class="calma-tablet__dedo" d="M300 352c-6 4-8 10-2 14l22 14c8 4 16 0 18-8 2-10-4-18-12-20l-24-8" fill="#fff"/>
<!-- Burbujas -->
<g class="calma-tablet__burbuja" style="--i:0">
<path d="M40 96h128a8 8 0 0 1 8 8v80a8 8 0 0 1-8 8h-14l8 16-24-16H40a8 8 0 0 1-8-8v-80a8 8 0 0 1 8-8Z" fill="#fff"/>
<g class="calma-tablet__red" stroke-width="2"><path d="M70 140l30-18 30 10 20 26M70 140l30 24 24-8M100 122l0 42"/>
<circle cx="70" cy="140" r="5" fill="{NAVY}"/><circle cx="100" cy="122" r="5" fill="{NAVY}"/><circle cx="130" cy="132" r="5" fill="{NAVY}"/><circle cx="150" cy="158" r="5" fill="{NAVY}"/><circle cx="100" cy="164" r="5" fill="{NAVY}"/><circle cx="124" cy="156" r="5" fill="{NAVY}"/></g>
</g>
<g class="calma-tablet__burbuja" style="--i:1">
<circle cx="370" cy="130" r="50" fill="#fff"/><path d="M336 168l-10 16 22-8"/>
<path d="M346 168c4-14 14-20 24-20s20 6 24 20" fill="{NAVY}" stroke="none"/><circle cx="370" cy="128" r="16" fill="#fff"/>
<rect x="350" y="114" width="40" height="16" rx="6" fill="{NAVY}" stroke="none"/>
</g>
<g class="calma-tablet__burbuja" style="--i:2">
<rect x="14" y="222" width="130" height="100" rx="6" fill="#fff"/><path d="M14 236h130" stroke-width="12"/>
<path d="M30 250v58h100"/>
<path class="calma-tablet__area" d="M32 306 60 272l26 8 20-6 24-24v56Z" fill="{NAVY}" stroke="none"/>
<path class="calma-tablet__linea" pathLength="1" d="M32 306 60 272l26 8 20-6 24-24" stroke-width="2.4"/>
</g>
<g class="calma-tablet__burbuja" style="--i:3">
<rect x="344" y="228" width="104" height="92" rx="6" fill="#fff"/><path d="M344 242h104" stroke-width="12"/>
<circle cx="396" cy="272" r="14" fill="{NAVY}" stroke="none"/><rect x="362" y="296" width="68" height="12" rx="3" fill="{NAVY}" stroke="none"/>
</g>
<g class="calma-tablet__burbuja" style="--i:4">
<circle cx="76" cy="446" r="50" fill="#fff"/><path d="M116 418l12-14-18 6"/>
<rect x="46" y="436" width="60" height="38" rx="5" fill="#fff"/>
<circle cx="62" cy="452" r="5" fill="{NAVY}" stroke="none"/><path d="M54 467c2-6 14-6 16 0" stroke-width="2.4"/><path d="M76 450h22M76 460h16" stroke-width="2.4"/>
<path class="calma-tablet__arco" d="M70 436v-8a8 8 0 0 1 16 0v8"/><rect x="66" y="432" width="24" height="12" rx="3" fill="{NAVY}" stroke="none"/>
</g>
<g class="calma-tablet__burbuja" style="--i:5">
<path d="M346 424c-4-18 14-30 28-22 6-14 30-14 36 0 16-6 32 8 26 24 14 6 12 28-4 30-2 16-22 22-34 12-10 12-32 10-38-4-16 2-26-18-14-28Z" fill="#fff"/>
<circle cx="340" cy="484" r="7" fill="#fff"/><circle cx="328" cy="500" r="4" fill="#fff"/>
<g class="calma-tablet__arbol" stroke-width="2"><path d="M390 424v12M370 444h40M370 444v10M410 444v10M360 460h20M400 460h20"/>
<circle cx="390" cy="420" r="6" fill="{NAVY}"/><circle cx="370" cy="452" r="5" fill="{NAVY}"/><circle cx="410" cy="452" r="5" fill="{NAVY}"/>
<circle cx="360" cy="466" r="4" fill="{NAVY}"/><circle cx="380" cy="466" r="4" fill="{NAVY}"/><circle cx="400" cy="466" r="4" fill="{NAVY}"/><circle cx="420" cy="466" r="4" fill="{NAVY}"/></g>
</g>
</g>
</svg>'''
