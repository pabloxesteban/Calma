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
function get_permalink( $p = 0 ) { return ''; }
function wp_list_pluck( $l, $f ) { return array_column( $l, $f ); }
function get_query_var( $v ) { return ''; }
function status_header() {}
function add_rewrite_rule() {}
function get_transient() { return false; }
function set_transient() {}
function delete_transient() {}
function get_queried_object_id() { return $GLOBALS['ID']; }
function sanitize_textarea_field( $s ) { return $s; }
function wp_json_encode( $d, $f = 0 ) { return json_encode( $d, $f ); }
function is_page() { return false; }
require CALMA_DIR . 'includes/conversion.php';
if ( in_array( '--geo', $argv, true ) ) {
	require CALMA_DIR . 'includes/geo.php';
}

$api   = $root . '/docs/auditoria/snapshot-2026-09-26/api/';
$cats  = array_column( json_decode( file_get_contents( $api . 'cats.json' ), true ), 'slug', 'id' );
$posts = json_decode( file_get_contents( $api . 'posts.json' ), true );
// Cambios que la guía indica hacer en WordPress (Etapa 1 K01 y Etapa 3).
$overrides = json_decode( file_get_contents( $root . '/contenido/etapa-3/cta-por-entrada.json' ), true );
$geo = in_array( '--geo', $argv, true ) ? json_decode( file_get_contents( $root . '/contenido/etapa-5/articulos.json' ), true ) : null;
$por_slug = array();
foreach ( (array) ( $geo['articulos'] ?? array() ) as $a ) {
	$por_slug[ $a['slug'] ] = $a;
}
$taxo = in_array( '--geo', $argv, true ) ? json_decode( file_get_contents( $root . '/contenido/etapa-5/taxonomia.json' ), true ) : null;
$nueva_cat = array();
foreach ( (array) ( $taxo['asignacion'] ?? array() ) as $as ) {
	$nueva_cat[ $as['slug_entrada'] ] = array( $as['categoria'] );
}
$mapa_taxo = array();
foreach ( (array) ( $taxo['categorias'] ?? array() ) as $c ) {
	$mapa_taxo[ $c['slug'] ] = $c['area_cta'];
}
if ( $mapa_taxo ) {
	add_filter( 'calma_cta_area_por_categoria', fn( $m ) => array_merge( $m, $mapa_taxo ) );
}
$out = array();
foreach ( $posts as $p ) {
	$GLOBALS['ID'] = $p['id'];
	$slugs = array_map( fn( $c ) => $cats[ $c ], $p['categories'] );
	if ( isset( $overrides['categorias'][ $p['slug'] ] ) ) {
		$slugs = $overrides['categorias'][ $p['slug'] ];
	}
	$GLOBALS['CATS'][ $p['id'] ] = $slugs;
	if ( isset( $nueva_cat[ $p['slug'] ] ) ) {
		$GLOBALS['CATS'][ $p['id'] ] = $nueva_cat[ $p['slug'] ];
	}
	if ( isset( $por_slug[ $p['slug'] ] ) ) {
		// Igual que calma_geo_importar(): solo fuentes verificadas y definiciones adaptadas.
		$a = $por_slug[ $p['slug'] ];
		$GLOBALS['META'][ $p['id'] ]['calma_resumen'] = $a['resumen'];
		if ( ( $a['definicion']['tipo'] ?? '' ) === 'adaptada' ) {
			$GLOBALS['META'][ $p['id'] ]['calma_definicion'] = $a['definicion']['texto'];
		}
		$f = array_values( array_filter( $a['fuentes'], fn( $x ) => 'verificada' === $x['estado'] ) );
		if ( $f ) {
			$GLOBALS['META'][ $p['id'] ]['calma_fuentes'] = json_encode( array_map( fn( $x ) => array( 'texto' => $x['texto'], 'url' => $x['url'] ?? '' ), $f ), JSON_UNESCAPED_UNICODE );
		}
	}
	if ( isset( $overrides['area'][ $p['slug'] ] ) ) {
		$GLOBALS['META'][ $p['id'] ]['calma_cta_area'] = $overrides['area'][ $p['slug'] ];
	}
	$html = 'MARCADOR_CONTENIDO';
	foreach ( $GLOBALS['F']['the_content'] as $fn ) {
		$html = $fn( $html );
	}
	list( $antes, $despues ) = explode( 'MARCADOR_CONTENIDO', $html );
	$out[ $p['slug'] ] = array( 'antes' => $antes, 'despues' => $despues );
}
echo json_encode( $out, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );
