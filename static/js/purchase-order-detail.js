// PURCHASE ORDER TOTALS
    // Colour the totals based on quantity recevied
    let partsOrdered = document.querySelector('#parts-ordered');
        partsReceived = document.querySelector('#parts-received');
        partsOutstanding = document.querySelector('#parts-outstanding');

        if (partsReceived.innerHTML == partsOrdered.innerHTML){
            partsOutstanding.classList.add('complete')
            partsReceived.classList.add('complete')
        } else if (partsReceived.innerHTML > 1) {
            partsOutstanding.classList.add('partial-complete')
            partsReceived.classList.add('partial-complete')
        }

// PURCHASE TABLE ITEMS
    // Colour the rows in the table based on quantity received
    let receivedCell = document.querySelectorAll('.part-received');
        orderedCell = document.querySelectorAll('.part-ordered');
        rowNumber = document.querySelectorAll('.part-row .part-count');
        outstandingCell = document.querySelectorAll('.part-outstanding'); 
        outstandingIcon = document.querySelectorAll('.part-outstanding span');

        for (let i=0; i < orderedCell.length; i++){
            if (receivedCell[i].innerHTML > 0) {
                if (receivedCell[i].innerHTML == orderedCell[i].innerHTML ) {
                    rowNumber[i].classList.add('complete')
                    outstandingCell[i].classList.add('complete')
                    outstandingIcon[i].innerHTML = '<img src="/static/img/icons/check-circle-solid.svg">'
                    document.querySelectorAll('.part-select')[i].setAttribute('disabled','disabled');
                    document.querySelectorAll('.label-checkbox')[i].setAttribute('disabled','disabled');
                } else if (receivedCell[i].innerHTML > 0) {
                    rowNumber[i].classList.add('partial-complete')
                    outstandingCell[i].classList.add('partial-complete')
                    outstandingIcon[i].innerHTML = '<img src="/static/img/icons/adjust-solid.svg">'
                }
            }
        }

// PURCHASE ORDER DETAIL
    // SHOW STATUS - Show the status when edit icon is clicked
    let editIcon = document.querySelector('#edit-status-icon');
        editIcon.addEventListener('click', showStatusEdit);

        function showStatusEdit() {
            document.querySelector('.edit-status').style.display = 'block';
            document.querySelector('.display-status').style.display = 'none';
        }

    // STATUS COLOUR - Set the Colour of the Status based on it's state
    let currentStatus = document.querySelector('.display-status .status');
        
        if (currentStatus.innerHTML == 'Complete') {
            currentStatus.classList.add('complete')
        }
        else if (currentStatus.innerHTML == 'Part Receipt') {
            currentStatus.classList.add('partial-complete')
        }
        else if (currentStatus.innerHTML == 'Unleashed') {
            currentStatus.classList.add('unleashed')
        }

    // EDIT NOTE - Show the edit note form when the icon is clicked
    let editNoteIcon = document.querySelector('#edit-note-icon');
        editNoteIcon.addEventListener('click', showNoteEdit);

        function showNoteEdit() {
            document.querySelector('.edit-note').style.display = 'block';
            document.querySelector('.display-note').style.display = 'none';
        }

    // ADD/EDIT COMMENT - Click in the cell to edit the comment on the PO item
    let selectComment = document.querySelectorAll('.comments');
        
        for(let i=0; i < selectComment.length; i++) {
            selectComment[i].addEventListener('click', showCommentEdit); 

            function showCommentEdit(){
                document.querySelectorAll('.comments .edit')[i].style.display = 'block';
                document.querySelectorAll('.comments .show')[i].style.display = 'none';
            }
        }

    // SET MINIMUM ORDER QTY INPUT TO QUANTITY RECEIVED
        // DISABLE THE DELETE BUTTON IF PARTS HAVE BEEN RECEIVED
    let partsOrderedQtyInput = document.querySelectorAll('.further-actions .edit input');
        partsReceivedQty = document.querySelectorAll('.part-received');

    for(let i=0; i < partsOrderedQtyInput.length; i++) {
        partsOrderedQtyInput[i].setAttribute('min', partsReceivedQty[i].innerHTML);

            if(partsReceivedQty[i].innerHTML > 0){
                document.querySelectorAll('.delete-checkbox input')[i].setAttribute('disabled', 'disabled')
                document.querySelectorAll('.delete-part')[i].setAttribute('disabled', 'disabled')
            }
    }

    // DATE_UPDATED FIELD - Set the date value for the row which is updated
    let dateUpdated = document.querySelectorAll('.date_updated')
        selectClick = document.querySelectorAll('.part-select')
        today = new Date();
        date = today.getFullYear()+'-'+('0'+(today.getMonth()+1)).slice(-2)+'-'+('0'+today.getDate()).slice(-2);

        for(let i=0; i < selectClick.length; i++) {
            selectClick[i].addEventListener('click', addDate);

            function addDate(){
                dateUpdated[i].setAttribute('value', date);
            }
        }

    // EXPANDABLE PRODUCT TABLE ROW - Shows the product image when the row is clicked.
    let row = document.querySelectorAll('#purchase-order .icon-right');
        extra = document.querySelectorAll('#purchase-order .extra-content');

        for(let i=0; i < row.length; i++){
            row[i].addEventListener('click', expandContent);           
            
            function expandContent(){     
                extra[i].classList.toggle("expanded-grid");
                row[i].classList.toggle("icon-down");
                document.querySelectorAll('.product-image')[i].appendChild(extra[i]);
            }
        }  

    // ADD ITEMS - so that items can be both editing or adding, the TOTAL_FORMS value needs to be set
    let rowCount = document.querySelectorAll('.part-row').length;      

        // This makes up the elements of the name attribute required to submit the new row
        poId = document.querySelector('#po-id').innerHTML
        nameBase = 'purchaseorderitem_set-'
        poIdAttrib = nameBase + rowCount + '-purchaseorder'
        idAttrib = nameBase + rowCount + '-id'
        productAttrib = nameBase + rowCount + '-product'
        productSkuAttrib = nameBase + rowCount + '-product_sku'
        qtyAttrib = nameBase + rowCount + '-order_qty'
        
        // This sets the name value of 'Purchase Order', 'ID', 'Product' and 'Order Qty'
        document.querySelector('.po-id').setAttribute('name', poIdAttrib)
        document.querySelector('.po-id').setAttribute('value', poId)
        document.querySelector('.po-item-id').setAttribute('name', idAttrib)
        document.querySelector('.po-item-product').setAttribute('name', productAttrib)
        document.querySelector('.po-item-product-sku').setAttribute('name', productSkuAttrib)
        document.querySelector('.po-item-qty input').setAttribute('name', qtyAttrib)

        // Set the number of total forms based on the number of current rows
            // Editing an existing row - totalForms is the same as the row count
        totForms = rowCount
        document.querySelector('#id_purchaseorderitem_set-TOTAL_FORMS').setAttribute('value', totForms);

        // Adding a new row - the value of totForms needs to be one greater than the row count 
            // This is incremented when the Product SKU dropdown is clicked
       
        document.querySelector('.po-item-product input').addEventListener('input', setTotForms);  

            function setTotForms(){
                totForms = rowCount + 1;   // Value contained in the name attribute in the inputs
                document.querySelector('#id_purchaseorderitem_set-TOTAL_FORMS').setAttribute('value', totForms);
            }
    
    // OPEN ICON NEXT TOO HEADER - Add an icon to show the add items boxes
    let openPartAdd = document.querySelector('#open-part-add');
        receivedSelect = document.querySelectorAll('.received-select select');
        commentsInput = document.querySelectorAll('.comments .edit input');
        furtheractionsInput = document.querySelectorAll('.comments .edit input');

        // OPEN THE ADD PART BLOCK
        openPartAdd.addEventListener('click', openAddBlock);

        function openAddBlock(){
            document.querySelector('.add-po-item').style.display = 'inline-block';

            // When this block is open the input fields in the main row are disabled
            for(let i=0; i < receivedSelect.length; i++ ){
                document.querySelectorAll('.received-select select')[i].setAttribute('disabled', 'disabled');
                document.querySelectorAll('.comments .edit input')[i].setAttribute('disabled', 'disabled');
                document.querySelectorAll('.comments .edit button')[i].setAttribute('disabled', 'disabled');
                document.querySelectorAll('.further-actions button')[i].setAttribute('disabled', 'disabled');
                document.querySelectorAll('.further-actions .delete-part')[i].setAttribute('disabled', 'disabled');
                document.querySelectorAll('.further-actions input')[i].setAttribute('disabled', 'disabled');
            }
        }

        // CLOSE THE ADD PART BLOCK
            // Also set the total number of forms back to number of rows, so that the formset can be edited.     
        function closeAddBlock(){
            document.querySelector('.add-po-item').style.display = 'none';

            totForms = rowCount
            document.querySelector('#id_purchaseorderitem_set-TOTAL_FORMS').setAttribute('value', totForms);

            for(let i=0; i < receivedSelect.length; i++ ){
                document.querySelectorAll('.received-select select')[i].removeAttribute('disabled', 'disabled');
                document.querySelectorAll('.comments .edit input')[i].removeAttribute('disabled', 'disabled');
                document.querySelectorAll('.comments .edit button')[i].removeAttribute('disabled', 'disabled');
                document.querySelectorAll('.further-actions button')[i].removeAttribute('disabled', 'disabled');
                document.querySelectorAll('.further-actions .delete-part')[i].removeAttribute('disabled', 'disabled');
                document.querySelectorAll('.further-actions input')[i].removeAttribute('disabled', 'disabled');
            }
        }     

        // Make a contents section
        // Highlight a part and fade once it's been added
        // Quick addition of parts, no check box
        // QTY ordered value is always 1 in HTML, make this dynamic
        // Document HTML
        // Form error messages
        // Disable add part button if no product in there, or disable by default




