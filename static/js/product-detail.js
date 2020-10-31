//// CONTENTS - PRODUCT DETAIL ////

// 1. STOCK QUANTITY SET CLASS
// 2. STOCK MOVEMENT TABLE - SET THE STOCK QTY FORMAT IF IT IS NONE
// 3. OPEN AND CLOSE THE ADD MANUAL STOCK ADJUSTMENT BLOCK

//// JAVASCRIPT ////

// 1. STOCK QUANTITY SET CLASS
    // Style the Stock Quantity class depending on the quantity
    let stock = document.querySelectorAll('.stock span');

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
    
// 2. STOCK MOVEMENT TABLE - SET THE STOCK QTY FORMAT IF IT IS NONE
    let stockQty = document.querySelectorAll('.stock-movement .stock-qty')

    for(let i=0; i < stockQty.length; i++){
        let value = stockQty[i].innerHTML;
        if (value == 'None') {
            stockQty[i].innerHTML = '--'
        }
    } 

// 3. OPEN AND CLOSE THE ADD MANUAL STOCK ADJUSTMENT BLOCK
    let openAdjAdd = document.querySelector('#add-adj-icon'); 
        openAdjAdd.addEventListener('click', function(){
            document.querySelector('.add-adj-block').style.display = 'block';
        });

    let closeAdjAdd = document.querySelector('#close-adj-icon'); 
        closeAdjAdd.addEventListener('click', function(){
            document.querySelector('.add-adj-block').style.display = 'none';
        });
