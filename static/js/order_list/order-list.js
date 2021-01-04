//// CONTENTS - ORDER LIST ////

// 1. ORDER FILTERS 
// 2. SET THE BACKGROUND COLOUR OF THE ROW BASED ON ORDER STATUS


//// JAVASCRIPT ////

var query = document.querySelector.bind(document)
var queryAll = document.querySelectorAll.bind(document)

// 1. ORDER FILTERS 
    // BUTTON TO SET THE DATE SELECTOR AS TODAY
    let todayButton = query('.todayButton')
        date = new Date()
        todayFilter = date.getFullYear()+'-'+('0'+(date.getMonth()+1)).slice(-2)+'-'+('0'+date.getDate()).slice(-2)
        tomorrow = date.setDate(new Date().getDate()+1)
        tomorrowFilter = date.getFullYear()+'-'+('0'+(date.getMonth()+1)).slice(-2)+'-'+('0'+date.getDate()).slice(-2)
        
    todayButton.addEventListener('click', (event) => {
        event.preventDefault()
        query('#dateFromInput').value = todayFilter
        query('#dateToInput').value = tomorrowFilter
    })

    // BUTTON TO CLEAR THE JS FILTERS
    let clearButton = query('.clearButton')

    clearButton.addEventListener('click', (event) => {
        event.preventDefault()
        query('#id_order').value = ""
        query('#id_billing_lastname').value = ""
        query('#id_order_status').value = ""
        query('#dateFromInput').value = ""
        query('#dateToInput').value = ""
    })

// 2. SET THE BACKGROUND COLOUR OF THE ROW BASED ON ORDER STATUS
var tableRow = queryAll('#order-row');
var orderStatus = queryAll('.status span');

    for(let i=0; i < tableRow.length; i++){
        if(orderStatus[i].innerHTML == 'Shipment Created'){
            tableRow[i].classList.add('shipment-created');
        }
    }