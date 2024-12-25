 response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="ledger.pdf"'
            c = canvas.Canvas(response, pagesize=landscape(A3))
            width, height = landscape(A3)

            margin_left = 10 * mm
            margin_right = 15 * mm
            margin_top = 25 * mm
            top_section_height = 50 * mm
            table_header_height = 15 * mm
            line_height = 12
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margin_left, height - margin_top + 15, "Cavinkare Private Limited")
            c.setFont("Helvetica", 8)
            c.drawString(margin_left, height - margin_top , "Regional Office - South \"Cavainville\", No-12, Cenotaph Road, Chennai-600018")

            c.line(margin_left, height - margin_top - 5, width - margin_left, height - margin_top - 5)

            company_info_y = height - margin_top - top_section_height + 120
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin_left, company_info_y, "Company")
            c.setFont("Helvetica-Bold", 11)
            c.drawString(margin_left, company_info_y-12, company_name)
            c.setFont("Courier", 10)
            c.drawString(margin_left, company_info_y - 25, company_address)
            c.setFont("Courier", 12)
            c.drawString(margin_left, company_info_y-60, f"Account Statement from {start_date} to {end_date}")

            account_statement_width = 300
            account_statement_height = 80
            account_statement_x = width - margin_left - account_statement_width 
            account_statement_y = height - margin_top - account_statement_height - 5

            c.setStrokeColor(colors.black) 
            c.setLineWidth(1)             
            c.rect(
                account_statement_x,
                account_statement_y,
                account_statement_width,
                account_statement_height, 
                stroke=1  
            )
            c.setFillColor(colors.lightgrey)
            c.rect(
                account_statement_x,
                account_statement_y + account_statement_height - 20,
                account_statement_width,
                20,
                fill=1,
            )
            text_margin = 10
            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(account_statement_x + text_margin, account_statement_y + account_statement_height - 15, "Account Statement")
            c.setFont("Helvetica-Bold", 11)
            
            c.drawString(account_statement_x + text_margin, account_statement_y + account_statement_height - 35, "Date:")
            c.setFont("Courier", 10)
            c.drawString(account_statement_x + text_margin + 70, account_statement_y + account_statement_height - 35, f"{end_date.strftime('%d.%m.%Y')}")
            c.setFont("Helvetica-Bold", 11)
            c.drawString(account_statement_x + text_margin, account_statement_y + account_statement_height - 55, "Your account with us")
            c.setFont("Courier", 10)
            c.drawString(account_statement_x + text_margin, account_statement_y + account_statement_height -70, "2014494")


            current_y = height - margin_top - top_section_height+20
            c.line(margin_left, current_y+20, width - margin_left, current_y +20)
            c.setFont("Courier-Bold", 12) 
            def draw_page_border(c, margin_left, margin_right, margin_top, height):
                c.line(margin_left, margin_top-15, width - margin_left, margin_top-15)

            headers = ["Doc.No", "Doc.Date", "Doc.Type", "Item.Texts", "Dr.Amount", "Cr.Amount", "Balance"]
            header_x_positions = [margin_left, margin_left + 80, margin_left + 160, margin_left + 250, margin_left + 500, margin_left + 580, margin_left + 660]
            c.setFont("Courier-Bold", 12)
            for i, header in enumerate(headers):
                if header in ["Dr.Amount", "Cr.Amount", "Balance"]:
                    c.drawRightString(header_x_positions[i] + 40, current_y, header)
                else:
                    c.drawString(header_x_positions[i], current_y, header)
            current_y -= line_height

            c.setStrokeColor(colors.black)
            c.setLineWidth(1)
            c.line(margin_left, current_y , width - margin_left, current_y )
            current_y -= line_height

            c.setFont("Helvetica", 9)
            for entry in ledger_entries:
                if current_y < margin_top + line_height * 2: 
                    c.showPage()
                    current_y = height - margin_top - top_section_height
                    c.setFont("Courier-Bold", 12)
                    for i, header in enumerate(headers):
                        if header in ["Dr.Amount", "Cr.Amount", "Balance"]:
                            c.drawRightString(header_x_positions[i] + 40, current_y, header)
                        else:
                            c.drawString(header_x_positions[i], current_y, header)
                    current_y -= line_height
                    c.line(margin_left, current_y , width - margin_left, current_y )
                    current_y -= line_height
                    c.setFont("Helvetica", 9)

                entry_values = [
                    entry["Doc.No"],
                    entry["Doc.Date"].strftime('%d.%m.%Y') if entry["Doc.Date"] else '',
                    entry["Doc.Type"],
                    entry["Item.Texts"],
                    f"{entry['Dr.Amount']:.2f}" if entry['Dr.Amount'] > 0 else '0.00',
                    f"{entry['Cr.Amount']:.2f}" if entry['Cr.Amount'] > 0 else '0.00',
                    f"{entry['Balance']:.2f}"
                ]
                for i, value in enumerate(entry_values):
                    if headers[i] in ["Dr.Amount", "Cr.Amount", "Balance"]:
                        c.drawRightString(header_x_positions[i] + 40, current_y, str(value))
                    else:
                        c.drawString(header_x_positions[i], current_y, str(value))
                current_y -= line_height
            
            c.line(margin_left, margin_top+12, width - margin_left, margin_top+12) 
            c.setFont("Courier", 12)
            balance_text = f"Final Balance as of {end_date.strftime('%d.%m.%Y')}:"
            balance_amount = f"{ledger_entries[-1]['Balance']:.2f}"
            text_y = margin_top - (line_height // 2)
            c.drawString(margin_left, text_y, balance_text)
            c.drawRightString(width - margin_right - 15, text_y, balance_amount)

            draw_page_border(c, margin_left, margin_right, margin_top, height)

            c.save()
            return response