//// CONTENTS - PRODUCT LIST ////

// 1. TABLE ORDERING
// 2. LOOP TO SET THE ORDERING BY ASC OR DESC
// 3. LOOP TO SET THE DIRECTION OF THE ARROWS
// 4. STOCK QUANTITY SET CLASS

//// JAVASCRIPT ////

// 1. TABLE ORDERING
let tableHead = document.querySelectorAll('th');
len = window.location.href.split("&").length; // Get number of URL extensions
urlEnd = window.location.href.split("&")[len-1]; // Get the last URL Extension  
url = window.location.toString();

// 2. LOOP TO SET THE ORDERING BY ASC OR DESC
for(let i=0; i < tableHead.length; i++){
    
    tableHead[i].addEventListener('click', sortTable);

    function sortTable(){
        if (urlEnd.includes('o=-')) {
            path = '&o=' + tableHead[i].dataset.order;
        }
        else {
            path = '&o=-' + tableHead[i].dataset.order;
        }
        // REMOVES THE END OF THE URL AND REPLACES WITH THE NEW END
        if (len > 1) {
            window.location = url.replace('&' + urlEnd, path)
        }
        else {
            window.location.search += path; 
        }

    }
}

// 3. LOOP TO SET THE DIRECTION OF THE ARROWS
for(let i=0; i < tableHead.length; i++){

    if (urlEnd.includes(tableHead[i].dataset.order)){
        tableHead[i].firstElementChild.style.opacity = 'unset';
        tableHead[i].firstElementChild.style.backgroundImage = "url('/static/img/icons/caret-up-solid.svg')";

        if (urlEnd.includes('o=-')){
            tableHead[i].firstElementChild.style.backgroundImage = "url('/static/img/icons/caret-down-solid.svg')";
        }
        else {
            tableHead[i].firstElementChild.style.backgroundImage = "url('/static/img/icons/caret-up-solid.svg')";
        }
    }
}

// 4. STOCK QUANTITY SET CLASS
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

