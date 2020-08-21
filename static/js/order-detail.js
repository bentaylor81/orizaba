// BILLING DETAILS
    // Convert the purchased on website code to readable format
let purchased = document.querySelector('#purchased-on').innerHTML;

    if (purchased.includes('GARDEN')){
        site = 'gardentractorspares.co.uk'     
    } else if (purchased.includes('WESTWOOD')) {
        site = 'westwoodtractorspares.co.uk'    
    } else if (purchased.includes('COUNTAX')) {
        site = 'countaxtractorspares.co.uk' 
    } else if (purchased.includes('SNAPPER')) {
        site = 'snappertractorspares.co.uk' 
    } else if (purchased.includes('TORO')) {
        site = 'torotractorspares.co.uk' 
    } else if (purchased.includes('HAYTER')) {
        site = 'hayterspares.co.uk'
    } else if (purchased.includes('BRIGGS')) {
        site = 'briggsandstrattonparts.co.uk' 
    }
    document.querySelector('#purchased-on').innerHTML = site  

// DELIVERY DETAILS
    // Set the <tr> Class to Highlight if field is 'Not Set'
let del = document.querySelectorAll('#non-form tr');

for(let i=0; i < del.length; i++){
    if (del[i].textContent.includes('Not Set') == true){
        del[i].className = "highlight";
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


