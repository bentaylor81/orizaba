class PurchaseOrderDetail(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    template_name = 'app_products/purchase_order_detail/purchase-order-detail.html'
    model = PurchaseOrder
    form_class = PurchaseOrderForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        po_item_form = PoItemFormset(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form, po_item_form=po_item_form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all()
        po_item = PurchaseOrderItem.objects.filter(purchaseorder__po_id=self.object.pk)
        context['total_lines'] = po_item.count or 0 
        context['parts_ordered'] = po_item.aggregate(Sum('order_qty'))['order_qty__sum'] or 0
        context['parts_received'] = po_item.aggregate(Sum('received_qty'))['received_qty__sum'] or 0
        context['parts_outstanding'] = context['parts_ordered'] - context['parts_received'] or 0
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() 
        po_id = self.object.po_id

        if 'status' in request.POST or 'notes' in request.POST or 'edit-po' in request.POST:
            form = PurchaseOrderForm(self.request.POST, instance=self.object)  
            if form.is_valid(): 
                form.save()
                messages.success(request, 'Purchase Order Saved')
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.form_invalid(form)
        else:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            po_item_form = PoItemFormset(self.request.POST, instance=self.object)
            if (po_item_form.is_valid() and form.is_valid()):
                po_item_form.save()
                for form in po_item_form:
                    sku = form['product_sku'].value()
                    qty = form['delivery_qty'].value()  
                    product_id = int(form['product'].value())  
                    comments = form['comments'].value()
                    now = datetime.now()     
                    # STOCK MOVEMENT - ADD A ROW TO THE STOCK MOVEMENT TABLE    
                    if (qty and int(qty) != 0):
                        product_inst = Product.objects.get(pk=product_id)
                        # ADDS THE CURRENT STOCK QTY (PRODUCT TABLE) TO PURCHASE ORDER QTY
                        current_stock_qty = int(product_inst.orizaba_stock_qty) + int(qty) 
                        # SETS THE ROLLING STOCK VALUE IN THE STOCK MOVEMENT ROW
                        StockMovement.objects.create(date_added=now, product_id=product_inst, adjustment_qty=qty, movement_type="Purchase Order Receipt", purchaseorder_id=po_id, current_stock_qty=current_stock_qty, comments=comments) 
                        # SETS THE STOCK VALUE IN THE PRODUCT TABLE
                        Product.objects.filter(pk=product_id).update(orizaba_stock_qty=current_stock_qty)   
                    # PRODUCT LABEL - GENERATE LABEL BASED ON THE CHECKBOX
                    if (form['label'].value()==True):
                        # GENERATE A PDF FILE IN STATIC
                        projectUrl = 'http://' + request.get_host() + '/product/label/%s' % sku
                        pdfkit.from_url(projectUrl, "static/pdf/product-label.pdf", configuration=settings.WKHTMLTOPDF_CONFIG, options=settings.WKHTMLTOPDF_OPTIONS)        
                        # SELECT THE PRINTER
                        process = PrintProcess.objects.get(process_id=3)
                        printer_id = process.process_printer.printnode_id
                        # SEND TO PRINTNODE
                        payload = '{"printerId": '+str(printer_id)+', "title": "Label for: ' +str(sku)+ ' ", "contentType": "pdf_uri", "content":"https://orizaba.herokuapp.com/static/pdf/product-label.pdf", "source": "GTS Product Label", "options": {"copies": ' +str(qty)+ '}}'
                        response = requests.request("POST", "https://api.printnode.com/printjobs", headers=settings.PRINTNODE_HEADERS, data=payload)
                        print(response.text.encode('utf8'))
                return HttpResponseRedirect(self.get_success_url())
            else:
                return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('purchase-order-detail', kwargs={'pk': self.object.pk})   