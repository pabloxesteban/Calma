<?php
/**
 * Código Calma — Etapa 4: datos estructurados (JSON-LD).
 *
 * Un único @graph por página, con entidades enlazadas por @id
 * (.claude/skills/schema-markup/SKILL.md). Regla: solo datos visibles en el
 * sitio y verificados; lo pendiente se omite (nunca un [COMPLETAR] en el JSON).
 * El módulo Schema de Rank Math debe quedar desactivado para no duplicar.
 */

defined( 'ABSPATH' ) || exit;

function calma_org_id() {
	return home_url( '/#organization' );
}
function calma_site_id() {
	return home_url( '/#website' );
}

/**
 * Personas del equipo. Solo datos publicados en el sitio. Los campos que
 * dependen de placeholders (foto, alumniOf, hasCredential, sameAs de
 * Francisca y Emanuel) se agregan con el filtro `calma_schema_personas`
 * cuando estén confirmados.
 */
function calma_schema_personas() {
	$base = home_url( '/equipo/' );
	return apply_filters(
		'calma_schema_personas',
		array(
			'tatiana-x-stacul'         => array(
				'name'        => 'Tatiana X. Stacul',
				'jobTitle'    => 'Psicóloga',
				'description' => 'Psicóloga especializada en ciberpsicología y comportamiento en entornos digitales.',
				'knowsAbout'  => array( 'Ciberpsicología', 'Ciencias del comportamiento', 'Hábitos digitales', 'Bienestar digital' ),
				'sameAs'      => array( 'https://www.linkedin.com/in/tatiana-staculpsi/' ),
				'url'         => $base . 'tatiana-x-stacul/',
			),
			'francisca-cortes-santoro' => array(
				'name'        => 'Francisca Cortés Santoro',
				'jobTitle'    => 'Especialista en accesibilidad cognitiva y lenguaje',
				'description' => 'Trabaja en accesibilidad cognitiva: lectura fácil, lenguaje claro y carga cognitiva en webs y documentos.',
				'knowsAbout'  => array( 'Accesibilidad cognitiva', 'Lectura fácil', 'Lenguaje claro' ),
				'url'         => $base . 'francisca-cortes-santoro/',
			),
			'emanuel-c-franco'         => array(
				'name'        => 'Emanuel C. Franco',
				'jobTitle'    => 'Gestión de proyectos y procesos',
				'description' => 'Trabaja en gestión de proyectos y procesos: alcance, plazos y prioridades realistas.',
				'knowsAbout'  => array( 'Gestión de proyectos', 'Gestión de procesos' ),
				'url'         => $base . 'emanuel-c-franco/',
			),
		)
	);
}

function calma_schema_persona_id( $slug ) {
	return home_url( '/equipo/' . $slug . '/#person' );
}

function calma_schema_persona( $slug, $p ) {
	return array_filter(
		array(
			'@type'       => 'Person',
			'@id'         => calma_schema_persona_id( $slug ),
			'name'        => $p['name'],
			'jobTitle'    => $p['jobTitle'],
			'description' => $p['description'],
			'url'         => $p['url'],
			'image'       => $p['image'] ?? null,
			'knowsAbout'  => $p['knowsAbout'],
			'sameAs'      => $p['sameAs'] ?? null,
			'worksFor'    => array( '@id' => calma_org_id() ),
		)
	);
}

/**
 * Autor de una entrada → persona. Hoy todas las entradas son de Tatiana
 * (usuario `admin` hasta que se reasignen); el campo de usuario
 * `calma_persona` permite mapear otros autores.
 */
function calma_schema_autor_slug( $post ) {
	$slug = get_user_meta( (int) $post->post_author, 'calma_persona', true );
	return $slug && isset( calma_schema_personas()[ $slug ] ) ? $slug : 'tatiana-x-stacul';
}

function calma_schema_logo() {
	$id = (int) get_theme_mod( 'custom_logo' );
	if ( ! $id ) {
		return null;
	}
	$img = wp_get_attachment_image_src( $id, 'full' );
	return $img ? array( '@type' => 'ImageObject', 'url' => $img[0], 'width' => $img[1], 'height' => $img[2] ) : null;
}

/** Ruta de la página actual relativa a la home, p. ej. "equipo/tatiana-x-stacul". */
function calma_schema_ruta() {
	$obj = get_queried_object();
	return ( $obj instanceof WP_Post ) ? get_page_uri( $obj ) : '';
}

function calma_schema_breadcrumb( array $items ) {
	$list = array();
	foreach ( $items as $i => $it ) {
		$list[] = array_filter(
			array(
				'@type'    => 'ListItem',
				'position' => $i + 1,
				'name'     => $it[0],
				'item'     => $it[1] ?? null,
			)
		);
	}
	return array( '@type' => 'BreadcrumbList', '@id' => ( $items[ count( $items ) - 1 ][1] ?? home_url( '/' ) ) . '#breadcrumb', 'itemListElement' => $list );
}

/**
 * Preguntas frecuentes de Servicios que se pueden marcar: solo las que tienen
 * respuesta completa y visible (las que aún llevan [COMPLETAR] se omiten).
 */
function calma_schema_faq_servicios() {
	return apply_filters(
		'calma_schema_faq_servicios',
		array(
			array(
				'¿Qué pasa en el primer encuentro?',
				'Durante una hora entendemos tu contexto y le ponemos un nombre preciso a lo que ocurre. Sales con un objetivo por escrito. Si vemos que lo que necesitas no es un acompañamiento como este, te lo decimos ahí mismo.',
			),
		)
	);
}

function calma_schema_graph() {
	$graph    = array();
	$personas = calma_schema_personas();
	$inicio   = array( 'Inicio', home_url( '/' ) );

	$graph[] = array_filter(
		array(
			'@type'       => 'Organization',
			'@id'         => calma_org_id(),
			'name'        => 'Código Calma',
			'url'         => home_url( '/' ),
			'logo'        => calma_schema_logo(),
			'description' => 'Portal de ciberpsicología y bienestar digital en español, con mentoría y acompañamiento uno a uno.',
			'email'       => 'hola@codigocalma.com',
			'sameAs'      => array_filter( (array) apply_filters( 'calma_schema_org_sameas', array() ) ) ?: null,
			'member'      => array_map( fn( $s ) => array( '@id' => calma_schema_persona_id( $s ) ), array_keys( $personas ) ),
			'knowsAbout'  => array( 'Ciberpsicología', 'Bienestar digital', 'Accesibilidad cognitiva', 'Gestión de proyectos' ),
		)
	);
	$graph[] = array(
		'@type'           => 'WebSite',
		'@id'             => calma_site_id(),
		'url'             => home_url( '/' ),
		'name'            => 'Código Calma',
		'inLanguage'      => 'es',
		'publisher'       => array( '@id' => calma_org_id() ),
		'potentialAction' => array(
			'@type'       => 'SearchAction',
			'target'      => home_url( '/?s={search_term_string}' ),
			'query-input' => 'required name=search_term_string',
		),
	);

	$ruta = calma_schema_ruta();

	// Servicios: ProfessionalService + FAQPage + migas.
	if ( 'servicios' === $ruta ) {
		$url     = home_url( '/servicios/' );
		$graph[] = array(
			'@type'           => 'ProfessionalService',
			'@id'             => $url . '#service',
			'name'            => 'Código Calma — Mentoría y acompañamiento uno a uno',
			'url'             => $url,
			'description'     => 'Acompañamiento online, una persona por vez, en tres a seis sesiones: hábitos digitales y ciberpsicología, accesibilidad cognitiva y gestión de proyectos.',
			'provider'        => array( '@id' => calma_org_id() ),
			'availableLanguage' => 'es',
			'email'           => 'hola@codigocalma.com',
			'hasOfferCatalog' => array(
				'@type'           => 'OfferCatalog',
				'name'            => 'Acompañamientos',
				'itemListElement' => array(
					array( '@type' => 'Offer', 'itemOffered' => array( '@type' => 'Service', 'name' => 'Hábitos digitales y comportamiento', 'provider' => array( '@id' => calma_schema_persona_id( 'tatiana-x-stacul' ) ) ) ),
					array( '@type' => 'Offer', 'itemOffered' => array( '@type' => 'Service', 'name' => 'Accesibilidad cognitiva y lenguaje claro', 'provider' => array( '@id' => calma_schema_persona_id( 'francisca-cortes-santoro' ) ) ) ),
					array( '@type' => 'Offer', 'itemOffered' => array( '@type' => 'Service', 'name' => 'Gestión de proyectos y procesos', 'provider' => array( '@id' => calma_schema_persona_id( 'emanuel-c-franco' ) ) ) ),
				),
			),
		);
		$faq = calma_schema_faq_servicios();
		if ( $faq ) {
			$graph[] = array(
				'@type'      => 'FAQPage',
				'@id'        => $url . '#faq',
				'mainEntity' => array_map(
					fn( $q ) => array( '@type' => 'Question', 'name' => $q[0], 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $q[1] ) ),
					$faq
				),
			);
		}
		$graph[] = calma_schema_breadcrumb( array( $inicio, array( 'Servicios', $url ) ) );
	}

	// Equipo: índice y páginas de persona (ProfilePage).
	if ( 'equipo' === $ruta ) {
		foreach ( $personas as $slug => $p ) {
			$graph[] = calma_schema_persona( $slug, $p );
		}
		$graph[] = calma_schema_breadcrumb( array( $inicio, array( 'Equipo', home_url( '/equipo/' ) ) ) );
	} elseif ( 0 === strpos( $ruta, 'equipo/' ) && isset( $personas[ substr( $ruta, 7 ) ] ) ) {
		$slug    = substr( $ruta, 7 );
		$p       = $personas[ $slug ];
		$graph[] = calma_schema_persona( $slug, $p );
		$graph[] = array(
			'@type'      => 'ProfilePage',
			'@id'        => $p['url'] . '#webpage',
			'url'        => $p['url'],
			'name'       => $p['name'] . ' – Código Calma',
			'mainEntity' => array( '@id' => calma_schema_persona_id( $slug ) ),
			'isPartOf'   => array( '@id' => calma_site_id() ),
			'inLanguage' => 'es',
		);
		$graph[] = calma_schema_breadcrumb( array( $inicio, array( 'Equipo', home_url( '/equipo/' ) ), array( $p['name'], $p['url'] ) ) );
	}

	// Entradas: BlogPosting + autora + migas.
	if ( is_singular( 'post' ) ) {
		$post  = get_queried_object();
		$url   = get_permalink( $post );
		$autor = calma_schema_autor_slug( $post );
		$cats  = get_the_category( $post->ID );
		$cat   = $cats ? $cats[0] : null;
		$img   = has_post_thumbnail( $post ) ? wp_get_attachment_image_src( get_post_thumbnail_id( $post ), 'full' ) : null;
		$desc  = get_post_meta( $post->ID, 'rank_math_description', true ) ?: wp_strip_all_tags( get_the_excerpt( $post ) );
		$tags  = wp_get_post_tags( $post->ID, array( 'fields' => 'names' ) );

		$graph[] = calma_schema_persona( $autor, calma_schema_personas()[ $autor ] );
		$graph[] = array_filter(
			array(
				'@type'            => 'BlogPosting',
				'@id'              => $url . '#article',
				'headline'         => mb_substr( wp_strip_all_tags( get_the_title( $post ) ), 0, 110 ),
				'description'      => $desc ? mb_substr( $desc, 0, 300 ) : null,
				'image'            => $img ? array( '@type' => 'ImageObject', 'url' => $img[0], 'width' => $img[1], 'height' => $img[2] ) : null,
				'datePublished'    => get_the_date( 'c', $post ),
				'dateModified'     => get_the_modified_date( 'c', $post ),
				'author'           => array( '@id' => calma_schema_persona_id( $autor ) ),
				'publisher'        => array( '@id' => calma_org_id() ),
				'mainEntityOfPage' => $url,
				'isPartOf'         => array( '@id' => calma_site_id() ),
				'articleSection'   => $cat ? $cat->name : null,
				'keywords'         => $tags ?: null,
				'inLanguage'       => 'es',
			)
		);
		$migas = array( $inicio, array( 'Blog', home_url( '/blog/' ) ) );
		if ( $cat ) {
			$migas[] = array( $cat->name, get_category_link( $cat ) );
		}
		$migas[] = array( wp_strip_all_tags( get_the_title( $post ) ), $url );
		$graph[] = calma_schema_breadcrumb( $migas );
	}

	// Resto de páginas: migas simples.
	if ( is_page() && ! is_front_page() && $ruta && 'servicios' !== $ruta && 0 !== strpos( $ruta, 'equipo' ) ) {
		$graph[] = calma_schema_breadcrumb( array( $inicio, array( wp_strip_all_tags( get_the_title() ), get_permalink() ) ) );
	}

	return apply_filters( 'calma_schema_graph', $graph );
}

add_action( 'wp_head', function () {
	if ( is_admin() || is_feed() || is_404() ) {
		return;
	}
	$json = wp_json_encode(
		array( '@context' => 'https://schema.org', '@graph' => calma_schema_graph() ),
		JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE
	);
	echo "\n<script type=\"application/ld+json\" class=\"calma-schema\">" . $json . "</script>\n"; // phpcs:ignore WordPress.Security.EscapeOutput -- JSON codificado.
}, 20 );
