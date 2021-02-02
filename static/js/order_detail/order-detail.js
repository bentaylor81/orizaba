//// CONTENTS - ORDER DETAIL ////

// 1. BILLING DETAILS
// 4. EMAIL INVOICE - ADD CUSTOM MESSAGE TO TEMPLATE
// 5. DISABLE CREATE SHIPMENT BUTTON IF DELIVERY TYPE IS COLLECTION OR DELIVERY WITH ANOTHER ORDER
// 7. REFUNDS COMPONENT 

//// JAVASCRIPT ////

var query = document.querySelector.bind(document);
var queryAll = document.querySelectorAll.bind(document);

// 1. BILLING DETAILS
    // Convert the purchased on website code to readable format
let purchased = query('#purchased-on').innerHTML;

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
    } else {
        site = 'None'
    }
    query('#purchased-on').innerHTML = site  

// 4. EMAIL INVOICE - ADD CUSTOM MESSAGE TO TEMPLATE
let customMessage = query('.customMessage')
    emailTemplate = query('.emailTemplate')
    emailCustomMessage = query('.emailCustomMessage')
    submittedTextarea = query('.submittedTextarea')

    // IF NO CUSTOM MESSAGE IS ENTERED, SUBMIT THE DEFAULT MESSAGE
    submittedTextarea.innerHTML = emailTemplate.innerHTML

    // AS CONTENT IS TYPED, ADD MESSAGE TO THE TEMPLATE
    customMessage.addEventListener('keyup', function() {
        // ADD THE MESSAGE TO TEMPLATE AND SUBSTITUTE IN LINE BREAKS
        emailCustomMessage.innerHTML = customMessage.value.replace(/\n/g, '<br>\n')
        // ADD THE WHOLE EMAIL TEMPLATE HTML TO THE TEXTAREA TO BE SUBMITTED 
        submittedTextarea.innerHTML = emailTemplate.innerHTML    
    })

// 5. DISABLE CREATE SHIPMENT BUTTON IF DELIVERY TYPE IS COLLECTION OR DELIVERY WITH ANOTHER ORDER
let deliveryType = query('.delivery-type')
    deliveryTypeSelected =query('.delivery-type-selected') 
    createShipmentButton = query('.create-shipment button')

    // If Delivery Type is flatrate, change the text to Collection from Warehouse
    if(deliveryType.innerHTML == 'flatrate') {
        deliveryType.innerHTML = 'Collection from Warehouse'
        deliveryTypeSelected.innerHTML = 'Collection from Warehouse'
    }
    // If Delivery Type is Courier, change the text to Courier Delivery
    else if (deliveryType.innerHTML == 'Courier'){
        deliveryType.innerHTML = 'Courier Delivery'
        deliveryTypeSelected.innerHTML = 'Courier Delivery'
    }

    // Disable the Create Shipment button if Delivery Type is Collection or Combine Order
    if(deliveryType.innerHTML == 'Collection from Warehouse' || deliveryType.innerHTML == 'Combine with Another Order') {
        createShipmentButton.setAttribute('disabled', 'disabled');
        deliveryType.style.backgroundColor = '#1c89062e';
        deliveryType.style.padding = '5px';
    }
        

// REFUND COMPONENT - CALCULATE ITEM PRICE INC VAT
    let refItemAmount = queryAll('.refItemAmount')
        refItemAmountIncVat = queryAll('.refItemAmountIncVat')

        for(let i=0; i < refItemAmount.length; i++){
         refItemAmountIncVat[i].innerHTML = parseFloat(refItemAmount[i].innerHTML * 1.2).toFixed(2)
        }