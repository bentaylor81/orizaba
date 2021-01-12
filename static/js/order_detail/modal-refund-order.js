//// CONTENTS - REFUND ORDER MODAL ////

// 1. MAIN LOOP - CALCULATE TOTALS
    // 1A. WHEN CHECKBOXES ARE SELECTED, THE QTY IS XEROED OR RESTORED TO ORIGINAL
    // 1B. AS ORDER QTY IS CHANGED THE SELECTED TOTAL IS UPDATED
    // 1C. FUNCTION TO CALCULATE ALL OF THE TOTALS
// 2. MANUAL REFUND AMOUNTS - FORM SETTING IF USER CHOOSES MANUAL REFUND  
// 3. MANUAL REFUND NOT ALLOW FURTHER ITEM REFUNDS
// 3. MANUAL REFUND AMOUNTS
// 4. DISABLE THE REFUND BUTTON IF AMOUNT TO REFUND IF 0

//// JAVASCRIPT ////

// VARIABLES 
let refItemRow = queryAll('.refItemRow')
    refItemCheckbox = queryAll('.refItemCheckbox')
    refItemPrice = queryAll('.refItemPrice')
    refItemOrderedQty = queryAll('.refItemOrderedQty') 
    refItemQty = queryAll('.refItemQty') 
    refItemExVat = queryAll('.refItemExVat')
    refItemVat = queryAll('.refItemVat')
    refItemIncVat = queryAll('.refItemIncVat')
    selectedTotal = query('.selectedTotal')
    orderTotalPrice = query('.orderTotalPrice').innerHTML
    refTotalPrice = query('.refTotalPrice')
    refCheckInput = queryAll('.refCheckInput')
    manualLineDesc = query('.manualLineDesc')
    manualLineItemQty = query('.manualLineItemQty')
    manualLinePrice = query('.manualLinePrice')
    alreadyRefundedQty = queryAll('.alreadyRefundedQty')
    refundOrderButton = query('.refundOrderButton')
    totalRefunded = query('.totalRefunded')
    manualRefundCheck = query('.manualRefundCheck')

// 1. MAIN LOOP - CALCULATE TOTALS
for(let i=0; i < refItemRow.length; i++){
    // SET THE REFUNDQTY VALUE TO refItemOrderedQty - alreadyRefundedQty
    refItemQty[i].value = refItemOrderedQty[i].innerHTML - alreadyRefundedQty[i].innerHTML
    // SET THE MAX VALUE TO refItemOrderedQty - alreadyRefundedQty
    refItemQty[i].setAttribute('max', refItemQty[i].value)
    // UNCHECK THE CHECKBOX IF THE ABOVE IS 0
    if(refItemQty[i].value == 0) {
        refItemCheckbox[i].disabled = true
    }
    calculateTotals()

    // 1A. WHEN CHECKBOXES ARE SELECTED, THE QTY IS XEROED OR RESTORED TO ORIGINAL
    refItemCheckbox[i].addEventListener('change', () => {
        if(refItemCheckbox[i].checked == true) {
            refItemQty[i].value = refItemOrderedQty[i].innerHTML - alreadyRefundedQty[i].innerHTML
            // RESET MANUAL LINE PARAMETERS
            manualLineDesc.style.display = 'none'
            manualLineItemQty.value = 0
            query('#refund-order table').style.opacity = 'unset'
        }
        else {
            refItemQty[i].value = 0 
        }
        calculateTotals()
    }); 
    // 1B. AS ORDER QTY IS CHANGED THE SELECTED TOTAL IS UPDATED
    refItemQty[i].addEventListener('change', () => {
        // CHECKBOXES ARE RESTORED If QTY > 0 AND UNCHECKED IS QTY = 0
        if(refItemQty[i].value > 0) {
            refItemCheckbox[i].checked = true
            // RESET MANUAL LINE PARAMETERS
            manualLineDesc.style.display = 'none'
            manualLineItemQty.value = 0
            query('#refund-order table').style.opacity = 'unset'
        }
        else {
            refItemCheckbox[i].checked = false
        }
        calculateTotals()
    });      
    
    // 1C. FUNCTION TO CALCULATE ALL OF THE TOTALS
    function calculateTotals() {  
        // COUNT NUMBER OF CHECKBOXES CURRENTLY CHECKED  
        refItemCheckboxChecked = queryAll('.refItemCheckbox:checked')  
        // CALCULATE THE VAT AND TOTAL FIGURES
        refItemExVat[i].innerHTML = (refItemQty[i].value * (parseFloat(refItemPrice[i].innerHTML))).toFixed(2)
        refItemVat[i].innerHTML = ((parseFloat(refItemExVat[i].innerHTML) * 0.2).toFixed(2))
        refItemIncVat[i].innerHTML = ((parseFloat(refItemExVat[i].innerHTML) * 1.2).toFixed(2))
    
        // LOOP TO CALCULATE THE ROW TOTALS OF THE TABLE
        tableTotal = 0;
        for(let j=0; j < refItemRow.length; j++) { 
            tableTotal += parseFloat(refItemIncVat[j].innerHTML)
        }
            
        // SET THE SELECTED TOTAL TO TABLE TOTAL SET ABOVE
        // DUE TO MAGENTO ROUNDING ERROR, TOTALS ARE NOT CALCULATED BY JS IF ALL CHECKBOXES ARE CHECKED
        if(refItemCheckbox.length == refItemCheckboxChecked.length) {
            selectedTotal.innerHTML = parseFloat(orderTotalPrice)
        } else {
            selectedTotal.innerHTML = tableTotal.toFixed(2)
        }
        // SET AMOUNT TO REFUND FIELD TO THE SELECTED TOTAL AND MAX AMOUNT
        refTotalPrice.value = selectedTotal.innerHTML
        refTotalPrice.setAttribute('max', refTotalPrice.value)
    }
}

// 2. MANUAL REFUND AMOUNTS - FORM SETTING IF USER CHOOSES MANUAL REFUND    
refTotalPrice.addEventListener('keyup', () => {
    // IF AMOUNT TO REFUND INPUT IS MANUALLY CHANGED, UNCHECK ALL OTHER BOXES AND SET REST TO 0
    for(let i=0; i < refItemRow.length; i++){
        refItemCheckbox[i].checked = false
        refItemQty[i].value = 0 
        refItemExVat[i].innerHTML = 0
        refItemVat[i].innerHTML = 0
        refItemIncVat[i].innerHTML = 0            
    }
    manualLineDesc.style.display = 'block'
    manualLineItemQty.value = 1
    manualLinePrice.value = refTotalPrice.value
    // BLUR THE MAIN TABLE
    query('#refund-order table').style.opacity = '0.4'
}); 

// 3. MANUAL REFUND NOT ALLOW FURTHER ITEM REFUNDS - CHECK IF THERE ARE FURTHER ITEMS
if(manualRefundCheck.innerHTML == 'True'){
    
    // SET THE TOTAL PRICE BOX
    refTotalPrice.value = (orderTotalPrice - parseFloat(totalRefunded.innerHTML)).toFixed(2)
    refTotalPrice.setAttribute('max', refTotalPrice.value)
    // BLUR THE TABLE AND DISABLE CHECKBOXES
    query('#refund-order table').style.opacity = '0.4'
    for(let i=0; i < refItemRow.length; i++) {
        refItemQty[i].value = 0 
        refItemCheckbox[i].disabled = true
    }
    // SET THE MANUAL LINE INPUTS
    manualLineDesc.style.display = 'block'
    manualLineItemQty.value = 1
    manualLinePrice.value = refTotalPrice.value
}

// 4. DISABLE THE REFUND BUTTON IF AMOUNT TO REFUND IF 0
// Uncomment the if statement when putting feature live.
if(refTotalPrice.value == 0){
    refundOrderButton.setAttribute('disabled', 'disabled')
}




