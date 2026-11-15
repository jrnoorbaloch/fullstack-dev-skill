<?php
/**
 * Theme setup.
 *
 * @package starter-theme
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action(
	'after_setup_theme',
	function () {
		add_editor_style( 'assets/editor.css' );
	}
);

add_action(
	'init',
	function () {
		register_block_pattern_category(
			'starter-theme',
			array( 'label' => __( 'Starter Theme', 'starter-theme' ) )
		);

		register_block_style(
			'core/button',
			array(
				'name'         => 'pill',
				'label'        => __( 'Pill', 'starter-theme' ),
				'inline_style' => '.wp-block-button.is-style-pill .wp-block-button__link{border-radius:999px}',
			)
		);
	}
);
