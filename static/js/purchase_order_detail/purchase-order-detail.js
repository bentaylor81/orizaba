//// CONTENTS - PURCHASE ORDER DETAIL ////

// 1. TOP SECTION - COLOUR STATUS AND TOTALS
// 2. TOP SECTION - EDIT NOTES
// 3. ITEMS TABLE
    // 3A. COLOUR AND DISABLE ROWS BASED ON RECEIVED_STATUS
    // 3B. PRINT LABEL CHECKBOX
    // 3C. DISPLAY COMMENTS
    // 3D. EXPANDABLE PRODUCT TABLE ROW
    // 3E. MODEL - DISABLED RESET AND DELETE BUTTONS AND OPEN MODAL BUTTONS
// 4. ADD PART BLOCK AND SKU FILTER POPULATION
// 5. DISABLE OTHER DROPDOWNS ON LOAD

var query = document.querySelector.bind(document)
var queryAll = document.querySelectorAll.bind(document)

//// JAVASCRIPT ////

// 1. TOP SECTION - COLOUR STATUS AND TOTALS
let totalOrdered = document.querySelector('#parts-ordered')
    totalReceived = query('.totalReceived')
    totalOutstanding = query('.totalOutstanding')
    poStatus = query('.poStatus')

    if (totalOutstanding.innerHTML == 0){
        totalReceived.classList.add('complete')
        totalOutstanding.classList.add('complete')
        poStatus.classList.add('complete')
    } else if (totalReceived.innerHTML > 1) {
        totalReceived.classList.add('partial-complete')
        totalOutstanding.classList.add('partial-complete')
        poStatus.classList.add('partial-complete')
    }

// 2. TOP SECTION - EDIT NOTES
let editNoteIcon = query('.editNoteIcon')
    editNote = query('.editNote')
    displayNote = query('.displayNote') 

    editNoteIcon.addEventListener('click', () => {
        editNote.style.display = 'block'
        displayNote.style.display = 'none'
    })

// 3. ITEMS TABLE
let partRow = queryAll('.partRow') 
    poNumber = query('.poNumber')  
    // SECTION A - COLOUR AND DISABLE ROWS BASED ON RECEIVED_STATUS
    receivedStatus = queryAll('.receivedStatus')
    partCount = queryAll('.partCount')
    deliveryQty = queryAll('.deliveryQty')
    // SECTION B - PRINT LABEL CHECKBOX
    printLabelCheck = queryAll('.printLabelCheck')
    printLabel = queryAll('.printLabel')
    // SECTION C - DISPLAY COMMENTS
    comments = queryAll('.comments')
    showComment = queryAll('.showComment')
    editComment = queryAll('.editComment')
    editCommentInput = queryAll('.editCommentInput')
    // SECTION D - EXPANDABLE PRODUCT TABLE ROW
    rowArrowIcon = queryAll('.rowArrowIcon')
    extraContent = queryAll('.extraContent')
    // SECTION E - MODALS
    receivedQty = queryAll('.receivedQty')
    resetButton = queryAll('.resetButton')
    deleteButton = queryAll('.deleteButton')
    resetModal = queryAll('.resetModal') 
    deleteModal = queryAll('.deleteModal') 

    for(let i=0; i < partRow.length; i++) {
        // SECTION A 
        if(receivedStatus[i].innerHTML.includes('Full Receipt')) {
            partRow[i].style.background = '#1c8c0552'
            deliveryQty[i].setAttribute('hidden','hidden')
            printLabelCheck[i].setAttribute('hidden','hidden')
        } else if(receivedStatus[i].innerHTML.includes('Partial Receipt')) {
            partRow[i].style.background = '#ff710038'
        }
        // SECTION B
        checkLabel()
        printLabelCheck[i].addEventListener('change', checkLabel)

        function checkLabel() { 
            if(printLabelCheck[i].checked == true) {
                printLabel[i].value = 'true'
            } else {
                printLabel[i].value = 'false'
            }     
        }
        // SECTION C
        showComment[i].addEventListener('click', () => {
            if(editCommentInput[i].value == 'None') {
                editCommentInput[i].value = ''
            }
            editComment[i].value = ''
            editComment[i].style.display = 'block'
            showComment[i].style.display = 'none'
        })
            // SHOW THE COMMENT ICON
            if((showComment[i].innerHTML.includes('None')) || (showComment[i].innerHTML.trim() == '')) {
                showComment[i].innerHTML = '<i class="fas fa-edit"></i>'
            }
        // SECTION D
        rowArrowIcon[i].addEventListener('click', () => {
            extraContent[i].classList.toggle("expanded-grid")
            rowArrowIcon[i].classList.toggle("icon-down")
        })
        // SECTION E
        // DISBALE MODEL BUTTONS FOR RESET AND DELETE
        if(receivedQty[i].innerHTML == 0){
            resetButton[i].setAttribute('disabled', 'disabled')
        } else if(receivedQty[i].innerHTML != 0) {
            deleteButton[i].setAttribute('disabled', 'disabled')
        }
        // OPEN RESET MODAL        
        resetButton[i].addEventListener('click', () => {
            resetModal[i].style.display = 'block'
        })
        // OPEN DELETE MODAL
        deleteButton[i].addEventListener('click', () => {  
            deleteModal[i].style.display = 'block'
        })
    }

// 4. ADD PART BLOCK AND SKU FILTERING
    // VARS - ADD PART BLOCK
let openPartAdd = query('.openPartAdd')
    addPoItem = query('.addPoItem')
    poFilter = query('.poFilter')
    closePartAdd = query('.closePartAdd')
    poTable = query('.poTable')
    // VARS - SKU FILTERING
    filterInput = query('.filterInput')
    partSku = queryAll('.partSku')   
    emptyRow = query('.emptyRow')

    // EVENT LISTENERS
    openPartAdd.addEventListener('click', openAddBlock)
    closePartAdd.addEventListener('click', closeAddBlock )
    poTable.addEventListener('click', closeAddBlock )
    // OPEN AND CLOSE FUNCTIONS
    function openAddBlock() {
        localStorage.setItem('partAddBox', 'open')
        addPoItem.style.display = 'inline-block'
        poFilter.style.display = 'none'
        // REMOVE SKU FILTERING TO SHOW ALL RESULTS
        localStorage.setItem('poNumber', poNumber.innerHTML)
        localStorage.setItem('poFilterSku', '')
        skuTableFilter()
        noRowsMessage()
    }
    function closeAddBlock() {
        localStorage.setItem('partAddBox', 'closed')
        addPoItem.style.display = 'none'
        poFilter.style.display = 'block'
    }
    // LOCAL STORAGE FOR openPartAdd TO KEEP THE BOX OPEN IF SET TO OPEN
    if((localStorage.getItem('partAddBox') == 'open') && (localStorage.getItem('poNumber') == poNumber.innerHTML)) {
        openAddBlock()
    } else {
        closeAddBlock()
    }

    // SKU FILTER POPULATION
    activeRows = false
    if(partRow.length != 0) {
        activeRows = true
    } 
    // EVENT LISTENER
    filterInput.addEventListener('keyup', () => {
        localStorage.setItem('poFilterSku', filterInput.value)
        localStorage.setItem('poNumber', poNumber.innerHTML)
        skuTableFilter()     
        noRowsMessage()               
    })

    function skuTableFilter() {     
        // SO FILTER BY LOCAL STORAGE DOESN'T HAPPEN ON ALL PURCHASE ORDERS
        poNumberStorage = localStorage.getItem('poNumber')   
        if(poNumber.innerHTML === poNumberStorage) {    
            // FILTER ROWS IF ON THE CORRECT PURCHASE ORDER       
            filterInput.value = localStorage.getItem('poFilterSku')
            activeRows = false
            for(let i=0; i < partRow.length; i++){                 
                // FILTER THE TABLE         
                if(partSku[i].innerText.toLowerCase().includes(filterInput.value.toLowerCase())) {
                    partRow[i].style.display = 'table-row';   
                    activeRows = true                
                } else {
                    partRow[i].style.display = 'none';
                }
            }
        }     
    }
    function noRowsMessage() {
        if(activeRows == false) {
            emptyRow.removeAttribute('hidden', 'hidden')
        } else {
            emptyRow.setAttribute('hidden', 'hidden')
        }
    }
    skuTableFilter() 
    noRowsMessage()
       
// 5. DISABLE OTHER DROPDOWNS ON LOAD
    let deliveryQtySelect = queryAll('.deliveryQty:not([hidden="hidden"])')
        printLabelCheck = queryAll('.printLabelCheck:not([hidden="hidden"])')

    for(let i=0; i < deliveryQtySelect.length; i++){     
        deliveryQtySelect[i].addEventListener('click', disableOthers) 
        deliveryQtySelect[i].addEventListener('blur', enableAll)              
    }
    // DISABLE OR ENABLE FUNCTIONS
    function disableOthers(){
        for(let i=0; i < deliveryQtySelect.length; i++){                 
            if(this != deliveryQtySelect[i]){
                deliveryQtySelect[i].setAttribute('hidden', 'hidden')
                printLabelCheck[i].setAttribute('hidden', 'hidden')
            }      
        }
    }
    function enableAll(){
        for(let i=0; i < deliveryQtySelect.length; i++){ 
            deliveryQtySelect[i].removeAttribute('hidden', 'hidden')
            printLabelCheck[i].removeAttribute('hidden', 'hidden')
        }
    }

    