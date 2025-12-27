"""Utilidades para generación de PDF del inventario"""
from io import BytesIO
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from apps.inventario.models import Inventario


def generar_pdf_inventario(empresa_nit=None):
    """
    Genera un PDF con el inventario
    Args:
        empresa_nit: NIT de la empresa para filtrar (opcional)
    Returns:
        BytesIO buffer con el PDF generado
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    elements = []
    styles = getSampleStyleSheet()

    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    if empresa_nit:
        title = Paragraph(f"Reporte de Inventario - Empresa: {empresa_nit}", title_style)
        inventarios = Inventario.objects.filter(empresa__nit=empresa_nit).select_related('empresa', 'producto')
    else:
        title = Paragraph("Reporte de Inventario General", title_style)
        inventarios = Inventario.objects.all().select_related('empresa', 'producto')

    elements.append(title)

    # Fecha de generación
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    date_text = Paragraph(
        f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        date_style
    )
    elements.append(date_text)
    elements.append(Spacer(1, 20))

    # Tabla de inventario
    data = [['Empresa', 'Producto', 'Código', 'Cantidad', 'Ubicación']]

    for inv in inventarios:
        data.append([
            inv.empresa.nombre,
            inv.producto.nombre,
            inv.producto.codigo,
            str(inv.cantidad),
            inv.ubicacion or 'N/A'
        ])

    if len(data) == 1:
        data.append(['Sin datos', '', '', '', ''])

    table = Table(data, colWidths=[1.8*inch, 1.8*inch, 1*inch, 0.8*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976d2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (3, 1), (3, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdbdbd')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))

    elements.append(table)

    # Resumen
    elements.append(Spacer(1, 30))
    summary_style = ParagraphStyle(
        'Summary',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_LEFT
    )

    total_items = sum(inv.cantidad for inv in inventarios)
    total_productos = inventarios.count()

    summary = Paragraph(
        f"<b>Total de productos en inventario:</b> {total_productos}<br/>"
        f"<b>Total de items:</b> {total_items}",
        summary_style
    )
    elements.append(summary)

    # Footer
    elements.append(Spacer(1, 40))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    footer = Paragraph(
        "Lite Thinking - Sistema de Gestión de Inventario © 2025",
        footer_style
    )
    elements.append(footer)

    doc.build(elements)
    buffer.seek(0)
    return buffer
