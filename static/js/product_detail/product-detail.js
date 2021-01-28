//// CONTENTS - PRODUCT DETAIL ////

// 1. STOCK MOVEMENT TABLE
    // 1A. SET THE STOCK QTY FORMAT IF IT IS NONE
    // 1B. OPEN AND CLOSE THE ADD MANUAL STOCK ADJUSTMENT BLOCK
    // 1C. FILTER TABLE ITEMS FROM TEXT SEARCH AND DROPDOWN
// 2. STOCK STATUS
    // 2A. HIDE THE PURCHASE ORDER BOX IF NO ITEMS ON PURCHASE ORDERS
// 3. STOCK CHECK 
    // 3A. OPEN AND CLOSE THE DROPDOWN

//// JAVASCRIPT ////

var query = document.querySelector.bind(document);
var queryAll = document.querySelectorAll.bind(document);
var cn = console.log.bind(document);
    
// 1. STOCK MOVEMENT TABLE
    // 2A. - SET THE STOCK QTY FORMAT IF IT IS NONE
    let stockQty = queryAll('.stock-movement .stock-qty')
    for(let i=0; i < stockQty.length; i++){
        let value = stockQty[i].innerHTML;
        if (value == 'None') {
            stockQty[i].innerHTML = '--'
        }
    } 

    // 1B. OPEN AND CLOSE THE ADD MANUAL STOCK ADJUSTMENT BLOCK
    let openAdjIcon = query('#openAdjIcon') 
        openAdjBlock = query('.openAdjBlock')
        openAdjIcon.addEventListener('click', () => {
            openAdjBlock.style.display = 'block'
        })
    let closeAdjIcon = query('#closeAdjIcon'); 
        closeAdjIcon.addEventListener('click', () => {
            openAdjBlock.style.display = 'none'
        })

// 2. STOCK STATUS - HIDE THE PURCHASE ORDER BOX IF NO ITEMS ON PURCHASE ORDERS
    let poStatusBar = query('.poStatusBar')
        partsOutstanding = query('.partsOutstanding')

    if(partsOutstanding.innerHTML == 0) {
        poStatusBar.style.display = 'none'
    }
        
// 3. STOCK CHECK
    // 3A. OPEN AND CLOSE THE DROPDOWN
    let openCheckIcon = query('#openCheckIcon') 
        openCheckBlock = query('.openCheckBlock')
        openCheckIcon.addEventListener('click', () => {
            openCheckBlock.style.display = 'block'
        })
    let closeCheckIcon = query('#closeCheckIcon'); 
        closeCheckIcon.addEventListener('click', () => {
            openCheckBlock.style.display = 'none'
        })
    // 3B. ADJUST FORM INPUTS BASED ON ACTUAL STOCK ADDED
    let checkActQty = query('.checkActQty')
        checkAdjQty = query('.checkAdjQty')
        checkDiffQty = query('.checkDiffQty')
        differenceQty()

        checkActQty.addEventListener('keyup', () => {
            differenceQty()
        })

        function differenceQty() {
            // CALCULATE THE DIFFERENCE QTY
            checkDiffQty.value = checkActQty.value - checkAdjQty.value 
            // SET COLOURS OF THE INPUTS DEPENDING ON RESULT
            if(checkDiffQty.value != 0){
                checkDiffQty.style.background = "#ff710057"
            } else {
                checkDiffQty.style.background = "#1c8c0573"
            }
        }