#!/usr/bin/env python3
"""
MissaTech Leadership Presentation Generator
Creates executive slides with budget-prioritized recommendations
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def create_presentation(output_path=None):
    """Generate leadership presentation PDF."""

    if output_path is None:
        output_path = Path(__file__).parent / "MissaTech_Executive_Presentation.pdf"

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=landscape(LETTER),
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.HexColor('#1a365d')
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=30,
        textColor=colors.HexColor('#2c5282')
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=20,
        spaceAfter=15,
        textColor=colors.HexColor('#1a365d')
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=8,
        leading=16
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=20,
        spaceAfter=6,
        leading=14
    )

    elements = []

    # SLIDE 1: Title Slide
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph("MISSATECH DATA BREACH", title_style))
    elements.append(Paragraph("Impact Analysis & Strategic Recommendations", subtitle_style))
    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph("Executive Leadership Briefing", body_style))
    elements.append(Paragraph("Business Intelligence & Cybersecurity Audit", body_style))
    elements.append(PageBreak())

    # SLIDE 2: Executive Summary
    elements.append(Paragraph("Executive Summary: Critical Findings", heading_style))
    elements.append(Spacer(1, 0.3*inch))

    summary_data = [
        ['Metric', 'Value', 'Impact'],
        ['Total Financial Loss', '$73.6M', 'CRITICAL'],
        ['Records Exposed', '4.35M', 'HIGH'],
        ['Avg Detection Time', '12 days', 'UNACCEPTABLE'],
        ['Incidents Analyzed', '100', '-'],
        ['Notification Required', '86%', 'Compliance Risk']
    ]

    summary_table = Table(summary_data, colWidths=[3*inch, 2.5*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a365d')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
    ]))
    elements.append(summary_table)
    elements.append(PageBreak())

    # SLIDE 3: Cost Breakdown
    elements.append(Paragraph("Financial Impact by System", heading_style))
    elements.append(Spacer(1, 0.2*inch))

    system_data = [
        ['System', 'Total Cost', 'Avg/Incident', 'Priority'],
        ['Billing', '$28.7M', '$1.31M', '🔴 CRITICAL'],
        ['HR', '$19.7M', '$1.09M', '🔴 CRITICAL'],
        ['CRM', '$16.5M', '$866K', '🟠 HIGH'],
        ['Support', '$6.1M', '$288K', '🟡 MEDIUM'],
        ['Analytics', '$2.7M', '$136K', '🟢 LOW']
    ]

    system_table = Table(system_data, colWidths=[2*inch, 2*inch, 2*inch, 2*inch])
    system_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
    ]))
    elements.append(system_table)

    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("<b>Key Insight:</b> Billing and HR systems account for 66% of total losses", body_style))
    elements.append(PageBreak())

    # SLIDE 4: Root Cause Analysis
    elements.append(Paragraph("Root Cause: Attack Vector Analysis", heading_style))
    elements.append(Spacer(1, 0.2*inch))

    attack_data = [
        ['Attack Type', 'Incidents', 'Total Cost', '% of Losses'],
        ['Misconfiguration', '68', '$52.9M', '72%'],
        ['External Hacker', '16', '$11.6M', '16%'],
        ['Insider Threat', '16', '$9.2M', '12%']
    ]

    attack_table = Table(attack_data, colWidths=[2.5*inch, 1.5*inch, 2*inch, 1.5*inch])
    attack_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#c53030')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fff5f5')]),
    ]))
    elements.append(attack_table)

    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("<b>Critical Finding:</b> 72% of losses stem from PREVENTABLE misconfigurations", body_style))
    elements.append(Paragraph("• Infrastructure-as-Code could prevent majority of incidents", bullet_style))
    elements.append(Paragraph("• Current configuration management is inadequate", bullet_style))
    elements.append(PageBreak())

    # SLIDE 5: Budget-Prioritized Recommendations
    elements.append(Paragraph("Budget-Prioritized Action Plan", heading_style))
    elements.append(Spacer(1, 0.2*inch))

    budget_data = [
        ['Priority', 'Initiative', 'Investment', 'Expected ROI', 'Timeline'],
        ['1', 'Billing System Security Audit', '$500K-800K', '$3-5M savings', '0-30 days'],
        ['2', 'IaC + Security Scanning', '$1-2M', '$40-50M savings', '0-30 days'],
        ['3', 'SIEM/SOC Deployment', '$2-3M', '$15-20M savings', '0-30 days'],
        ['4', 'HR Zero-Trust Architecture', '$1-1.5M', '$8-10M savings', '30-90 days'],
        ['5', 'SOAR Implementation', '$1.5-2M', '$5-8M savings', '30-90 days'],
        ['6', 'Regional Standardization', '$500K-1M', '$3-5M savings', '30-90 days']
    ]

    budget_table = Table(budget_data, colWidths=[0.8*inch, 2.8*inch, 1.5*inch, 1.5*inch, 1.2*inch])
    budget_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#276749')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fff4')]),
        ('BACKGROUND', (0, 1), (-1, 3), colors.HexColor('#c6f6d5')),
    ]))
    elements.append(budget_table)
    elements.append(PageBreak())

    # SLIDE 6: ROI Analysis
    elements.append(Paragraph("Investment ROI Analysis", heading_style))
    elements.append(Spacer(1, 0.2*inch))

    roi_data = [
        ['Category', 'Amount'],
        ['Current Annual Breach Cost', '$73.6M'],
        ['', ''],
        ['Recommended Investment', '$8-12M'],
        ['', ''],
        ['Expected Savings', '$60-78M'],
        ['Net Annual Benefit', '$52-66M'],
        ['', ''],
        ['ROI', '82-106%']
    ]

    roi_table = Table(roi_data, colWidths=[4*inch, 3*inch])
    roi_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 3), (0, 3), 'Helvetica-Bold'),
        ('FONTNAME', (0, 5), (0, 6), 'Helvetica-Bold'),
        ('FONTNAME', (0, 8), (-1, 8), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 8), (-1, 8), 18),
        ('TEXTCOLOR', (0, 8), (-1, 8), colors.HexColor('#276749')),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#1a365d')),
        ('LINEBELOW', (0, 6), (-1, 6), 2, colors.HexColor('#276749')),
    ]))
    elements.append(roi_table)
    elements.append(PageBreak())

    # SLIDE 7: Quick Wins
    elements.append(Paragraph("Immediate Quick Wins (Week 1)", heading_style))
    elements.append(Spacer(1, 0.3*inch))

    elements.append(Paragraph("<b>1. Enable Cloud Security Posture Management (CSPM)</b>", body_style))
    elements.append(Paragraph("• AWS Config / Azure Policy / GCP Security Command Center", bullet_style))
    elements.append(Paragraph("• Cost: $0 (included in cloud services)", bullet_style))
    elements.append(Paragraph("• Impact: Immediate visibility into misconfigurations", bullet_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("<b>2. Enforce MFA on Billing & HR Systems</b>", body_style))
    elements.append(Paragraph("• Cost: Minimal (existing identity provider)", bullet_style))
    elements.append(Paragraph("• Impact: Reduces insider threat risk by 80%", bullet_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("<b>3. Enable Database Audit Logging</b>", body_style))
    elements.append(Paragraph("• Cost: Storage costs only", bullet_style))
    elements.append(Paragraph("• Impact: Reduces detection time from 12 to <5 days", bullet_style))
    elements.append(PageBreak())

    # SLIDE 8: KPIs
    elements.append(Paragraph("Success Metrics & KPIs", heading_style))
    elements.append(Spacer(1, 0.2*inch))

    kpi_data = [
        ['Metric', 'Current', 'Target (90 days)', 'Target (1 year)'],
        ['Mean Time to Detect (MTTD)', '12 days', '5 days', '<3 days'],
        ['Mean Time to Respond (MTTR)', '7 days', '4 days', '<3 days'],
        ['Cost per Breach', '$736K', '$500K', '<$300K'],
        ['Misconfiguration Rate', '68%', '40%', '<20%'],
        ['High-Sensitivity Exposure', '56%', '30%', '<10%']
    ]

    kpi_table = Table(kpi_data, colWidths=[2.5*inch, 1.5*inch, 1.8*inch, 1.8*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#553c9a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#faf5ff')]),
    ]))
    elements.append(kpi_table)
    elements.append(PageBreak())

    # SLIDE 9: Call to Action
    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph("Recommended Next Steps", title_style))
    elements.append(Spacer(1, 0.5*inch))

    elements.append(Paragraph("1. <b>APPROVE</b> immediate security investment of $8-12M", body_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("2. <b>AUTHORIZE</b> emergency Billing system security audit", body_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("3. <b>ESTABLISH</b> Security Operations Center (SOC) capability", body_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("4. <b>IMPLEMENT</b> weekly security posture reviews", body_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("5. <b>TRACK</b> progress via monitoring dashboard", body_style))

    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph("Expected Net Benefit: $52-66M annually", subtitle_style))

    # Build PDF
    doc.build(elements)
    print(f"Presentation saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    create_presentation()
