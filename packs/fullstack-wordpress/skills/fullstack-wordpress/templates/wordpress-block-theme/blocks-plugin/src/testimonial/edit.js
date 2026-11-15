import { __ } from '@wordpress/i18n';
import { InspectorControls, RichText, useBlockProps } from '@wordpress/block-editor';
import { PanelBody, RangeControl } from '@wordpress/components';

export default function Edit( { attributes, setAttributes } ) {
	const { quote, author, role, rating } = attributes;
	const blockProps = useBlockProps( { className: 'starter-testimonial' } );

	return (
		<>
			<InspectorControls>
				<PanelBody title={ __( 'Settings', 'starter-blocks' ) }>
					<RangeControl
						label={ __( 'Star rating', 'starter-blocks' ) }
						value={ rating }
						onChange={ ( value ) => setAttributes( { rating: value ?? 5 } ) }
						min={ 0 }
						max={ 5 }
					/>
				</PanelBody>
			</InspectorControls>
			<figure { ...blockProps }>
				<div className="starter-testimonial__stars" aria-hidden="true">
					{ '★'.repeat( rating ) + '☆'.repeat( 5 - rating ) }
				</div>
				<RichText
					tagName="blockquote"
					className="starter-testimonial__quote"
					value={ quote }
					onChange={ ( value ) => setAttributes( { quote: value } ) }
					placeholder={ __( 'Write the customer’s words…', 'starter-blocks' ) }
				/>
				<figcaption>
					<RichText
						tagName="strong"
						value={ author }
						onChange={ ( value ) => setAttributes( { author: value } ) }
						placeholder={ __( 'Name', 'starter-blocks' ) }
						allowedFormats={ [] }
					/>
					<RichText
						tagName="span"
						className="starter-testimonial__role"
						value={ role }
						onChange={ ( value ) => setAttributes( { role: value } ) }
						placeholder={ __( 'Role, Company', 'starter-blocks' ) }
						allowedFormats={ [] }
					/>
				</figcaption>
			</figure>
		</>
	);
}
