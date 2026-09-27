<?php
/**
 * Código Calma — Mapa de temas (Etapa 7).
 *
 * Los seis temas salen de data/mapa-temas.json (generado por
 * contenido/etapa-7/generar-bloques.py a partir de la taxonomía de la Etapa 5).
 * Los artículos se leen de WordPress: cada entrada publicada con su categoría
 * y sus etiquetas, así lo nuevo aparece solo. Dos temas (o dos artículos) se
 * unen por las etiquetas que comparten. No se inventan temas ni artículos.
 *
 * - [calma_mapa]: mapa completo (Inicio, Blog, página pilar).
 * - "Sigue explorando": al final de cada entrada, el artículo en el centro y
 *   los más conectados alrededor (misma categoría y etiquetas en común).
 *
 * Sin JavaScript todo se lee como listas; calma-organismo.js agrega el mapa.
 *
 * @package codigo-calma
 */

defined( 'ABSPATH' ) || exit;

/**
 * Datos del mapa (una vez por petición).
 *
 * data/mapa-temas.json define los seis temas (textos, posición y qué
 * categorías del blog abarca cada uno). Los artículos, en cambio, se leen de
 * WordPress: cada entrada publicada con su categoría y sus etiquetas. Así, lo
 * que Tatiana publique aparece solo en el mapa y en "Sigue explorando".
 * Sin WordPress (vista previa), se usan los artículos del JSON.
 */
function calma_mapa_datos() {
	static $datos = null;
	if ( null !== $datos ) {
		return $datos;
	}
	$archivo = CALMA_DIR . 'data/mapa-temas.json';
	$datos   = is_readable( $archivo ) ? json_decode( (string) file_get_contents( $archivo ), true ) : array();
	$datos   = is_array( $datos ) ? $datos : array();
	if ( function_exists( 'get_posts' ) && function_exists( 'get_transient' ) ) {
		$vivos = get_transient( 'calma_mapa_articulos' );
		if ( false === $vivos ) {
			$vivos = calma_mapa_articulos_de_wordpress( $datos );
			set_transient( 'calma_mapa_articulos', $vivos, DAY_IN_SECONDS );
		}
		if ( $vivos ) {
			$datos = calma_mapa_con_articulos( $datos, $vivos );
		}
	}
	$datos = apply_filters( 'calma_mapa_datos', $datos );
	return $datos;
}

/** Entradas publicadas con su categoría principal y sus etiquetas. */
function calma_mapa_articulos_de_wordpress( $datos ) {
	$tema_de = array();
	foreach ( (array) ( $datos['temas'] ?? array() ) as $t ) {
		foreach ( (array) $t['categorias'] as $c ) {
			$tema_de[ $c ] = $t['k'];
		}
	}
	$out     = array();
	$entradas = get_posts( array( 'post_type' => 'post', 'post_status' => 'publish', 'numberposts' => 200, 'orderby' => 'date', 'order' => 'DESC' ) );
	foreach ( $entradas as $p ) {
		$cats = get_the_category( $p->ID );
		$cat  = null;
		foreach ( $cats as $c ) {
			if ( isset( $tema_de[ $c->slug ] ) ) {
				$cat = $c;
				break;
			}
		}
		$cat  = $cat ?: ( $cats[0] ?? null );
		$tags = wp_get_post_tags( $p->ID );
		$out[ $p->post_name ] = array(
			'titulo'           => get_the_title( $p ),
			'categoria'        => $cat ? $cat->slug : '',
			'categoria_nombre' => $cat ? $cat->name : '',
			'tema'             => ( $cat && isset( $tema_de[ $cat->slug ] ) ) ? $tema_de[ $cat->slug ] : 'ciberpsicologia',
			'etiquetas'        => wp_list_pluck( $tags, 'slug' ),
			'etiquetas_nombres' => wp_list_pluck( $tags, 'name', 'slug' ),
		);
	}
	return $out;
}

/** Reemplaza los artículos del JSON por los de WordPress y rearma cada tema. */
function calma_mapa_con_articulos( $datos, $articulos ) {
	foreach ( $articulos as $a ) {
		foreach ( (array) ( $a['etiquetas_nombres'] ?? array() ) as $slug => $nombre ) {
			$datos['etiquetas'][ $slug ] = $nombre;
		}
	}
	$datos['articulos'] = $articulos;
	foreach ( $datos['temas'] as $i => $t ) {
		$datos['temas'][ $i ]['articulos'] = array_keys( array_filter( $articulos, function ( $a ) use ( $t ) {
			return $a['tema'] === $t['k'];
		} ) );
	}
	return $datos;
}

/** Al publicar, editar o borrar una entrada, el mapa se vuelve a calcular. */
foreach ( array( 'save_post_post', 'deleted_post', 'edited_category', 'edited_post_tag' ) as $calma_evento ) {
	add_action( $calma_evento, function () {
		delete_transient( 'calma_mapa_articulos' );
	} );
}

/** Etiquetas (nombres) que comparten dos listas de slugs. */
function calma_mapa_comunes( $a, $b ) {
	$d = calma_mapa_datos();
	$n = array();
	foreach ( array_intersect( (array) $a, (array) $b ) as $slug ) {
		$n[] = $d['etiquetas'][ $slug ] ?? $slug;
	}
	sort( $n );
	return $n;
}

/** Etiquetas de todos los artículos de un tema. */
function calma_mapa_etiquetas_tema( $tema ) {
	$d   = calma_mapa_datos();
	$out = array();
	foreach ( (array) $tema['articulos'] as $slug ) {
		$out = array_merge( $out, (array) ( $d['articulos'][ $slug ]['etiquetas'] ?? array() ) );
	}
	return array_values( array_unique( $out ) );
}

/** Minúsculas con la primera en mayúscula ("Atención, hábitos"). */
function calma_mapa_lista( $nombres ) {
	$t = function_exists( 'mb_strtolower' ) ? mb_strtolower( implode( ', ', $nombres ) ) : strtolower( implode( ', ', $nombres ) );
	return function_exists( 'mb_strtoupper' ) ? mb_strtoupper( mb_substr( $t, 0, 1 ) ) . mb_substr( $t, 1 ) : ucfirst( $t );
}

/** Uniones del mapa completo: el centro con todos y los temas entre sí. */
function calma_mapa_aristas() {
	$d      = calma_mapa_datos();
	$temas  = (array) ( $d['temas'] ?? array() );
	$centro = $temas[0] ?? null;
	$out    = array();
	if ( ! $centro ) {
		return $out;
	}
	$borde = array_slice( $temas, 1 );
	foreach ( $borde as $t ) {
		$out[] = array( $centro, $t, array() );
	}
	$n = count( $borde );
	for ( $i = 0; $i < $n; $i++ ) {
		for ( $j = $i + 1; $j < $n; $j++ ) {
			$comun = calma_mapa_comunes( calma_mapa_etiquetas_tema( $borde[ $i ] ), calma_mapa_etiquetas_tema( $borde[ $j ] ) );
			if ( $comun ) {
				$out[] = array( $borde[ $i ], $borde[ $j ], $comun );
			}
		}
	}
	return $out;
}

/** Trazo de una unión: recta desde el centro, curva hacia adentro entre temas del borde. */
function calma_mapa_curva( $a, $b ) {
	if ( 'ciberpsicologia' === $a['k'] ) {
		return sprintf( 'M%s %s L%s %s', $a['x'], $a['y'], $b['x'], $b['y'] );
	}
	$mx = ( $a['x'] + $b['x'] ) / 2;
	$my = ( $a['y'] + $b['y'] ) / 2;
	return sprintf( 'M%s %s Q%.1f %.1f %s %s', $a['x'], $a['y'], $mx + ( 50 - $mx ) * 0.35, $my + ( 50 - $my ) * 0.35, $b['x'], $b['y'] );
}

/** Mapa completo de temas. */
function calma_mapa_html() {
	$d = calma_mapa_datos();
	if ( empty( $d['temas'] ) ) {
		return '';
	}
	$aristas = calma_mapa_aristas();
	$lineas  = '';
	foreach ( $aristas as $n => $ar ) {
		list( $a, $b, $c ) = $ar;
		$trazo   = calma_mapa_curva( $a, $b );
		$lineas .= sprintf(
			'<path class="calma-mapa__arista" data-a="%1$s" data-b="%2$s" style="--i:%3$d;--peso:%4$d" pathLength="1" d="%5$s"/><path class="calma-mapa__senal" data-a="%1$s" data-b="%2$s" pathLength="1" d="%5$s"/>',
			esc_attr( $a['k'] ),
			esc_attr( $b['k'] ),
			$n,
			max( 1, count( $c ) ),
			esc_attr( $trazo )
		);
	}
	$nodos   = '';
	$paneles = '';
	foreach ( $d['temas'] as $t ) {
		$centro = 'ciberpsicologia' === $t['k'];
		$nodos .= sprintf(
			'<button type="button" class="calma-mapa__nodo%1$s" style="--x:%2$s;--y:%3$s" data-tema="%4$s" aria-controls="tema-%4$s" aria-pressed="false"><span class="calma-mapa__punto" aria-hidden="true"></span><span class="calma-mapa__nombre">%5$s</span></button>',
			$centro ? ' calma-mapa__nodo--centro' : '',
			esc_attr( $t['x'] ),
			esc_attr( $t['y'] ),
			esc_attr( $t['k'] ),
			esc_html( $t['nombre'] )
		);
		// Con qué se conecta (las tres uniones más fuertes).
		$conecta = array();
		foreach ( $aristas as $ar ) {
			list( $a, $b, $comun ) = $ar;
			if ( ! $comun || ! in_array( $t['k'], array( $a['k'], $b['k'] ), true ) ) {
				continue;
			}
			$otro      = $a['k'] === $t['k'] ? $b : $a;
			$conecta[] = array( count( $comun ), sprintf( '<li><strong>%s</strong><span>%s</span></li>', esc_html( $otro['nombre'] ), esc_html( calma_mapa_lista( array_slice( $comun, 0, 3 ) ) ) ) );
		}
		usort( $conecta, function ( $x, $y ) {
			return $y[0] - $x[0];
		} );
		$conecta = array_slice( wp_list_pluck( $conecta, 1 ), 0, 3 );
		$arts    = '';
		foreach ( (array) $t['articulos'] as $slug ) {
			$arts .= sprintf( '<li><a href="%s">%s</a></li>', esc_url( home_url( '/' . $slug . '/' ) ), esc_html( $d['articulos'][ $slug ]['titulo'] ?? $slug ) );
		}
		$enlaces = '';
		foreach ( (array) $t['enlaces'] as $e ) {
			$enlaces .= sprintf( '<a class="calma-link" href="%s">%s</a>', esc_url( home_url( $e[1] ) ), esc_html( $e[0] ) );
		}
		$sub      = ( ! $centro && $t['sub'] !== $t['nombre'] ) ? ' <span class="calma-mapa__sub">· ' . esc_html( $t['sub'] ) . '</span>' : '';
		$paneles .= '<article class="calma-mapa__panel" id="tema-' . esc_attr( $t['k'] ) . '" data-tema="' . esc_attr( $t['k'] ) . '" aria-labelledby="tema-' . esc_attr( $t['k'] ) . '-titulo">'
			. '<div class="calma-mapa__panel-cabeza"><h3 id="tema-' . esc_attr( $t['k'] ) . '-titulo">' . esc_html( $t['nombre'] ) . $sub . '</h3>'
			. '<p class="calma-mapa__texto">' . esc_html( $t['texto'] ) . '</p></div>'
			. '<div class="calma-mapa__panel-cuerpo">'
			. ( $arts ? '<p class="calma-mapa__rotulo">Artículos</p><ul class="calma-mapa__articulos">' . $arts . '</ul>' : '' )
			. ( $conecta ? '<p class="calma-mapa__rotulo">Se conecta con</p><ul class="calma-mapa__conexiones">' . implode( '', $conecta ) . '</ul>' : '' )
			. '<p class="calma-mapa__enlaces">' . $enlaces . '</p></div></article>';
	}
	return '<section class="calma-mapa" id="mapa-temas" aria-labelledby="mapa-titulo">'
		. '<div class="calma-mapa__head"><h2 id="mapa-titulo">Explora por <em>temas</em></h2>'
		. '<p class="calma-sub">La ciberpsicología está en el centro: cruza la psicología con la tecnología. Elige un tema para ver sus artículos y con qué se conecta.</p></div>'
		. '<div class="calma-mapa__cuerpo">'
		. '<div class="calma-mapa__grafo" hidden><svg class="calma-mapa__svg" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true" focusable="false">' . $lineas . '</svg>'
		. '<div class="calma-mapa__nodos" role="group" aria-label="Temas del mapa">' . $nodos . '</div></div>'
		. '<div class="calma-mapa__paneles" aria-live="polite">' . $paneles . '</div>'
		. '</div></section>';
}
add_shortcode( 'calma_mapa', 'calma_mapa_html' );

/**
 * Artículos más conectados con uno: 2 puntos si comparten categoría y 1 por
 * cada etiqueta en común. Solo entran los que tienen alguna conexión.
 */
function calma_mapa_relacionados( $slug, $max = 4 ) {
	$d    = calma_mapa_datos();
	$base = $d['articulos'][ $slug ] ?? null;
	if ( ! $base ) {
		return array();
	}
	$lista = array();
	foreach ( (array) $d['articulos'] as $otro => $a ) {
		if ( $otro === $slug ) {
			continue;
		}
		$comun  = calma_mapa_comunes( $base['etiquetas'], $a['etiquetas'] );
		$misma  = $a['categoria'] === $base['categoria'];
		$puntos = count( $comun ) + ( $misma ? 2 : 0 );
		if ( $puntos > 0 ) {
			$lista[] = array( 'slug' => $otro, 'puntos' => $puntos, 'comun' => $comun, 'misma' => $misma, 'a' => $a );
		}
	}
	usort( $lista, function ( $x, $y ) {
		return $y['puntos'] - $x['puntos'] ?: strcmp( $x['a']['titulo'], $y['a']['titulo'] );
	} );
	return array_slice( $lista, 0, $max );
}

/** "Sigue explorando": el artículo en el centro y sus conexiones alrededor. */
function calma_mapa_articulo_html( $slug ) {
	$d    = calma_mapa_datos();
	$base = $d['articulos'][ $slug ] ?? null;
	$rel  = calma_mapa_relacionados( $slug );
	if ( ! $base || ! $rel ) {
		return '';
	}
	$temas = array();
	foreach ( (array) $d['temas'] as $t ) {
		$temas[ $t['k'] ] = $t;
	}
	// Posiciones alrededor del centro (viewBox 100 × 64).
	$pos    = array( array( 16, 14 ), array( 84, 14 ), array( 16, 50 ), array( 84, 50 ) );
	$lineas = '';
	$puntos = '';
	$items  = '';
	foreach ( $rel as $i => $r ) {
		list( $x, $y ) = $pos[ $i ];
		$trazo   = sprintf( 'M50 32 Q%.1f %.1f %s %s', ( 50 + $x ) / 2, ( 32 + $y ) / 2 + ( $y < 32 ? 6 : -6 ), $x, $y );
		$lineas .= sprintf( '<path class="calma-explora__arista" data-i="%1$d" style="--peso:%2$d" pathLength="1" d="%3$s"/><path class="calma-explora__senal" data-i="%1$d" pathLength="1" d="%3$s"/>', $i, $r['puntos'], $trazo );
		$puntos .= sprintf( '<circle class="calma-explora__nodo" data-i="%d" cx="%s" cy="%s" r="2.6"/>', $i, $x, $y );
		$tema    = $temas[ $r['a']['tema'] ]['nombre'] ?? '';
		$porque  = $r['comun'] ? 'Comparten: ' . calma_mapa_lista( array_slice( $r['comun'], 0, 3 ) ) : 'Mismo tema';
		$items  .= sprintf(
			'<li data-i="%1$d"><a href="%2$s"><span class="calma-explora__tema">%3$s</span><span class="calma-explora__titulo">%4$s</span><span class="calma-explora__porque">%5$s</span></a></li>',
			$i,
			esc_url( home_url( '/' . $r['slug'] . '/' ) ),
			esc_html( $tema ),
			esc_html( $r['a']['titulo'] ),
			esc_html( $porque )
		);
	}
	$tema_base = $temas[ $base['tema'] ] ?? null;
	$enlace    = sprintf( '<a class="calma-link" href="%s">Más de %s</a>', esc_url( home_url( '/category/' . $base['categoria'] . '/' ) ), esc_html( $base['categoria_nombre'] ) );
	return '<section class="calma-explora" aria-labelledby="explora-titulo">'
		. '<h2 id="explora-titulo">Sigue <em>explorando</em></h2>'
		. '<p class="calma-explora__intro">Artículos conectados con este por los temas que comparten.</p>'
		. '<div class="calma-explora__cuerpo">'
		. '<svg class="calma-explora__svg" viewBox="0 0 100 64" aria-hidden="true" focusable="false">' . $lineas . $puntos
		. '<circle class="calma-explora__centro" cx="50" cy="32" r="5"/><circle class="calma-explora__halo" cx="50" cy="32" r="8.5"/></svg>'
		. '<ol class="calma-explora__lista">' . $items . '</ol></div>'
		. '<p class="calma-explora__enlaces">' . $enlace . ' <a class="calma-link" href="' . esc_url( home_url( '/#mapa-temas' ) ) . '">Ver el mapa de temas</a></p>'
		. '</section>';
}

/** Agrega "Sigue explorando" al final de cada entrada (antes de la caja de consulta). */
add_filter( 'the_content', function ( $contenido ) {
	if ( ! is_singular( 'post' ) || ! in_the_loop() || ! is_main_query() ) {
		return $contenido;
	}
	$slug = get_post_field( 'post_name', get_the_ID() );
	return $contenido . calma_mapa_articulo_html( $slug );
}, 18 );
