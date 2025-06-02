import logging
import os
from typing import List, Dict, Any
from tabulate import tabulate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def display_variants(annotated_variants: List[Dict[str, Any]]) -> None:
    """
    Displays a list of annotated variants in a tabular format.
    
    Parameters:
        annotated_variants (List[Dict]): List of dictionaries with variant info and annotations.
    
    Raises:
        ValueError: If annotated_variants is not a list or contains invalid data
    """
    try:
        if not isinstance(annotated_variants, list):
            raise ValueError("Input must be a list of variant dictionaries")
            
        if not annotated_variants:
            logger.warning("No variants to display")
            return

        # Define headers and their order
        headers = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'GENE', 'IMPACT']
        
        # Prepare data rows
        rows = []
        for var in annotated_variants:
            try:
                row = [
                    var.get('CHROM', 'N/A'),
                    var.get('POS', 'N/A'),
                    var.get('ID', '.'),
                    var.get('REF', 'N/A'),
                    ','.join(var.get('ALT', [])) if isinstance(var.get('ALT'), list) else 'N/A',
                    var.get('QUAL', '.'),
                    var.get('GENE', 'Unknown'),
                    var.get('IMPACT', 'Unknown')
                ]
                rows.append(row)
            except KeyError as e:
                logger.warning(f"Missing required field in variant: {e}")
                continue

        # Display table using tabulate
        print(tabulate(rows, headers=headers, tablefmt='grid'))
        logger.info(f"Displayed {len(rows)} variants")

    except Exception as e:
        logger.error(f"Error displaying variants: {str(e)}")
        raise

def main():
    """Main entry point for the dashboard application."""
    try:
        from vcf_parser import parse_vcf
        from vcf_annotator import annotate_variants
        from display import display_variants
        from annotator import annotate_variants

        vcf_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample.vcf")
        
        logger.info(f"Processing VCF file: {vcf_path}")
        variants = parse_vcf(vcf_path)
        annotated = annotate_variants(variants)
        display_variants(annotated)
        
    except ImportError as e:
        logger.error(f"Failed to import required modules: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main()