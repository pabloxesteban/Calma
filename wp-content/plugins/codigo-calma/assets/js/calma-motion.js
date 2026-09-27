/**
 * Código Calma — Etapa 6: movimiento.
 * - Entradas al hacer scroll (IntersectionObserver) solo para elementos que
 *   empiezan fuera de la primera pantalla: nada visible se oculta y, sin JS,
 *   todo se ve igual.
 * - Header compacto al bajar, barra de progreso de lectura en entradas.
 * - Fondos del hero y halos que siguen al puntero y al scroll (no hay bucles).
 * - Brillo de tarjetas que sigue al cursor. Cifras que se cuentan al aparecer.
 * Respeta prefers-reduced-motion (solo deja el header y la barra de progreso fuera).
 */
( function () {
	'use strict';

	var reducir = window.matchMedia && window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;
	var raiz = document.documentElement;
	var raf = window.requestAnimationFrame || function ( fn ) { return setTimeout( fn, 16 ); };

	/* Header compacto y variables de scroll ----------------------------------- */
	var ticking = false;
	var progreso = null;
	function onScroll() {
		if ( ticking ) {
			return;
		}
		ticking = true;
		raf( function () {
			var y = window.scrollY || window.pageYOffset;
			document.body.classList.toggle( 'calma-scrolled', y > 12 );
			if ( ! reducir ) {
				raiz.style.setProperty( '--calma-scroll', Math.min( y, 1200 ) );
			}
			if ( progreso ) {
				var alto = document.documentElement.scrollHeight - window.innerHeight;
				progreso.style.setProperty( '--calma-read', alto > 0 ? Math.min( 1, y / alto ).toFixed( 4 ) : 0 );
			}
			ticking = false;
		} );
	}

	/* Entradas al hacer scroll ------------------------------------------------- */
	var SELECTORES = [
		'.calma-section__head', '.calma-card', '.calma-steps > li', '.calma-quote', '.calma-faq details',
		'.calma-timeline__list', '.calma-tools__card', '.calma-cta', '.calma-notice',
		'.loop-entry', '.kt-blocks-info-box-link-wrap', '.zolo-flip-box', '.calma-article-cta',
		'.calma-fuentes', '.calma-newsletter', '.calma-prosa > h2', '.calma-footer > *',
		'.entry-content > .wp-block-kadence-rowlayout', '.single-post .entry-content > h2'
	].join( ',' );

	function prepararEntradas() {
		if ( reducir || ! ( 'IntersectionObserver' in window ) ) {
			return;
		}
		raiz.classList.add( 'calma-motion' );
		var limite = window.innerHeight * 0.92;
		var io = new IntersectionObserver( function ( entradas ) {
			entradas.forEach( function ( e ) {
				if ( e.isIntersecting ) {
					e.target.classList.add( 'is-visible' );
					io.unobserve( e.target );
				}
			} );
		}, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 } );

		var vistos = new Set();
		document.querySelectorAll( SELECTORES ).forEach( function ( el ) {
			// No se animan elementos ya visibles ni los que están dentro de otro animado.
			if ( el.getBoundingClientRect().top < limite || el.closest( '.calma-reveal' ) ) {
				return;
			}
			var padre = el.parentElement;
			var i = 0;
			if ( padre ) {
				i = Array.prototype.indexOf.call( padre.children, el );
			}
			el.style.setProperty( '--calma-delay', ( Math.min( i, 5 ) * 0.08 ).toFixed( 2 ) + 's' );
			el.classList.add( 'calma-reveal' );
			if ( el.matches( '.calma-timeline__list' ) ) {
				el.querySelectorAll( '.calma-timeline__event' ).forEach( function ( ev, n ) {
					ev.style.setProperty( '--calma-i', n );
				} );
			}
			vistos.add( el );
			io.observe( el );
		} );
	}

	/* Puntero: halos del hero y brillo de tarjetas ----------------------------- */
	function prepararPuntero() {
		if ( reducir || ! window.matchMedia( '(hover: hover) and (pointer: fine)' ).matches ) {
			return;
		}
		var pendiente = null;
		document.addEventListener( 'pointermove', function ( ev ) {
			if ( pendiente ) {
				return;
			}
			pendiente = raf( function () {
				pendiente = null;
				raiz.style.setProperty( '--calma-px', ( ev.clientX / window.innerWidth - 0.5 ).toFixed( 3 ) );
				raiz.style.setProperty( '--calma-py', ( ev.clientY / window.innerHeight - 0.5 ).toFixed( 3 ) );
				var tarjeta = ev.target.closest && ev.target.closest( '.calma-card, .loop-entry, .calma-tools__card' );
				if ( tarjeta ) {
					var r = tarjeta.getBoundingClientRect();
					tarjeta.style.setProperty( '--calma-mx', ( ev.clientX - r.left ) + 'px' );
					tarjeta.style.setProperty( '--calma-my', ( ev.clientY - r.top ) + 'px' );
				}
			} );
		}, { passive: true } );
	}

	/* Cifras que se cuentan ---------------------------------------------------- */
	function prepararCifras() {
		if ( reducir || ! ( 'IntersectionObserver' in window ) ) {
			return;
		}
		var cifras = document.querySelectorAll( '.kt-blocks-info-box-title, .calma-cifra' );
		var io = new IntersectionObserver( function ( entradas ) {
			entradas.forEach( function ( e ) {
				if ( ! e.isIntersecting ) {
					return;
				}
				io.unobserve( e.target );
				var el = e.target;
				var original = el.textContent;
				var m = original.match( /(\d+)/ );
				if ( ! m ) {
					return;
				}
				var fin = parseInt( m[ 1 ], 10 );
				var t0 = null;
				el.setAttribute( 'aria-label', original.trim() );
				function paso( t ) {
					if ( ! t0 ) {
						t0 = t;
					}
					var p = Math.min( 1, ( t - t0 ) / 1200 );
					var v = Math.round( fin * ( 1 - Math.pow( 1 - p, 3 ) ) );
					el.textContent = original.replace( m[ 1 ], v );
					if ( p < 1 ) {
						raf( paso );
					} else {
						el.textContent = original;
						el.removeAttribute( 'aria-label' );
					}
				}
				raf( paso );
			} );
		}, { threshold: 0.6 } );
		cifras.forEach( function ( el ) {
			if ( /\d/.test( el.textContent ) && el.textContent.length < 24 ) {
				io.observe( el );
			}
		} );
	}

	function iniciar() {
		if ( document.body.classList.contains( 'single-post' ) ) {
			progreso = document.createElement( 'div' );
			progreso.className = 'calma-progress';
			progreso.setAttribute( 'aria-hidden', 'true' );
			document.body.appendChild( progreso );
		}
		prepararEntradas();
		prepararPuntero();
		prepararCifras();
		window.addEventListener( 'scroll', onScroll, { passive: true } );
		onScroll();
	}

	if ( document.readyState === 'loading' ) {
		document.addEventListener( 'DOMContentLoaded', iniciar );
	} else {
		iniciar();
	}
}() );
