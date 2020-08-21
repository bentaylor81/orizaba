// STOCK QUANTITY SET CLASS
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

// PRODUCT LIST - EXPANDABLE PRODUCT TABLE ROW
    // Expand the table row when click to show .extra-content
    let row = document.querySelectorAll('#products tr.main-row');
        extra = document.querySelectorAll('#products tr.extra-content');
        children = document.querySelectorAll('.no-js')

    for(let tr=0; tr < row.length; tr++){
        row[tr].addEventListener('click', expandContent);
        children[tr].addEventListener('click', e => e.stopPropagation());
            
        function expandContent(){         
            extra[tr].classList.toggle("active");
        }
    }  
        
    