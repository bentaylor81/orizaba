// BILLING DETAILS
    // Convert the purchased on website code to readable format
let purchased = document.querySelector('#purchased-on').innerHTML;

    if (purchased.includes('GARD')){
        site = 'gardentractorspares.co.uk'     
    } else if (purchased.includes('WEST')) {
        site = 'westwoodtractorspares.co.uk'    
    } else if (purchased.includes('COUN')) {
        site = 'countaxtractorspares.co.uk' 
    } else if (purchased.includes('SNAP')) {
        site = 'snappertractorspares.co.uk' 
    } else if (purchased.includes('TORO')) {
        site = 'torotractorspares.co.uk' 
    } else if (purchased.includes('HAYT')) {
        site = 'hayterspares.co.uk'
    } else if (purchased.includes('BRIG')) {
        site = 'briggsandstrattonparts.co.uk' 
    } 
    document.querySelector('#purchased-on').innerHTML = site  

// CREATE PICKLIST 
    //Limit the Send Qty !> Item Qty
    // Set the initial Send Qty = Item Qty
let sendQty = document.querySelectorAll('#send-qty input');
    itemQty = document.querySelectorAll('#item-qty');

for(let i=0; i < sendQty.length; i++){
    sendQty[i].setAttribute("max", itemQty[i].innerHTML);
    sendQty[i].setAttribute("value", itemQty[i].innerHTML);
}

// EMAIL INVOICE - OPEN MODAL
let emailButton = document.querySelector('#email-invoice');
    emailButton.addEventListener('click', emailInvoice)

function emailInvoice(event) {
    event.preventDefault()   
}

// EMAIL INVOICE - ADD CUSTOM MESSAGE TO TEMPLATE
let customMessage = document.querySelector('#custom-message-textarea')
    emailTemplate = document.querySelector('#email-template')
    emailTemplateCustom = document.querySelector('#email-custom-message')
    submittedTextarea = document.querySelector('#submitted-textarea')

    // If no custom message is entered, submit the default message
    submittedTextarea.innerHTML = emailTemplate.innerHTML

    // As content a customer message is typed, it is added to the template and then to the submitted textarea
    customMessage.addEventListener('keyup', function() {

        // Adds lines breaks to the text
        formatText = customMessage.value.replace(/\n/g, '<br>\n')
        // Adds the text aboce to the email template html
        emailTemplateCustom.innerHTML = formatText;
        // Add the whole email template HTML to the textarea to be submitted to Mailgun 
        submittedTextarea.innerHTML = emailTemplate.innerHTML    
    });

// CREATE SHIPMENT - MODAL 
let itemRow = document.querySelectorAll('.item-table .item-row')
    weight = document.querySelectorAll('.item-table .weight')
    price = document.querySelectorAll('.item-table .price')
    itemQty = document.querySelectorAll('.item-table .item-qty input');
    sendQty = document.querySelectorAll('.item-table .send-qty input')
    totalItemPriceTd = document.querySelectorAll('.item-table .total-item-price')
    totalItemWeightTd = document.querySelectorAll('.item-table .total-item-weight')
    totalPriceField = document.querySelector('.total-price')
    totalWeightField = document.querySelector('.total-weight')
    totalWeight = 0
    totalPrice = 0
    
    // CALCULATE THE INITIAL TOTAL WEIGHT AND TOTAL PRICE
    for(let i=0; i<itemRow.length; i++) {
        // Populate the total item price and weight table cells
        totalItemPriceTd[i].innerHTML = sendQty[i].value * price[i].innerHTML 
        totalItemWeightTd[i].innerHTML = sendQty[i].value * weight[i].innerHTML
        // Calculate the initial total price and weight
        totalPrice += parseFloat(totalItemPriceTd[i].innerHTML)
        totalWeight += parseFloat(totalItemWeightTd[i].innerHTML)
        // Populate the total price and weight fields
        totalPriceField.innerHTML = '£' + totalPrice.toFixed(2)    
        totalWeightField.innerHTML = totalWeight.toFixed(2) + 'kg'
        // Set the inputs for price and weight based on calculations above
        document.querySelector('#total_price').value = totalPrice.toFixed(2) 
        document.querySelector('#total_weight').value = totalWeight.toFixed(2)
    }
    
    // CALCULATE THE TOTAL PRICE AND WEIGHT AS THE SEND QTY IS CHANGED
    for(let i=0; i<itemRow.length; i++) {
        // Event listener when the send quantities are changed
        sendQty[i].addEventListener('change', function(){
            totalPrice = 0
            totalWeight = 0
            // Populate the total item price and weight table cells
            totalItemPriceTd[i].innerHTML = (sendQty[i].value * price[i].innerHTML)
            totalItemWeightTd[i].innerHTML = (sendQty[i].value * weight[i].innerHTML)
            // Calculate the initial total price and weight
            for(let j=0; j<itemRow.length; j++) { 
                totalPrice += parseFloat(totalItemPriceTd[j].innerHTML)
                totalWeight += parseFloat(totalItemWeightTd[j].innerHTML)
            }
            // Populate the total price and weight fields
            totalPriceField.innerHTML = '£' + totalPrice.toFixed(2)
            totalWeightField.innerHTML = totalWeight.toFixed(2) + 'kg'  
            // Set the inputs for price and weight based on calculations above
            document.querySelector('#total_price').value = totalPrice.toFixed(2)
            document.querySelector('#total_weight').value = totalWeight.toFixed(2)
       });       
    }
    // DISABLE SUBMIT BUTTON IF FIELDS ARE NOT SET
    let deliveryMethodSelect = document.querySelector('.shipping-info select')
        deliveryMethodDiv = document.querySelector('.delivery-method-div')
        shippingActionsButton = document.querySelector('.shipment-actions button')
        deliveryMethodDiv.style.backgroundColor = '#1c89062e'

        // DISABLE THE BUTTON IF NO METHOD IS SELECTED
        // SET THE COLOUR OF THE DELIVERY METHOD LABEL
        deliveryMethodSelect.addEventListener('change', function(){
            if(deliveryMethodSelect.value == 'Select Delivery Method') {
                deliveryMethodDiv.style.backgroundColor = '#1c89062e'
                shippingActionsButton.setAttribute('disabled', 'disabled')
            } 
            else {
                shippingActionsButton.removeAttribute('disabled', 'disabled')
                deliveryMethodDiv.style.backgroundColor = 'unset'
            }
        });
    // LOCAL STORAGE SAVE THE DATE
    let dateSent = document.querySelector('.date-method input')
        savedDate = localStorage.getItem('sentDate')
    
        // GET TODAYS DATE
        today = new Date();
        date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
        // POPULATE THE DATE FILTER WITH THE VALUE IN LOCAL STORAGE
        if(savedDate > date) {
            dateSent.value = savedDate
        }
        // SAVE THE DATE INTO LOCAL STORAGE
        dateSent.addEventListener('change', () => {
            localStorage.setItem('sentDate', dateSent.value);
        } )