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

// DELIVERY DETAILS
    // Set the <tr> Class to Highlight if field is 'Not Set'
let del = document.querySelectorAll('#non-form tr');
    buttonPick = document.querySelector('#button-pick');
    buttonShip = document.querySelector('#button-ship');

for(let i=0; i < del.length; i++){
    if (del[i].textContent.includes('Not Set') == true) {
        del[i].className = "highlight";
        buttonPick.setAttribute('disabled', '');
        buttonShip.setAttribute('disabled', '');
    }
}

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