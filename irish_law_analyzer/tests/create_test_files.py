from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_sample_contract():
    """Create a sample employment contract PDF"""
    pdf = FPDF(format='A4')
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)
    pdf.set_margin(20)  # Set margins to avoid text overflow
    
    # Add content
    content = """
    EMPLOYMENT CONTRACT

    This Employment Contract ("Agreement") is made between Company Ltd. ("Employer")
    and John Doe ("Employee") on the date stated below.

    1. POSITION AND DUTIES
    Position: Software Developer
    Duties: Development and maintenance of software applications

    2. COMPENSATION
    Salary: 50,000 EUR per annum
    Payment Schedule: Monthly
    
    3. WORKING HOURS
    Standard Hours: 40 hours per week
    Work Schedule: Monday to Friday, 9:00 AM to 5:00 PM

    4. ANNUAL LEAVE
    Entitlement: 20 days per year
    
    5. NOTICE PERIOD
    Notice Period: 1 month

    6. PROBATION PERIOD
    Duration: 6 months
    
    7. CONFIDENTIALITY
    The Employee agrees to maintain confidentiality of company information.

    8. TERMINATION
    This agreement may be terminated by either party with written notice.

    Signed by:
    
    ________________                    ________________
    Employer                           Employee
    
    Date: _____________
    """
    
    # Write content line by line with proper spacing
    pdf.set_auto_page_break(auto=True, margin=15)
    for line in content.split('\n'):
        if line.strip():  # Only process non-empty lines
            if line.strip().startswith('EMPLOYMENT CONTRACT'):
                pdf.set_font("Helvetica", 'B', 14)  # Bold and larger for title
                pdf.cell(0, 10, line.strip(), ln=True, align='C')
                pdf.set_font("Helvetica", size=10)  # Reset font
            else:
                pdf.multi_cell(0, 8, line.strip(), align='L')
        else:
            pdf.ln(5)  # Add some space between paragraphs
    
    # Save the file
    output_path = Path(__file__).parent / "test_files" / "sample_contract.pdf"
    pdf.output(str(output_path))
    return output_path

def create_sample_letter():
    """Create a sample termination letter as an image"""
    # Create a new image with white background
    width = 1000  # Increased width
    height = 1400  # Increased height
    img = Image.new('RGB', (width, height), color='white')
    d = ImageDraw.Draw(img)
    
    # Use default font with larger size
    font = ImageFont.load_default()

    # Add content
    content = """
    TERMINATION NOTICE

    Date: January 15, 2024

    Dear Mr. Smith,

    This letter serves as formal notice of termination of your employment
    with Company Ltd., effective February 15, 2024.

    This decision has been made due to [reason for termination].

    According to your contract, you are entitled to a notice period of
    30 days. During this period, you are expected to continue your
    regular duties and assist in the handover of your responsibilities.

    Final payment will include:
    - Salary until last working day
    - Payment in lieu of unused annual leave
    - Pro-rata bonus (if applicable)

    Please return all company property by your last working day.

    You have the right to appeal this decision within 5 working days.

    If you have any questions, please contact HR department.

    Sincerely,
    HR Manager
    Company Ltd.
    """

    # Write text on image with more spacing
    y_position = 50
    for line in content.split('\n'):
        if line.strip():  # Only process non-empty lines
            d.text((50, y_position), line.strip(), font=font, fill='black')
            y_position += 25  # Reduced spacing between lines
        else:
            y_position += 40  # More space between paragraphs

    # Save the image
    output_path = Path(__file__).parent / "test_files" / "sample_letter.jpg"
    img.save(str(output_path))
    return output_path

def main():
    """Create all test files"""
    # Create test_files directory if it doesn't exist
    test_files_dir = Path(__file__).parent / "test_files"
    test_files_dir.mkdir(exist_ok=True)

    # Create test files
    try:
        contract_path = create_sample_contract()
        letter_path = create_sample_letter()

        print(f"Created test files successfully:")
        print(f"- Contract: {contract_path}")
        print(f"- Letter: {letter_path}")
    except Exception as e:
        print(f"Error creating test files: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()