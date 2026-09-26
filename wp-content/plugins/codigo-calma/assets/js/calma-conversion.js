/**
 * Código Calma — flujo de consulta (Etapa 3).
 * 1. /contacto/?area=habitos|accesibilidad|proyectos preselecciona la opción
 *    "¿Sobre qué quieres consultar?" del formulario (Kadence Advanced Form).
 * 2. Al enviarse con éxito un formulario de Kadence, registra el evento
 *    `generate_lead` en dataLayer / gtag si hay analítica instalada.
 * Sin dependencias. No hace nada si no encuentra lo que busca.
 */
( function () {
	'use strict';

	var AREAS = {
		habitos: 'hábitos',
		accesibilidad: 'accesibilidad',
		proyectos: 'proyectos',
		nose: 'todavía'
	};

	function normalizar( texto ) {
		return ( texto || '' ).toString().toLowerCase().normalize( 'NFD' ).replace( /[̀-ͯ]/g, '' );
	}

	function preseleccionarArea() {
		var params = new URLSearchParams( window.location.search );
		var area = params.get( 'area' );
		if ( ! area || ! AREAS[ area ] ) {
			return;
		}
		var clave = normalizar( AREAS[ area ] );
		var radios = document.querySelectorAll( '.wp-block-kadence-advanced-form input[type="radio"]' );
		for ( var i = 0; i < radios.length; i++ ) {
			var label = document.querySelector( 'label[for="' + radios[ i ].id + '"]' );
			var texto = normalizar( radios[ i ].value + ' ' + ( label ? label.textContent : '' ) );
			if ( texto.indexOf( clave ) !== -1 ) {
				radios[ i ].checked = true;
				radios[ i ].dispatchEvent( new Event( 'change', { bubbles: true } ) );
				break;
			}
		}
	}

	function registrarConsulta( evento ) {
		var detalle = ( evento && evento.detail ) || {};
		var area = new URLSearchParams( window.location.search ).get( 'area' ) || '';
		var datos = { event: 'generate_lead', form_id: detalle.uniqueId || '', area: area };
		window.dataLayer = window.dataLayer || [];
		window.dataLayer.push( datos );
		if ( typeof window.gtag === 'function' ) {
			window.gtag( 'event', 'generate_lead', { form_id: datos.form_id, area: area } );
		}
	}

	function iniciar() {
		preseleccionarArea();
		document.body.addEventListener( 'kb-advanced-form-success', registrarConsulta );
	}

	if ( document.readyState === 'loading' ) {
		document.addEventListener( 'DOMContentLoaded', iniciar );
	} else {
		iniciar();
	}
}() );
