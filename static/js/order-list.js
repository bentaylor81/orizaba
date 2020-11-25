var query = document.querySelector.bind(document);
var queryAll = document.querySelectorAll.bind(document);

// SET THE BACKGROUND COLOUR OF THE ROW BASED ON ORDER STATUS
var tableRow = queryAll('#order-row');
var orderStatus = document.querySelectorAll('.status span');
    console.log(orderStatus)

    for(let i=0; i < tableRow.length; i++){
        console.log(orderStatus[i].innerHTML)
        if(orderStatus[i].innerHTML == 'Shipment Created'){
            tableRow[i].classList.add('shipment-created');
        }
    }

