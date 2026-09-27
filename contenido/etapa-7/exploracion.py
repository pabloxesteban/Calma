#!/usr/bin/env python3
"""Exploración de estilo: tres direcciones visuales con el mismo contenido real
(Equipo, Herramientas y Descargas) para elegir cómo sigue el sitio.

  A · Editorial — papel, tipografía grande, grilla asimétrica, monogramas.
  B · Nocturno  — secciones oscuras con la red del hero, luz que sigue al puntero.
  C · Capas     — fondo de tonos difusos, tarjetas translúcidas con profundidad.

Genera exploracion/index.html (se publica en GitHub Pages junto a la vista
previa, con noindex). No toca el plugin ni las páginas de WordPress.
Ejecutar: python3 contenido/etapa-7/exploracion.py
"""
import html
import pathlib
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from recursos import HABITOS, APPS, GUIAS, SUBIDAS  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parents[2]
OUT = RAIZ / 'exploracion'
FUENTES = '../vista-previa/codigo-calma/assets/fonts/'

TONOS = {
    'psicologia': ('#f6efe1', '#e2c17e', '#7a4d00'),
    'ia': ('#efedf9', '#bdb0ee', '#5b3fb8'),
    'neurociencia': ('#e9f1f8', '#9cc3e3', '#1d5f94'),
    'bienestar': ('#e8f3ee', '#9fd0c0', '#1f6b47'),
    'tecnologia': ('#f8ece6', '#ebb79c', '#9a3412'),
}

PERSONAS = [
    ('TS', 'Tatiana X. Stacul', 'Psicología', 'Psicóloga · ciberpsicología y comportamiento',
     'Hábitos digitales, desgaste y atención en el trabajo digital.', 'psicologia', 'Tatiana'),
    ('FC', 'Francisca Cortés Santoro', 'Accesibilidad cognitiva', 'Accesibilidad cognitiva y lenguaje',
     'Lectura fácil, lenguaje claro y carga cognitiva.', 'ia', 'Francisca'),
    ('EF', 'Emanuel C. Franco', 'Gestión de proyectos', 'Gestión de proyectos y procesos',
     'Alcance, plazos y procesos que se puedan sostener.', 'neurociencia', 'Emanuel'),
]

FLECHA = ('<svg class="flecha" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false">'
          '<path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')
BAJAR = ('<svg class="flecha" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false">'
         '<path d="M12 4v13M6 12l6 6 6-6M5 21h14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')
AFUERA = ('<svg class="flecha" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false">'
          '<path d="M7 17 17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')

DIRECCIONES = [
    ('editorial', 'A · Editorial',
     'Papel cálido, títulos grandes y grilla asimétrica tipo revista. Cada persona con un monograma enorme en su tono; '
     'las apps como un directorio; las guías como libros con lomo. Serio, cálido, muy legible.'),
    ('nocturno', 'B · Nocturno',
     'Secciones oscuras con la misma red de circuitos del hero. Una luz suave sigue al puntero sobre cada tarjeta y las '
     'figuras brillan en el tono de cada tema. Más tecnológico, sin perder calma.'),
    ('capas', 'C · Capas',
     'Fondo de tonos difusos (los de los temas) y tarjetas translúcidas que se inclinan apenas con el puntero. Profundidad '
     'y luz, estilo producto moderno. Suave y amable.'),
]


def e(t):
    return html.escape(t, quote=True)


def tono(tema):
    t, a, x = TONOS[tema]
    return f'--tono:{t};--acento:{a};--txt:{x}'


def cabecera(num, titulo, texto, pref):
    return (f'<header class="cab"><p class="cab__num" aria-hidden="true">{num}</p>'
            f'<h2 class="cab__titulo" id="{pref}-{num}">{titulo}</h2>' + (f'<p class="cab__texto">{texto}</p>' if texto else '') + '</header>')


def equipo(pref):
    items = ''.join(
        f'<li class="persona anima" style="{tono(tema)};--i:{i}"><a class="persona__enlace" href="https://pabloxesteban.github.io/Calma/vista-previa/equipo/">'
        f'<span class="persona__mono" aria-hidden="true">{ini}</span>'
        f'<span class="persona__area">{area}</span><span class="persona__nombre">{nombre}</span>'
        f'<span class="persona__rol">{rol}</span><span class="persona__texto">{texto}</span>'
        f'<span class="persona__ir">Conocer a {corto}<span class="boton-flecha">{FLECHA}</span></span></a></li>'
        for i, (ini, nombre, area, rol, texto, tema, corto) in enumerate(PERSONAS))
    return (f'<section class="bloque bloque--equipo" aria-labelledby="{pref}-01">'
            + cabecera('01', 'El equipo de <em>Código Calma</em>',
                       'Somos tres personas que miran la tecnología desde lugares distintos: la psicología, la accesibilidad cognitiva y la gestión de proyectos. Trabajamos con el mismo recorrido; cambia el terreno según lo que traigas.', pref)
            + f'<ul class="personas">{items}</ul></section>')


def herramientas(pref):
    habitos = ''.join(
        f'<li class="habito anima" style="{tono(tema)};--i:{i}">{fig()}<span class="chip">{chip}</span>'
        f'<h3>{titulo}</h3><p>{texto}</p></li>'
        for i, (tema, fig, chip, titulo, texto) in enumerate(HABITOS))
    grupos = ''
    for n, (tema, titulo, apps) in enumerate(APPS):
        filas = ''.join(
            f'<li class="app anima" style="{tono(tema)};--i:{i}"><a class="app__enlace" href="{e(url)}" rel="noopener" target="_blank">'
            f'<img class="app__logo" src="{SUBIDAS}{img}" width="{lado}" height="{lado}" alt="" loading="lazy" decoding="async">'
            f'<span class="app__nombre">{e(nombre)}</span><span class="app__desc">{e(texto)}</span>'
            f'<span class="app__ir">{AFUERA}<span class="sr"> (se abre en una pestaña nueva)</span></span></a></li>'
            for i, (nombre, texto, url, img, lado, alt) in enumerate(apps))
        grupos += (f'<div class="apps__grupo" style="{tono(tema)}"><h3 class="apps__titulo" id="{pref}-apps-{n}">{titulo}</h3>'
                   f'<ul class="apps__lista" aria-labelledby="{pref}-apps-{n}">{filas}</ul></div>')
    return (f'<section class="bloque bloque--herramientas" aria-labelledby="{pref}-02">'
            + cabecera('02', 'Pequeños hábitos, <em>gran diferencia</em>.',
                       'Estas herramientas no reemplazan el acompañamiento profesional. Son puntos de partida que muchas personas encuentran útiles.', pref)
            + f'<ul class="habitos">{habitos}</ul><div class="apps">{grupos}</div>'
            '<p class="aviso">Este contenido es educativo. Las apps recomendadas acompañan el bienestar diario y no reemplazan atención profesional.</p></section>')


def descargas(pref):
    colores = ['#3a3a3a', '#6b2fd6', '#1b2a6b', '#0f3b5c']
    items = ''
    for i, (titulo, tl, texto, dl, pdf, img, alt) in enumerate(GUIAS):
        lang_t = f' lang="{tl}"' if tl else ''
        lang_d = f' lang="{dl}"' if dl else ''
        items += (f'<li class="guia anima" style="--i:{i};--lomo:{colores[i]}"><div class="libro"><div class="libro__tapa">'
                  f'<img src="{SUBIDAS}{img}" width="400" height="400" alt="{e(alt)}" loading="lazy" decoding="async"></div></div>'
                  f'<div class="guia__texto"><p class="guia__autora">Por Tatiana X. Stacul</p>'
                  f'<h3><span{lang_t}>{e(titulo)}</span>{" (en inglés)" if tl else ""}</h3><p{lang_d}>{e(texto)}</p>'
                  f'<a class="guia__boton" href="https://codigocalma.com/wp-content/uploads/{pdf}" download>'
                  f'Descargar<span class="sr"> {e(titulo)}</span> <span class="guia__formato">PDF</span>{BAJAR}</a></div></li>')
    return (f'<section class="bloque bloque--descargas" aria-labelledby="{pref}-03">'
            + cabecera('03', 'Libros de <em>descarga gratuita</em>',
                       '', pref)
            + f'<ul class="guias">{items}</ul></section>')


CSS = r'''
@font-face{font-family:Lora;src:url(FUENTES/lora-latin-wght-normal.woff2) format("woff2");font-weight:400 700;font-display:swap}
@font-face{font-family:Lora;src:url(FUENTES/lora-latin-wght-italic.woff2) format("woff2");font-weight:400 700;font-style:italic;font-display:swap}
@font-face{font-family:Inter;src:url(FUENTES/inter-latin-wght-normal.woff2) format("woff2");font-weight:100 900;font-display:swap}
:root{--paper:#faf8f4;--paper2:#f2eee6;--ink:#1b2233;--ink2:#4a5263;--teal:#0f6b6b;--azul:#1d5f94;--linea:#e3ded3;--linea2:#cfc8ba;
--serif:Lora,Georgia,serif;--sans:Inter,system-ui,sans-serif;--ease:cubic-bezier(.22,1,.36,1)}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:400 1.0625rem/1.65 var(--sans);-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
h2,h3{margin:0;font-family:var(--serif);font-weight:600;line-height:1.12;letter-spacing:-.015em}
p{margin:0}
ul{list-style:none;margin:0;padding:0}
a{color:inherit}
.sr{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
:focus-visible{outline:3px solid var(--azul);outline-offset:3px}

/* Barra de elección */
.selector{position:sticky;top:0;z-index:20;color:var(--ink);background:rgb(250 248 244/.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--linea)}
.selector__in{max-width:1200px;margin:auto;padding:14px 20px;display:flex;flex-wrap:wrap;gap:12px 24px;align-items:center;justify-content:space-between}
.selector__marca{font:600 1rem/1.3 var(--serif)}
.selector__marca small{display:block;font:400 .8125rem/1.4 var(--sans);color:var(--ink2)}
.pestanas{display:flex;gap:6px;padding:4px;background:var(--paper2);border-radius:999px}
.pestanas button{min-height:44px;padding:0 18px;border:0;border-radius:999px;background:none;color:var(--ink);font:600 .9375rem var(--sans);cursor:pointer}
.pestanas button[aria-selected=true]{background:var(--ink);color:#fff}
.intro-dir{position:relative;z-index:1;max-width:1200px;margin:0 auto;padding:40px 20px 0}
.intro-dir p{max-width:70ch;color:var(--ink2)}
.intro-dir strong{color:var(--ink)}
.panel{padding-bottom:80px}
.panel[hidden]{display:none}

/* Estructura común */
.bloque{max-width:1200px;margin:0 auto;padding:clamp(56px,9vw,112px) 20px 0}
.cab{display:grid;gap:12px 48px;margin-bottom:40px}
@media(min-width:900px){.cab{grid-template-columns:1.1fr .9fr;align-items:end}.cab__num{grid-column:1/-1}}
.cab__titulo{font-size:clamp(2.1rem,1.4rem + 3vw,3.6rem)}
.cab__titulo em{font-style:italic;font-weight:500;color:var(--azul)}
.cab__texto{color:var(--ink2);max-width:52ch}
.flecha{flex:none}
.chip{display:inline-block;align-self:flex-start;padding:3px 12px;border-radius:999px;font:600 .8125rem/1.5 var(--sans)}
.habito h3{font-size:1.375rem}
.habito p{color:var(--ink2)}
.calma-org{display:block;width:100%;max-width:190px;height:auto;overflow:visible;fill:none;stroke:currentColor;stroke-width:1.2;stroke-linecap:round}
.calma-org *{transform-box:fill-box;transform-origin:center}
.calma-org .o-anillo{stroke-opacity:calc(.8 - var(--i)*.2)}
.calma-org .o-nucleo{fill:currentColor;stroke:none}
.calma-org .o-trazo{stroke-width:1.6;stroke-dasharray:1}
.calma-org .o-onda{stroke-width:1.6}
.aviso{margin-top:40px;max-width:70ch;font-size:.9375rem;color:var(--ink2)}
.guia h3{font-size:1.25rem}
.guia__autora{font-size:.875rem;color:var(--ink2)}
.guia__boton{display:inline-flex;align-items:center;gap:8px;min-height:44px;font-weight:600;text-decoration:none}
.guia__formato{font-size:.75rem;font-weight:700;letter-spacing:.04em;padding:2px 6px;border-radius:4px;border:1px solid currentColor}

/* ============================ A · EDITORIAL ============================ */
.d-editorial .cab{border-top:1px solid var(--ink);padding-top:18px}
.d-editorial .cab__num{font:500 .875rem/1 var(--sans);color:var(--teal);letter-spacing:.08em}
.d-editorial .personas{display:grid;gap:20px}
@media(min-width:900px){.d-editorial .personas{grid-template-columns:1.25fr 1fr 1fr}}
.d-editorial .persona__enlace{position:relative;display:flex;flex-direction:column;gap:6px;min-height:440px;padding:32px;overflow:hidden;background:var(--tono);text-decoration:none;isolation:isolate}
.d-editorial .persona__mono{position:absolute;z-index:-1;right:-.06em;top:-.3em;font:italic 500 clamp(10rem,16vw,13rem)/1 var(--serif);color:var(--acento);opacity:.75;letter-spacing:-.06em;transition:transform 1.1s var(--ease)}
.d-editorial .persona__area{font:600 .8125rem/1.4 var(--sans);color:var(--txt);margin-bottom:auto}
.d-editorial .persona__nombre{font:600 1.75rem/1.1 var(--serif);max-width:12ch}
.d-editorial .persona__rol{font-weight:600;color:var(--txt);font-size:.9375rem}
.d-editorial .persona__texto{color:var(--ink2);max-width:28ch}
.d-editorial .persona__ir{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:20px;padding-top:16px;border-top:1px solid rgb(27 34 51/.15);font-weight:600}
.boton-flecha{display:grid;place-items:center;width:44px;height:44px;border-radius:50%;border:1px solid currentColor;transition:background-color .4s var(--ease),color .4s var(--ease),transform .5s var(--ease)}
.d-editorial .persona__enlace:hover .persona__mono,.d-editorial .persona__enlace:focus-visible .persona__mono{transform:translate(-14px,14px) rotate(-4deg)}
.d-editorial .persona__enlace:hover .boton-flecha,.d-editorial .persona__enlace:focus-visible .boton-flecha{background:var(--ink);color:#fff;transform:rotate(-45deg)}
.d-editorial .habitos{display:grid;gap:20px}
@media(min-width:900px){.d-editorial .habitos{grid-template-columns:1.3fr 1fr;grid-template-rows:auto auto}.d-editorial .habito:first-child{grid-row:span 2}}
.d-editorial .habito{display:flex;flex-direction:column;gap:12px;padding:32px;background:var(--tono);color:var(--ink)}
.d-editorial .habito .calma-org{color:var(--txt);margin-bottom:auto}
.d-editorial .habito:first-child .calma-org{max-width:320px;margin:20px 0 auto}
.d-editorial .habito:first-child h3{font-size:2rem}
.d-editorial .chip{background:rgb(255 255 255/.7);color:var(--txt)}
.d-editorial .apps{margin-top:72px;display:grid;gap:56px}
@media(min-width:900px){.d-editorial .apps__grupo{display:grid;grid-template-columns:.8fr 2fr;gap:48px;align-items:start}.d-editorial .apps__titulo{position:sticky;top:96px}}
.d-editorial .apps__titulo{font-size:1.5rem;margin-bottom:16px;padding-left:18px;border-left:4px solid var(--acento)}
.d-editorial .apps__lista{border-top:1px solid var(--linea2)}
.d-editorial .app__enlace{display:grid;grid-template-columns:56px 1fr 44px;grid-template-areas:"logo nombre ir" "logo desc ir";gap:2px 20px;align-items:center;padding:20px 12px;border-bottom:1px solid var(--linea2);text-decoration:none;transition:background-color .4s var(--ease)}
.d-editorial .app__logo{grid-area:logo;width:56px;height:56px;border-radius:14px;object-fit:cover;transition:transform .6s var(--ease)}
.d-editorial .app__nombre{grid-area:nombre;font:600 1.25rem/1.2 var(--serif)}
.d-editorial .app__desc{grid-area:desc;color:var(--ink2);font-size:.9375rem;max-width:62ch}
.d-editorial .app__ir{grid-area:ir;display:grid;place-items:center;width:44px;height:44px;border-radius:50%;color:var(--txt);transition:transform .5s var(--ease),background-color .4s}
.d-editorial .app__enlace:hover{background:var(--tono)}
.d-editorial .app__enlace:hover .app__logo{transform:rotate(-6deg) scale(1.06)}
.d-editorial .app__enlace:hover .app__ir{background:#fff;transform:translate(3px,-3px)}
.d-editorial .guias{display:grid;gap:48px 32px;grid-template-columns:repeat(auto-fill,minmax(min(100%,230px),1fr))}
.d-editorial .libro{perspective:1200px;padding:10px 18px 26px 10px}
.d-editorial .libro__tapa{position:relative;transform:rotateY(-18deg);transform-origin:left center;transition:transform .9s var(--ease);box-shadow:18px 22px 30px -18px rgb(27 34 51/.55);border-radius:2px 6px 6px 2px;overflow:hidden}
.d-editorial .libro__tapa::before{content:"";position:absolute;z-index:1;inset:0 auto 0 0;width:12px;background:linear-gradient(90deg,rgb(0 0 0/.35),rgb(0 0 0/.05))}
.d-editorial .libro__tapa::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgb(0 0 0/.25),transparent 8%,rgb(255 255 255/.12) 10%,transparent 16%);pointer-events:none}
.d-editorial .guia:hover .libro__tapa{transform:rotateY(-6deg) translateY(-6px)}
.d-editorial .guia__texto{display:flex;flex-direction:column;gap:6px;margin-top:8px}
.d-editorial .guia__texto>p:not([class]){color:var(--ink2);font-size:.9375rem}
.d-editorial .guia__boton{color:var(--azul);margin-top:6px}
@media(prefers-reduced-motion:no-preference){
 .d-editorial .persona.anima:not(.visto) .persona__mono{transform:translateY(-60%)}
 .d-editorial .habito.anima.visto .o-trazo{animation:conectar 1.6s var(--ease) calc(var(--i,0)*.3s) backwards}
 .d-editorial .guia.anima:not(.visto) .libro__tapa{transform:rotateY(-70deg)}
}

/* ============================ B · NOCTURNO ============================ */
.d-nocturno{background:#0b1322;color:#e8edf5;--ink2:#a9b4c7}
.d-nocturno .intro-dir strong{color:#fff}
.d-nocturno .intro-dir p{color:#a9b4c7}
.d-nocturno .bloque{position:relative}
.d-nocturno .panel-fondo{position:relative;background:
 linear-gradient(rgb(255 255 255/.035) 1px,transparent 1px) 0 0/56px 56px,
 linear-gradient(90deg,rgb(255 255 255/.035) 1px,transparent 1px) 0 0/56px 56px}
.d-nocturno .cab__num{font:500 .875rem/1 var(--sans);color:#5fd4c4;letter-spacing:.08em;display:flex;align-items:center;gap:12px}
.d-nocturno .cab__num::after{content:"";height:1px;width:64px;background:linear-gradient(90deg,#5fd4c4,transparent)}
.d-nocturno .cab__titulo{color:#fff}
.d-nocturno .cab__titulo em{color:transparent;background:linear-gradient(90deg,#9cc3e3,#bdb0ee);-webkit-background-clip:text;background-clip:text}
.d-nocturno .cab__texto{color:#a9b4c7}
.d-nocturno .personas,.d-nocturno .habitos{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr))}
.luz{position:relative;background:#111b2e;border:1px solid rgb(255 255 255/.08);border-radius:16px;overflow:hidden;isolation:isolate}
.luz::before{content:"";position:absolute;inset:0;z-index:-1;background:radial-gradient(420px circle at var(--mx,50%) var(--my,-40%),color-mix(in srgb,var(--acento) 26%,transparent),transparent 45%);opacity:0;transition:opacity .5s var(--ease)}
.luz::after{content:"";position:absolute;inset:0;border-radius:inherit;padding:1px;background:radial-gradient(300px circle at var(--mx,50%) var(--my,-40%),var(--acento),transparent 50%);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;opacity:0;transition:opacity .5s var(--ease);pointer-events:none}
.luz:hover::before,.luz:hover::after,.luz:focus-within::before,.luz:focus-within::after{opacity:1}
.d-nocturno .persona__enlace{display:flex;flex-direction:column;gap:6px;min-height:380px;padding:28px;text-decoration:none}
.d-nocturno .persona__mono{display:grid;place-items:center;width:72px;height:72px;margin-bottom:auto;border-radius:50%;font:600 1.5rem/1 var(--serif);color:var(--acento);border:1px solid var(--acento);box-shadow:0 0 0 6px color-mix(in srgb,var(--acento) 12%,transparent),0 0 40px -6px var(--acento);transition:box-shadow .6s var(--ease)}
.d-nocturno .persona__enlace:hover .persona__mono{box-shadow:0 0 0 10px color-mix(in srgb,var(--acento) 16%,transparent),0 0 60px -4px var(--acento)}
.d-nocturno .persona__area{margin-top:28px;font:600 .8125rem/1.4 var(--sans);color:var(--acento)}
.d-nocturno .persona__nombre{font:600 1.625rem/1.12 var(--serif);color:#fff}
.d-nocturno .persona__rol{color:#cbd4e2;font-size:.9375rem}
.d-nocturno .persona__texto{color:#a9b4c7}
.d-nocturno .persona__ir{display:flex;align-items:center;justify-content:space-between;margin-top:18px;font-weight:600;color:#fff}
.d-nocturno .boton-flecha{border-color:rgb(255 255 255/.25)}
.d-nocturno .persona__enlace:hover .boton-flecha{background:var(--acento);border-color:var(--acento);color:#0b1322;transform:rotate(-45deg)}
.d-nocturno .habito{display:flex;flex-direction:column;gap:12px;padding:28px}
.d-nocturno .habito .calma-org{color:var(--acento);filter:drop-shadow(0 0 8px color-mix(in srgb,var(--acento) 70%,transparent));margin:8px 0 12px}
.d-nocturno .habito h3{color:#fff}
.d-nocturno .habito p{color:#a9b4c7}
.d-nocturno .chip{background:color-mix(in srgb,var(--acento) 18%,transparent);color:var(--acento)}
.d-nocturno .apps{margin-top:64px;display:grid;gap:48px}
.d-nocturno .apps__titulo{font-size:1.375rem;color:#fff;margin-bottom:18px;display:flex;align-items:center;gap:12px}
.d-nocturno .apps__titulo::before{content:"";width:10px;height:10px;border-radius:50%;background:var(--acento);box-shadow:0 0 14px var(--acento)}
.d-nocturno .apps__lista{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr))}
.d-nocturno .app__enlace{display:grid;grid-template-columns:auto 1fr;grid-template-areas:"logo ir" "nombre nombre" "desc desc";gap:10px;height:100%;padding:24px;text-decoration:none}
.d-nocturno .app__logo{grid-area:logo;width:60px;height:60px;border-radius:16px;object-fit:cover;box-shadow:0 0 0 1px rgb(255 255 255/.12),0 12px 30px -12px var(--acento)}
.d-nocturno .app__ir{grid-area:ir;justify-self:end;color:#a9b4c7;transition:transform .5s var(--ease),color .4s}
.d-nocturno .app__enlace:hover .app__ir{color:var(--acento);transform:translate(3px,-3px)}
.d-nocturno .app__nombre{grid-area:nombre;margin-top:10px;font:600 1.25rem/1.2 var(--serif);color:#fff}
.d-nocturno .app__desc{grid-area:desc;color:#a9b4c7;font-size:.9375rem}
.d-nocturno .aviso{color:#a9b4c7}
.d-nocturno .guias{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr))}
.d-nocturno .guia{padding:18px;display:flex;flex-direction:column;gap:16px;--acento:#9cc3e3}
.d-nocturno .libro__tapa{border-radius:10px;overflow:hidden;box-shadow:0 24px 50px -24px var(--lomo),0 0 0 1px rgb(255 255 255/.08);transition:transform .8s var(--ease)}
.d-nocturno .guia:hover .libro__tapa{transform:translateY(-6px) scale(1.02)}
.d-nocturno .guia__texto{display:flex;flex-direction:column;gap:6px;flex:1}
.d-nocturno .guia h3{color:#fff}
.d-nocturno .guia__autora,.d-nocturno .guia__texto>p:not([class]){color:#a9b4c7}
.d-nocturno .guia__boton{margin-top:auto;color:#9cc3e3}
@media(prefers-reduced-motion:no-preference){
 .d-nocturno .anima:not(.visto){opacity:.001;transform:translateY(24px)}
 .d-nocturno .anima{transition:opacity .9s var(--ease) calc(var(--i,0)*.1s),transform .9s var(--ease) calc(var(--i,0)*.1s)}
 .d-nocturno .habito.visto .o-anillo{animation:pulso 1.8s var(--ease) calc(var(--i)*.25s) 2 backwards}
 .d-nocturno .habito.visto .o-trazo{animation:conectar 1.6s var(--ease) calc(var(--i,0)*.3s) backwards}
}

/* ============================ C · CAPAS ============================ */
.d-capas .panel-fondo{position:relative;overflow:hidden;background:var(--paper)}
.d-capas .panel-fondo::before{content:"";position:absolute;inset:-10%;z-index:0;pointer-events:none;background:
 radial-gradient(38% 30% at 12% 8%,#f3e3c3 0,transparent 70%),
 radial-gradient(34% 28% at 88% 18%,#e2dcfa 0,transparent 70%),
 radial-gradient(40% 30% at 78% 52%,#d7e8f6 0,transparent 70%),
 radial-gradient(36% 26% at 16% 70%,#d6efe4 0,transparent 70%),
 radial-gradient(34% 24% at 70% 92%,#f6ddd0 0,transparent 70%);
 filter:blur(20px);transform:translateY(calc(var(--scroll,0)*-60px))}
.d-capas .bloque{position:relative;z-index:1}
.d-capas .cab__num{display:inline-flex;justify-self:start;align-items:center;justify-content:center;width:44px;height:44px;border-radius:50%;background:rgb(255 255 255/.7);box-shadow:0 8px 24px -14px rgb(27 34 51/.5);font:600 .875rem var(--sans);color:var(--teal)}
.vidrio{position:relative;background:rgb(255 255 255/.58);-webkit-backdrop-filter:blur(18px) saturate(1.4);backdrop-filter:blur(18px) saturate(1.4);border:1px solid rgb(255 255 255/.9);border-radius:24px;box-shadow:0 1px 0 rgb(255 255 255/.9) inset,0 24px 60px -34px rgb(27 34 51/.45);transform:perspective(900px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg)) translateY(var(--ty,0px));transition:transform .6s var(--ease),box-shadow .6s var(--ease)}
.vidrio:hover{--ty:-4px;box-shadow:0 1px 0 rgb(255 255 255/.9) inset,0 34px 70px -34px rgb(27 34 51/.5)}
.d-capas .personas,.d-capas .habitos{display:grid;gap:20px;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr))}
.d-capas .persona__enlace{display:flex;flex-direction:column;gap:6px;min-height:400px;padding:28px;text-decoration:none}
.d-capas .persona__mono{display:grid;place-items:center;width:104px;height:104px;margin-bottom:auto;border-radius:50%;font:italic 600 2rem/1 var(--serif);color:var(--txt);background:radial-gradient(circle at 30% 25%,#fff 0,var(--tono) 40%,var(--acento) 100%);box-shadow:0 20px 40px -20px var(--acento),inset 0 -8px 20px -8px rgb(255 255 255/.6);transition:transform .8s var(--ease)}
.d-capas .persona__enlace:hover .persona__mono{transform:scale(1.06) rotate(-6deg)}
.d-capas .persona__area{margin-top:24px;font:600 .8125rem/1.4 var(--sans);color:var(--txt)}
.d-capas .persona__nombre{font:600 1.625rem/1.12 var(--serif)}
.d-capas .persona__rol{color:var(--txt);font-weight:600;font-size:.9375rem}
.d-capas .persona__texto{color:var(--ink2)}
.d-capas .persona__ir{display:flex;align-items:center;justify-content:space-between;margin-top:18px;font-weight:600}
.d-capas .boton-flecha{border:0;background:var(--ink);color:#fff}
.d-capas .persona__enlace:hover .boton-flecha{transform:rotate(-45deg);background:var(--txt)}
.d-capas .habito{display:flex;flex-direction:column;gap:12px;padding:28px}
.d-capas .habito .calma-org{color:var(--txt);margin:0 0 8px;padding:18px;max-width:none;width:100%;border-radius:18px;background:linear-gradient(135deg,var(--tono),#fff)}
.d-capas .chip{background:var(--tono);color:var(--txt)}
.d-capas .apps{margin-top:64px;display:grid;gap:40px}
.d-capas .apps__titulo{font-size:1.375rem;margin-bottom:16px}
.d-capas .apps__lista{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr))}
.d-capas .app__enlace{display:grid;grid-template-columns:64px 1fr 32px;grid-template-areas:"logo nombre ir" "logo desc desc";gap:4px 16px;align-items:start;padding:20px;height:100%;text-decoration:none}
.d-capas .app__logo{grid-area:logo;width:64px;height:64px;border-radius:18px;object-fit:cover;box-shadow:0 14px 30px -16px rgb(27 34 51/.6)}
.d-capas .app__nombre{grid-area:nombre;font:600 1.1875rem/1.25 var(--serif);align-self:center}
.d-capas .app__desc{grid-area:desc;color:var(--ink2);font-size:.9375rem}
.d-capas .app__ir{grid-area:ir;color:var(--txt);transition:transform .5s var(--ease)}
.d-capas .app__enlace:hover .app__ir{transform:translate(3px,-3px)}
.d-capas .guias{display:grid;gap:28px;grid-template-columns:repeat(auto-fill,minmax(min(100%,250px),1fr))}
.d-capas .guia{padding:16px 16px 22px;display:flex;flex-direction:column;gap:16px}
.d-capas .libro__tapa{border-radius:16px;overflow:hidden;box-shadow:0 22px 40px -22px rgb(27 34 51/.6);transform:rotate(calc((var(--i) - 1.5)*1.6deg));transition:transform .8s var(--ease)}
.d-capas .guia:hover .libro__tapa{transform:rotate(0) scale(1.03)}
.d-capas .guia__texto{display:flex;flex-direction:column;gap:6px;flex:1;padding:0 4px}
.d-capas .guia__texto>p:not([class]){color:var(--ink2);font-size:.9375rem}
.d-capas .guia__boton{margin-top:auto;align-self:flex-start;padding:0 18px;border-radius:999px;background:var(--ink);color:#fff}
.d-capas .guia__formato{border-color:rgb(255 255 255/.5)}
@media(prefers-reduced-motion:no-preference){
 .d-capas .anima:not(.visto){opacity:.001;transform:perspective(900px) translateY(30px) scale(.98)}
 .d-capas .anima{transition:opacity 1s var(--ease) calc(var(--i,0)*.12s),transform 1s var(--ease) calc(var(--i,0)*.12s),box-shadow .6s var(--ease)}
 .d-capas .habito.visto .o-anillo{animation:pulso 1.8s var(--ease) calc(var(--i)*.25s) 2 backwards}
 .d-capas .habito.visto .o-trazo{animation:conectar 1.6s var(--ease) calc(var(--i,0)*.3s) backwards}
}

@keyframes conectar{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
@keyframes pulso{from{transform:scale(.35);stroke-opacity:1}70%{stroke-opacity:.2}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{transition:none!important;animation:none!important}.d-capas .panel-fondo::before{transform:none}}
@media(max-width:600px){.d-editorial .persona__enlace{min-height:360px}}
'''.replace('FUENTES/', FUENTES)

JS = r'''
(function(){
 var botones=[].slice.call(document.querySelectorAll('[role=tab]'));
 var reducido=matchMedia('(prefers-reduced-motion: reduce)').matches;
 function mostrar(id,foco){
  botones.forEach(function(b){var si=b.getAttribute('aria-controls')===id;b.setAttribute('aria-selected',si);b.tabIndex=si?0:-1;document.getElementById(b.getAttribute('aria-controls')).hidden=!si;if(si&&foco)b.focus();});
  document.body.className='d-'+id;
  try{history.replaceState(null,'','#'+id)}catch(e){}
  observar();
 }
 botones.forEach(function(b,i){
  b.addEventListener('click',function(){mostrar(b.getAttribute('aria-controls'))});
  b.addEventListener('keydown',function(ev){var d=ev.key==='ArrowRight'?1:ev.key==='ArrowLeft'?-1:0;if(d){ev.preventDefault();var n=botones[(i+d+botones.length)%botones.length];mostrar(n.getAttribute('aria-controls'),true)}});
 });
 var io='IntersectionObserver' in window&&!reducido?new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('visto');io.unobserve(en.target)}})},{threshold:.2}):null;
 function observar(){document.querySelectorAll('.panel:not([hidden]) .anima:not(.visto)').forEach(function(el){if(io)io.observe(el);else el.classList.add('visto')})}
 // B: la luz sigue al puntero. C: la tarjeta se inclina apenas.
 if(!reducido){
  document.addEventListener('pointermove',function(ev){
   var t=ev.target.closest&&ev.target.closest('.luz, .vidrio');if(!t||ev.pointerType!=='mouse')return;
   var r=t.getBoundingClientRect(),x=ev.clientX-r.left,y=ev.clientY-r.top;
   if(t.classList.contains('luz')){t.style.setProperty('--mx',x+'px');t.style.setProperty('--my',y+'px')}
   else{t.style.setProperty('--ry',((x/r.width-.5)*6).toFixed(2)+'deg');t.style.setProperty('--rx',((.5-y/r.height)*6).toFixed(2)+'deg')}
  },{passive:true});
  document.addEventListener('pointerout',function(ev){var t=ev.target.closest&&ev.target.closest('.vidrio');if(t&&!t.contains(ev.relatedTarget)){t.style.removeProperty('--rx');t.style.removeProperty('--ry')}});
  var fondo=null;addEventListener('scroll',function(){fondo=fondo||document.querySelector('#capas .panel-fondo');if(fondo)fondo.style.setProperty('--scroll',(scrollY/document.body.scrollHeight).toFixed(3))},{passive:true});
 }
 function desdeHash(){var h=(location.hash||'').slice(1);mostrar(['editorial','nocturno','capas'].indexOf(h)>=0?h:'editorial')}addEventListener('hashchange',desdeHash);desdeHash();
})();
'''


def panel(clave, nombre, texto):
    cuerpo = equipo(clave) + herramientas(clave) + descargas(clave)
    if clave == 'nocturno':
        cuerpo = cuerpo.replace('class="persona anima"', 'class="persona anima luz"').replace('class="habito anima"', 'class="habito anima luz"') \
                       .replace('class="app anima"', 'class="app anima luz"').replace('class="guia anima"', 'class="guia anima luz"')
    if clave == 'capas':
        cuerpo = cuerpo.replace('class="persona anima"', 'class="persona anima vidrio"').replace('class="habito anima"', 'class="habito anima vidrio"') \
                       .replace('class="app anima"', 'class="app anima vidrio"').replace('class="guia anima"', 'class="guia anima vidrio"')
    return (f'<div class="panel" id="{clave}" role="tabpanel" aria-labelledby="tab-{clave}" hidden><div class="panel-fondo">'
            f'<div class="intro-dir"><p><strong>{nombre}.</strong> {texto}</p></div>{cuerpo}</div></div>')


def pagina():
    tabs = ''.join(f'<button type="button" role="tab" id="tab-{c}" aria-controls="{c}" aria-selected="false" tabindex="-1">{n}</button>'
                   for c, n, _ in DIRECCIONES)
    paneles = ''.join(panel(c, n, t) for c, n, t in DIRECCIONES)
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Código Calma · exploración de estilo</title>
<link rel="preload" href="{FUENTES}lora-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style></head>
<body class="d-editorial">
<div class="selector"><div class="selector__in"><p class="selector__marca">Código Calma · exploración de estilo<small>Mismo contenido real, tres direcciones. Elegí una (o qué tomar de cada una).</small></p>
<div class="pestanas" role="tablist" aria-label="Dirección visual">{tabs}</div></div></div>
<main>{paneles}</main>
<script>{JS}</script>
</body></html>
'''


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    (OUT / 'index.html').write_text(pagina(), encoding='utf-8')
    print('exploracion/index.html')
