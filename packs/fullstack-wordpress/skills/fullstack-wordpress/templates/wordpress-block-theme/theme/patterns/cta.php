<?php
/**
 * Title: Call to action
 * Slug: starter-theme/cta
 * Categories: starter-theme, call-to-action
 * Keywords: cta, contact, signup
 */
?>
<!-- wp:group {"align":"wide","anchor":"contact","backgroundColor":"primary","textColor":"base","style":{"spacing":{"padding":{"top":"var:preset|spacing|50","bottom":"var:preset|spacing|50","left":"var:preset|spacing|50","right":"var:preset|spacing|50"}},"border":{"radius":"24px"}},"layout":{"type":"constrained","contentSize":"640px"}} -->
<div id="contact" class="wp-block-group alignwide has-base-color has-primary-background-color has-text-color has-background" style="border-radius:24px;padding-top:var(--wp--preset--spacing--50);padding-right:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--50);padding-left:var(--wp--preset--spacing--50)"><!-- wp:heading {"textAlign":"center","textColor":"base"} -->
<h2 class="wp-block-heading has-text-align-center has-base-color has-text-color"><?php esc_html_e( 'Ready to start?', 'starter-theme' ); ?></h2>
<!-- /wp:heading -->
<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
<div class="wp-block-buttons"><!-- wp:button {"backgroundColor":"base","textColor":"contrast","className":"is-style-pill"} -->
<div class="wp-block-button is-style-pill"><a class="wp-block-button__link has-contrast-color has-base-background-color has-text-color has-background wp-element-button" href="mailto:hello@example.com"><?php esc_html_e( 'Contact us', 'starter-theme' ); ?></a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons --></div>
<!-- /wp:group -->
