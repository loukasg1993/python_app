from reportlab.lib.pagesizes import letter, A4
from .models import personal_information, appointment

from datetime import datetime, timezone, timedelta

from reportlab.lib.pagesizes import letter

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus.tables import Table, TableStyle, colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch


class MyPrint:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

    def add_page_number(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        page_number_text = "%d" % (doc.page)
        canvas.drawCentredString(
            0.75 * inch,
            0.75 * inch,
            page_number_text
        )
        canvas.restoreState()

    def pdf_tomorrow(self):
        now_date = datetime.today().date()

        if now_date.isoweekday() == 5:
            tomorrow = now_date + timedelta(days=3)
        elif now_date.isoweekday() == 6:
            tomorrow = now_date + timedelta(days=2)
        else:
            tomorrow = now_date + timedelta(days=1)
        doses_tomorrow = appointment.objects.filter(date__contains=tomorrow)

        total_dose = 0
        id = []
        amka = []
        date = []
        dose = []
        for i in doses_tomorrow:
            p = i.dose
            id.append(i.id)
            amka.append(i.amka)
            dose.append(i.dose)
            date.append(i.date)
            total_dose = total_dose + p

        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=72,
                                bottomMargin=72,
                                pagesize=self.pagesize)

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.

        amka_tuple = list(zip(amka, date, dose))
        # for i,j in zip(amka,date):
        #     i=str(i)
        #     j=str(j)
        #     amka_tuple.append(i,j)
        total_dose = str(round(total_dose, 4))
        amka_tuple.insert(0, ['Amka', 'Date', 'Dose'])

        table = Table(amka_tuple, colWidths=150, rowHeights=40)

        table.setStyle(TableStyle(
            [('LINEABOVE', (0, 0), (-1, 0), 2, colors.lightskyblue),
             ('LINEABOVE', (0, 1), (-1, -1), 0.25, colors.black),
             ('LINEBELOW', (0, -1), (-1, -1), 2, colors.lightskyblue),
             ('ALIGN', (1, 1), (-1, -1), 'CENTER')]
        ))
        I = Image(
            'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQUmiT5AnD1x_BM_qDzo1pnXyjVuSabRrmZug&usqp=CAU')
        elements.append(I)
        elements.append(Spacer(2, 0.3 * inch))
        elements.append(table)
        elements.append(Paragraph('Total Dose:', styles['Heading2']))
        elements.append(Paragraph(total_dose, styles['Heading2']))
        doc.build(elements,
                  onFirstPage=self.add_page_number,
                  onLaterPages=self.add_page_number,
                  )

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf


class MyPrints:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

    def add_page_number(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        page_number_text = "%d" % (doc.page)
        canvas.drawCentredString(
            0.75 * inch,
            0.75 * inch,
            page_number_text
        )
        canvas.restoreState()

    def pdf_tomorrow(self):
        now_date = datetime.today().date()

        last = now_date + timedelta(days=-365)
        last_year = last.year
        last_year_info = appointment.objects.filter(date__contains=last_year)
        # .values_list('id','amka','dose','date')
        total_dose = 0
        total_bmi = 0
        id = []
        amka = []
        bmi = []
        dose = []
        dates = []

        for i in last_year_info:
            p = i.dose
            bm = i.bmi
            id.append(i.id)
            amka.append(i.amka)
            bmi.append(i.bmi)
            dose.append(i.dose)
            dates.append(i.date)
            total_bmi = total_bmi + bm
            total_dose = total_dose + p
        avg_bmi = total_bmi / len(bmi)
        avg_dose = total_dose / len(dose)
        date=[]
        for i in dates:
            i = datetime.strftime(i, '%Y/%m/%d %H:%M')
            date.append(i)

        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=72,
                                bottomMargin=72,
                                pagesize=self.pagesize)

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.

        last_year_tuple = list(zip(id,amka,bmi, date, dose))

        avg_dose = str(round(avg_dose, 4))
        avg_bmi  = str(round(avg_bmi, 4))
        last_year_tuple.insert(0, ['Id','       Amka','        Bmi', '     Date', '       Dose'])

        table = Table(last_year_tuple, colWidths=80, rowHeights=40)

        table.setStyle(TableStyle(
            [('LINEABOVE', (0, 0), (-1, 0), 2, colors.lightskyblue),
             ('LINEABOVE', (0, 1), (-1, -1), 0.25, colors.black),
             ('LINEBELOW', (0, -1), (-1, -1), 2, colors.lightskyblue),
             ('ALIGN', (1, 1), (-1, -1), 'CENTER')]
        ))
        I = Image(
            'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQUmiT5AnD1x_BM_qDzo1pnXyjVuSabRrmZug&usqp=CAU')
        elements.append(I)
        elements.append(Spacer(2, 0.3 * inch))
        elements.append(Paragraph('Average Dose: '+avg_dose, styles['Heading2']))
        # elements.append(Paragraph(avg_dose, styles['Heading2']))
        elements.append(Paragraph('Average Bmi: '+avg_bmi, styles['Heading2']))
        # elements.append(Paragraph(avg_bmi, styles['Heading2']))
        elements.append(table)

        # for name in names:
        #     elements.append(Paragraph(name['name'], styles['Heading1']))
        #
        # for i in date:
        #     i=str(i)
        #
        #     elements.append(Paragraph(i, styles['Normal']))
        # for j in amka:
        #     j=str(amka)
        #     elements.append(Paragraph(j, styles['Normal']))
        doc.build(elements,
                  onFirstPage=self.add_page_number,
                  onLaterPages=self.add_page_number,
                  )

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf