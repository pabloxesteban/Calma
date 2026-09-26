<?php
/**
 * Renderiza con el código real del plugin (includes/conversion.php) la caja de
 * consulta de cada entrada del snapshot, usando stubs mínimos de WordPress.
 * Uso: php staging/preview/php/render-cta.php > salida.json
 */
define( 'ABSPATH', '/' );
$root = dirname( __DIR__, 3 );
define( 'CALMA_DIR', $root . '/wp-content/plugins/codigo-calma/' );
define( 'CALMA_URL', 'https://codigocalma.com/wp-content/plugins/codigo-calma/' );
$GLOBALS['F'] = array(); $GLOBALS['CATS'] = array(); $GLOBALS['META'] = array();
function apply_filters( $n, $v ) { return $v; }
function add_filter( $n, $f, $p = 10 ) { $GLOBALS['F'][ $n ][] = $f; }
function add_action() {}
function add_shortcode() {}
function home_url( $p = '' ) { return 'https://codigocalma.com' . $p; }
function add_query_arg( $k, $v, $u ) { return $u . '?' . $k . '=' . $v; }
function get_post_meta( $id, $k, $s ) { return $GLOBALS['META'][ $id ][ $k ] ?? ''; }
function sanitize_key( $k ) { return strtolower( $k ); }
function wp_get_post_categories( $id, $a ) { return $GLOBALS['CATS'][ $id ] ?? array(); }
function get_option( $k, $d = '' ) { return $d; }
function esc_url( $u ) { return htmlspecialchars( $u, ENT_QUOTES ); }
function esc_html( $s ) { return htmlspecialchars( $s, ENT_QUOTES ); }
function esc_attr( $s ) { return htmlspecialchars( $s, ENT_QUOTES ); }
function absint( $v ) { return abs( (int) $v ); }
function get_post_status( $i ) { return 'publish'; }
function do_blocks( $b ) { return ''; }
function is_singular( $t ) { return true; }
function in_the_loop() { return true; }
function is_main_query() { return true; }
$GLOBALS['ID'] = 0;
function get_the_ID() { return $GLOBALS['ID']; }
require CALMA_DIR . 'includes/conversion.php';

$api   = $root . '/docs/auditoria/snapshot-2026-09-26/api/';
$cats  = array_column( json_decode( file_get_contents( $api . 'cats.json' ), true ), 'slug', 'id' );
$posts = json_decode( file_get_contents( $api . 'posts.json' ), true );
// Cambios que la guía indica hacer en WordPress (Etapa 1 K01 y Etapa 3).
$overrides = json_decode( file_get_contents( $root . '/contenido/etapa-3/cta-por-entrada.json' ), true );
$out = array();
foreach ( $posts as $p ) {
	$GLOBALS['ID'] = $p['id'];
	$slugs = array_map( fn( $c ) => $cats[ $c ], $p['categories'] );
	if ( isset( $overrides['categorias'][ $p['slug'] ] ) ) {
		$slugs = $overrides['categorias'][ $p['slug'] ];
	}
	$GLOBALS['CATS'][ $p['id'] ] = $slugs;
	if ( isset( $overrides['area'][ $p['slug'] ] ) ) {
		$GLOBALS['META'][ $p['id'] ]['calma_cta_area'] = $overrides['area'][ $p['slug'] ];
	}
	$out[ $p['slug'] ] = ( $GLOBALS['F']['the_content'][0] )( '' );
}
echo json_encode( $out, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );
