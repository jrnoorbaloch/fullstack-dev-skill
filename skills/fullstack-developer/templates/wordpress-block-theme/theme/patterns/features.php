<?php
/**
 * Title: Features (3 columns)
 * Slug: starter-theme/features
 * Categories: starter-theme, columns
 * Keywords: features, services, benefits
 */

$starter_features = array(
	array( __( 'Fast', 'starter-theme' ), __( 'Describe the first benefit in one sentence.', 'starter-theme' ) ),
	array( __( 'Reliable', 'starter-theme' ), __( 'Describe the second benefit in one sentence.', 'starter-theme' ) ),
	array( __( 'Supported', 'starter-theme' ), __( 'Describe the third benefit in one sentence.', 'starter-theme' ) ),
);
?>
<!-- wp:group {"align":"wide","anchor":"features","style":{"spacing":{"padding":{"bottom":"var:preset|spacing|60"}}},"layout":{"type":"default"}} -->
<div id="features" class="wp-block-group alignwide" style="padding-bottom:var(--wp--preset--spacing--60)"><!-- wp:columns -->
<div class="wp-block-columns">
<?php foreach ( $starter_features as $starter_feature ) : ?>
<!-- wp:column {"backgroundColor":"surface","style":{"spacing":{"padding":{"top":"var:preset|spacing|40","bottom":"var:preset|spacing|40","left":"var:preset|spacing|40","right":"var:preset|spacing|40"}},"border":{"radius":"16px"}}} -->
<div class="wp-block-column has-surface-background-color has-background" style="border-radius:16px;padding-top:var(--wp--preset--spacing--40);padding-right:var(--wp--preset--spacing--40);padding-bottom:var(--wp--preset--spacing--40);padding-left:var(--wp--preset--spacing--40)"><!-- wp:heading {"level":3,"fontSize":"large"} -->
<h3 class="wp-block-heading has-large-font-size"><?php echo esc_html( $starter_feature[0] ); ?></h3>
<!-- /wp:heading -->
<!-- wp:paragraph {"textColor":"muted"} -->
<p class="has-muted-color has-text-color"><?php echo esc_html( $starter_feature[1] ); ?></p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->
<?php endforeach; ?>
</div>
<!-- /wp:columns --></div>
<!-- /wp:group -->
