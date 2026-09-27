/**
 * Código Calma — Etapa 7: "tecnología que se comporta como una mente".
 * Dirección de arte: docs/direccion-arte-organismo.md
 *
 * 1. Hero: la flor dentro de una red viva y suelta (Canvas 2D). Los nodos
 *    aparecen y se conectan, la red respira unos segundos y queda quieta.
 *    Pasar sobre la flor emite una onda que recorre la red. El puntero (o el dedo) la perturba y
 *    vuelve sola al equilibrio: presencia → perturbación → regulación. Los
 *    nodos tocados se "activan", contagian a sus vecinos y se apagan despacio.
 *    No hay bucle permanente: el dibujo se detiene cuando la red está en calma.
 * 2. Figuras (cifras y seis estados) que se encienden al entrar en pantalla y
 *    al pasar el puntero o el foco. Duran menos de 5 s.
 * 3. Hallazgos de los seis estados como disclosure accesible (botón + región).
 * 4. Láminas: las imágenes de tarjetas fuera de la primera pantalla se
 *    descubren al llegar. El texto nunca se oculta.
 * 5. Línea de tiempo: la línea crece con el scroll, las épocas se encienden
 *    y una figura se transforma (objeto → red → dispositivo → plataforma →
 *    inteligencia). El scroll siempre es nativo.
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
	   Una red suelta que ocupa todo el sector de la flor: nodos de tamaños y
	   brillos distintos, uniones curvas e irregulares y algunos nodos sin
	   conexión. Al cargar, los nodos aparecen uno a uno y las uniones se
	   dibujan entre ellos (conexión, no zoom). Respira unos segundos y se queda
	   quieta. Pasar sobre la flor emite una onda que recorre la red.
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

		var W = 0, H = 0, DPR = 1, cx = 0, cy = 0, R = 0, movil = false;
		var nodos = [], aristas = [];
		var puntero = { x: -9999, y: -9999, activo: false };
		var onda = null; // { t0, max }
		var corriendo = false, visible = true, t0 = 0, ultimo = 0, vigilia = 0;
		var lentos = 0, avisos = 0; // regulador de rendimiento
		var DESPERTAR = 4200; // ms: aparición + respiración que se apaga (< 5 s)
		var RESPIRO = 2600; // ms de respiración después de cada interacción

		function azar( semilla ) {
			// Pseudoaleatorio estable: la red tiene siempre la misma forma.
			var s = semilla;
			return function () {
				s = ( s * 16807 ) % 2147483647;
				return ( s - 1 ) / 2147483646;
			};
		}
		function suave( x ) {
			x = Math.max( 0, Math.min( 1, x ) );
			return x * x * ( 3 - 2 * x );
		}
		function ahoraMs() {
			return window.performance ? performance.now() : Date.now();
		}

		function medir() {
			var r = seccion.getBoundingClientRect();
			var f = flor.getBoundingClientRect();
			DPR = Math.min( window.devicePixelRatio || 1, 1.5 );
			W = r.width;
			H = r.height;
			movil = W < 900;
			canvas.width = Math.round( W * DPR );
			canvas.height = Math.round( H * DPR );
			ctx.setTransform( DPR, 0, 0, DPR, 0, 0 );
			cx = f.left - r.left + f.width / 2;
			cy = f.top - r.top + f.height / 2;
			R = f.width * 0.46;
		}

		function construir() {
			var rnd = azar( 20260927 );
			var objetivo = movil ? 64 : 150;
			if ( equipoModesto ) {
				objetivo = Math.round( objetivo * 0.7 );
			}
			var minDist = movil ? 24 : 30;
			// Sector de la flor: la mitad derecha en escritorio, la parte baja en celular.
			var x0 = movil ? 0 : W * 0.4, y0 = movil ? H * 0.42 : 0;
			nodos = [];
			var intentos = 0;
			while ( nodos.length < objetivo && intentos < objetivo * 60 ) {
				intentos++;
				var x = x0 + rnd() * ( W - x0 ), y = y0 + rnd() * ( H - y0 );
				var dx = x - cx, dy = y - cy;
				var d = Math.sqrt( dx * dx + dy * dy );
				if ( d < R * 0.8 ) {
					continue; // detrás de la flor no se ve
				}
				// Más densa cerca de la flor, suelta hacia los bordes.
				var densidad = 0.28 + 0.72 * Math.exp( -Math.pow( d / ( R * 2.6 ), 2 ) );
				if ( rnd() > densidad ) {
					continue;
				}
				var libre = true;
				for ( var k = 0; k < nodos.length; k++ ) {
					var ex = nodos[ k ].rx - x, ey = nodos[ k ].ry - y;
					if ( ex * ex + ey * ey < minDist * minDist ) {
						libre = false;
						break;
					}
				}
				if ( ! libre ) {
					continue;
				}
				var t = rnd();
				nodos.push( {
					rx: x, ry: y, x: x, y: y, vx: 0, vy: 0,
					r: 0.7 + t * t * 2.2, // la mayoría chicos, algunos más grandes
					brillo: 0.35 + rnd() * 0.5,
					act: 0,
					fase: rnd() * Math.PI * 2,
					amp: 2 + rnd() * 6,
					vel: 0.6 + rnd() * 0.8,
					aparece: 200 + rnd() * 1500 + Math.min( 1, d / ( R * 4 ) ) * 500,
					dist: d,
					dendrita: d < R * 1.9 && rnd() < 0.55,
					curva: ( rnd() - 0.5 ) * 0.5,
					vec: []
				} );
			}
			// Uniones irregulares: cada nodo busca entre 0 y 4 vecinos cercanos.
			aristas = [];
			var alcance = movil ? 78 : 96;
			var vistas = {};
			nodos.forEach( function ( a, i ) {
				var grado = Math.floor( rnd() * rnd() * 5 ); // muchos con 0–1, pocos con 3–4
				var cerca = [];
				nodos.forEach( function ( b, j ) {
					if ( j === i ) {
						return;
					}
					var d2 = ( b.rx - a.rx ) * ( b.rx - a.rx ) + ( b.ry - a.ry ) * ( b.ry - a.ry );
					if ( d2 < alcance * alcance ) {
						cerca.push( { j: j, d: d2 } );
					}
				} );
				cerca.sort( function ( p, q ) { return p.d - q.d; } );
				for ( var k = 0; k < cerca.length && grado > 0; k++ ) {
					if ( rnd() < 0.3 ) {
						continue; // saltea algunos: menos estructura
					}
					var j = cerca[ k ].j;
					var clave = i < j ? i + '-' + j : j + '-' + i;
					if ( ! vistas[ clave ] ) {
						vistas[ clave ] = 1;
						aristas.push( { a: i, b: j, curva: ( rnd() - 0.5 ) * 0.7, alfa: 0.45 + rnd() * 0.55 } );
						a.vec.push( j );
						nodos[ j ].vec.push( i );
						grado--;
					}
				}
			} );
		}

		function enReposo() {
			nodos.forEach( function ( p ) {
				p.x = p.rx;
				p.y = p.ry;
				p.vx = p.vy = 0;
				p.act = 0;
			} );
			onda = null;
		}

		// Curva cuadrática desde a hacia b, dibujada hasta la fracción g.
		function curva( ax, ay, bx, by, k, g ) {
			var mx = ( ax + bx ) / 2 - ( by - ay ) * k;
			var my = ( ay + by ) / 2 + ( bx - ax ) * k;
			ctx.beginPath();
			ctx.moveTo( ax, ay );
			if ( g >= 1 ) {
				ctx.quadraticCurveTo( mx, my, bx, by );
			} else {
				var q1x = ax + ( mx - ax ) * g, q1y = ay + ( my - ay ) * g;
				var q2x = q1x + ( ( mx + ( bx - mx ) * g ) - q1x ) * g;
				var q2y = q1y + ( ( my + ( by - my ) * g ) - q1y ) * g;
				ctx.quadraticCurveTo( q1x, q1y, q2x, q2y );
			}
			ctx.stroke();
		}

		function dibujar( edad ) {
			ctx.clearRect( 0, 0, W, H );
			var i, p, vis;
			// Dendritas: del borde de la flor a algunos nodos cercanos.
			for ( i = 0; i < nodos.length; i++ ) {
				p = nodos[ i ];
				if ( ! p.dendrita ) {
					continue;
				}
				vis = suave( ( edad - p.aparece ) / 800 );
				if ( vis <= 0 ) {
					continue;
				}
				var dx = p.x - cx, dy = p.y - cy;
				var dist = Math.sqrt( dx * dx + dy * dy ) || 1;
				ctx.strokeStyle = 'rgba(29,95,148,' + ( ( 0.1 + p.act * 0.5 ) * vis ).toFixed( 3 ) + ')';
				ctx.lineWidth = 0.6 + p.act * 0.6;
				curva( cx + dx / dist * R * 0.82, cy + dy / dist * R * 0.82, p.x, p.y, p.curva, vis );
			}
			// Uniones: se dibujan de un nodo al otro cuando ambos aparecieron.
			for ( i = 0; i < aristas.length; i++ ) {
				var e = aristas[ i ], a = nodos[ e.a ], b = nodos[ e.b ];
				var g = suave( ( edad - Math.max( a.aparece, b.aparece ) ) / 700 );
				if ( g <= 0 ) {
					continue;
				}
				var act = Math.max( a.act, b.act ) * 0.8 + Math.min( a.act, b.act ) * 0.2;
				ctx.strokeStyle = act > 0.03 ?
					'rgba(15,107,107,' + ( 0.14 + act * 0.6 ).toFixed( 3 ) + ')' :
					'rgba(29,95,148,' + ( 0.22 * e.alfa ).toFixed( 3 ) + ')';
				ctx.lineWidth = 0.55 + act * 0.8;
				curva( a.x, a.y, b.x, b.y, e.curva, g );
			}
			// Nodos.
			for ( i = 0; i < nodos.length; i++ ) {
				p = nodos[ i ];
				vis = suave( ( edad - p.aparece ) / 600 );
				if ( vis <= 0 ) {
					continue;
				}
				ctx.fillStyle = p.act > 0.03 ?
					'rgba(15,107,107,' + ( ( 0.55 + p.act * 0.45 ) * vis ).toFixed( 3 ) + ')' :
					'rgba(29,95,148,' + ( p.brillo * vis ).toFixed( 3 ) + ')';
				ctx.beginPath();
				ctx.arc( p.x, p.y, p.r + p.act * 1.8, 0, Math.PI * 2 );
				ctx.fill();
				if ( p.act > 0.12 ) {
					// Halo de activación: la "atención" que deja el contacto.
					ctx.strokeStyle = 'rgba(15,107,107,' + ( p.act * 0.35 ).toFixed( 3 ) + ')';
					ctx.lineWidth = 0.8;
					ctx.beginPath();
					ctx.arc( p.x, p.y, p.r + 3 + p.act * 7, 0, Math.PI * 2 );
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
			// Regulador: cuadros lentos sostenidos (no durante la carga) → reposo;
			// a la segunda vez, la red queda quieta.
			if ( edad > 1200 && dt > 34 ) {
				if ( ++lentos > 45 ) {
					lentos = 0;
					if ( ++avisos > 1 ) {
						pocosRecursos = true;
					}
					detener();
					return;
				}
			} else {
				lentos = Math.max( 0, lentos - 2 );
			}
			// Respiración: amplitud que se apaga sola (al cargar y tras cada interacción).
			var respira = Math.max( 1 - edad / DESPERTAR, 1 - ( ahora - vigilia ) / RESPIRO, 0 );
			respira = respira * respira;
			var radio = movil ? 90 : 140;
			var radioOnda = onda ? ( ahora - onda.t0 ) / 1500 * onda.max : -1;
			if ( onda && radioOnda > onda.max + 40 ) {
				onda = null;
			}
			var energia = 0, i, p;
			for ( i = 0; i < nodos.length; i++ ) {
				p = nodos[ i ];
				var ox = Math.cos( ahora / 1000 * p.vel + p.fase ) * p.amp * respira;
				var oy = Math.sin( ahora / 1300 * p.vel + p.fase * 1.3 ) * p.amp * respira;
				var fx = ( p.rx + ox - p.x ) * 0.02, fy = ( p.ry + oy - p.y ) * 0.02;
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
				if ( radioOnda > 0 && Math.abs( p.dist - radioOnda ) < 26 ) {
					// La onda de la flor: empuja apenas hacia afuera y enciende.
					var ux = ( p.x - cx ) / ( p.dist || 1 ), uy = ( p.y - cy ) / ( p.dist || 1 );
					fx += ux * 0.5;
					fy += uy * 0.5;
					p.act = Math.max( p.act, 0.85 * ( 1 - radioOnda / ( onda.max + 40 ) ) + 0.15 );
				}
				p.vx = ( p.vx + fx ) * 0.86;
				p.vy = ( p.vy + fy ) * 0.86;
				p.x += p.vx;
				p.y += p.vy;
				energia += Math.abs( p.vx ) + Math.abs( p.vy );
			}
			// Conexión: la activación se contagia (0,45 por salto) y se olvida despacio.
			for ( i = 0; i < nodos.length; i++ ) {
				p = nodos[ i ];
				var vecina = 0;
				for ( var v = 0; v < p.vec.length; v++ ) {
					vecina = Math.max( vecina, nodos[ p.vec[ v ] ].act );
				}
				p.act = Math.max( p.act * 0.965, vecina * 0.45 );
				if ( p.act < 0.004 ) {
					p.act = 0;
				}
				energia += p.act;
			}
			dibujar( edad );
			if ( respira === 0 && ! puntero.activo && ! onda && energia < 0.4 ) {
				detener();
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

		function detener() {
			corriendo = false;
			enReposo();
			dibujar( 1e9 );
		}

		function tocar( x, y ) {
			puntero.x = x;
			puntero.y = y;
			puntero.activo = true;
			vigilia = ahoraMs();
			despertar();
		}

		function emitirOnda() {
			if ( quieto() || pocosRecursos ) {
				return;
			}
			var t = ahoraMs();
			if ( onda && t - onda.t0 < 1200 ) {
				return;
			}
			onda = { t0: t, max: Math.max( W - cx, cx, H ) };
			vigilia = t;
			despertar();
		}

		function posicion( ev ) {
			var r = seccion.getBoundingClientRect();
			return { x: ev.clientX - r.left, y: ev.clientY - r.top };
		}

		medir();
		construir();
		if ( quieto() || pocosRecursos ) {
			detener();
		} else {
			t0 = ahoraMs();
			despertar();
		}
		raf( function () {
			canvas.classList.add( 'is-lista' );
		} );

		seccion.addEventListener( 'pointermove', function ( ev ) {
			var q = posicion( ev );
			tocar( q.x, q.y );
		}, { passive: true } );
		seccion.addEventListener( 'pointerdown', function ( ev ) {
			var q = posicion( ev );
			tocar( q.x, q.y );
			if ( ev.pointerType !== 'mouse' ) {
				// En pantallas táctiles, un toque es una perturbación breve.
				setTimeout( function () {
					puntero.activo = false;
				}, 260 );
			}
		}, { passive: true } );
		seccion.addEventListener( 'pointerleave', function () {
			puntero.activo = false;
		} );
		// La flor: al pasar (o tocarla) gira despacio y emite una onda por la red.
		flor.addEventListener( 'pointerenter', emitirOnda );
		flor.addEventListener( 'pointerdown', function () {
			emitirOnda();
			seccion.classList.add( 'is-flor-activa' );
			setTimeout( function () {
				seccion.classList.remove( 'is-flor-activa' );
			}, 1800 );
		}, { passive: true } );
		// El foco del teclado también "toca" la red, cerca del elemento enfocado.
		seccion.addEventListener( 'focusin', function ( ev ) {
			var r = seccion.getBoundingClientRect();
			var e = ev.target.getBoundingClientRect();
			tocar( Math.min( W - 10, e.right - r.left + 40 ), e.top - r.top + e.height / 2 );
			setTimeout( function () {
				puntero.activo = false;
			}, 400 );
		} );

		if ( 'IntersectionObserver' in window ) {
			new IntersectionObserver( function ( e ) {
				visible = e[ 0 ].isIntersecting;
				if ( ! visible && corriendo ) {
					detener();
				}
			} ).observe( seccion );
		}
		document.addEventListener( 'visibilitychange', function () {
			if ( document.hidden && corriendo ) {
				detener();
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
				detener();
			}, 200 );
		} );
		this.pausar = detener;
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
	   5. Línea de tiempo: la línea crece con el scroll (nativo), cada época se
	   enciende cuando la línea la alcanza y, en escritorio, una figura hecha
	   de los mismos 40 nodos se transforma: objeto → red → dispositivo →
	   plataforma → inteligencia. Solo se redibuja cuando cambia el scroll.
	   ------------------------------------------------------------------------ */
	var N_FORMA = 40;

	function formas() {
		var F = {}, i, t;
		function perimetro( pts, n ) {
			// Reparte n puntos a lo largo de un polígono cerrado.
			var largos = [], total = 0, out = [];
			for ( i = 0; i < pts.length; i++ ) {
				var a = pts[ i ], b = pts[ ( i + 1 ) % pts.length ];
				var l = Math.hypot( b[ 0 ] - a[ 0 ], b[ 1 ] - a[ 1 ] );
				largos.push( l );
				total += l;
			}
			for ( var k = 0; k < n; k++ ) {
				var d = total * k / n, s = 0;
				for ( i = 0; i < pts.length; i++ ) {
					if ( d <= s + largos[ i ] ) {
						var f = ( d - s ) / largos[ i ], p = pts[ i ], q = pts[ ( i + 1 ) % pts.length ];
						out.push( [ p[ 0 ] + ( q[ 0 ] - p[ 0 ] ) * f, p[ 1 ] + ( q[ 1 ] - p[ 1 ] ) * f ] );
						break;
					}
					s += largos[ i ];
				}
			}
			return out;
		}
		function linea( a, b, n ) {
			var out = [];
			for ( var k = 0; k < n; k++ ) {
				t = n === 1 ? 0.5 : k / ( n - 1 );
				out.push( [ a[ 0 ] + ( b[ 0 ] - a[ 0 ] ) * t, a[ 1 ] + ( b[ 1 ] - a[ 1 ] ) * t ] );
			}
			return out;
		}
		var rnd = ( function () {
			var s = 1975;
			return function () {
				s = ( s * 16807 ) % 2147483647;
				return ( s - 1 ) / 2147483646;
			};
		}() );

		// Objeto: la computadora personal (pantalla, pie y base).
		F.objeto = { u: 0.25, p: perimetro( [ [ -0.8, -0.7 ], [ 0.8, -0.7 ], [ 0.8, 0.25 ], [ -0.8, 0.25 ] ], 26 )
			.concat( linea( [ 0, 0.32 ], [ 0, 0.5 ], 3 ) ).concat( linea( [ -0.5, 0.6 ], [ 0.5, 0.6 ], 11 ) ) };
		// Red: un globo de nodos conectados.
		var red = perimetro( [ [ 0, -0.85 ], [ 0.6, -0.6 ], [ 0.85, 0 ], [ 0.6, 0.6 ], [ 0, 0.85 ], [ -0.6, 0.6 ], [ -0.85, 0 ], [ -0.6, -0.6 ] ], 16 );
		for ( i = 0; i < 24; i++ ) {
			var ang = rnd() * Math.PI * 2, rr = Math.sqrt( rnd() ) * 0.72;
			red.push( [ Math.cos( ang ) * rr, Math.sin( ang ) * rr ] );
		}
		F.red = { u: 0.42, p: red };
		// Dispositivo: el teléfono (contorno, parlante y botón).
		F.dispositivo = { u: 0.2, p: perimetro( [ [ -0.42, -0.88 ], [ 0.42, -0.88 ], [ 0.42, 0.88 ], [ -0.42, 0.88 ] ], 34 )
			.concat( linea( [ -0.1, -0.74 ], [ 0.1, -0.74 ], 3 ) ).concat( [ [ -0.05, 0.72 ], [ 0.05, 0.72 ], [ 0, 0.66 ] ] ) };
		// Plataforma: capas apiladas y nodos que flotan encima.
		var capas = [];
		[ -0.2, 0.2, 0.6 ].forEach( function ( y ) {
			capas = capas.concat( perimetro( [ [ -0.8, y ], [ 0, y - 0.3 ], [ 0.8, y ], [ 0, y + 0.3 ] ], 12 ) );
		} );
		F.plataforma = { u: 0.33, p: capas.concat( [ [ -0.45, -0.8 ], [ 0.45, -0.8 ], [ 0, -0.95 ], [ 0.12, -0.68 ] ] ) };
		// Inteligencia: un tejido orgánico (filotaxis con irregularidad).
		var ia = [];
		for ( i = 0; i < N_FORMA; i++ ) {
			var r = 0.88 * Math.sqrt( ( i + 0.5 ) / N_FORMA ), a2 = i * 2.39996;
			ia.push( [ Math.cos( a2 ) * r * 1.05 + ( rnd() - 0.5 ) * 0.08, Math.sin( a2 ) * r * 0.9 + ( rnd() - 0.5 ) * 0.08 ] );
		}
		F.inteligencia = { u: 0.36, p: ia };

		// Mismo orden angular en todas: la transformación gira, no se desarma.
		Object.keys( F ).forEach( function ( k ) {
			F[ k ].p.sort( function ( a, b ) { return Math.atan2( a[ 1 ], a[ 0 ] ) - Math.atan2( b[ 1 ], b[ 0 ] ); } );
		} );
		return F;
	}

	function prepararTiempo() {
		var seccion = document.querySelector( '.calma-tiempo' );
		if ( ! seccion ) {
			return;
		}
		var lista = seccion.querySelector( '.calma-tiempo__lista' );
		var epocas = Array.prototype.slice.call( seccion.querySelectorAll( '.calma-tiempo__epoca' ) );
		var figura = seccion.querySelector( '.calma-tiempo__figura' );
		var rotulo = seccion.querySelector( '.calma-tiempo__rotulo' );
		if ( ! lista || ! epocas.length ) {
			return;
		}
		var F = formas();
		var claves = epocas.map( function ( e ) { return e.getAttribute( 'data-forma' ); } );
		var canvas = null, ctx = null, lado = 0, DPR = 1, ultimoF = -1, pendiente = false;

		if ( figura && window.HTMLCanvasElement ) {
			figura.hidden = false;
			canvas = document.createElement( 'canvas' );
			figura.querySelector( '.calma-tiempo__lienzo' ).appendChild( canvas );
			ctx = canvas.getContext( '2d' );
		}

		function medirLienzo() {
			if ( ! canvas ) {
				return;
			}
			lado = canvas.parentNode.getBoundingClientRect().width;
			DPR = Math.min( window.devicePixelRatio || 1, 1.5 );
			canvas.width = Math.round( lado * DPR );
			canvas.height = Math.round( lado * DPR );
			ctx.setTransform( DPR, 0, 0, DPR, 0, 0 );
			ultimoF = -1;
		}

		function dibujarForma( f ) {
			if ( ! ctx || ! lado ) {
				return;
			}
			var i0 = Math.max( 0, Math.min( claves.length - 1, Math.floor( f ) ) );
			var i1 = Math.min( claves.length - 1, i0 + 1 );
			var t = f - i0;
			t = t * t * ( 3 - 2 * t );
			var A = F[ claves[ i0 ] ], B = F[ claves[ i1 ] ];
			var umbral = A.u + ( B.u - A.u ) * t;
			var escala = lado * 0.4, c = lado / 2;
			var pts = [];
			for ( var k = 0; k < N_FORMA; k++ ) {
				var a = A.p[ k ], b = B.p[ k ];
				// Un leve desvío durante el cambio: la forma "piensa" antes de llegar.
				var desvio = Math.sin( t * Math.PI ) * 0.12 * Math.sin( k * 1.7 );
				pts.push( [ ( a[ 0 ] + ( b[ 0 ] - a[ 0 ] ) * t + desvio ), ( a[ 1 ] + ( b[ 1 ] - a[ 1 ] ) * t - desvio * 0.6 ) ] );
			}
			// Cerca de una época la figura se "enciende" (verde azulado).
			var llegada = 1 - Math.sin( t * Math.PI );
			ctx.clearRect( 0, 0, lado, lado );
			ctx.lineWidth = 1;
			for ( var i = 0; i < N_FORMA; i++ ) {
				for ( var j = i + 1; j < N_FORMA; j++ ) {
					var dx = pts[ i ][ 0 ] - pts[ j ][ 0 ], dy = pts[ i ][ 1 ] - pts[ j ][ 1 ];
					var d = Math.sqrt( dx * dx + dy * dy );
					if ( d < umbral ) {
						var al = ( 1 - d / umbral ) * 0.8 + 0.12;
						ctx.strokeStyle = 'rgba(' + ( llegada > 0.6 ? '15,107,107,' : '29,95,148,' ) + al.toFixed( 3 ) + ')';
						ctx.beginPath();
						ctx.moveTo( c + pts[ i ][ 0 ] * escala, c + pts[ i ][ 1 ] * escala );
						ctx.lineTo( c + pts[ j ][ 0 ] * escala, c + pts[ j ][ 1 ] * escala );
						ctx.stroke();
					}
				}
			}
			ctx.fillStyle = llegada > 0.6 ? '#0f6b6b' : '#1d5f94';
			for ( var n = 0; n < N_FORMA; n++ ) {
				ctx.beginPath();
				ctx.arc( c + pts[ n ][ 0 ] * escala, c + pts[ n ][ 1 ] * escala, 2.4, 0, Math.PI * 2 );
				ctx.fill();
			}
			if ( rotulo ) {
				rotulo.textContent = 'Fig. ' + ( '0' + ( Math.round( f ) + 1 ) ).slice( -2 ) + ' — ' + epocas[ Math.round( f ) ].getAttribute( 'data-concepto' );
			}
		}

		function actualizar() {
			pendiente = false;
			var r = lista.getBoundingClientRect();
			var alto = Math.max( 1, r.height - 40 );
			var ref = window.innerHeight * 0.62;
			var p = Math.max( 0, Math.min( 1, ( ref - r.top - 20 ) / alto ) );
			var yLinea = p * alto;
			var vivo = ! quieto();
			seccion.classList.toggle( 'is-vivo', vivo );
			seccion.style.setProperty( '--calma-tiempo-p', vivo ? p.toFixed( 4 ) : 1 );
			var ys = epocas.map( function ( e ) { return e.offsetTop; } );
			var actual = -1;
			epocas.forEach( function ( e, i ) {
				var encendida = ys[ i ] <= yLinea + 1;
				e.classList.toggle( 'is-encendida', encendida );
				if ( encendida ) {
					actual = i;
				}
			} );
			epocas.forEach( function ( e, i ) {
				e.classList.toggle( 'is-actual', vivo && i === actual );
			} );
			// Posición continua de la figura entre épocas.
			var f = 0;
			for ( var i = 0; i < ys.length - 1; i++ ) {
				if ( yLinea >= ys[ i ] ) {
					f = i + Math.min( 1, ( yLinea - ys[ i ] ) / ( ys[ i + 1 ] - ys[ i ] ) );
				}
			}
			if ( yLinea >= ys[ ys.length - 1 ] ) {
				f = ys.length - 1;
			}
			if ( ! vivo ) {
				f = Math.max( 0, actual ); // sin movimiento: cambios de estado, sin transición
			}
			if ( Math.abs( f - ultimoF ) > 0.002 ) {
				ultimoF = f;
				dibujarForma( f );
			}
		}

		function pedir() {
			if ( ! pendiente ) {
				pendiente = true;
				raf( actualizar );
			}
		}

		medirLienzo();
		actualizar();
		window.addEventListener( 'scroll', pedir, { passive: true } );
		window.addEventListener( 'resize', function () {
			medirLienzo();
			pedir();
		} );
		raiz.addEventListener( 'calma-quieto', pedir );
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
			raiz.dispatchEvent( new Event( 'calma-quieto' ) );
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
		prepararTiempo();

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
