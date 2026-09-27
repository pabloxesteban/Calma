/**
 * Código Calma — Etapa 7: "tecnología que se comporta como una mente".
 * Dirección de arte: docs/direccion-arte-organismo.md
 *
 * 1. Hero: la flor como núcleo de un circuito (Canvas 2D). Las pistas crecen
 *    desde la flor y por ellas viajan señales: hacia afuera al cargar y al
 *    pasar sobre la flor, hacia la flor cuando el puntero se acerca a un
 *    nodo. La red no se deforma. La flor gira despacio con el scroll. El puntero (o el dedo) la perturba y
 *    vuelve sola al equilibrio: presencia → perturbación → regulación. Los
 *    nodos tocados se "activan", contagian a sus vecinos y se apagan despacio.
 *    No hay bucle permanente: el dibujo se detiene cuando la red está en calma.
 * 2. Figuras (cifras y seis estados) que se encienden al entrar en pantalla y
 *    al pasar el puntero o el foco. Duran menos de 5 s.
 * 3. Seis estados como tarjetas que se dan vuelta: toda la cara es clicable,
 *    el botón "Dar vuelta" es el control accesible y la cara oculta queda inert.
 * 4. Láminas: las imágenes de tarjetas fuera de la primera pantalla se
 *    descubren al llegar. El texto nunca se oculta.
 * 5. Línea de tiempo: la línea crece con el scroll, las épocas se encienden
 *    y una figura de puntos (cada punto, una persona) muestra cómo la
 *    tecnología las fue conectando en cada época. El scroll siempre es nativo.
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
	   1. Hero: la flor como núcleo de un circuito
	   Las pistas de circuito de los pétalos se prolongan hacia afuera en rutas
	   a 45° (como una placa) que terminan en nodos. Por esas pistas viajan
	   señales: al cargar, de la flor hacia afuera (la mente se conecta con el
	   mundo); al acercar el puntero a un nodo, del nodo hacia la flor (la
	   atención llega a la mente); al pasar sobre la flor, una onda sale por
	   todas las pistas. La red no se deforma: lo que se mueve es la señal.
	   Todo se detiene solo cuando no quedan señales en viaje.
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
		var fondo = document.createElement( 'canvas' ); // retícula de puntos, se dibuja una vez
		var fctx = fondo.getContext( '2d' );

		var W = 0, H = 0, DPR = 1, cx = 0, cy = 0, R = 0, movil = false;
		var pistas = [], senales = [];
		var corriendo = false, visible = true, t0 = 0, ultimo = 0, crecido = false;
		var lentos = 0, avisos = 0;
		var CRECER = 1700; // ms en que las pistas se dibujan desde la flor
		var VEL = 0.42; // px por ms

		function azar( semilla ) {
			var s = semilla;
			return function () {
				s = ( s * 16807 ) % 2147483647;
				return ( s - 1 ) / 2147483646;
			};
		}
		function ahoraMs() {
			return window.performance ? performance.now() : Date.now();
		}
		function suave( x ) {
			x = Math.max( 0, Math.min( 1, x ) );
			return x * x * ( 3 - 2 * x );
		}

		function medir() {
			var r = seccion.getBoundingClientRect();
			var f = flor.getBoundingClientRect();
			DPR = Math.min( window.devicePixelRatio || 1, 1.5 );
			W = r.width;
			H = r.height;
			movil = W < 900;
			[ canvas, fondo ].forEach( function ( c ) {
				c.width = Math.round( W * DPR );
				c.height = Math.round( H * DPR );
			} );
			ctx.setTransform( DPR, 0, 0, DPR, 0, 0 );
			fctx.setTransform( DPR, 0, 0, DPR, 0, 0 );
			cx = f.left - r.left + f.width / 2;
			cy = f.top - r.top + f.height / 2;
			R = f.width * 0.46;
		}

		function dentro( p ) {
			return p[ 0 ] > 6 && p[ 0 ] < W - 6 && p[ 1 ] > 6 && p[ 1 ] < H - 6;
		}

		// Rutas a 45°: salen del borde de la flor, giran una o dos veces y terminan en un nodo.
		function construir() {
			var rnd = azar( 20260927 );
			var n = movil ? 16 : 30;
			var paso = Math.PI / 4;
			pistas = [];
			for ( var i = 0; i < n; i++ ) {
				var th = ( i / n ) * Math.PI * 2 + ( rnd() - 0.5 ) * 0.12;
				var p0 = [ cx + Math.cos( th ) * R * 0.86, cy + Math.sin( th ) * R * 0.86 ];
				var d0 = Math.round( th / paso ) * paso;
				var giro = ( rnd() < 0.5 ? -1 : 1 ) * paso;
				var tramos = [
					[ d0, R * ( 0.22 + rnd() * 0.45 ) ],
					[ d0 + giro, R * ( 0.18 + rnd() * 0.6 ) ]
				];
				if ( rnd() < 0.65 ) {
					tramos.push( [ d0, R * ( 0.2 + rnd() * 0.9 ) ] );
				}
				var pts = [ p0 ];
				for ( var k = 0; k < tramos.length; k++ ) {
					var ult = pts[ pts.length - 1 ];
					var sig = [ ult[ 0 ] + Math.cos( tramos[ k ][ 0 ] ) * tramos[ k ][ 1 ], ult[ 1 ] + Math.sin( tramos[ k ][ 0 ] ) * tramos[ k ][ 1 ] ];
					if ( ! dentro( sig ) ) {
						break;
					}
					pts.push( sig );
				}
				if ( pts.length < 2 ) {
					continue;
				}
				var pista = { pts: pts, act: 0, ultimaSenal: 0 };
				medirPista( pista );
				pistas.push( pista );
				// Algunas pistas tienen una derivación corta con su propio nodo.
				if ( pts.length > 2 && rnd() < 0.4 ) {
					var base = pts[ 1 ], dir = d0 - giro;
					var fin = [ base[ 0 ] + Math.cos( dir ) * R * 0.35, base[ 1 ] + Math.sin( dir ) * R * 0.35 ];
					if ( dentro( fin ) ) {
						var rama = { pts: [ base, fin ], act: 0, ultimaSenal: 0, rama: true, padre: pista };
						medirPista( rama );
						pistas.push( rama );
					}
				}
			}
			dibujarFondo();
		}

		function medirPista( p ) {
			p.largos = [ 0 ];
			for ( var k = 1; k < p.pts.length; k++ ) {
				p.largos.push( p.largos[ k - 1 ] + Math.hypot( p.pts[ k ][ 0 ] - p.pts[ k - 1 ][ 0 ], p.pts[ k ][ 1 ] - p.pts[ k - 1 ][ 1 ] ) );
			}
			p.total = p.largos[ p.largos.length - 1 ];
			p.fin = p.pts[ p.pts.length - 1 ];
		}

		// Punto a la distancia s del inicio de la pista.
		function punto( p, s ) {
			s = Math.max( 0, Math.min( p.total, s ) );
			for ( var k = 1; k < p.pts.length; k++ ) {
				if ( s <= p.largos[ k ] ) {
					var f = ( s - p.largos[ k - 1 ] ) / ( ( p.largos[ k ] - p.largos[ k - 1 ] ) || 1 );
					return [ p.pts[ k - 1 ][ 0 ] + ( p.pts[ k ][ 0 ] - p.pts[ k - 1 ][ 0 ] ) * f, p.pts[ k - 1 ][ 1 ] + ( p.pts[ k ][ 1 ] - p.pts[ k - 1 ][ 1 ] ) * f ];
				}
			}
			return p.fin;
		}

		function trazo( p, desde, hasta ) {
			ctx.beginPath();
			var a = punto( p, desde );
			ctx.moveTo( a[ 0 ], a[ 1 ] );
			for ( var k = 1; k < p.pts.length; k++ ) {
				if ( p.largos[ k ] > desde && p.largos[ k ] < hasta ) {
					ctx.lineTo( p.pts[ k ][ 0 ], p.pts[ k ][ 1 ] );
				}
			}
			var b = punto( p, hasta );
			ctx.lineTo( b[ 0 ], b[ 1 ] );
			ctx.stroke();
		}

		function dibujarFondo() {
			// Retícula de puntos muy tenue alrededor de la flor: el "sustrato" técnico.
			fctx.clearRect( 0, 0, W, H );
			var sep = movil ? 20 : 24;
			for ( var x = sep / 2; x < W; x += sep ) {
				for ( var y = sep / 2; y < H; y += sep ) {
					var d = Math.hypot( x - cx, y - cy );
					if ( d < R * 0.9 ) {
						continue;
					}
					var a = 0.22 * Math.max( 0, 1 - d / ( R * 4.2 ) );
					if ( a > 0.01 ) {
						fctx.fillStyle = 'rgba(29,95,148,' + a.toFixed( 3 ) + ')';
						fctx.fillRect( x - 0.75, y - 0.75, 1.5, 1.5 );
					}
				}
			}
		}

		function dibujar( ahora ) {
			var edad = ahora - t0;
			ctx.clearRect( 0, 0, W, H );
			ctx.drawImage( fondo, 0, 0, W, H );
			ctx.lineCap = 'round';
			ctx.lineJoin = 'round';
			var i, p;
			for ( i = 0; i < pistas.length; i++ ) {
				p = pistas[ i ];
				var retraso = p.rama ? 500 : ( i % 7 ) * 60;
				var g = crecido ? 1 : suave( ( edad - retraso ) / ( CRECER - 420 ) );
				if ( g <= 0 ) {
					continue;
				}
				// Pista: azul tenue; se aviva (verde azulado) cuando pasa una señal.
				ctx.lineWidth = 1.1;
				ctx.strokeStyle = p.act > 0.02 ?
					'rgba(15,107,107,' + ( 0.28 + p.act * 0.5 ).toFixed( 3 ) + ')' :
					'rgba(29,95,148,0.28)';
				trazo( p, 0, p.total * g );
				if ( g >= 1 ) {
					// Nodo al final de la pista (una "vía" del circuito).
					var f = p.fin;
					ctx.fillStyle = p.act > 0.02 ? 'rgba(15,107,107,' + ( 0.6 + p.act * 0.4 ).toFixed( 3 ) + ')' : 'rgba(29,95,148,0.55)';
					ctx.beginPath();
					ctx.arc( f[ 0 ], f[ 1 ], 2.6, 0, Math.PI * 2 );
					ctx.fill();
					ctx.strokeStyle = 'rgba(29,95,148,' + ( 0.22 + p.act * 0.4 ).toFixed( 3 ) + ')';
					ctx.lineWidth = 1;
					ctx.beginPath();
					ctx.arc( f[ 0 ], f[ 1 ], 5.5 + p.act * 3, 0, Math.PI * 2 );
					ctx.stroke();
				}
			}
			// Señales en viaje: un tramo brillante con estela.
			for ( i = 0; i < senales.length; i++ ) {
				var s = senales[ i ];
				if ( s.s < 0 || s.s > s.p.total ) {
					continue; // todavía no salió
				}
				var cola = 26;
				var desde = s.dir > 0 ? s.s - cola : s.s;
				var hasta = s.dir > 0 ? s.s : s.s + cola;
				var grad;
				var a0 = punto( s.p, desde ), a1 = punto( s.p, hasta );
				grad = ctx.createLinearGradient( a0[ 0 ], a0[ 1 ], a1[ 0 ], a1[ 1 ] );
				grad.addColorStop( s.dir > 0 ? 0 : 1, 'rgba(15,107,107,0)' );
				grad.addColorStop( s.dir > 0 ? 1 : 0, 'rgba(15,107,107,0.95)' );
				ctx.strokeStyle = grad;
				ctx.lineWidth = 2.2;
				trazo( s.p, desde, hasta );
				var cabeza = punto( s.p, s.s );
				ctx.fillStyle = 'rgba(15,107,107,0.95)';
				ctx.beginPath();
				ctx.arc( cabeza[ 0 ], cabeza[ 1 ], 2.4, 0, Math.PI * 2 );
				ctx.fill();
			}
		}

		function enviar( p, dir, demora ) {
			senales.push( { p: p, dir: dir, s: dir > 0 ? -VEL * ( demora || 0 ) : p.total + VEL * ( demora || 0 ) } );
		}

		function paso( ahora ) {
			if ( ! corriendo ) {
				return;
			}
			var dt = ultimo ? Math.min( 48, ahora - ultimo ) : 16;
			ultimo = ahora;
			if ( ahora - t0 > 1200 && dt > 34 ) {
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
			if ( ! crecido && ahora - t0 > CRECER + 600 ) {
				crecido = true;
			}
			// Avanzar señales; al llegar, encienden el nodo (hacia afuera) o la flor (hacia adentro).
			for ( var i = senales.length - 1; i >= 0; i-- ) {
				var s = senales[ i ];
				if ( s.dir > 0 ) {
					s.s += VEL * dt;
					if ( s.s >= 0 ) {
						s.p.act = Math.max( s.p.act, 0.7 );
					}
					if ( s.s >= s.p.total ) {
						s.p.act = 1;
						senales.splice( i, 1 );
					}
				} else {
					s.s -= VEL * dt;
					if ( s.s <= s.p.total ) {
						s.p.act = Math.max( s.p.act, 0.7 );
					}
					if ( s.s <= 0 ) {
						senales.splice( i, 1 );
						if ( s.p.padre ) {
							// Desde una derivación, la señal sigue por la pista principal.
							var base = s.p.padre.largos[ 1 ];
							senales.push( { p: s.p.padre, dir: -1, s: base } );
						} else {
							latido();
						}
					}
				}
			}
			var activo = senales.length > 0;
			for ( var k = 0; k < pistas.length; k++ ) {
				pistas[ k ].act *= 0.955;
				if ( pistas[ k ].act < 0.01 ) {
					pistas[ k ].act = 0;
				} else {
					activo = true;
				}
			}
			dibujar( ahora );
			if ( crecido && ! activo ) {
				corriendo = false;
				return;
			}
			raf( paso );
		}

		// La flor "recibe" la señal: un brillo breve.
		var tLatido = null;
		function latido() {
			seccion.classList.add( 'is-senal' );
			clearTimeout( tLatido );
			tLatido = setTimeout( function () {
				seccion.classList.remove( 'is-senal' );
			}, 420 );
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
			crecido = true;
			senales = [];
			pistas.forEach( function ( p ) {
				p.act = 0;
			} );
			dibujar( ahoraMs() );
		}

		function onda() {
			if ( quieto() || pocosRecursos ) {
				return;
			}
			pistas.forEach( function ( p, i ) {
				if ( ! p.rama ) {
					enviar( p, 1, ( i % 5 ) * 70 );
				}
			} );
			despertar();
		}

		// El puntero cerca de un nodo: la señal viaja del nodo hacia la flor.
		function cerca( x, y ) {
			if ( quieto() || pocosRecursos || ! crecido ) {
				return;
			}
			var t = ahoraMs(), radio = movil ? 70 : 90, hubo = false;
			pistas.forEach( function ( p ) {
				if ( t - p.ultimaSenal < 1400 ) {
					return;
				}
				if ( Math.hypot( p.fin[ 0 ] - x, p.fin[ 1 ] - y ) < radio ) {
					p.ultimaSenal = t;
					p.act = 1;
					enviar( p, -1, 0 );
					hubo = true;
				}
			} );
			if ( hubo ) {
				despertar();
			}
		}

		function posicion( ev ) {
			var r = seccion.getBoundingClientRect();
			return [ ev.clientX - r.left, ev.clientY - r.top ];
		}

		medir();
		construir();
		if ( quieto() || pocosRecursos ) {
			detener();
		} else {
			t0 = ahoraMs();
			// Al cargar: las pistas crecen desde la flor y unas pocas señales salen hacia afuera.
			var rnd = azar( 7 );
			pistas.forEach( function ( p ) {
				if ( ! p.rama && rnd() < 0.4 ) {
					enviar( p, 1, CRECER + rnd() * 1400 );
				}
			} );
			despertar();
		}
		raf( function () {
			canvas.classList.add( 'is-lista' );
		} );

		seccion.addEventListener( 'pointermove', function ( ev ) {
			var q = posicion( ev );
			cerca( q[ 0 ], q[ 1 ] );
		}, { passive: true } );
		seccion.addEventListener( 'pointerdown', function ( ev ) {
			var q = posicion( ev );
			cerca( q[ 0 ], q[ 1 ] );
		}, { passive: true } );
		flor.addEventListener( 'pointerenter', onda );
		flor.addEventListener( 'pointerdown', function () {
			onda();
			seccion.classList.add( 'is-flor-activa' );
			setTimeout( function () {
				seccion.classList.remove( 'is-flor-activa' );
			}, 1800 );
		}, { passive: true } );
		// El foco del teclado en el hero también dispara la onda.
		seccion.addEventListener( 'focusin', onda );

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
		var ancho = W, tResize = null;
		window.addEventListener( 'resize', function () {
			clearTimeout( tResize );
			tResize = setTimeout( function () {
				var r = seccion.getBoundingClientRect();
				if ( Math.abs( r.width - ancho ) < 2 && Math.abs( r.height - H ) < 40 ) {
					return;
				}
				ancho = r.width;
				medir();
				construir();
				detener();
			}, 200 );
		} );
		this.pausar = detener;
	}

	/* La flor gira despacio con el scroll (mientras el hero está en pantalla). */
	function prepararFlor() {
		var flor = document.querySelector( '.calma-hero__media img' );
		if ( ! flor ) {
			return;
		}
		var pendiente = false;
		function girar() {
			pendiente = false;
			var y = Math.min( window.scrollY || window.pageYOffset, 2000 );
			flor.style.setProperty( '--calma-flor-giro', quieto() ? 0 : ( y * 0.045 ).toFixed( 2 ) );
		}
		window.addEventListener( 'scroll', function () {
			if ( ! pendiente ) {
				pendiente = true;
				raf( girar );
			}
		}, { passive: true } );
		raiz.addEventListener( 'calma-quieto', girar );
		girar();
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
		var figuras = document.querySelectorAll( '.calma-cifra, .calma-estado, .calma-person, .calma-habito' );
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
		var lista = document.querySelector( '.calma-estados' );
		if ( ! lista ) {
			return;
		}
		var tarjetas = Array.prototype.slice.call( lista.querySelectorAll( '.calma-estado' ) );
		lista.classList.add( 'calma-estados--giro' );
		tarjetas.forEach( function ( tarjeta, n ) {
			var girar = tarjeta.querySelector( '.calma-estado__girar' );
			var volver = tarjeta.querySelector( '.calma-estado__volver' );
			var frente = tarjeta.querySelector( '.calma-estado__frente' );
			var dorso = tarjeta.querySelector( '.calma-estado__dorso' );
			if ( ! girar || ! volver || ! frente || ! dorso ) {
				return;
			}
			tarjeta.style.setProperty( '--calma-n', n );
			girar.hidden = false;
			volver.hidden = false;
			dorso.setAttribute( 'tabindex', '-1' );
			function poner( girada, mover ) {
				tarjeta.classList.toggle( 'is-girada', girada );
				girar.setAttribute( 'aria-expanded', girada ? 'true' : 'false' );
				// La cara que no se ve no se lee ni recibe foco.
				frente.inert = girada;
				dorso.inert = ! girada;
				if ( girada ) {
					frente.setAttribute( 'aria-hidden', 'true' );
					dorso.removeAttribute( 'aria-hidden' );
				} else {
					dorso.setAttribute( 'aria-hidden', 'true' );
					frente.removeAttribute( 'aria-hidden' );
				}
				if ( mover ) {
					( girada ? dorso : girar ).focus( { preventScroll: true } );
				}
			}
			tarjeta._calmaPoner = poner;
			poner( false, false );
			// Toda la cara es clicable (el botón sigue siendo el control accesible).
			frente.addEventListener( 'click', function ( ev ) {
				if ( ev.target.closest( 'a' ) ) {
					return;
				}
				// Una por vez: la que estaba dada vuelta vuelve a su estado original.
				tarjetas.forEach( function ( otra ) {
					if ( otra !== tarjeta && otra.classList.contains( 'is-girada' ) && otra._calmaPoner ) {
						otra._calmaPoner( false, false );
					}
				} );
				// El foco se mueve solo con teclado (un clic de teclado tiene detail 0).
				poner( true, ev.detail === 0 );
			} );
			// Una vez dada vuelta, un clic en cualquier parte la devuelve (menos en el enlace de la fuente).
			dorso.addEventListener( 'click', function ( ev ) {
				if ( ev.target.closest( 'a' ) ) {
					return;
				}
				poner( false, ev.detail === 0 );
				encender( tarjeta );
			} );
			dorso.addEventListener( 'keydown', function ( ev ) {
				if ( ev.key === 'Escape' ) {
					poner( false, true );
				}
			} );
		} );
		// Al llegar a la sección, las tarjetas se asoman una vez: se pueden dar vuelta.
		if ( ! quieto() && 'IntersectionObserver' in window ) {
			var io = new IntersectionObserver( function ( e ) {
				if ( e[ 0 ].isIntersecting ) {
					io.disconnect();
					tarjetas.forEach( function ( t ) {
						t.classList.add( 'is-asomo' );
						setTimeout( function () {
							t.classList.remove( 'is-asomo' );
						}, 2400 );
					} );
				}
			}, { threshold: 0.35 } );
			io.observe( lista );
		}
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
		document.querySelectorAll( '.loop-entry .post-thumbnail, .kb-row-layout-id1204_6c7f8b-e0 .kb-is-ratio-image, .calma-descarga__portada' ).forEach( function ( el ) {
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
	   5. Línea de tiempo: la línea crece con el scroll (nativo) y cada época se
	   enciende cuando la línea la alcanza. En escritorio, una figura fija
	   muestra cómo la tecnología fue conectando a las personas (cada punto es
	   una persona) y se transforma de una época a la otra con el scroll:
	   1. Objeto: pocas personas tienen una computadora; el resto, sin conexión.
	   2. Red: muchas se conectan a través de unos pocos nodos (la Web).
	   3. Dispositivo: todas llevan su dispositivo y están conectadas entre sí.
	   4. Plataforma: las personas se agrupan alrededor de plataformas.
	   5. Inteligencia: un sistema en el centro conectado con todas.
	   ------------------------------------------------------------------------ */
	function redesDeEpoca() {
		var rnd = ( function () {
			var s = 1975;
			return function () {
				s = ( s * 16807 ) % 2147483647;
				return ( s - 1 ) / 2147483646;
			};
		}() );
		var N = 46, P = [], i, k;
		// Base: personas repartidas en un disco, sin amontonarse.
		while ( P.length < N ) {
			var ang = rnd() * Math.PI * 2, r = Math.sqrt( rnd() ) * 0.88;
			var x = Math.cos( ang ) * r, y = Math.sin( ang ) * r, libre = true;
			for ( k = 0; k < P.length; k++ ) {
				if ( Math.hypot( P[ k ].b[ 0 ] - x, P[ k ].b[ 1 ] - y ) < 0.17 ) {
					libre = false;
					break;
				}
			}
			if ( libre ) {
				P.push( { b: [ x, y ], ang: Math.atan2( y, x ) } );
			}
		}
		var hubs = [ [ -0.42, -0.4 ], [ 0.46, -0.3 ], [ -0.3, 0.46 ], [ 0.4, 0.44 ] ];
		var plataformas = [ [ -0.46, -0.3 ], [ 0.5, -0.12 ], [ -0.04, 0.55 ] ];
		P.forEach( function ( p, n ) {
			p.pc = n % 7 === 0; // unas pocas, con computadora
			p.online = p.pc || rnd() < 0.45;
			var mejor = 0, dmin = 9;
			hubs.forEach( function ( h, j ) {
				var d = Math.hypot( h[ 0 ] - p.b[ 0 ], h[ 1 ] - p.b[ 1 ] );
				if ( d < dmin ) {
					dmin = d;
					mejor = j;
				}
			} );
			p.hub = mejor;
			mejor = 0;
			dmin = 9;
			plataformas.forEach( function ( c, j ) {
				var d = Math.hypot( c[ 0 ] - p.b[ 0 ], c[ 1 ] - p.b[ 1 ] );
				if ( d < dmin ) {
					dmin = d;
					mejor = j;
				}
			} );
			p.plat = mejor;
			var c = plataformas[ mejor ];
			var jit = [ ( rnd() - 0.5 ) * 0.1, ( rnd() - 0.5 ) * 0.1 ];
			var anillo = 0.42 + ( n % 3 ) * 0.2;
			// Posición de la persona en cada época.
			p.pos = [
				p.b,
				p.b,
				[ p.b[ 0 ] + jit[ 0 ], p.b[ 1 ] + jit[ 1 ] ],
				[ c[ 0 ] + ( p.b[ 0 ] - c[ 0 ] ) * 0.42, c[ 1 ] + ( p.b[ 1 ] - c[ 1 ] ) * 0.42 ],
				[ Math.cos( p.ang ) * anillo, Math.sin( p.ang ) * anillo ]
			];
		} );
		// Vecinos (para la época del dispositivo: todas conectadas entre sí).
		P.forEach( function ( p ) {
			p.vec = P.map( function ( q, j ) {
				return { j: j, d: Math.hypot( q.pos[ 2 ][ 0 ] - p.pos[ 2 ][ 0 ], q.pos[ 2 ][ 1 ] - p.pos[ 2 ][ 1 ] ) };
			} ).sort( function ( a, b ) { return a.d - b.d; } ).slice( 1, 3 ).map( function ( o ) { return o.j; } );
		} );
		for ( i = 0; i < P.length; i++ ) {
			P[ i ].i = i;
		}
		return { P: P, hubs: hubs, plataformas: plataformas };
	}

	// Opacidad de cada capa en las 5 épocas.
	var CAPAS = {
		pc: [ 1, 0.6, 0, 0, 0 ],
		hubs: [ 0, 1, 0.25, 0, 0 ],
		lineasHub: [ 0, 1, 0.15, 0, 0 ],
		anillos: [ 0, 0, 1, 0.45, 0.25 ],
		malla: [ 0, 0, 1, 0.25, 0.1 ],
		plataformas: [ 0, 0, 0, 1, 0 ],
		lineasPlat: [ 0, 0, 0, 1, 0.15 ],
		ia: [ 0, 0, 0, 0, 1 ]
	};

	function prepararTiempo() {
		var seccion = document.querySelector( '.calma-tiempo' );
		if ( ! seccion ) {
			return;
		}
		var lista = seccion.querySelector( '.calma-tiempo__lista' );
		var epocas = Array.prototype.slice.call( seccion.querySelectorAll( '.calma-tiempo__epoca' ) );
		var figura = seccion.querySelector( '.calma-tiempo__figura' );
		if ( ! lista || ! epocas.length ) {
			return;
		}
		var anio = figura && figura.querySelector( '.calma-tiempo__anio' );
		var rotulo = figura && figura.querySelector( '.calma-tiempo__rotulo' );
		var canvas = null, ctx = null, lado = 0, DPR = 1, ultimoF = -1, epocaRotulo = -1, pendiente = false, tAnio = null;
		var red = redesDeEpoca();

		if ( figura && window.HTMLCanvasElement ) {
			figura.hidden = false;
			canvas = document.createElement( 'canvas' );
			figura.querySelector( '.calma-tiempo__lienzo' ).appendChild( canvas );
			ctx = canvas.getContext( '2d' );
		}

		function medir() {
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

		function dibujar( f ) {
			if ( ! ctx || ! lado ) {
				return;
			}
			var i0 = Math.max( 0, Math.min( 4, Math.floor( f ) ) ), i1 = Math.min( 4, i0 + 1 );
			var t = f - i0;
			t = t * t * ( 3 - 2 * t );
			function capa( nombre ) {
				var v = CAPAS[ nombre ];
				return v[ i0 ] + ( v[ i1 ] - v[ i0 ] ) * t;
			}
			var c = lado / 2, e = lado * 0.46;
			function X( v ) {
				return c + v * e;
			}
			var P = red.P;
			var pts = P.map( function ( p ) {
				var a = p.pos[ i0 ], b = p.pos[ i1 ];
				return [ X( a[ 0 ] + ( b[ 0 ] - a[ 0 ] ) * t ), X( a[ 1 ] + ( b[ 1 ] - a[ 1 ] ) * t ) ];
			} );
			// ¿Qué tan "conectada" está cada persona en cada época?
			function encendida( p, ep ) {
				return ep === 0 ? ( p.pc ? 1 : 0 ) : ep === 1 ? ( p.online ? 1 : 0 ) : 1;
			}
			ctx.clearRect( 0, 0, lado, lado );
			ctx.lineWidth = 1;
			var a;

			// Red: líneas a los nodos de la Web.
			a = capa( 'lineasHub' );
			if ( a > 0.01 ) {
				ctx.strokeStyle = 'rgba(29,95,148,' + ( 0.35 * a ).toFixed( 3 ) + ')';
				P.forEach( function ( p, n ) {
					if ( p.online ) {
						var h = red.hubs[ p.hub ];
						ctx.beginPath();
						ctx.moveTo( pts[ n ][ 0 ], pts[ n ][ 1 ] );
						ctx.lineTo( X( h[ 0 ] ), X( h[ 1 ] ) );
						ctx.stroke();
					}
				} );
			}
			// Dispositivo: todas conectadas con sus vecinas.
			a = capa( 'malla' );
			if ( a > 0.01 ) {
				ctx.strokeStyle = 'rgba(29,95,148,' + ( 0.38 * a ).toFixed( 3 ) + ')';
				P.forEach( function ( p, n ) {
					p.vec.forEach( function ( j ) {
						ctx.beginPath();
						ctx.moveTo( pts[ n ][ 0 ], pts[ n ][ 1 ] );
						ctx.lineTo( pts[ j ][ 0 ], pts[ j ][ 1 ] );
						ctx.stroke();
					} );
				} );
			}
			// Plataforma: cada persona unida a su plataforma.
			a = capa( 'lineasPlat' );
			if ( a > 0.01 ) {
				ctx.strokeStyle = 'rgba(15,107,107,' + ( 0.4 * a ).toFixed( 3 ) + ')';
				P.forEach( function ( p, n ) {
					var q = red.plataformas[ p.plat ];
					ctx.beginPath();
					ctx.moveTo( pts[ n ][ 0 ], pts[ n ][ 1 ] );
					ctx.lineTo( X( q[ 0 ] ), X( q[ 1 ] ) );
					ctx.stroke();
				} );
			}
			// Inteligencia: un sistema en el centro, conectado con todas.
			a = capa( 'ia' );
			if ( a > 0.01 ) {
				ctx.strokeStyle = 'rgba(15,107,107,' + ( 0.28 * a ).toFixed( 3 ) + ')';
				pts.forEach( function ( q ) {
					ctx.beginPath();
					ctx.moveTo( c, c );
					ctx.quadraticCurveTo( ( c + q[ 0 ] ) / 2 + ( q[ 1 ] - c ) * 0.18, ( c + q[ 1 ] ) / 2 - ( q[ 0 ] - c ) * 0.18, q[ 0 ], q[ 1 ] );
					ctx.stroke();
				} );
				ctx.fillStyle = 'rgba(15,107,107,' + a.toFixed( 3 ) + ')';
				ctx.beginPath();
				ctx.arc( c, c, lado * 0.045, 0, Math.PI * 2 );
				ctx.fill();
				ctx.strokeStyle = 'rgba(15,107,107,' + ( 0.35 * a ).toFixed( 3 ) + ')';
				[ 0.075, 0.105 ].forEach( function ( r ) {
					ctx.beginPath();
					ctx.arc( c, c, lado * r, 0, Math.PI * 2 );
					ctx.stroke();
				} );
			}
			// Nodos de la Web y plataformas.
			a = capa( 'hubs' );
			if ( a > 0.01 ) {
				ctx.fillStyle = 'rgba(27,34,51,' + a.toFixed( 3 ) + ')';
				red.hubs.forEach( function ( h ) {
					ctx.fillRect( X( h[ 0 ] ) - 5, X( h[ 1 ] ) - 5, 10, 10 );
				} );
			}
			a = capa( 'plataformas' );
			if ( a > 0.01 ) {
				ctx.strokeStyle = 'rgba(15,107,107,' + a.toFixed( 3 ) + ')';
				ctx.fillStyle = 'rgba(216,235,232,' + a.toFixed( 3 ) + ')';
				red.plataformas.forEach( function ( q ) {
					ctx.beginPath();
					ctx.rect( X( q[ 0 ] ) - 13, X( q[ 1 ] ) - 13, 26, 26 );
					ctx.fill();
					ctx.stroke();
				} );
			}
			// Personas.
			var anillos = capa( 'anillos' ), pc = capa( 'pc' ), iaA = capa( 'ia' );
			P.forEach( function ( p, n ) {
				var on = encendida( p, i0 ) + ( encendida( p, i1 ) - encendida( p, i0 ) ) * t;
				var x = pts[ n ][ 0 ], y = pts[ n ][ 1 ];
				if ( p.pc && pc > 0.01 ) {
					// La computadora personal, al lado de la persona.
					ctx.strokeStyle = 'rgba(27,34,51,' + pc.toFixed( 3 ) + ')';
					ctx.strokeRect( x + 6, y - 9, 11, 8 );
				}
				if ( anillos > 0.01 ) {
					ctx.strokeStyle = 'rgba(29,95,148,' + ( 0.55 * anillos ).toFixed( 3 ) + ')';
					ctx.beginPath();
					ctx.arc( x, y, 7, 0, Math.PI * 2 );
					ctx.stroke();
				}
				var r = 3.2;
				if ( on > 0.5 ) {
					ctx.fillStyle = iaA > 0.5 ? '#0f6b6b' : '#1d5f94';
				} else {
					ctx.fillStyle = '#b4ad9f';
				}
				ctx.beginPath();
				ctx.arc( x, y, r, 0, Math.PI * 2 );
				ctx.fill();
			} );
		}

		function mostrarEpoca( i ) {
			if ( ! figura || i === epocaRotulo ) {
				return;
			}
			epocaRotulo = i;
			var e = epocas[ i ];
			if ( rotulo ) {
				rotulo.textContent = 'Fig. ' + ( '0' + ( i + 1 ) ).slice( -2 ) + ' — ' + e.getAttribute( 'data-concepto' );
			}
			if ( anio ) {
				var texto = e.querySelector( '.calma-tiempo__anios' ).firstChild.nodeValue;
				if ( quieto() ) {
					anio.textContent = texto;
				} else {
					anio.classList.add( 'is-cambio' );
					clearTimeout( tAnio );
					tAnio = setTimeout( function () {
						anio.textContent = texto;
						anio.classList.remove( 'is-cambio' );
					}, 260 );
				}
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
			var actual = 0;
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
			// Posición continua entre épocas: la figura se transforma con el scroll.
			var f = 0;
			for ( var i = 0; i < ys.length - 1; i++ ) {
				if ( yLinea >= ys[ i ] ) {
					f = i + Math.min( 1, ( yLinea - ys[ i ] ) / ( ys[ i + 1 ] - ys[ i ] ) );
				}
			}
			if ( ! vivo ) {
				f = actual; // sin movimiento: cambios de estado, sin transición
			}
			mostrarEpoca( actual );
			if ( Math.abs( f - ultimoF ) > 0.002 ) {
				ultimoF = f;
				dibujar( f );
			}
		}

		function pedir() {
			if ( ! pendiente ) {
				pendiente = true;
				raf( actualizar );
			}
		}

		medir();
		actualizar();
		window.addEventListener( 'scroll', pedir, { passive: true } );
		window.addEventListener( 'resize', function () {
			medir();
			pedir();
		} );
		raiz.addEventListener( 'calma-quieto', pedir );
	}

	/* ------------------------------------------------------------------------
	   5b. Accesos: cada personaje llega a su pose final siguiendo el scroll
	   (--p de 0 a 1 mientras la tarjeta entra en pantalla). Al llegar, y al
	   pasar el puntero o el foco, parpadea y hace su gesto (menos de 2 s).
	   ------------------------------------------------------------------------ */
	function prepararAccesos() {
		var tarjetas = Array.prototype.slice.call( document.querySelectorAll( '.calma-acceso' ) );
		if ( ! tarjetas.length ) {
			return;
		}
		var pendiente = false;
		function saludar( t ) {
			if ( quieto() ) {
				return;
			}
			t.classList.remove( 'is-vivo' );
			void t.offsetWidth;
			t.classList.add( 'is-vivo' );
			clearTimeout( t._calmaT );
			t._calmaT = setTimeout( function () {
				t.classList.remove( 'is-vivo' );
			}, 2200 );
		}
		function actualizar() {
			pendiente = false;
			var vh = window.innerHeight;
			tarjetas.forEach( function ( t ) {
				if ( quieto() ) {
					t.style.setProperty( '--p', 1 );
					return;
				}
				var r = t.getBoundingClientRect();
				// 0 cuando la tarjeta asoma por abajo; 1 cuando su borde superior pasa el 45 % de la pantalla.
				var p = Math.max( 0, Math.min( 1, ( vh - r.top ) / ( vh * 0.55 ) ) );
				t.style.setProperty( '--p', p.toFixed( 3 ) );
				if ( p >= 1 && ! t._calmaLlego ) {
					t._calmaLlego = true;
					saludar( t );
				} else if ( p < 0.6 ) {
					t._calmaLlego = false;
				}
			} );
		}
		function pedir() {
			if ( ! pendiente ) {
				pendiente = true;
				raf( actualizar );
			}
		}
		tarjetas.forEach( function ( t ) {
			var ultimo = 0;
			function otraVez() {
				var ahora = Date.now();
				if ( ahora - ultimo > 2400 && t._calmaLlego ) {
					ultimo = ahora;
					saludar( t );
				}
			}
			if ( finoHover ) {
				t.addEventListener( 'pointerenter', otraVez );
			}
			t.addEventListener( 'focusin', otraVez );
		} );
		actualizar();
		window.addEventListener( 'scroll', pedir, { passive: true } );
		window.addEventListener( 'resize', pedir );
		raiz.addEventListener( 'calma-quieto', pedir );
	}

	/* ------------------------------------------------------------------------
	   5c. Mapa de temas: la lista de temas pasa a ser un mapa. Un tema por vez
	   (botones con aria-pressed); al elegir uno se encienden sus uniones y una
	   señal las recorre, y el panel muestra sus artículos y conexiones.
	   ------------------------------------------------------------------------ */
	function prepararMapa() {
		var mapa = document.querySelector( '.calma-mapa' );
		if ( ! mapa ) {
			return;
		}
		var grafo = mapa.querySelector( '.calma-mapa__grafo' );
		var nodos = Array.prototype.slice.call( mapa.querySelectorAll( '.calma-mapa__nodo' ) );
		var paneles = Array.prototype.slice.call( mapa.querySelectorAll( '.calma-mapa__panel' ) );
		var aristas = Array.prototype.slice.call( mapa.querySelectorAll( '.calma-mapa__arista' ) );
		var senales = Array.prototype.slice.call( mapa.querySelectorAll( '.calma-mapa__senal' ) );
		if ( ! grafo || ! nodos.length ) {
			return;
		}
		grafo.hidden = false;
		mapa.classList.add( 'calma-mapa--vivo' );

		function marcar( tema, senal ) {
			var vecinos = {};
			aristas.forEach( function ( a ) {
				var toca = a.getAttribute( 'data-a' ) === tema || a.getAttribute( 'data-b' ) === tema;
				a.classList.toggle( 'is-on', toca );
				a.classList.toggle( 'is-apagada', ! toca );
				if ( toca ) {
					vecinos[ a.getAttribute( 'data-a' ) ] = 1;
					vecinos[ a.getAttribute( 'data-b' ) ] = 1;
				}
			} );
			// La señal sale del tema elegido hacia sus vecinos.
			senales.forEach( function ( s ) {
				var toca = s.getAttribute( 'data-a' ) === tema || s.getAttribute( 'data-b' ) === tema;
				s.classList.remove( 'is-senal' );
				if ( toca && senal && ! quieto() ) {
					s.style.animationDirection = s.getAttribute( 'data-a' ) === tema ? 'normal' : 'reverse';
					void s.getBoundingClientRect();
					s.classList.add( 'is-senal' );
				}
			} );
			nodos.forEach( function ( n ) {
				var k = n.getAttribute( 'data-tema' );
				n.classList.toggle( 'is-vecino', k !== tema && !! vecinos[ k ] );
			} );
		}

		var actual = null;
		function elegir( tema, senal ) {
			actual = tema;
			nodos.forEach( function ( n ) {
				n.setAttribute( 'aria-pressed', n.getAttribute( 'data-tema' ) === tema ? 'true' : 'false' );
			} );
			paneles.forEach( function ( p ) {
				p.hidden = p.getAttribute( 'data-tema' ) !== tema;
			} );
			marcar( tema, senal );
		}

		nodos.forEach( function ( n ) {
			n.addEventListener( 'click', function () {
				elegir( n.getAttribute( 'data-tema' ), true );
			} );
			if ( finoHover ) {
				// Al pasar, se ven sus uniones sin cambiar el panel.
				n.addEventListener( 'pointerenter', function () {
					marcar( n.getAttribute( 'data-tema' ), false );
				} );
				n.addEventListener( 'pointerleave', function () {
					marcar( actual, false );
				} );
			}
		} );
		elegir( 'ciberpsicologia', false );

		// Al llegar a la sección, las uniones se dibujan desde el centro.
		if ( ! quieto() && 'IntersectionObserver' in window ) {
			mapa.classList.add( 'is-esperando' );
			var io = new IntersectionObserver( function ( e ) {
				if ( e[ 0 ].isIntersecting ) {
					io.disconnect();
					mapa.classList.remove( 'is-esperando' );
					setTimeout( function () {
						marcar( actual, true );
					}, 900 );
				}
			}, { threshold: 0.3 } );
			io.observe( grafo );
		}
	}

	/* ------------------------------------------------------------------------
	   5d. "Sigue explorando": al pasar por un artículo de la lista se enciende
	   su unión en el mapa (y al revés); al llegar, una señal sale del centro.
	   ------------------------------------------------------------------------ */
	function prepararExplora() {
		var caja = document.querySelector( '.calma-explora' );
		if ( ! caja ) {
			return;
		}
		function marcar( i ) {
			caja.querySelectorAll( '[data-i]' ).forEach( function ( el ) {
				el.classList.toggle( 'is-on', i !== null && el.getAttribute( 'data-i' ) === String( i ) );
			} );
		}
		caja.querySelectorAll( '.calma-explora__lista li' ).forEach( function ( li ) {
			var i = li.getAttribute( 'data-i' );
			li.addEventListener( 'pointerenter', function () {
				marcar( i );
			} );
			li.addEventListener( 'pointerleave', function () {
				marcar( null );
			} );
			li.addEventListener( 'focusin', function () {
				marcar( i );
			} );
			li.addEventListener( 'focusout', function () {
				marcar( null );
			} );
		} );
		if ( ! quieto() && 'IntersectionObserver' in window ) {
			var io = new IntersectionObserver( function ( e ) {
				if ( e[ 0 ].isIntersecting ) {
					io.disconnect();
					caja.querySelectorAll( '.calma-explora__senal' ).forEach( function ( s ) {
						s.classList.add( 'is-senal' );
					} );
				}
			}, { threshold: 0.4 } );
			io.observe( caja );
		}
	}

	/* ------------------------------------------------------------------------
	   5e. Pasos de Servicios: la línea que une los pasos crece con el scroll y
	   cada paso se enciende cuando la línea lo alcanza (como la línea de tiempo).
	   ------------------------------------------------------------------------ */
	function prepararPasos() {
		document.querySelectorAll( '.calma-steps, .calma-formacion' ).forEach( function ( lista ) {
			var pasos = Array.prototype.slice.call( lista.children );
			if ( pasos.length < 2 ) {
				return;
			}
			var pendiente = false;
			function actualizar() {
				pendiente = false;
				var vivo = ! quieto();
				lista.classList.toggle( 'is-vivo', vivo );
				var r = lista.getBoundingClientRect();
				var vh = window.innerHeight;
				// 0 cuando la lista entra por abajo; 1 cuando llega a la mitad de la pantalla.
				var p = vivo ? Math.max( 0, Math.min( 1, ( vh * 0.85 - r.top ) / ( vh * 0.45 ) ) ) : 1;
				lista.style.setProperty( '--calma-pasos-p', p.toFixed( 3 ) );
				pasos.forEach( function ( li, i ) {
					li.classList.toggle( 'is-encendido', p >= i / ( pasos.length - 1 ) - 0.001 );
				} );
			}
			function pedir() {
				if ( ! pendiente ) {
					pendiente = true;
					raf( actualizar );
				}
			}
			actualizar();
			window.addEventListener( 'scroll', pedir, { passive: true } );
			window.addEventListener( 'resize', pedir );
			raiz.addEventListener( 'calma-quieto', pedir );
		} );
	}

	/* ------------------------------------------------------------------------
	   5g. Equipo: al pasar por la tarjeta de una persona (puntero o teclado),
	   la figura "tres miradas" destaca su área, atenúa las otras y manda una
	   señal por su línea hacia "lo que traigas" (conectar).
	   ------------------------------------------------------------------------ */
	function prepararMiradas() {
		var figura = document.querySelector( '.calma-miradas' );
		if ( ! figura ) {
			return;
		}
		document.querySelectorAll( '.calma-equipo .calma-person' ).forEach( function ( tarjeta ) {
			var m = tarjeta.className.match( /calma-person--([a-z]+)/ );
			if ( ! m ) {
				return;
			}
			var persona = m[ 1 ];
			function activar() {
				figura.setAttribute( 'data-activa', persona );
				if ( quieto() ) {
					return;
				}
				var clase = 'is-senal-' + persona;
				figura.classList.remove( clase );
				void figura.getBoundingClientRect();
				figura.classList.add( clase );
				clearTimeout( figura[ '_calma' + persona ] );
				figura[ '_calma' + persona ] = setTimeout( function () {
					figura.classList.remove( clase );
				}, 2200 );
			}
			function soltar() {
				if ( figura.getAttribute( 'data-activa' ) === persona ) {
					figura.removeAttribute( 'data-activa' );
				}
			}
			tarjeta.addEventListener( 'mouseenter', activar );
			tarjeta.addEventListener( 'focusin', activar );
			tarjeta.addEventListener( 'mouseleave', soltar );
			tarjeta.addEventListener( 'focusout', soltar );
		} );
	}

	/* ------------------------------------------------------------------------
	   5f. Lectura de artículos: tiempo de lectura (contado del texto real) e
	   índice del artículo con las secciones H2. En pantallas anchas va al
	   costado y marca la sección que se está leyendo; en el resto, desplegable.
	   ------------------------------------------------------------------------ */
	function slug( texto, usados ) {
		var base = texto.toLowerCase().normalize( 'NFD' ).replace( /[\u0300-\u036f]/g, '' )
			.replace( /[^a-z0-9]+/g, '-' ).replace( /^-+|-+$/g, '' ).slice( 0, 60 ) || 'seccion';
		var s = base, n = 2;
		while ( usados[ s ] || document.getElementById( s ) ) {
			s = base + '-' + n++;
		}
		usados[ s ] = 1;
		return s;
	}

	function prepararLectura() {
		if ( ! document.body.classList.contains( 'single-post' ) ) {
			return;
		}
		var cuerpo = document.querySelector( '.single-post .entry-content.single-content' );
		if ( ! cuerpo ) {
			return;
		}
		// Tiempo de lectura: solo el texto del artículo (sin cajas agregadas).
		var palabras = 0;
		Array.prototype.forEach.call( cuerpo.children, function ( el ) {
			if ( el.matches( 'p, ul, ol, h2, h3, h4, blockquote, figure, .wp-block-quote' ) ) {
				palabras += ( el.textContent.trim().match( /\S+/g ) || [] ).length;
			}
		} );
		var meta = document.querySelector( '.single-post .entry-header .entry-meta' );
		if ( meta && palabras > 80 ) {
			var min = Math.max( 1, Math.round( palabras / 200 ) );
			var chip = document.createElement( 'span' );
			chip.className = 'calma-lectura';
			chip.textContent = min + ' min de lectura';
			meta.appendChild( chip );
		}
		// Índice: secciones H2 del texto de la autora.
		var titulos = Array.prototype.filter.call( cuerpo.children, function ( el ) {
			return el.tagName === 'H2';
		} );
		if ( titulos.length < 3 ) {
			// Artículos con pocas secciones H2: el índice usa también los subtítulos H3.
			titulos = Array.prototype.filter.call( cuerpo.children, function ( el ) {
				return el.tagName === 'H2' || el.tagName === 'H3';
			} );
		}
		if ( titulos.length < 3 ) {
			return;
		}
		var usados = {};
		// <nav> con un título (pantallas anchas) o un botón que despliega la lista (el resto).
		var indice = document.createElement( 'nav' );
		indice.className = 'calma-indice';
		indice.setAttribute( 'aria-label', 'En este artículo' );
		var envoltura = document.createElement( 'div' );
		var titulo = document.createElement( 'p' );
		titulo.className = 'calma-indice__titulo';
		titulo.textContent = 'En este artículo';
		var boton = document.createElement( 'button' );
		boton.type = 'button';
		boton.className = 'calma-indice__boton';
		boton.textContent = 'En este artículo';
		boton.setAttribute( 'aria-expanded', 'false' );
		boton.setAttribute( 'aria-controls', 'calma-indice-lista' );
		var lista = document.createElement( 'ol' );
		lista.id = 'calma-indice-lista';
		var enlaces = titulos.map( function ( h ) {
			if ( ! h.id ) {
				h.id = slug( h.textContent, usados );
			}
			var li = document.createElement( 'li' );
			if ( h.tagName === 'H3' ) {
				li.className = 'calma-indice__sub';
			}
			var a = document.createElement( 'a' );
			a.href = '#' + h.id;
			a.textContent = h.textContent.trim();
			li.appendChild( a );
			lista.appendChild( li );
			return a;
		} );
		envoltura.appendChild( titulo );
		envoltura.appendChild( boton );
		envoltura.appendChild( lista );
		indice.appendChild( envoltura );
		boton.addEventListener( 'click', function () {
			var abrir = boton.getAttribute( 'aria-expanded' ) !== 'true';
			boton.setAttribute( 'aria-expanded', abrir ? 'true' : 'false' );
			indice.classList.toggle( 'is-abierto', abrir );
		} );
		var caja = cuerpo.querySelector( '.calma-resumen' );
		if ( caja && caja.parentNode === cuerpo ) {
			cuerpo.insertBefore( indice, caja.nextSibling );
		} else {
			cuerpo.insertBefore( indice, cuerpo.firstChild );
		}
		// Sección actual y secciones ya leídas.
		var pendiente = false;
		function marcar() {
			pendiente = false;
			var actual = -1;
			titulos.forEach( function ( h, i ) {
				if ( h.getBoundingClientRect().top < window.innerHeight * 0.35 ) {
					actual = i;
				}
			} );
			enlaces.forEach( function ( a, i ) {
				if ( i === actual ) {
					a.setAttribute( 'aria-current', 'true' );
				} else {
					a.removeAttribute( 'aria-current' );
				}
				a.classList.toggle( 'is-leido', i < actual );
			} );
			var alto = raiz.scrollHeight - window.innerHeight;
			indice.style.setProperty( '--calma-read', alto > 0 ? Math.min( 1, ( window.scrollY || window.pageYOffset ) / alto ).toFixed( 4 ) : 0 );
		}
		window.addEventListener( 'scroll', function () {
			if ( ! pendiente ) {
				pendiente = true;
				raf( marcar );
			}
		}, { passive: true } );
		marcar();
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
		prepararAccesos();
		prepararFlor();
		prepararMapa();
		prepararExplora();
		prepararPasos();
		prepararLectura();
		prepararMiradas();

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
