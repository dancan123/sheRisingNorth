import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

pdf_path = os.path.join("assets", "docs", "She_Is_Rising_From_The_North_Press_Kit.pdf")

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    leftMargin=36,
    rightMargin=36,
    topMargin=32,
    bottomMargin=32
)

styles = getSampleStyleSheet()

# Custom color palette matching website
c_deep = colors.HexColor("#1a0e05")
c_dark = colors.HexColor("#2d1a0a")
c_gold = colors.HexColor("#d4a853")
c_earth = colors.HexColor("#7a4520")
c_warm = colors.HexColor("#c97d3e")
c_sand = colors.HexColor("#f7f2ea")
c_cream = colors.HexColor("#faf6ef")
c_muted = colors.HexColor("#555555")

# Custom typography styles
style_kicker = ParagraphStyle(
    'Kicker',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8,
    leading=10,
    textColor=c_warm,
    textTransform='uppercase',
    alignment=0,
    spaceAfter=4
)

style_title = ParagraphStyle(
    'Title',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=20,
    leading=23,
    textColor=c_deep,
    spaceAfter=4
)

style_subtitle = ParagraphStyle(
    'Subtitle',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=10.5,
    leading=14,
    textColor=c_earth,
    spaceAfter=10
)

style_h2 = ParagraphStyle(
    'Heading2',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11.5,
    leading=14,
    textColor=c_deep,
    spaceBefore=7,
    spaceAfter=4
)

style_body = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8.5,
    leading=11.5,
    textColor=colors.HexColor("#222222"),
    spaceAfter=5
)

style_body_bold = ParagraphStyle(
    'BodyBold',
    parent=style_body,
    fontName='Helvetica-Bold'
)

style_quote = ParagraphStyle(
    'Quote',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=9.5,
    leading=13,
    textColor=c_deep,
    alignment=1
)

style_stat_num = ParagraphStyle(
    'StatNum',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=16,
    textColor=c_deep,
    alignment=1
)

style_stat_lbl = ParagraphStyle(
    'StatLbl',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=7,
    leading=9,
    textColor=c_earth,
    alignment=1
)

story = []

# ==========================================
# PAGE 1: EXHIBITION OVERVIEW & STATEMENT
# ==========================================

# Top bar metadata
top_data = [
    [
        Paragraph("<b>EXHIBITION PRESS PACK &amp; CURATORIAL BRIEF</b>", style_kicker),
        Paragraph("<font color='#d4a853'><b>FOR IMMEDIATE RELEASE</b></font>", ParagraphStyle('RightNotice', parent=style_kicker, alignment=2))
    ]
]
t_top = Table(top_data, colWidths=[360, 163])
t_top.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ('TOPPADDING', (0,0), (-1,-1), 0),
]))
story.append(t_top)
story.append(Spacer(1, 4))

story.append(Paragraph("SHE IS RISING FROM THE NORTH", style_title))
story.append(Paragraph("A Documentary Photography Project, Photo-Book &amp; Education Initiative across Northern Kenya &bull; By Hildah Kathure in Partnership with MOV Foundation", style_subtitle))
story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceBefore=0, spaceAfter=8))

# Impact Metrics Strip (4 columns)
stat_data = [
    [
        Paragraph("<b>479+</b>", style_stat_num),
        Paragraph("<b>~100</b>", style_stat_num),
        Paragraph("<b>25+ Yrs</b>", style_stat_num),
        Paragraph("<b>90+</b>", style_stat_num)
    ],
    [
        Paragraph("Girls Sponsored Through High School", style_stat_lbl),
        Paragraph("Scholars to University &amp; Colleges", style_stat_lbl),
        Paragraph("MOV Foundation in Northern Kenya", style_stat_lbl),
        Paragraph("Authentic Documentary Photographs", style_stat_lbl)
    ]
]
t_stats = Table(stat_data, colWidths=[130, 131, 131, 131])
t_stats.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), c_sand),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LINEBEFORE', (1,0), (-1,-1), 0.5, c_gold),
]))
story.append(t_stats)
story.append(Spacer(1, 9))

# Curatorial Overview
story.append(Paragraph("EXECUTIVE SUMMARY &amp; CURATORIAL NARRATIVE", style_h2))
story.append(Paragraph(
    "<b>'She Is Rising from the North'</b> is a landmark documentary exhibition, photographic monograph, and ongoing educational advocacy project chronicling fifteen years of transformative female leadership in Northern Kenya (Isiolo, Samburu, Marsabit, and Garissa counties). Created by acclaimed Kenyan documentary filmmaker and photographer <b>Hildah Kathure</b> in partnership with <b>MOV Foundation (Stichting MOV, The Netherlands)</b>, the initiative reframes the public perception of Northern Kenya from a narrative of passive vulnerability to one of extraordinary resilience, intellect, and economic agency.",
    style_body
))
story.append(Paragraph(
    "For pastoralist girls, secondary school is rarely a given. Severe distances, costly boarding fees, recurring climate droughts, and deep-seated pressures toward early marriage create profound barriers after primary school. Yet, through long-term sponsorship, 479+ young women have broken through these structural obstacles. Kathure's camera provides an intimate, dignifying witness to their trajectory—from the pastoralist rangelands to university lecture halls, surgical wards, and corporate boardrooms.",
    style_body
))

# The Three Acts Table
story.append(Spacer(1, 4))
story.append(Paragraph("THE THREE-ACT STRUCTURE OF THE EXHIBITION &amp; BOOK", style_h2))

act_data = [
    [
        Paragraph("<b>ACT I: ON THE GRAZING FIELDS</b><br/><font color='#555555'>The pastoralist foundation. Life in Isiolo and Samburu; water journeys, livestock herding, and dreams quietly carried under the desert sun.</font>", style_body),
        Paragraph("<b>ACT II: AT SCHOOL</b><br/><font color='#555555'>The arrival at boarding secondary school. Discovering science, debates, and personal voice. Dreams transform into uniforms, certificates, and ambition.</font>", style_body),
        Paragraph("<b>ACT III: ON THE JOB</b><br/><font color='#555555'>The graduates in society. Doctors, teachers, veterinarians, hospital CEOs, and entrepreneurs proving education is an engine of generational prosperity.</font>", style_body)
    ]
]
t_acts = Table(act_data, colWidths=[174, 174, 175])
t_acts.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f5ede0")),
    ('BOX', (0,0), (-1,-1), 0.5, c_gold),
    ('INNERGRID', (0,0), (-1,-1), 0.5, c_gold),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(t_acts)
story.append(Spacer(1, 9))

# Callout Quote Banner
quote_data = [
    [
        Paragraph("<b>&ldquo;Northern Kenya is often described as marginalized. But these girls are not a margin. They are the centre of a future we all share. Inequality is not fate. Education can turn a life around.&rdquo;</b><br/><font size='7.5' color='#7a4520'>&mdash; HILDAH KATHURE, Photographer &amp; MOV Liaison Officer</font>", style_quote)
    ]
]
t_quote = Table(quote_data, colWidths=[523])
t_quote.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#faf2e6")),
    ('LINELEFT', (0,0), (-1,-1), 3.5, c_gold),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ('LEFTPADDING', (0,0), (-1,-1), 12),
    ('RIGHTPADDING', (0,0), (-1,-1), 12),
]))
story.append(t_quote)

story.append(PageBreak())

# ==========================================
# PAGE 2: CASE STUDIES, POLICY & CONTACTS
# ==========================================

story.append(Paragraph("WOMEN WHO ROSE &bull; EVIDENCE OF GENERATIONAL IMPACT", style_kicker))
story.append(Paragraph("PROFILES IN COURAGE &amp; TRANSFORMATIVE LEADERSHIP", style_title))
story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceBefore=0, spaceAfter=8))

# 3 Case Profiles
cases_data = [
    [
        Paragraph("<b>Dr. Zeinab Gura</b><br/><font color='#7a4520'><b>CEO, Kenyatta University TRRH (Nairobi)</b></font><br/>From pastoralist roots in Northern Kenya to leading one of East Africa's premier national referral hospitals. <i>&ldquo;Education gave me more than a profession; it gave me the confidence to lead and prove dreams from the North are valid.&rdquo;</i>", style_body),
        Paragraph("<b>Batula Fayo</b><br/><font color='#7a4520'><b>Teacher, Kisima Primary School</b></font><br/>Educated through MOV Foundation sponsorship, Batula returned directly to her home community to teach the next generation of girls. <i>&ldquo;Standing in front of the chalkboard, I show every girl that her mind belongs at the front of the room.&rdquo;</i>", style_body),
        Paragraph("<b>Kamila Abkanu</b><br/><font color='#7a4520'><b>Veterinary Doctor &amp; Ag. Director</b></font><br/>Acting Director of Livestock for Isiolo County. Protecting pastoralist herds—the vital backbone of community economy. <i>&ldquo;Treating animals protects families' dignity, livelihood, and resilience against drought.&rdquo;</i>", style_body)
    ]
]
t_cases = Table(cases_data, colWidths=[174, 174, 175])
t_cases.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), c_sand),
    ('BOX', (0,0), (-1,-1), 0.5, c_gold),
    ('INNERGRID', (0,0), (-1,-1), 0.5, c_gold),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(t_cases)
story.append(Spacer(1, 9))

# Economic Policy Case for Donors & Institutions
story.append(Paragraph("THE ECONOMIC CASE: EDUCATION AS SYSTEMIC COMBAT AGAINST POVERTY", style_h2))
story.append(Paragraph(
    "Data compiled within the photo-book highlights that secondary education for a girl in Northern Kenya delivers an estimated <b>20–25% increase in lifetime earnings</b> and fundamentally breaks the multi-generational cycle of early child marriage. The initiative advocates for three concrete policy and institutional priorities:",
    style_body
))

policy_items = [
    [Paragraph("&bull;", style_body_bold), Paragraph("<b>Targeted Secondary Boarding Subsidies:</b> Eliminating the fatal transition gap between Grade 8 and Form 1 where most girls drop out due to boarding fee shortfalls.", style_body)],
    [Paragraph("&bull;", style_body_bold), Paragraph("<b>Fairer Higher Education Financing:</b> Reforming student loan criteria to prevent pastoralist university qualifiers from forfeiting admissions due to lack of upfront tuition.", style_body)],
    [Paragraph("&bull;", style_body_bold), Paragraph("<b>100% Proceeds Model:</b> All sales of books and photo prints go directly and transparently into secondary school tuition fees for deserving girls from Isiolo and surrounding counties.", style_body)]
]
t_policy = Table(policy_items, colWidths=[15, 508])
t_policy.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ('TOPPADDING', (0,0), (-1,-1), 2),
]))
story.append(t_policy)
story.append(Spacer(1, 9))

# Exhibition & Purchasing Specifications
story.append(Paragraph("EXHIBITION SPECIFICATIONS &amp; HOW TO ENGAGE", style_h2))

spec_data = [
    [
        Paragraph("<b>DOCUMENTARY PHOTO-BOOK</b><br/>Hardcover collector's edition containing 90+ authentic documentary photographs, essays, and economic analysis.<br/><b>Price:</b> KSh 2,500 (100% goes to school fees)", style_body),
        Paragraph("<b>CURATED MUSEUM PRINTS</b><br/>Fine-art exhibition prints on archival photographic paper.<br/><b>A2 Print:</b> KSh 3,000 &bull; <b>A1 Print:</b> KSh 5,000<br/>Direct KCB Paybill: <b>522533</b> | Acc: <b>8144533</b>", style_body),
        Paragraph("<b>EXHIBITION TOUR DATES</b><br/><b>Nairobi:</b> Baraza Media Lab<br/><b>Isiolo:</b> Catholic Mission Hall<br/><b>Gafarsa:</b> Community Hall<br/><b>Merti:</b> March 2027 Upcoming", style_body)
    ]
]
t_specs = Table(spec_data, colWidths=[174, 174, 175])
t_specs.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f9f5ee")),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#d0c4b4")),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e5dcd0")),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(t_specs)
story.append(Spacer(1, 9))

# Media & Curatorial Contact Box
contact_data = [
    [
        Paragraph("<b>MEDIA, CURATORIAL &amp; DONOR INQUIRIES</b>", ParagraphStyle('ContactH', parent=style_kicker, textColor=colors.white)),
        Paragraph("<b>MOV FOUNDATION PARTNERSHIP</b>", ParagraphStyle('ContactH2', parent=style_kicker, textColor=colors.white))
    ],
    [
        Paragraph(
            "<b>Hildah Kathure</b> &mdash; Author, Photographer, MOV Liaison Officer<br/>"
            "Kalmax Productions &bull; Nairobi, Kenya<br/>"
            "<b>Phone / WhatsApp:</b> +254 (0) 720 280 171<br/>"
            "<b>Email:</b> hildahk83@gmail.com &bull; <b>Web:</b> www.kalmaxproductions.com",
            ParagraphStyle('ContactB1', parent=style_body, textColor=colors.white)
        ),
        Paragraph(
            "<b>MOV Foundation (Stichting MOV)</b><br/>"
            "Active in Northern Kenya education &amp; SME development for 25+ years<br/>"
            "<b>Web:</b> www.stichtingmov.nl &bull; <b>Project Portal:</b> sherisingnorth.com<br/>"
            "<b>High School Sponsorship:</b> KCB Paybill 522533 / Till 8144533",
            ParagraphStyle('ContactB2', parent=style_body, textColor=colors.white)
        )
    ]
]
t_contact = Table(contact_data, colWidths=[261, 262])
t_contact.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), c_deep),
    ('LINEBELOW', (0,0), (-1,0), 1, c_gold),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
]))
story.append(t_contact)

doc.build(story)
print(f"Generated Press Kit PDF at {pdf_path}")
