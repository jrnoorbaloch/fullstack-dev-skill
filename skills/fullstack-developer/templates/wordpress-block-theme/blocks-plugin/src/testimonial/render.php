<?php
/**
 * Server-side render for starter/testimonial.
 *
 * @package starter-blocks
 *
 * @var array $attributes Block attributes.
 */

$starter_quote  = isset( $attributes['quote'] ) ? $attributes['quote'] : '';
$starter_author = isset( $attributes['author'] ) ? $attributes['author'] : '';
$starter_role   = isset( $attributes['role'] ) ? $attributes['role'] : '';
$starter_rating = isset( $attributes['rating'] ) ? max( 0, min( 5, (int) $attributes['rating'] ) ) : 5;

if ( '' === trim( wp_strip_all_tags( $starter_quote ) ) ) {
	return;
}
?>
<figure <?php echo get_block_wrapper_attributes( array( 'class' => 'starter-testimonial' ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>>
	<div class="starter-testimonial__stars" role="img" aria-label="<?php echo esc_attr( sprintf( /* translators: %d: rating out of 5 */ __( '%d out of 5 stars', 'starter-blocks' ), $starter_rating ) ); ?>">
		<?php echo esc_html( str_repeat( '★', $starter_rating ) . str_repeat( '☆', 5 - $starter_rating ) ); ?>
	</div>
	<blockquote class="starter-testimonial__quote"><?php echo wp_kses_post( $starter_quote ); ?></blockquote>
	<figcaption>
		<strong><?php echo esc_html( wp_strip_all_tags( $starter_author ) ); ?></strong>
		<?php if ( $starter_role ) : ?>
			<span class="starter-testimonial__role"><?php echo esc_html( wp_strip_all_tags( $starter_role ) ); ?></span>
		<?php endif; ?>
	</figcaption>
</figure>
