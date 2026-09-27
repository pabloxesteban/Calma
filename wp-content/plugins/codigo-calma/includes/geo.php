<?php
/**
 * Código Calma — Etapa 5: GEO y estructura del blog.
 *
 * - /llms.txt generado desde el contenido publicado (se actualiza solo).
 * - Caja "En resumen" (campo `calma_resumen`, opcional `calma_definicion`) al
 *   inicio de cada entrada y sección "Fuentes" (campo `calma_fuentes`, JSON
 *   [{texto,url}]) al final; ambos alimentan el JSON-LD (abstract, citation).
 * - `wp calma geo-import`: carga resúmenes, definiciones, fuentes verificadas y
 *   niveles de encabezado desde data/articulos.json.
 * - `wp calma taxonomia`: aplica data/taxonomia.json (categorías, etiquetas,
 *   asignación, limpieza y redirecciones 301 en Rank Math).
 * Ambas herramientas tienen vista previa en Herramientas → Código Calma: blog.
 */

defined( 'ABSPATH' ) || exit;

/* ---------------------------------------------------------------------------
 * 1. llms.txt
 * ------------------------------------------------------------------------- */

add_action( 'init', function () {
	add_rewrite_rule( '^llms\.txt$', 'index.php?calma_llms=1', 'top' );
	// Reescrituras nuevas tras actualizar el plugin (una sola vez por versión).
	if ( get_option( 'calma_rewrite_version' ) !== CALMA_VERSION ) {
		flush_rewrite_rules( false );
		update_option( 'calma_rewrite_version', CALMA_VERSION );
	}
} );
add_filter( 'query_vars', fn( $v ) => array_merge( $v, array( 'calma_llms' ) ) );
add_filter( 'redirect_canonical', fn( $url ) => get_query_var( 'calma_llms' ) ? false : $url );

function calma_llms_descripcion( $post ) {
	$texto = get_post_meta( $post->ID, 'calma_resumen', true )
		?: get_post_meta( $post->ID, 'rank_math_description', true )
		?: wp_strip_all_tags( get_the_excerpt( $post ) );
	return trim( preg_replace( '/\s+/', ' ', (string) $texto ) );
}

function calma_llms_linea( $post ) {
	$desc = calma_llms_descripcion( $post );
	return sprintf( '- [%s](%s)%s', wp_strip_all_tags( get_the_title( $post ) ), get_permalink( $post ), $desc ? ': ' . $desc : '' );
}

function calma_llms_contenido() {
	$cache = get_transient( 'calma_llms' );
	if ( $cache ) {
		return $cache;
	}
	$l   = array();
	$l[] = '# Código Calma';
	$l[] = '';
	$l[] = '> Portal de ciberpsicología en español: cómo la tecnología influye en la conducta, la atención y el bienestar, con artículos basados en investigación y acompañamiento uno a uno (online, una persona por vez).';
	$l[] = '';
	$l[] = 'Idioma: español. Contacto: hola@codigocalma.com. Los artículos son divulgativos y no reemplazan una evaluación ni un tratamiento profesional.';
	$l[] = '';
	$l[] = '## Equipo';
	foreach ( calma_schema_personas() as $p ) {
		$l[] = sprintf( '- [%s](%s): %s', $p['name'], $p['url'], $p['description'] );
	}
	$l[] = '';
	$l[] = '## Servicios';
	foreach ( array( 'servicios', 'contacto' ) as $ruta ) {
		$page = get_page_by_path( $ruta );
		if ( $page && 'publish' === $page->post_status ) {
			$l[] = calma_llms_linea( $page );
		}
	}
	$l[] = '';
	$l[] = '## Guías principales';
	foreach ( array( 'ciberpsicologia', 'bienestar-digital', 'herramientas', 'test', 'descargas' ) as $ruta ) {
		$page = get_page_by_path( $ruta );
		if ( $page && 'publish' === $page->post_status ) {
			$l[] = calma_llms_linea( $page );
		}
	}
	$cats = get_categories( array( 'hide_empty' => true ) );
	if ( $cats ) {
		$l[] = '';
		$l[] = '## Temas del blog';
		foreach ( $cats as $c ) {
			$desc = trim( preg_replace( '/\s+/', ' ', wp_strip_all_tags( $c->description ) ) );
			$l[] = sprintf( '- [%s](%s)%s', $c->name, get_category_link( $c ), $desc ? ': ' . wp_trim_words( $desc, 30, '…' ) : '' );
		}
	}
	$l[] = '';
	$l[] = '## Artículos';
	foreach ( get_posts( array( 'numberposts' => 200, 'post_status' => 'publish' ) ) as $post ) {
		$l[] = calma_llms_linea( $post );
	}
	$l[] = '';
	$l[] = '## Opcional';
	foreach ( array( 'testimonios', 'equipo' ) as $ruta ) {
		$page = get_page_by_path( $ruta );
		if ( $page && 'publish' === $page->post_status ) {
			$l[] = calma_llms_linea( $page );
		}
	}
	$out = implode( "\n", $l ) . "\n";
	set_transient( 'calma_llms', $out, DAY_IN_SECONDS );
	return $out;
}

add_action( 'save_post', fn() => delete_transient( 'calma_llms' ) );
add_action( 'edited_category', fn() => delete_transient( 'calma_llms' ) );

add_action( 'template_redirect', function () {
	if ( ! get_query_var( 'calma_llms' ) ) {
		return;
	}
	status_header( 200 );
	header( 'Content-Type: text/markdown; charset=utf-8' );
	header( 'X-Robots-Tag: noindex' );
	echo calma_llms_contenido(); // phpcs:ignore WordPress.Security.EscapeOutput -- texto plano.
	exit;
} );

/* ---------------------------------------------------------------------------
 * 2. "En resumen" y "Fuentes" en las entradas
 * ------------------------------------------------------------------------- */

function calma_fuentes_de( $post_id ) {
	$fuentes = json_decode( (string) get_post_meta( $post_id, 'calma_fuentes', true ), true );
	return is_array( $fuentes ) ? array_values( array_filter( $fuentes, fn( $f ) => ! empty( $f['texto'] ) ) ) : array();
}

add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'post' ) || ! in_the_loop() || ! is_main_query() ) {
		return $content;
	}
	$id      = get_the_ID();
	$resumen = trim( (string) get_post_meta( $id, 'calma_resumen', true ) );
	$antes   = '';
	if ( $resumen ) {
		$antes = '<aside class="calma-resumen" aria-label="En resumen"><p><strong>En resumen:</strong> ' . esc_html( $resumen ) . '</p>';
		$def   = trim( (string) get_post_meta( $id, 'calma_definicion', true ) );
		if ( $def ) {
			$antes .= '<p class="calma-resumen__def">' . esc_html( $def ) . '</p>';
		}
		$antes .= '</aside>';
	}
	$despues = '';
	$fuentes = calma_fuentes_de( $id );
	if ( $fuentes ) {
		$despues = '<section class="calma-fuentes" aria-labelledby="calma-fuentes-titulo"><h2 id="calma-fuentes-titulo">Fuentes</h2><ol>';
		foreach ( $fuentes as $f ) {
			$despues .= '<li>' . esc_html( $f['texto'] );
			if ( ! empty( $f['url'] ) ) {
				$despues .= ' <a href="' . esc_url( $f['url'] ) . '" rel="noopener">' . esc_html( preg_replace( '#^https?://#', '', $f['url'] ) ) . '</a>';
			}
			$despues .= '</li>';
		}
		$despues .= '</ol></section>';
	}
	return $antes . $content . $despues;
}, 15 );

add_filter( 'calma_schema_graph', function ( $graph ) {
	if ( ! is_singular( 'post' ) ) {
		return $graph;
	}
	$id = get_queried_object_id();
	foreach ( $graph as &$nodo ) {
		if ( 'BlogPosting' !== ( $nodo['@type'] ?? '' ) ) {
			continue;
		}
		$resumen = trim( (string) get_post_meta( $id, 'calma_resumen', true ) );
		if ( $resumen ) {
			$nodo['abstract'] = $resumen;
		}
		$urls = array_values( array_filter( wp_list_pluck( calma_fuentes_de( $id ), 'url' ) ) );
		if ( $urls ) {
			$nodo['citation'] = $urls;
		}
	}
	return $graph;
} );

/* ---------------------------------------------------------------------------
 * 3. Importadores (vista previa + aplicar)
 * ------------------------------------------------------------------------- */

function calma_geo_json( $archivo ) {
	$f = CALMA_DIR . 'data/' . $archivo;
	return is_readable( $f ) ? json_decode( (string) file_get_contents( $f ), true ) : null;
}

function calma_post_por_slug( $slug ) {
	$p = get_posts( array( 'name' => $slug, 'post_type' => 'post', 'post_status' => 'any', 'numberposts' => 1 ) );
	return $p ? $p[0] : null;
}

/**
 * Sube de nivel un encabezado de bloque (h3 → h2) por su texto exacto.
 */
function calma_subir_encabezado( $contenido, $texto, $de = 3, $a = 2 ) {
	$patron = '#<!-- wp:heading \{([^}]*)"level":' . $de . '([^}]*)\} -->\s*<h' . $de . '([^>]*)>(.*?)</h' . $de . '>\s*<!-- /wp:heading -->#s';
	$cambios = 0;
	$nuevo   = preg_replace_callback( $patron, function ( $m ) use ( $texto, $de, $a, &$cambios ) {
		$plano = trim( html_entity_decode( wp_strip_all_tags( $m[4] ), ENT_QUOTES, 'UTF-8' ) );
		if ( $plano !== trim( $texto ) ) {
			return $m[0];
		}
		$cambios++;
		$attrs = trim( $m[1] . $m[2], ', ' );
		$json  = $attrs ? '{' . $attrs . '}' : '';
		if ( 2 !== $a ) {
			$json = '{' . ltrim( '"level":' . $a . ( $attrs ? ',' . $attrs : '' ), ',' ) . '}';
		}
		// Nivel 2 es el valor por defecto del bloque: se omite el atributo.
		return '<!-- wp:heading ' . ( $json ? $json . ' ' : '' ) . '--><h' . $a . $m[3] . '>' . $m[4] . '</h' . $a . '><!-- /wp:heading -->';
	}, $contenido );
	return array( $nuevo, $cambios );
}

function calma_geo_importar( $aplicar = false ) {
	$data    = calma_geo_json( 'articulos.json' );
	$informe = array();
	foreach ( (array) ( $data['articulos'] ?? array() ) as $a ) {
		$post = calma_post_por_slug( $a['slug'] );
		if ( ! $post ) {
			$informe[] = array( 'slug' => $a['slug'], 'resumen' => '-', 'fuentes' => '-', 'h2' => '-', 'estado' => 'no encontrada' );
			continue;
		}
		$fuentes = array_values( array_filter( (array) ( $a['fuentes'] ?? array() ), fn( $f ) => 'verificada' === ( $f['estado'] ?? '' ) ) );
		$fuentes = array_map( fn( $f ) => array( 'texto' => $f['texto'], 'url' => $f['url'] ?? '' ), $fuentes );
		$def     = ( $a['definicion']['tipo'] ?? '' ) === 'adaptada' ? $a['definicion']['texto'] : '';
		$contenido = $post->post_content;
		$subidos   = 0;
		foreach ( (array) ( $a['h2'] ?? array() ) as $h ) {
			$de = (int) preg_replace( '/\D/', '', (string) ( $h['nivel_actual'] ?? 'h3' ) ) ?: 3;
			$a2 = (int) preg_replace( '/\D/', '', (string) ( $h['despues_nivel'] ?? 'h2' ) ) ?: 2;
			list( $contenido, $n ) = calma_subir_encabezado( $contenido, $h['antes'], $de, $a2 );
			$subidos += $n;
		}
		if ( $aplicar ) {
			update_post_meta( $post->ID, 'calma_resumen', sanitize_textarea_field( $a['resumen'] ?? '' ) );
			$def ? update_post_meta( $post->ID, 'calma_definicion', sanitize_textarea_field( $def ) ) : delete_post_meta( $post->ID, 'calma_definicion' );
			$fuentes ? update_post_meta( $post->ID, 'calma_fuentes', wp_slash( wp_json_encode( $fuentes, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) ) ) : delete_post_meta( $post->ID, 'calma_fuentes' );
			if ( $subidos ) {
				wp_update_post( array( 'ID' => $post->ID, 'post_content' => wp_slash( $contenido ) ) ); // Queda una revisión para deshacer.
			}
		}
		$informe[] = array(
			'slug'    => $a['slug'],
			'resumen' => str_word_count( (string) ( $a['resumen'] ?? '' ) ) ? 'sí' : 'no',
			'fuentes' => count( $fuentes ),
			'h2'      => $subidos . '/' . count( (array) ( $a['h2'] ?? array() ) ),
			'estado'  => $aplicar ? 'actualizada' : 'lista',
		);
	}
	delete_transient( 'calma_llms' );
	return $informe;
}

function calma_taxonomia_aplicar( $aplicar = false ) {
	$t       = calma_geo_json( 'taxonomia.json' );
	$informe = array();
	if ( ! $t ) {
		return array( array( 'accion' => 'error', 'detalle' => 'Falta data/taxonomia.json' ) );
	}
	$mapa = array();
	foreach ( $t['categorias'] as $c ) {
		$existe    = get_term_by( 'slug', $c['slug'], 'category' );
		$informe[] = array( 'accion' => $existe ? 'actualizar categoría' : 'crear categoría', 'detalle' => $c['slug'] );
		if ( $aplicar ) {
			$existe
				? wp_update_term( $existe->term_id, 'category', array( 'name' => $c['nombre'], 'description' => $c['descripcion'] ) )
				: wp_insert_term( $c['nombre'], 'category', array( 'slug' => $c['slug'], 'description' => $c['descripcion'] ) );
		}
		if ( ! empty( $c['area_cta'] ) ) {
			$mapa[ $c['slug'] ] = $c['area_cta'];
		}
	}
	foreach ( (array) ( $t['etiquetas'] ?? array() ) as $e ) {
		if ( ! get_term_by( 'slug', $e['slug'], 'post_tag' ) ) {
			$informe[] = array( 'accion' => 'crear etiqueta', 'detalle' => $e['slug'] );
			if ( $aplicar ) {
				wp_insert_term( $e['nombre'], 'post_tag', array( 'slug' => $e['slug'] ) );
			}
		}
	}
	foreach ( $t['asignacion'] as $as ) {
		$post = calma_post_por_slug( $as['slug_entrada'] );
		if ( ! $post ) {
			$informe[] = array( 'accion' => 'entrada no encontrada', 'detalle' => $as['slug_entrada'] );
			continue;
		}
		$informe[] = array( 'accion' => 'asignar', 'detalle' => $as['slug_entrada'] . ' → ' . $as['categoria'] . ' [' . implode( ', ', $as['etiquetas'] ) . ']' );
		if ( $aplicar ) {
			$cat = get_term_by( 'slug', $as['categoria'], 'category' );
			if ( $cat ) {
				wp_set_post_terms( $post->ID, array( (int) $cat->term_id ), 'category', false );
			}
			$tags = array_filter( array_map( fn( $s ) => get_term_by( 'slug', $s, 'post_tag' ), $as['etiquetas'] ) );
			wp_set_post_terms( $post->ID, array_map( fn( $x ) => (int) $x->term_id, $tags ), 'post_tag', false );
		}
	}
	foreach ( array( 'category' => $t['eliminar_categorias'] ?? array(), 'post_tag' => $t['eliminar_etiquetas'] ?? array() ) as $tax => $slugs ) {
		foreach ( $slugs as $slug ) {
			$term = get_term_by( 'slug', $slug, $tax );
			if ( ! $term ) {
				continue;
			}
			$informe[] = array( 'accion' => 'eliminar ' . ( 'category' === $tax ? 'categoría' : 'etiqueta' ), 'detalle' => $slug );
			if ( $aplicar && ! ( 'category' === $tax && (int) get_option( 'default_category' ) === (int) $term->term_id ) ) {
				wp_delete_term( $term->term_id, $tax );
			}
		}
	}
	$rm = class_exists( '\RankMath\Redirections\Redirection' );
	foreach ( (array) ( $t['redirecciones'] ?? array() ) as $r ) {
		$origen    = trim( $r['origen'], '/' );
		$ya        = $rm && class_exists( '\RankMath\Redirections\DB' ) && \RankMath\Redirections\DB::match_redirections( $origen );
		$accion = $rm ? ( $ya ? 'redirección existente' : 'crear redirección 301' ) : 'redirección (Rank Math inactivo: crearla a mano)';
		if ( $aplicar && $rm && ! $ya ) {
			$id = \RankMath\Redirections\Redirection::from(
				array(
					'url_to'      => $r['destino'],
					'header_code' => (string) ( $r['tipo'] ?? 301 ),
					'status'      => 'active',
					'sources'     => array( array( 'pattern' => $origen, 'comparison' => 'exact' ) ),
				)
			)->save();
			// Si Rank Math no pudo guardarla (módulo Redirecciones inactivo, tabla ausente…), se informa.
			$accion = $id ? 'redirección 301 creada' : 'ERROR: no se pudo crear (revisar Rank Math → Redirecciones)';
		}
		$informe[] = array( 'accion' => $accion, 'detalle' => $origen . ' → ' . $r['destino'] );
	}
	if ( $aplicar && $mapa ) {
		update_option( 'calma_cta_mapa', $mapa );
	}
	delete_transient( 'calma_llms' );
	return $informe;
}

// La caja de consulta usa el mapa categoría → área de la taxonomía nueva.
add_filter( 'calma_cta_area_por_categoria', function ( $mapa ) {
	$nuevo = get_option( 'calma_cta_mapa' );
	return is_array( $nuevo ) && $nuevo ? array_merge( $mapa, $nuevo ) : $mapa;
} );

add_action( 'admin_menu', function () {
	add_management_page( 'Código Calma: blog', 'Código Calma: blog', 'manage_options', 'calma-blog', 'calma_blog_pantalla' );
} );

function calma_blog_pantalla() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$accion = sanitize_key( $_POST['calma_accion'] ?? '' );
	if ( $accion && check_admin_referer( 'calma_blog' ) ) {
		'taxonomia' === $accion ? calma_taxonomia_aplicar( true ) : calma_geo_importar( true );
		echo '<div class="notice notice-success"><p>Cambios aplicados.</p></div>';
	}
	echo '<div class="wrap"><h1>Código Calma: blog</h1>';
	foreach ( array(
		'taxonomia' => array( 'Taxonomía y redirecciones', calma_taxonomia_aplicar( false ), array( 'accion', 'detalle' ) ),
		'geo'       => array( 'Resúmenes, fuentes y encabezados', calma_geo_importar( false ), array( 'slug', 'resumen', 'fuentes', 'h2', 'estado' ) ),
	) as $clave => $bloque ) {
		echo '<h2>' . esc_html( $bloque[0] ) . '</h2><table class="widefat striped"><thead><tr>';
		foreach ( $bloque[2] as $col ) {
			echo '<th>' . esc_html( $col ) . '</th>';
		}
		echo '</tr></thead><tbody>';
		foreach ( $bloque[1] as $fila ) {
			echo '<tr>';
			foreach ( $bloque[2] as $col ) {
				echo '<td>' . esc_html( (string) ( $fila[ $col ] ?? '' ) ) . '</td>';
			}
			echo '</tr>';
		}
		echo '</tbody></table><form method="post" style="margin:1em 0 2em">';
		wp_nonce_field( 'calma_blog' );
		echo '<input type="hidden" name="calma_accion" value="' . esc_attr( $clave ) . '">';
		submit_button( 'Aplicar: ' . $bloque[0], 'primary', 'submit', false );
		echo '</form>';
	}
	echo '</div>';
}

if ( defined( 'WP_CLI' ) && WP_CLI ) {
	WP_CLI::add_command( 'calma geo-import', function ( $args, $assoc ) {
		WP_CLI\Utils\format_items( 'table', calma_geo_importar( empty( $assoc['dry-run'] ) ), array( 'slug', 'resumen', 'fuentes', 'h2', 'estado' ) );
	} );
	WP_CLI::add_command( 'calma taxonomia', function ( $args, $assoc ) {
		WP_CLI\Utils\format_items( 'table', calma_taxonomia_aplicar( empty( $assoc['dry-run'] ) ), array( 'accion', 'detalle' ) );
	} );
}

/* ---------------------------------------------------------------------------
 * 4. Página pilar /ciberpsicologia/: Article + FAQPage desde su contenido
 * ------------------------------------------------------------------------- */

/**
 * Extrae preguntas (h3) y respuestas de la sección "Preguntas frecuentes" (h2).
 * Omite las respuestas que aún tienen [COMPLETAR] o [verificar].
 */
function calma_faq_desde_contenido( $html ) {
	if ( ! preg_match( '#<h2[^>]*>\s*Preguntas frecuentes\s*</h2>(.*?)(?=<h2|$)#si', $html, $m ) ) {
		return array();
	}
	$faq = array();
	foreach ( preg_split( '#(?=<h3)#i', $m[1] ) as $trozo ) {
		if ( ! preg_match( '#<h3[^>]*>(.*?)</h3>(.*)#si', $trozo, $q ) ) {
			continue;
		}
		$respuesta = trim( preg_replace( '/\s+/', ' ', wp_strip_all_tags( $q[2] ) ) );
		if ( '' === $respuesta || preg_match( '/COMPLETAR|verificar/i', $respuesta ) ) {
			continue;
		}
		$faq[] = array( trim( wp_strip_all_tags( $q[1] ) ), $respuesta );
	}
	return $faq;
}

add_filter( 'calma_schema_graph', function ( $graph ) {
	if ( ! is_page() || 'ciberpsicologia' !== calma_schema_ruta() ) {
		return $graph;
	}
	$post  = get_queried_object();
	$url   = get_permalink( $post );
	$html  = apply_filters( 'the_content', $post->post_content ); // phpcs:ignore WordPress.NamingConventions.PrefixAllGlobals -- filtro del core.
	$graph[] = calma_schema_persona( 'tatiana-x-stacul', calma_schema_personas()['tatiana-x-stacul'] );
	$graph[] = array(
		'@type'            => 'Article',
		'@id'              => $url . '#article',
		'headline'         => '¿Qué es la ciberpsicología?',
		'about'            => array( '@type' => 'Thing', 'name' => 'Ciberpsicología' ),
		'author'           => array( '@id' => calma_schema_persona_id( 'tatiana-x-stacul' ) ),
		'publisher'        => array( '@id' => calma_org_id() ),
		'datePublished'    => get_the_date( 'c', $post ),
		'dateModified'     => get_the_modified_date( 'c', $post ),
		'mainEntityOfPage' => $url,
		'inLanguage'       => 'es',
	);
	$faq = calma_faq_desde_contenido( $html );
	if ( $faq ) {
		$graph[] = array(
			'@type'      => 'FAQPage',
			'@id'        => $url . '#faq',
			'mainEntity' => array_map( fn( $q ) => array( '@type' => 'Question', 'name' => $q[0], 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $q[1] ) ), $faq ),
		);
	}
	return $graph;
} );
