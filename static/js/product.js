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

// TABLE ORDERING

    let tableHead = document.querySelectorAll('th');
    tableHeadIdon = tableHead
        len = window.location.href.split("&").length; // Get number of URL extensions
        urlEnd = window.location.href.split("&")[len-1]; // Get the last URL Extension
        

        console.log(window.location.href)
            console.log(len)
            console.log(urlEnd)

        for(let i=0; i < tableHead.length; i++){
            
            tableHead[i].addEventListener('click', sortTable);

            function sortTable(){

                if (urlEnd.includes('o=-')) {
                    console.log('desc');
                    path = '&o=' + tableHead[i].dataset.order;
                }
                else {
                    console.log('asc'); 
                    path = '&o=-' + tableHead[i].dataset.order;
                }
                // Try and make it so that here it removes the urlEnd, so the url doesn't get too long
                window.location.search += path;
            }
        }

        for(let i=0; i < tableHead.length; i++){

            if (urlEnd.includes(tableHead[i].dataset.order)){
                tableHead[i].firstElementChild.style.display = 'block';
                console.log(tableHead[i].dataset.order);
                if (urlEnd.includes('o=-')){
                    tableHead[i].firstElementChild.className = "arrow-down";
                    console.log('Descend')
                }
                else {
                    tableHead[i].firstElementChild.className = "arrow-up";
                    console.log('Ascend')
                }
            }
        }


    // This all relates to changing the arrow state, I think a separate for loop is needed for the arrow classes.
    // WRITE UP NOTES
    // tableHead[i].firstElementChild.style.display = 'block';
    // if(tableHead[i].firstElementChild.className == "arrow-down"){
    //     tableHead[i].firstElementChild.className = "arrow-up";
    // } else {
    //     tableHead[i].firstElementChild.className = "arrow-down";
    // }

    

// ** REMOVED DUE TO PAGE LOAD TIME **
// // PRODUCT LIST - EXPANDABLE PRODUCT TABLE ROW
//     // Expand the table row when click to show .extra-content
//     let row = document.querySelectorAll('#products tr.main-row');
//         extra = document.querySelectorAll('#products tr.extra-content');
//         children = document.querySelectorAll('.no-js')

//     for(let tr=0; tr < row.length; tr++){
//         row[tr].addEventListener('click', expandContent);
//         children[tr].addEventListener('click', e => e.stopPropagation());
            
//         function expandContent(){         
//             extra[tr].classList.toggle("active");
//         }
//     }  
        
    