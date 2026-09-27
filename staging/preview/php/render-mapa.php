<?php
/**
 * Renderiza con el código real del plugin (includes/mapa.php) el mapa de temas
 * ([calma_mapa]) y el "Sigue explorando" de cada entrada, con stubs mínimos de
 * WordPress. Uso: php staging/preview/php/render-mapa.php > salida.json
 */
define( 'ABSPATH', '/' );
$root = dirname( __DIR__, 3 );
define( 'CALMA_DIR', $root . '/wp-content/plugins/codigo-calma/' );
function apply_filters( $n, $v ) { return $v; }
function add_filter() {}
function add_shortcode() {}
function home_url( $p = '' ) { return 'https://codigocalma.com' . $p; }
function esc_url( $u ) { return htmlspecialchars( $u, ENT_QUOTES ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function wp_list_pluck( $l, $f ) { return array_column( $l, $f ); }
require CALMA_DIR . 'includes/mapa.php';

$out = array( 'mapa' => calma_mapa_html(), 'articulos' => array() );
foreach ( array_keys( calma_mapa_datos()['articulos'] ) as $slug ) {
	$out['articulos'][ $slug ] = calma_mapa_articulo_html( $slug );
}
echo json_encode( $out, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
