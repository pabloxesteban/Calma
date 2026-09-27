/**
 * Código Calma — Etapa 7: "tecnología que se comporta como una mente".
 * Dirección de arte: docs/direccion-arte-organismo.md
 *
 * 1. Hero: la flor dentro de una red viva (Canvas 2D). La red crece desde la
 *    flor, se asienta y queda quieta. El puntero (o el dedo) la perturba y
 *    vuelve sola al equilibrio: presencia → perturbación → regulación. Los
 *    nodos tocados se "activan", contagian a sus vecinos y se apagan despacio.
 *    No hay bucle permanente: el dibujo se detiene cuando la red está en calma.
 * 2. Figuras (cifras y seis estados) que se encienden al entrar en pantalla y
 *    al pasar el puntero o el foco. Duran menos de 5 s.
 * 3. Hallazgos de los seis estados como disclosure accesible (botón + región).
 * 4. Láminas: las imágenes de tarjetas fuera de la primera pantalla se
 *    descubren al llegar. El texto nunca se oculta.
 * 5. Tarjetas de artículos con una inclinación mínima que sigue al puntero.
 * 6. Header compacto, barra de lectura y control "Reducir movimiento".
 *
 * Sin JavaScript, con prefers-reduced-motion, en equipos de pocos recursos o
 * con "Reducir movimiento", cada pieza queda en su estado final.
 */
( function () {
	'use strict';

	var raiz = document.documentElement;
	var mqReducir = window.matchMedia ? window.matchMedia( '(prefers-reduced-motion: reduce)' ) : { matches: false };
	var finoHover = window.matchMedia && window.matchMedia( '(hover: hover) and (pointer: fine)' ).matches;
	var raf = window.requestAnimationFrame || function ( fn ) { return setTimeout( fn, 16 ); };
	var CLAVE = 'calma-quieto';

	function leerQuieto() {
		try {
			return window.localStorage.getItem( CLAVE ) === '1';
		} catch ( e ) {
			return false;
		}
	}
	function guardarQuieto( v ) {
		try {
			window.localStorage.setItem( CLAVE, v ? '1' : '0' );
		} catch ( e ) {}
	}
	if ( leerQuieto() ) {
		raiz.classList.add( 'calma-quieto' );
	}
	function quieto() {
		return mqReducir.matches || raiz.classList.contains( 'calma-quieto' );
	}
	var nav = window.navigator || {};
	// Ahorro de datos o memoria mínima: red quieta desde el inicio.
	var pocosRecursos = !! ( ( nav.deviceMemory && nav.deviceMemory <= 1 ) ||
		( nav.connection && nav.connection.saveData ) );
	// Pocos núcleos: menos nodos (y el regulador de cuadros decide el resto).
	var equipoModesto = !! ( ( nav.hardwareConcurrency && nav.hardwareConcurrency <= 2 ) ||
		( nav.deviceMemory && nav.deviceMemory <= 2 ) );

	/* ------------------------------------------------------------------------
	   1. Red viva del hero
	   ------------------------------------------------------------------------ */
	function RedViva( seccion ) {
		var flor = seccion.querySelector( '.calma-hero__media img' );
		if ( ! flor || ! window.HTMLCanvasElement ) {
			return;
		}
		var canvas = document.createElement( 'canvas' );
		canvas.className = 'calma-red';
		canvas.setAttribute( 'aria-hidden', 'true' );
		seccion.insertBefore( canvas, seccion.firstChild );
		var ctx = canvas.getContext( '2d' );
		if ( ! ctx ) {
			return;
		}

		var W = 0, H = 0, DPR = 1, cx = 0, cy = 0, R = 0;
		var nodos = [], aristas = [];
		var puntero = { x: -9999, y: -9999, activo: false };
		var corriendo = false, visible = true, t0 = 0, ultimo = 0;
		var lentos = 0, avisos = 0; // regulador de rendimiento
		var DESPERTAR = 2600; // ms de crecimiento inicial

		function azar( semilla ) {
			// Pseudoaleatorio estable: la red tiene siempre la misma forma.
			var s = semilla;
			return function () {
				s = ( s * 16807 ) % 2147483647;
				return ( s - 1 ) / 2147483646;
			};
		}

		function medir() {
			var r = seccion.getBoundingClientRect();
			var f = flor.getBoundingClientRect();
			DPR = Math.min( window.devicePixelRatio || 1, 1.5 );
			W = r.width;
			H = r.height;
			canvas.width = Math.round( W * DPR );
			canvas.height = Math.round( H * DPR );
			ctx.setTransform( DPR, 0, 0, DPR, 0, 0 );
			cx = f.left - r.left + f.width / 2;
			cy = f.top - r.top + f.height / 2;
			R = f.width * 0.46;
		}

		function construir() {
			var rnd = azar( 20260927 );
			var movil = W < 700;
			var n = movil ? 46 : 110;
			if ( equipoModesto ) {
				n = Math.round( n * 0.7 );
			}
			nodos = [];
			var intentos = 0;
			while ( nodos.length < n && intentos < n * 30 ) {
				intentos++;
				var lejos = rnd() < 0.18;
				var ang = rnd() * Math.PI * 2;
				// Densidad orgánica: más nodos cerca de la flor, algunos sueltos lejos.
				var d = lejos ? R * ( 1.9 + rnd() * 2.6 ) : R * ( 1.08 + Math.pow( rnd(), 0.8 ) * 1.25 );
				var x = cx + Math.cos( ang ) * d * ( movil ? 1.15 : 1.35 );
				var y = cy + Math.sin( ang ) * d;
				if ( x < 4 || x > W - 4 || y < 4 || y > H - 4 ) {
					continue;
				}
				var ok = true;
				for ( var k = 0; k < nodos.length; k++ ) {
					var dx = nodos[ k ].rx - x, dy = nodos[ k ].ry - y;
					if ( dx * dx + dy * dy < 22 * 22 ) {
						ok = false;
						break;
					}
				}
				if ( ! ok ) {
					continue;
				}
				nodos.push( {
					rx: x, ry: y, x: x, y: y, vx: 0, vy: 0,
					r: 1 + rnd() * 1.5, act: 0, fase: rnd() * Math.PI * 2,
					dendrita: d < R * 1.5, vec: []
				} );
			}
			// Cada nodo se une a sus 2–3 vecinos más cercanos: una red, no una nube.
			aristas = [];
			var vistas = {};
			nodos.forEach( function ( a, i ) {
				var orden = nodos.map( function ( b, j ) {
					return { j: j, d: ( b.rx - a.rx ) * ( b.rx - a.rx ) + ( b.ry - a.ry ) * ( b.ry - a.ry ) };
				} ).sort( function ( p, q ) { return p.d - q.d; } );
				var m = 2 + ( i % 3 === 0 ? 1 : 0 );
				for ( var k = 1; k <= m && k < orden.length; k++ ) {
					var j = orden[ k ].j;
					var clave = i < j ? i + '-' + j : j + '-' + i;
					if ( ! vistas[ clave ] && orden[ k ].d < R * R * 1.8 ) {
						vistas[ clave ] = 1;
						aristas.push( [ i, j ] );
						a.vec.push( j );
						nodos[ j ].vec.push( i );
					}
				}
			} );
		}

		function colocarEnReposo() {
			nodos.forEach( function ( p ) {
				p.x = p.rx;
				p.y = p.ry;
				p.vx = p.vy = 0;
				p.act = 0;
			} );
		}

		function colocarEnSemilla() {
			// La red nace de la flor: todos los nodos parten cerca del centro.
			nodos.forEach( function ( p ) {
				p.x = cx + ( p.rx - cx ) * 0.35;
				p.y = cy + ( p.ry - cy ) * 0.35;
				p.vx = p.vy = 0;
			} );
		}

		function dibujar( crecimiento ) {
			ctx.clearRect( 0, 0, W, H );
			var alfa = Math.min( 1, crecimiento );
			// Dendritas: de los nodos cercanos al borde de la flor.
			ctx.lineWidth = 0.7;
			for ( var i = 0; i < nodos.length; i++ ) {
				var p = nodos[ i ];
				if ( ! p.dendrita ) {
					continue;
				}
				var dx = p.x - cx, dy = p.y - cy;
				var dist = Math.sqrt( dx * dx + dy * dy ) || 1;
				var bx = cx + dx / dist * R * 0.82, by = cy + dy / dist * R * 0.82;
				ctx.strokeStyle = 'rgba(29,95,148,' + ( ( 0.12 + p.act * 0.45 ) * alfa ).toFixed( 3 ) + ')';
				ctx.beginPath();
				ctx.moveTo( bx, by );
				ctx.lineTo( p.x, p.y );
				ctx.stroke();
			}
			// Aristas: más visibles donde hay actividad (atención).
			for ( var k = 0; k < aristas.length; k++ ) {
				var a = nodos[ aristas[ k ][ 0 ] ], b = nodos[ aristas[ k ][ 1 ] ];
				var act = ( a.act + b.act ) / 2;
				ctx.strokeStyle = act > 0.02 ?
					'rgba(15,107,107,' + ( ( 0.18 + act * 0.7 ) * alfa ).toFixed( 3 ) + ')' :
					'rgba(29,95,148,' + ( 0.16 * alfa ).toFixed( 3 ) + ')';
				ctx.lineWidth = 0.6 + act * 0.8;
				ctx.beginPath();
				ctx.moveTo( a.x, a.y );
				ctx.lineTo( b.x, b.y );
				ctx.stroke();
			}
			// Nodos.
			for ( var n = 0; n < nodos.length; n++ ) {
				var q = nodos[ n ];
				ctx.fillStyle = q.act > 0.02 ?
					'rgba(15,107,107,' + ( ( 0.55 + q.act * 0.45 ) * alfa ).toFixed( 3 ) + ')' :
					'rgba(29,95,148,' + ( 0.5 * alfa ).toFixed( 3 ) + ')';
				ctx.beginPath();
				ctx.arc( q.x, q.y, q.r + q.act * 1.6, 0, Math.PI * 2 );
				ctx.fill();
				if ( q.act > 0.12 ) {
					// Halo de activación: la "atención" que deja el contacto.
					ctx.strokeStyle = 'rgba(15,107,107,' + ( q.act * 0.35 * alfa ).toFixed( 3 ) + ')';
					ctx.lineWidth = 0.8;
					ctx.beginPath();
					ctx.arc( q.x, q.y, q.r + 3 + q.act * 7, 0, Math.PI * 2 );
					ctx.stroke();
				}
			}
		}

		function paso( ahora ) {
			if ( ! corriendo ) {
				return;
			}
			var dt = ultimo ? Math.min( 48, ahora - ultimo ) : 16;
			ultimo = ahora;
			var edad = ahora - t0;
			// Regulador: si los cuadros son lentos de forma sostenida (no durante
			// la carga), la red se detiene en reposo; a la segunda vez, queda quieta.
			if ( edad > 1200 && dt > 34 ) {
				lentos++;
				if ( lentos > 45 ) {
					lentos = 0;
					avisos++;
					colocarEnReposo();
					dibujar( 1 );
					corriendo = false;
					if ( avisos > 1 ) {
						pocosRecursos = true;
					}
					return;
				}
			} else {
				lentos = Math.max( 0, lentos - 2 );
			}
			var despertando = edad < DESPERTAR;
			var k = despertando ? 0.012 : 0.02; // resorte hacia el reposo
			var amort = 0.86;
			var radio = W < 700 ? 90 : 130;
			var energia = 0;
			var i, p;

			for ( i = 0; i < nodos.length; i++ ) {
				p = nodos[ i ];
				var fx = ( p.rx - p.x ) * k, fy = ( p.ry - p.y ) * k;
				// Respiración que se apaga sola durante el despertar.
				if ( despertando ) {
					var aten = 1 - edad / DESPERTAR;
					fx += Math.cos( ahora / 900 + p.fase ) * 0.05 * aten;
					fy += Math.sin( ahora / 1100 + p.fase ) * 0.05 * aten;
				}
				if ( puntero.activo ) {
					var dx = p.x - puntero.x, dy = p.y - puntero.y;
					var d2 = dx * dx + dy * dy;
					if ( d2 < radio * radio ) {
						var d = Math.sqrt( d2 ) || 1;
						var fuerza = Math.pow( 1 - d / radio, 2 ) * 1.6;
						fx += dx / d * fuerza;
						fy += dy / d * fuerza;
						p.act = Math.min( 1, p.act + fuerza * 0.2 );
					}
				}
				p.vx = ( p.vx + fx ) * amort;
				p.vy = ( p.vy + fy ) * amort;
				p.x += p.vx;
				p.y += p.vy;
				energia += Math.abs( p.vx ) + Math.abs( p.vy ) + Math.abs( p.rx - p.x ) * 0.02 + Math.abs( p.ry - p.y ) * 0.02;
			}
			// Conexión: la activación se contagia a los vecinos y se apaga despacio (memoria).
			for ( i = 0; i < nodos.length; i++ ) {
				p = nodos[ i ];
				var vecina = 0;
				for ( var v = 0; v < p.vec.length; v++ ) {
					vecina = Math.max( vecina, nodos[ p.vec[ v ] ].act );
				}
				// Contagio atenuado (0,45 por salto) y olvido gradual: siempre converge a 0.
				p.act = Math.max( p.act * 0.965, vecina * 0.45 );
				if ( p.act < 0.004 ) {
					p.act = 0;
				}
				energia += p.act;
			}
			dibujar( despertando ? edad / 900 : 1 );
			if ( ! despertando && ! puntero.activo && energia < 0.4 ) {
				colocarEnReposo();
				dibujar( 1 );
				corriendo = false;
				return;
			}
			raf( paso );
		}

		function despertar() {
			if ( corriendo || ! visible || quieto() || pocosRecursos ) {
				return;
			}
			corriendo = true;
			ultimo = 0;
			raf( paso );
		}

		function estatico() {
			corriendo = false;
			colocarEnReposo();
			dibujar( 1 );
		}

		function posicion( ev ) {
			var r = seccion.getBoundingClientRect();
			puntero.x = ev.clientX - r.left;
			puntero.y = ev.clientY - r.top;
		}

		medir();
		construir();
		if ( quieto() || pocosRecursos ) {
			estatico();
		} else {
			colocarEnSemilla();
			t0 = window.performance ? performance.now() : Date.now();
			despertar();
		}
		raf( function () {
			canvas.classList.add( 'is-lista' );
		} );

		seccion.addEventListener( 'pointermove', function ( ev ) {
			posicion( ev );
			puntero.activo = true;
			despertar();
		}, { passive: true } );
		seccion.addEventListener( 'pointerdown', function ( ev ) {
			// En pantallas táctiles, un toque es una onda breve.
			posicion( ev );
			puntero.activo = true;
			despertar();
			if ( ev.pointerType !== 'mouse' ) {
				setTimeout( function () {
					puntero.activo = false;
				}, 260 );
			}
		}, { passive: true } );
		seccion.addEventListener( 'pointerleave', function () {
			puntero.activo = false;
		} );
		// El foco del teclado también "toca" la red, cerca del elemento enfocado.
		seccion.addEventListener( 'focusin', function ( ev ) {
			var r = seccion.getBoundingClientRect();
			var e = ev.target.getBoundingClientRect();
			puntero.x = Math.min( W - 10, e.right - r.left + 40 );
			puntero.y = e.top - r.top + e.height / 2;
			puntero.activo = true;
			despertar();
			setTimeout( function () {
				puntero.activo = false;
			}, 400 );
		} );

		if ( 'IntersectionObserver' in window ) {
			new IntersectionObserver( function ( e ) {
				visible = e[ 0 ].isIntersecting;
				if ( ! visible ) {
					corriendo = false;
				}
			} ).observe( seccion );
		}
		document.addEventListener( 'visibilitychange', function () {
			if ( document.hidden ) {
				corriendo = false;
			}
		} );
		var ancho = W;
		var tResize = null;
		window.addEventListener( 'resize', function () {
			clearTimeout( tResize );
			tResize = setTimeout( function () {
				var r = seccion.getBoundingClientRect();
				if ( Math.abs( r.width - ancho ) < 2 && Math.abs( r.height - H ) < 40 ) {
					return; // barra de direcciones del móvil: no rehacer la red
				}
				ancho = r.width;
				medir();
				construir();
				estatico();
			}, 200 );
		} );
		this.pausar = estatico;
	}

	/* ------------------------------------------------------------------------
	   2. Figuras que se encienden (cifras y estados)
	   ------------------------------------------------------------------------ */
	function encender( el ) {
		if ( quieto() ) {
			return;
		}
		el.classList.remove( 'is-vivo' );
		// Forzar reflow para poder repetir la animación.
		void el.offsetWidth;
		el.classList.add( 'is-vivo' );
		clearTimeout( el._calmaT );
		el._calmaT = setTimeout( function () {
			el.classList.remove( 'is-vivo' );
		}, 4600 );
	}

	function prepararFiguras() {
		var figuras = document.querySelectorAll( '.calma-cifra, .calma-estado' );
		if ( ! figuras.length ) {
			return;
		}
		if ( 'IntersectionObserver' in window ) {
			var io = new IntersectionObserver( function ( entradas ) {
				entradas.forEach( function ( e ) {
					if ( e.isIntersecting ) {
						io.unobserve( e.target );
						var i = Array.prototype.indexOf.call( e.target.parentElement.children, e.target );
						setTimeout( function () {
							encender( e.target );
						}, Math.min( i, 5 ) * 140 );
					}
				} );
			}, { threshold: 0.45 } );
			figuras.forEach( function ( f ) {
				io.observe( f );
			} );
		}
		document.querySelectorAll( '.calma-estado' ).forEach( function ( f ) {
			var ultimo = 0;
			function otraVez() {
				var ahora = Date.now();
				if ( ahora - ultimo > 5000 ) {
					ultimo = ahora;
					encender( f );
				}
			}
			if ( finoHover ) {
				f.addEventListener( 'pointerenter', otraVez );
			}
			f.addEventListener( 'focusin', otraVez );
		} );
	}

	/* ------------------------------------------------------------------------
	   3. Hallazgos: disclosure accesible
	   ------------------------------------------------------------------------ */
	function prepararHallazgos() {
		document.querySelectorAll( '.calma-estado' ).forEach( function ( tarjeta ) {
			var boton = tarjeta.querySelector( '.calma-estado__abrir' );
			var panel = tarjeta.querySelector( '.calma-estado__hallazgo' );
			if ( ! boton || ! panel ) {
				return;
			}
			boton.hidden = false;
			function poner( abierto ) {
				boton.setAttribute( 'aria-expanded', abierto ? 'true' : 'false' );
				boton.firstChild.nodeValue = abierto ? 'Ocultar el hallazgo' : 'Ver el hallazgo';
				tarjeta.classList.toggle( 'is-cerrado', ! abierto );
				tarjeta.classList.toggle( 'is-abierto', abierto );
			}
			poner( false );
			boton.addEventListener( 'click', function () {
				var abrir = boton.getAttribute( 'aria-expanded' ) !== 'true';
				poner( abrir );
				if ( abrir ) {
					encender( tarjeta );
				}
			} );
		} );
	}

	/* ------------------------------------------------------------------------
	   4. Láminas: imágenes de tarjetas que se descubren al llegar
	   ------------------------------------------------------------------------ */
	function prepararLaminas() {
		if ( quieto() || ! ( 'IntersectionObserver' in window ) ) {
			return;
		}
		var limite = window.innerHeight * 0.95;
		var io = new IntersectionObserver( function ( entradas ) {
			entradas.forEach( function ( e ) {
				if ( e.isIntersecting ) {
					io.unobserve( e.target );
					e.target.classList.add( 'is-visto' );
				}
			} );
		}, { threshold: 0.25 } );
		document.querySelectorAll( '.loop-entry .post-thumbnail, .kb-row-layout-id1204_6c7f8b-e0 .kb-is-ratio-image' ).forEach( function ( el ) {
			if ( el.getBoundingClientRect().top < limite ) {
				return;
			}
			var item = el.closest( 'li, .wp-block-kadence-column' );
			var i = item && item.parentElement ? Array.prototype.indexOf.call( item.parentElement.children, item ) % 3 : 0;
			el.style.setProperty( '--calma-delay', ( i * 0.12 ).toFixed( 2 ) + 's' );
			el.classList.add( 'calma-lamina' );
			io.observe( el );
		} );
	}

	/* ------------------------------------------------------------------------
	   5. Tarjetas de artículos: inclinación mínima (máx. 1,5°)
	   ------------------------------------------------------------------------ */
	function prepararTarjetas() {
		if ( ! finoHover ) {
			return;
		}
		document.querySelectorAll( '.loop-entry' ).forEach( function ( t ) {
			var pendiente = null;
			t.addEventListener( 'pointermove', function ( ev ) {
				if ( quieto() || pendiente ) {
					return;
				}
				pendiente = raf( function () {
					pendiente = null;
					var r = t.getBoundingClientRect();
					var x = ( ev.clientX - r.left ) / r.width - 0.5;
					var y = ( ev.clientY - r.top ) / r.height - 0.5;
					t.style.setProperty( '--calma-tx', ( x * 3 ).toFixed( 2 ) );
					t.style.setProperty( '--calma-ty', ( y * -3 ).toFixed( 2 ) );
				} );
			} );
			t.addEventListener( 'pointerleave', function () {
				t.style.setProperty( '--calma-tx', 0 );
				t.style.setProperty( '--calma-ty', 0 );
			} );
		} );
	}

	/* ------------------------------------------------------------------------
	   6. Header, barra de lectura y "Reducir movimiento"
	   ------------------------------------------------------------------------ */
	var progreso = null;
	var ticking = false;
	function onScroll() {
		if ( ticking ) {
			return;
		}
		ticking = true;
		raf( function () {
			var y = window.scrollY || window.pageYOffset;
			document.body.classList.toggle( 'calma-scrolled', y > 12 );
			if ( progreso ) {
				var alto = raiz.scrollHeight - window.innerHeight;
				progreso.style.setProperty( '--calma-read', alto > 0 ? Math.min( 1, y / alto ).toFixed( 4 ) : 0 );
			}
			ticking = false;
		} );
	}

	function prepararControl( red ) {
		var pie = document.querySelector( '.site-footer' );
		if ( ! pie || mqReducir.matches ) {
			return; // Si el sistema ya pide menos movimiento, no hace falta el control.
		}
		var envoltura = document.createElement( 'div' );
		envoltura.className = 'calma-quieto-wrap';
		var b = document.createElement( 'button' );
		b.type = 'button';
		b.className = 'calma-quieto-toggle';
		b.textContent = 'Reducir movimiento';
		b.setAttribute( 'aria-pressed', raiz.classList.contains( 'calma-quieto' ) ? 'true' : 'false' );
		b.addEventListener( 'click', function () {
			var activo = ! raiz.classList.contains( 'calma-quieto' );
			raiz.classList.toggle( 'calma-quieto', activo );
			b.setAttribute( 'aria-pressed', activo ? 'true' : 'false' );
			guardarQuieto( activo );
			if ( activo && red && red.pausar ) {
				red.pausar();
			}
		} );
		envoltura.appendChild( b );
		pie.appendChild( envoltura );
	}

	function iniciar() {
		if ( document.body.classList.contains( 'single-post' ) ) {
			progreso = document.createElement( 'div' );
			progreso.className = 'calma-progress';
			progreso.setAttribute( 'aria-hidden', 'true' );
			document.body.appendChild( progreso );
		}
		window.addEventListener( 'scroll', onScroll, { passive: true } );
		onScroll();
		prepararHallazgos();
		prepararLaminas();
		prepararFiguras();
		prepararTarjetas();

		var hero = document.querySelector( '.calma-hero' );
		var red = null;
		function arrancarRed() {
			if ( hero && hero.querySelector( '.calma-hero__media img' ) ) {
				red = new RedViva( hero );
			}
			prepararControl( red );
		}
		// La red arranca después del contenido principal (no compite con el LCP).
		if ( 'requestIdleCallback' in window ) {
			window.requestIdleCallback( arrancarRed, { timeout: 1200 } );
		} else {
			setTimeout( arrancarRed, 300 );
		}
	}

	if ( document.readyState === 'loading' ) {
		document.addEventListener( 'DOMContentLoaded', iniciar );
	} else {
		iniciar();
	}
}() );
