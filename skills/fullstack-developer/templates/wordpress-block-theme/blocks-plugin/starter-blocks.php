<?php
/**
 * Plugin Name:       Starter Blocks
 * Description:       Custom blocks (Testimonial) for the starter theme.
 * Version:           1.0.0
 * Requires at least: 6.7
 * Requires PHP:      7.4
 * License:           GPL-2.0-or-later
 * Text Domain:       starter-blocks
 *
 * @package starter-blocks
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Register every block found in build/ (uses the blocks manifest when available).
 */
function starter_blocks_init() {
	$manifest = __DIR__ . '/build/blocks-manifest.php';
	if ( function_exists( 'wp_register_block_types_from_metadata_collection' ) && file_exists( $manifest ) ) {
		wp_register_block_types_from_metadata_collection( __DIR__ . '/build', $manifest );
		return;
	}
	foreach ( glob( __DIR__ . '/build/*/block.json' ) as $block_json ) {
		register_block_type( dirname( $block_json ) );
	}
}
add_action( 'init', 'starter_blocks_init' );
