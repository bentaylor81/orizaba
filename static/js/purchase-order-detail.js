//// CONTENTS ////

// 1. PURCHASE ORDER TOTALS COLOURS
// 2. PURCHASE TABLE ITEMS COLOUR THE ROWS
// 3. SHOW STATUS
// 4. STATUS COLOUR
// 5. EDIT NOTE
// 6. ADD/EDIT COMMENT
// 7. SET MINIMUM ORDER QTY IN INPUT
// 8. DATE_UPDATED FIELD
// 9. EXPANDABLE PRODUCT TABLE ROW
// 10. ADD ITEMS
// 11. OPEN ICON NEXT TOO HEADER
// 12. OPEN THE ADD PART BLOCK
// 13. CLOSE THE ADD PART BLOCK
// 14. SKU FILTER BOX
// 15. PRODUCT ADD BLANK OTHER DROPDOWNS
// 16. DATE RECEIVED FILTERING - ** REMOVED **


//// JAVASCRIPT ////

// 1. PURCHASE ORDER TOTALS COLOURS
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

// 2. PURCHASE TABLE ITEMS
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

// 3. SHOW STATUS - Show the status when edit icon is clicked
let editIcon = document.querySelector('#edit-status-icon');
    editIcon.addEventListener('click', showStatusEdit);

function showStatusEdit() {
    document.querySelector('.edit-status').style.display = 'block';
    document.querySelector('.display-status').style.display = 'none';
}

// 4. STATUS COLOUR - Set the Colour of the Status based on it's state
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

// 5. EDIT NOTE - Show the edit note form when the icon is clicked
let editNoteIcon = document.querySelector('#edit-note-icon');
editNoteIcon.addEventListener('click', showNoteEdit);

function showNoteEdit() {
    document.querySelector('.edit-note').style.display = 'block';
    document.querySelector('.display-note').style.display = 'none';
}

// 6. ADD/EDIT COMMENT - Click in the cell to edit the comment on the PO item
let selectComment = document.querySelectorAll('.comments');

for(let i=0; i < selectComment.length; i++) {
    selectComment[i].addEventListener('click', showCommentEdit); 

    function showCommentEdit(){
        document.querySelectorAll('.comments .edit')[i].style.display = 'block';
        document.querySelectorAll('.comments .show')[i].style.display = 'none';
    }
}

// 7. SET MINIMUM ORDER QTY INPUT TO QUANTITY RECEIVED
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

// 8. DATE_UPDATED FIELD - Set the date value for the row which is updated
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

// 9. EXPANDABLE PRODUCT TABLE ROW - Shows the product image when the row is clicked.
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

// 10. ADD ITEMS - so that items can be both editing or adding, the TOTAL_FORMS value needs to be set
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

// 11. OPEN ICON NEXT TOO HEADER - Add an icon to show the add items boxes
let openPartAdd = document.querySelector('#open-part-add');
    receivedSelect = document.querySelectorAll('.received-select select');
    commentsInput = document.querySelectorAll('.comments .edit input');
    furtheractionsInput = document.querySelectorAll('.comments .edit input');

// 12. OPEN THE ADD PART BLOCK
openPartAdd.addEventListener('click', openAddBlock);

function openAddBlock() {
    document.querySelector('.add-po-item').style.display = 'inline-block';
    document.querySelector('.po-filter').style.display = 'none';
    localStorage.setItem('partAddBox', 'open');

    // When this block is open the input fields in the main row are disabled
    for(let i=0; i < receivedSelect.length; i++ ){
        document.querySelectorAll('.received-select select')[i].setAttribute('disabled', 'disabled');
        document.querySelectorAll('.comments .edit input')[i].setAttribute('disabled', 'disabled');
        document.querySelectorAll('.comments .edit button')[i].setAttribute('disabled', 'disabled');
        document.querySelectorAll('.further-actions button')[i].setAttribute('disabled', 'disabled');
        document.querySelectorAll('.further-actions .delete-part')[i].setAttribute('disabled', 'disabled');
        document.querySelectorAll('.further-actions input')[i].setAttribute('disabled', 'disabled');
        document.querySelectorAll('.label-checkbox')[i].setAttribute('disabled','disabled');
    }
}

// 13. CLOSE THE ADD PART BLOCK
    // Also set the total number of forms back to number of rows, so that the formset can be edited.     
function closeAddBlock(){
    document.querySelector('.add-po-item').style.display = 'none';
    document.querySelector('.po-filter').style.display = 'block';
    localStorage.setItem('partAddBox', 'closed');

    totForms = rowCount
    document.querySelector('#id_purchaseorderitem_set-TOTAL_FORMS').setAttribute('value', totForms);

    for(let i=0; i < receivedSelect.length; i++ ){
        document.querySelectorAll('.received-select select')[i].removeAttribute('disabled', 'disabled');
        document.querySelectorAll('.comments .edit input')[i].removeAttribute('disabled', 'disabled');
        document.querySelectorAll('.comments .edit button')[i].removeAttribute('disabled', 'disabled');
        document.querySelectorAll('.further-actions button')[i].removeAttribute('disabled', 'disabled');
        document.querySelectorAll('.further-actions .delete-part')[i].removeAttribute('disabled', 'disabled');
        document.querySelectorAll('.further-actions input')[i].removeAttribute('disabled', 'disabled');
        document.querySelectorAll('.label-checkbox')[i].removeAttribute('disabled','disabled');

        // This makes sure it doesn't re-enable the checkbox for the already completed row.
        if (receivedCell[i].innerHTML == orderedCell[i].innerHTML ) {
            document.querySelectorAll('.part-select')[i].setAttribute('disabled','disabled');
            document.querySelectorAll('.label-checkbox')[i].setAttribute('disabled','disabled');
        }
    }
}     
    // LOCAL STORAGE FOR openPartAdd TO KEEP THE BOX OPEN IF SET TO OPEN
    if(localStorage.getItem('partAddBox') == 'open') {
        openAddBlock()
    } else {
        closeAddBlock()
    }

// 14. SKU FILTER BOX - THE LIST DROPS DOWN WHEN SKU IS ADDED INTO THE FILTER BOX
let filterInput= document.querySelector('.po-filter #sku-input');
    tableSku = document.querySelectorAll('.part-sku');   
    partRow = document.querySelectorAll('.part-row');

    // ADJUST THE RESULTS ON EACH KEY PRESS IN THE FILTER BOX
    filterInput.addEventListener('keyup', function() {
        let inputSku = filterInput.value;
        localStorage.setItem('poFilterSku', filterInput.value); // Save to local storage on keyup

        for(let i=0; i < tableSku.length; i++){                 
            if(tableSku[i].innerText.includes(inputSku)) {
                partRow[i].style.display = 'table-row';                   
            } else {
                partRow[i].style.display = 'none';
            }
        }            
    });

    // GET LOCAL STORAGE AND POPULATE THE INPUT BOX
    const skuFilter = document.querySelector('.po-filter input');
        
        skuFilter.value = localStorage.getItem('poFilterSku')

    // SET THE VALUE OF THE INPUT TO THE LOCAL STORAGE VALUE
    let inputSku = filterInput.value;

        for(let i=0; i < tableSku.length; i++){                 
            if(tableSku[i].innerText.includes(inputSku)) {
                partRow[i].style.display = 'table-row';                   
            } else {
                partRow[i].style.display = 'none';
            }
        }

// 15. PRODUCT ADD BLANK OTHER DROPDOWNS
// This stops other dropdowns being selected once the option in a dropdown has been clicked. 
    let partSelect = document.querySelectorAll('.part-select:not([disabled="disabled"])')
        labelCheckbox = document.querySelectorAll('.label-checkbox:not([disabled="disabled"])')

        for(let i=0; i < partSelect.length; i++){           
            partSelect[i].addEventListener('focus', disableOther);     
            partSelect[i].addEventListener('blur', enableOther);
        }
    // Disables the other dropdowns
        function disableOther(){
            for(let i=0; i < partSelect.length; i++){                 
                if(this != partSelect[i]){
                    partSelect[i].setAttribute('disabled', 'disabled')
                    labelCheckbox[i].setAttribute('disabled', 'disabled')
                }       
            }
        }
    // Re-enables the other dropdowns when you click out of the clicked dropdown
        function enableOther(){
            for(let i=0; i < partSelect.length; i++){                 
                if(this != partSelect[i]){
                    partSelect[i].removeAttribute('disabled', 'disabled')
                    labelCheckbox[i].removeAttribute('disabled', 'disabled')
                }    
            }
        }

// // 16. DATE RECEIVED FILTERING - SHOW THE DATE RECEIVED FILTER WITH A DROPDOWN OF THE DATES
// REMOVED AS WE WON'T USE THIS PAGE TO FILTER THE DATE WHEN UPLOADING TO UNLEASHED
// let dateFilterSelect = document.querySelector('.po-filter #date-select');
//     dateReceived = document.querySelectorAll('#purchase-order .date-received');
    
//     for(let i=0; i < dateReceived.length; i++){
//         if(dateReceived[i].innerText != '') {
//             if(i==0 || dateReceived[i].innerHTML != dateReceived[i-1].innerHTML) {
//                 dateOption = "<option>" + dateReceived[i].innerHTML + "</option>"
//                 dateFilterSelect.insertAdjacentHTML('beforeend', dateOption)
//             }
//         }
//     }

//     // SHOW / HIDE ROWS BASED ON THE DATE
//     dateFilterSelect.addEventListener('input', function() {
//         let filterDate = dateFilterSelect.value;

//         for(let i=0; i < dateReceived.length; i++) {                 
//             if(dateReceived[i].innerText.includes(filterDate)) {
//                 partRow[i].style.display = 'table-row';                   
//             } else {
//                 partRow[i].style.display = 'none';
//             }
//         }            
//     });



