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
    if (del[i].textContent.includes('Not Set') == true){
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


