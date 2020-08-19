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
