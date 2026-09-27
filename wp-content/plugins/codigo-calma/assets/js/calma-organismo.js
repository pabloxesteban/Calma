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
			poner( false, false );
			// Toda la cara es clicable (el botón sigue siendo el control accesible).
			frente.addEventListener( 'click', function ( ev ) {
				if ( ev.target.closest( 'a' ) ) {
					return;
				}
				poner( true, true );
			} );
			volver.addEventListener( 'click', function () {
				poner( false, true );
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
