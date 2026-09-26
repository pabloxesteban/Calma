<?php
/**
 * Código Calma — Etapa 3: flujo de consulta.
 *
 * - Caja "¿Te identificas con esto?" al final de cada entrada, con la
 *   profesional que corresponde según la categoría (o el campo personalizado
 *   `calma_cta_area` de la entrada: habitos | accesibilidad | proyectos |
 *   equipo | ninguna).
 * - Aviso breve de urgencias en entradas de salud mental.
 * - Newsletter: [calma_newsletter] y bloque tras la caja, solo si hay un
 *   formulario configurado en Ajustes > Lectura (si no, no se muestra nada).
 * - JS: preselección del área en /contacto/?area=… y evento generate_lead.
 */

defined( 'ABSPATH' ) || exit;

/**
 * Textos de la caja por área. Editables con el filtro `calma_cta_textos`.
 */
function calma_cta_textos() {
	$contacto = home_url( '/contacto/' );
	$textos   = array(
		'habitos'       => array(
			'titulo'     => '¿Te identificas con esto?',
			'texto'      => 'Tatiana acompaña procesos de cambio de hábitos digitales, uno a uno y online. En unas líneas nos cuentas qué te pasa y te respondemos en 48 horas hábiles.',
			'boton'      => 'Consultar con Tatiana',
			'url'        => add_query_arg( 'area', 'habitos', $contacto ),
		),
		'proyectos'     => array(
			'titulo'     => '¿Tu proyecto se desbordó?',
			'texto'      => 'Emanuel ayuda a reconstruir alcance, plazos y procesos que no se sostienen. Cuéntanos en unas líneas dónde estás y te respondemos en 48 horas hábiles.',
			'boton'      => 'Consultar con Emanuel',
			'url'        => add_query_arg( 'area', 'proyectos', $contacto ),
		),
		'accesibilidad' => array(
			'titulo'     => '¿Tu web se entiende?',
			'texto'      => 'Francisca revisa webs y documentos para que la información no solo se perciba, sino que se entienda. Te respondemos en 48 horas hábiles.',
			'boton'      => 'Consultar con Francisca',
			'url'        => add_query_arg( 'area', 'accesibilidad', $contacto ),
		),
		'equipo'        => array(
			'titulo'     => '¿Quieres hablarlo con alguien?',
			'texto'      => 'Trabajamos con una persona por vez, en un recorrido de tres a seis sesiones online. Cuéntanos en unas líneas qué necesitas y te decimos quién del equipo encaja mejor.',
			'boton'      => 'Solicitar una consulta',
			'url'        => $contacto,
		),
	);
	return apply_filters( 'calma_cta_textos', $textos );
}

/**
 * Área por categoría (slugs actuales; la Etapa 5 actualiza la taxonomía).
 */
function calma_cta_area_de_entrada( $post_id ) {
	$manual = get_post_meta( $post_id, 'calma_cta_area', true );
	if ( $manual ) {
		return sanitize_key( $manual );
	}
	$mapa = apply_filters(
		'calma_cta_area_por_categoria',
		array(
			'ciberseguridad' => 'equipo',
			'psicologia'     => 'habitos',
			'bienestar'      => 'habitos',
			'ciberpsicologia' => 'habitos',
			'neurociencia'   => 'habitos',
		)
	);
	foreach ( wp_get_post_categories( $post_id, array( 'fields' => 'slugs' ) ) as $slug ) {
		if ( isset( $mapa[ $slug ] ) ) {
			return $mapa[ $slug ];
		}
	}
	return 'equipo';
}

function calma_es_salud_mental( $post_id ) {
	$excluidas = apply_filters( 'calma_categorias_sin_aviso', array( 'ciberseguridad' ) );
	$slugs     = wp_get_post_categories( $post_id, array( 'fields' => 'slugs' ) );
	// Aviso en toda entrada que tenga al menos una categoría fuera de las excluidas.
	return empty( $slugs ) || (bool) array_diff( $slugs, $excluidas );
}

function calma_aviso_urgencias_html() {
	$url = get_option( 'calma_url_lineas_ayuda', '' );
	$enlace = $url
		? sprintf( ' <a href="%s">Ver líneas de ayuda</a>', esc_url( $url ) )
		: ' <span class="calma-placeholder">[COMPLETAR: enlace a líneas de ayuda]</span>';
	return '<p class="calma-aviso">Este espacio no es un servicio de urgencias. Si estás en crisis o en riesgo, contacta ahora con los servicios de emergencia de tu país.' . $enlace . '</p>';
}

add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'post' ) || ! in_the_loop() || ! is_main_query() ) {
		return $content;
	}
	$post_id = get_the_ID();
	$area    = calma_cta_area_de_entrada( $post_id );
	if ( 'ninguna' === $area ) {
		return $content;
	}
	$textos = calma_cta_textos();
	$t      = $textos[ $area ] ?? $textos['equipo'];

	$html  = '<aside class="calma-article-cta" aria-labelledby="calma-article-cta-title">';
	$html .= '<h2 class="calma-article-cta__title" id="calma-article-cta-title">' . esc_html( $t['titulo'] ) . '</h2>';
	$html .= '<p>' . esc_html( $t['texto'] ) . '</p>';
	$html .= '<p class="calma-article-cta__actions"><a class="calma-btn calma-btn--primary" href="' . esc_url( $t['url'] ) . '">' . esc_html( $t['boton'] ) . '</a>';
	$html .= ' <a class="calma-article-cta__link" href="' . esc_url( home_url( '/servicios/' ) ) . '">Ver cómo trabajamos</a></p>';
	if ( calma_es_salud_mental( $post_id ) ) {
		$html .= calma_aviso_urgencias_html();
	}
	$html .= '</aside>';
	$html .= calma_newsletter_html();

	return $content . $html;
}, 20 );

/**
 * Newsletter: renderiza el Kadence Advanced Form configurado. Sin formulario
 * configurado no se muestra nada (nunca un formulario que no envía).
 */
function calma_newsletter_html() {
	$form_id = absint( get_option( 'calma_newsletter_form_id', 0 ) );
	if ( ! $form_id || 'publish' !== get_post_status( $form_id ) ) {
		return '';
	}
	$form = do_blocks( '<!-- wp:kadence/advanced-form {"id":' . $form_id . '} /-->' );
	return '<section class="calma-newsletter" aria-labelledby="calma-newsletter-title">'
		. '<h2 class="calma-newsletter__title" id="calma-newsletter-title">' . esc_html( get_option( 'calma_newsletter_titulo', 'Una reflexión breve sobre bienestar digital' ) ) . '</h2>'
		. '<p>' . esc_html( get_option( 'calma_newsletter_texto', 'Ideas basadas en investigación para usar la tecnología con más intención. Sin spam y sin prisas: puedes darte de baja cuando quieras.' ) ) . '</p>'
		. $form . '</section>';
}
add_shortcode( 'calma_newsletter', 'calma_newsletter_html' );

/**
 * Ajustes > Lectura: formulario de newsletter, textos y enlace a líneas de ayuda.
 */
add_action( 'admin_init', function () {
	$campos = array(
		'calma_newsletter_form_id' => array( 'ID del formulario de newsletter (Kadence Advanced Form)', 'absint' ),
		'calma_newsletter_titulo'  => array( 'Título del bloque de newsletter', 'sanitize_text_field' ),
		'calma_newsletter_texto'   => array( 'Texto del bloque de newsletter', 'sanitize_text_field' ),
		'calma_url_lineas_ayuda'   => array( 'URL de la página de líneas de ayuda (aviso de urgencias)', 'esc_url_raw' ),
	);
	add_settings_section( 'calma_conversion', 'Código Calma · Consultas y newsletter', '__return_false', 'reading' );
	foreach ( $campos as $id => $def ) {
		register_setting( 'reading', $id, array( 'sanitize_callback' => $def[1] ) );
		add_settings_field( $id, $def[0], function () use ( $id ) {
			printf( '<input type="text" class="regular-text" name="%1$s" id="%1$s" value="%2$s">', esc_attr( $id ), esc_attr( get_option( $id, '' ) ) );
		}, 'reading', 'calma_conversion' );
	}
} );

add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_script( 'calma-conversion', CALMA_URL . 'assets/js/calma-conversion.js', array(), filemtime( CALMA_DIR . 'assets/js/calma-conversion.js' ), array( 'strategy' => 'defer', 'in_footer' => true ) );
	wp_enqueue_style( 'calma-etapa3', CALMA_URL . 'assets/css/calma-etapa3.css', array( 'calma-etapa2' ), filemtime( CALMA_DIR . 'assets/css/calma-etapa3.css' ) );
}, 21 );
