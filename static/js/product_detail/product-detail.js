//// CONTENTS - PRODUCT DETAIL ////

// 1. STOCK QUANTITY SET CLASS
// 2. STOCK MOVEMENT TABLE - SET THE STOCK QTY FORMAT IF IT IS NONE
    // 2A. - SET THE STOCK QTY FORMAT IF IT IS NONE
    // 2B. OPEN AND CLOSE THE ADD MANUAL STOCK ADJUSTMENT BLOCK
    // 2C. FILTER TABLE ITEMS FROM TEXT SEARCH AND DROPDOWN
// 3. STOCK STATUS - HIDE THE PURCHASE ORDER BOX IF NO ITEMS ON PURCHASE ORDERS

//// JAVASCRIPT ////

var query = document.querySelector.bind(document);
var queryAll = document.querySelectorAll.bind(document);
var cn = console.log.bind(document);

// 1. STOCK QUANTITY SET CLASS
    // Style the Stock Quantity class depending on the quantity
    let stock = queryAll('.stock span');

    for(let i=0; i < stock.length; i++){
        let value = stock[i].innerHTML;
        if (value > 5) {
            stock[i].className = 'good-stock';
        } else if (value == 0) {
            stock[i].className = 'no-stock';
        } else {
            stock[i].className = 'low-stock';
        }
    } 
    
// 2. STOCK MOVEMENT TABLE
    // 2A. - SET THE STOCK QTY FORMAT IF IT IS NONE
    let stockQty = queryAll('.stock-movement .stock-qty')
    for(let i=0; i < stockQty.length; i++){
        let value = stockQty[i].innerHTML;
        if (value == 'None') {
            stockQty[i].innerHTML = '--'
        }
    } 

    // 2B. OPEN AND CLOSE THE ADD MANUAL STOCK ADJUSTMENT BLOCK
    let openAdjAdd = query('#add-adj-icon'); 
        openAdjAdd.addEventListener('click', function(){
            query('.add-adj-block').style.display = 'block';
        });
    let closeAdjAdd = query('#close-adj-icon'); 
        closeAdjAdd.addEventListener('click', function(){
            query('.add-adj-block').style.display = 'none';
        });

// 3. STOCK STATUS - HIDE THE PURCHASE ORDER BOX IF NO ITEMS ON PURCHASE ORDERS
    let poStatusBar = query('.poStatusBar')
        partsOutstanding = query('.partsOutstanding')

    if(partsOutstanding.innerHTML == 0) {
        cn('gen')
        poStatusBar.style.display = 'none'
    }
        