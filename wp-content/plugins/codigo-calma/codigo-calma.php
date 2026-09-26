<?php
/**
 * Plugin Name:       Código Calma
 * Description:       Design system (tokens calma-*) y correcciones del sitio sobre el tema Kadence, sin tema hijo (así se conservan los ajustes del Personalizador).
 * Version:           1.2.0-etapa3
 * Requires at least: 6.4
 * Requires PHP:      8.0
 * Author:            Código Calma
 * Text Domain:       codigo-calma
 *
 * Etapa 1: tokens + correcciones críticas de maquetación, contraste y
 * animaciones. Ver docs/implementacion/etapa-1.md.
 */

defined( 'ABSPATH' ) || exit;

define( 'CALMA_VERSION', '1.2.0-etapa3' );
define( 'CALMA_URL', plugin_dir_url( __FILE__ ) );
define( 'CALMA_DIR', plugin_dir_path( __FILE__ ) );

/**
 * Estilos: se cargan después de los de Kadence para que los tokens
 * `--calma-*` puedan sobrescribir su paleta global.
 */
add_action( 'wp_enqueue_scripts', function () {
	$uri = CALMA_URL . 'assets/css/';
	$dir = CALMA_DIR . 'assets/css/';
	$dep = wp_style_is( 'kadence-global', 'registered' ) ? array( 'kadence-global' ) : array();

	wp_enqueue_style(
		'calma-tokens',
		$uri . 'calma-tokens.css',
		$dep,
		filemtime( $dir . 'calma-tokens.css' )
	);
	wp_enqueue_style( 'calma-fonts', $uri . 'calma-fonts.css', array(), filemtime( $dir . 'calma-fonts.css' ) );
	wp_enqueue_style( 'calma-etapa1', $uri . 'calma-etapa1.css', array( 'calma-tokens' ), filemtime( $dir . 'calma-etapa1.css' ) );
	wp_enqueue_style( 'calma-etapa2', $uri . 'calma-etapa2.css', array( 'calma-etapa1', 'calma-fonts' ), filemtime( $dir . 'calma-etapa2.css' ) );
}, 20 );

/**
 * Animaciones de entrada (plugin "Blocks Animation" de Otter).
 * Dejan contenido invisible (`visibility: hidden`) o desplazado fuera de
 * pantalla en mobile. Lo recomendado es desactivar el plugin; esto es la red
 * de seguridad por si queda activo. El plugin encola sus archivos durante
 * render_block, así que se quitan justo antes de imprimir el pie.
 * El CSS de calma-etapa1.css además neutraliza la clase .animated.
 */
add_action( 'wp_footer', function () {
	foreach ( array( 'otter-animation-frontend', 'otter-typing', 'otter-count' ) as $handle ) {
		wp_dequeue_script( $handle );
	}
	wp_dequeue_style( 'otter-animation' );
}, 5 );

/**
 * Contact Form 7 está instalado pero ningún formulario lo usa: el de
 * /contacto/ es un Kadence Advanced Form. Evita cargar su CSS/JS en todo el sitio.
 */
add_filter( 'wpcf7_load_js', '__return_false' );
add_filter( 'wpcf7_load_css', '__return_false' );

/**
 * Página de entradas (/blog/): el título está oculto en Kadence y la página
 * queda sin H1. Lo ideal es activarlo en Personalizar > Blog > Archivo;
 * si sigue oculto, se imprime uno aquí.
 */
add_action( 'kadence_before_main_content', function () {
	if ( ! is_home() || is_front_page() || ! function_exists( 'Kadence\\kadence' ) ) {
		return;
	}
	$layout = \Kadence\kadence();
	if ( $layout->show_in_content_title() || $layout->show_hero_title() ) {
		return;
	}
	$page_id = (int) get_option( 'page_for_posts' );
	printf(
		'<header class="calma-archive-header"><h1 class="calma-archive-title">%s</h1></header>',
		esc_html( $page_id ? get_the_title( $page_id ) : __( 'Blog', 'codigo-calma' ) )
	);
} );

/**
 * Etapa 2 · Fuentes locales: se deja de pedir Google Fonts (Kadence carga Lora,
 * Inter y Jost desde fonts.googleapis.com) y se precargan las dos que usa el
 * primer render. Equivale a elegir "Inherit"/fuentes del sistema en el
 * Personalizador y a activar "Cargar fuentes localmente".
 */
// Kadence (tema) entrega sus fuentes a Kadence Blocks, que imprime un único
// <link id="kadence-fonts-gfonts-css"> en wp_head (prioridad 90) y wp_footer.
add_filter( 'kadence_blocks_print_google_fonts', '__return_false' );
add_filter( 'kadence_blocks_print_footer_google_fonts', '__return_false' );

add_action( 'wp_head', function () {
	foreach ( array( 'inter-latin-wght-normal.woff2', 'lora-latin-wght-normal.woff2' ) as $font ) {
		printf(
			'<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' . "\n",
			esc_url( CALMA_URL . 'assets/fonts/' . $font )
		);
	}
}, 1 );

/**
 * Etapa 2 · Logo: se muestra a 48 px pero WordPress declara sizes="100vw" y el
 * navegador descarga la versión de 512 px. Con sizes="48px" baja la de 150 px.
 */
add_filter( 'get_custom_logo_image_attributes', function ( $attr ) {
	$attr['sizes'] = '48px';
	return $attr;
} );

// Etapa 3 · Flujo de consulta (caja al final de artículos, newsletter, área preseleccionada).
require_once CALMA_DIR . 'includes/conversion.php';
