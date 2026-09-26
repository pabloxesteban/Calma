<?php
/**
 * Código Calma — Etapa 4: importación de metadatos SEO a Rank Math.
 *
 * Lee data/seo-metadatos.json (copia de contenido/etapa-4/seo-metadatos.json) y
 * escribe título, descripción, palabra clave y Open Graph en los campos de Rank
 * Math de cada página, entrada y categoría. Herramientas → "Código Calma: SEO"
 * (vista previa y botón) o `wp calma seo-import [--dry-run]`.
 * No borra nada: solo sobrescribe los campos que trae el archivo.
 */

defined( 'ABSPATH' ) || exit;

function calma_seo_datos() {
	$file = CALMA_DIR . 'data/seo-metadatos.json';
	$data = is_readable( $file ) ? json_decode( (string) file_get_contents( $file ), true ) : null;
	return is_array( $data['entradas'] ?? null ) ? $data['entradas'] : array();
}

/**
 * Busca el objeto de WordPress de una entrada del archivo.
 *
 * @return array{0:string,1:int}|null ['post'|'term', id]
 */
function calma_seo_objetivo( array $e ) {
	$slug = trim( (string) ( $e['slug'] ?? '' ), '/' );
	switch ( $e['tipo'] ?? '' ) {
		case 'category':
			$term = get_term_by( 'slug', $slug, 'category' );
			return $term ? array( 'term', (int) $term->term_id ) : null;
		case 'post':
			$posts = get_posts( array( 'name' => $slug, 'post_type' => 'post', 'post_status' => 'any', 'numberposts' => 1 ) );
			return $posts ? array( 'post', (int) $posts[0]->ID ) : null;
		default:
			if ( 'home' === $slug && (int) get_option( 'page_on_front' ) ) {
				return array( 'post', (int) get_option( 'page_on_front' ) );
			}
			$page = get_page_by_path( $slug );
			if ( ! $page && ! empty( $e['url'] ) ) {
				// Descargas: el archivo usa la URL nueva (/descargas/) aunque el slug aún sea descargas-2.
				$id   = url_to_postid( $e['url'] );
				$page = $id ? get_post( $id ) : null;
			}
			return $page ? array( 'post', (int) $page->ID ) : null;
	}
}

function calma_seo_campos( array $e ) {
	return array_filter(
		array(
			'rank_math_title'                => $e['title'] ?? '',
			'rank_math_description'          => $e['description'] ?? '',
			'rank_math_focus_keyword'        => $e['focus_keyword'] ?? '',
			'rank_math_facebook_title'       => $e['og_title'] ?? '',
			'rank_math_facebook_description' => $e['og_description'] ?? '',
		),
		'strlen'
	);
}

/**
 * @return array<int,array{slug:string,estado:string,id:int}>
 */
function calma_seo_importar( $aplicar = false ) {
	$informe = array();
	foreach ( calma_seo_datos() as $e ) {
		$obj = calma_seo_objetivo( $e );
		if ( ! $obj ) {
			$informe[] = array( 'slug' => $e['slug'], 'estado' => 'no encontrado', 'id' => 0 );
			continue;
		}
		if ( $aplicar ) {
			foreach ( calma_seo_campos( $e ) as $k => $v ) {
				'term' === $obj[0] ? update_term_meta( $obj[1], $k, $v ) : update_post_meta( $obj[1], $k, $v );
			}
		}
		$informe[] = array( 'slug' => $e['slug'], 'estado' => $aplicar ? 'actualizado' : 'listo', 'id' => $obj[1] );
	}
	return $informe;
}

add_action( 'admin_menu', function () {
	add_management_page( 'Código Calma: SEO', 'Código Calma: SEO', 'manage_options', 'calma-seo', 'calma_seo_pantalla' );
} );

function calma_seo_pantalla() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$aplicar = isset( $_POST['calma_seo_importar'] ) && check_admin_referer( 'calma_seo_importar' );
	$informe = calma_seo_importar( $aplicar );
	echo '<div class="wrap"><h1>Código Calma: metadatos SEO</h1>';
	if ( $aplicar ) {
		echo '<div class="notice notice-success"><p>Metadatos importados en Rank Math.</p></div>';
	}
	echo '<p>Títulos, descripciones y Open Graph de <code>data/seo-metadatos.json</code>. Revisa la tabla y pulsa importar. Sobrescribe solo esos campos de Rank Math.</p>';
	echo '<table class="widefat striped"><thead><tr><th>Slug</th><th>ID</th><th>Estado</th></tr></thead><tbody>';
	foreach ( $informe as $fila ) {
		printf( '<tr><td>%s</td><td>%d</td><td>%s</td></tr>', esc_html( $fila['slug'] ), (int) $fila['id'], esc_html( $fila['estado'] ) );
	}
	echo '</tbody></table><form method="post" style="margin-top:1em">';
	wp_nonce_field( 'calma_seo_importar' );
	submit_button( 'Importar metadatos en Rank Math', 'primary', 'calma_seo_importar' );
	echo '</form></div>';
}

if ( defined( 'WP_CLI' ) && WP_CLI ) {
	/**
	 * Importa data/seo-metadatos.json en Rank Math.
	 *
	 * ## OPTIONS
	 * [--dry-run]
	 * : Solo muestra qué se actualizaría.
	 */
	WP_CLI::add_command( 'calma seo-import', function ( $args, $assoc ) {
		$informe = calma_seo_importar( empty( $assoc['dry-run'] ) );
		WP_CLI\Utils\format_items( 'table', $informe, array( 'slug', 'id', 'estado' ) );
	} );
}
