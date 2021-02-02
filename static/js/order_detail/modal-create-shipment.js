//// CONTENTS - CREATE SHIPMENT MODAL ////

// 1. CALCULATE THE INITIAL TOTAL WEIGHT AND PRICE
// 2. ON SEND QTY CHANGE CALCULATE THE TOTAL PRICE AND WEIGHT
// 3. DISABLE SUBMIT BUTTON IF FIELDS ARE NOT SET
// 4. LOCAL STORAGE SAVE THE DATE
// 5. CHECK IF SHIPMENT HAS ALREADY BEEN CREATED

//// JAVASCRIPT ////

var query = document.querySelector.bind(document)
var queryAll = document.querySelectorAll.bind(document)

// VARIABLES 
let itemRow = queryAll('.itemRow')
    itemWeight = queryAll('.itemWeight')
    itemPrice = queryAll('.itemPrice')
    itemQty = queryAll('.itemQty')
    sendQty = queryAll('.sendQty')
    totalItemWeight = queryAll('.totalItemWeight')
    totalItemPrice = queryAll('.totalItemPrice')
    totalPriceField = query('.totalPriceField')
    totalWeightField = query('.totalWeightField')
    totalPriceInput = query('#totalPriceInput')
    totalWeightInput = query('#totalWeightInput')
    totalWeight = 0
    totalPrice = 0
    
// 1. CALCULATE THE INITIAL TOTAL WEIGHT AND PRICE
function productInfoFields() {
    for(let i=0; i<itemRow.length; i++) {
        // POPULATE THE TOTAL ITEM PRICE AND WEIGHT TABLE CELLS
        totalItemPrice[i].innerHTML = sendQty[i].value * itemPrice[i].innerHTML 
        totalItemWeight[i].innerHTML = sendQty[i].value * itemWeight[i].innerHTML
        // CALULATE THE INITIAL TOTAL PRICE AND WEIGHT FIELDS
        totalPrice += parseFloat(totalItemPrice[i].innerHTML)
        totalWeight += parseFloat(totalItemWeight[i].innerHTML)
        // POPULATE THE TOTAL PRICE AND WEIGHT FIELDS
        totalPriceField.innerHTML = '£' + totalPrice.toFixed(2)    
        totalWeightField.innerHTML = totalWeight.toFixed(2) + 'kg'
        // SET THE FORM INPUTS FOR PRICE AND WEIGHT BASED ON CALCULATIONS ABOVE
        totalPriceInput.value = totalPrice.toFixed(2) 
        totalWeightInput.value = totalWeight.toFixed(2)
    }
}  
productInfoFields()

// 2. ON SEND QTY CHANGE CALCULATE THE TOTAL PRICE AND WEIGHT
for(let i=0; i<itemRow.length; i++) {
    // EVENT LISTENER WHEN THE SEND QTY IS CHANGED
    sendQty[i].addEventListener('change', () => {
        totalPrice = 0
        totalWeight = 0
        // POPULATE THE TOTAL ITEM PRICE AND WEIGHT TABLE CELLS
        totalItemPrice[i].innerHTML = sendQty[i].value * itemPrice[i].innerHTML 
        totalItemWeight[i].innerHTML = sendQty[i].value * itemWeight[i].innerHTML
        // CALCULATE THE INITIAL TOTAL PRICE AND WEIGHT
        for(let j=0; j<itemRow.length; j++) { 
            totalPrice += parseFloat(totalItemPrice[j].innerHTML)
            totalWeight += parseFloat(totalItemWeight[j].innerHTML)
        }
        // POPULATE THE TOTAL PRICE AND WEIGHT FIELDS
        totalPriceField.innerHTML = '£' + totalPrice.toFixed(2)    
        totalWeightField.innerHTML = totalWeight.toFixed(2) + 'kg'
        // SET THE FORM INPUTS FOR PRICE AND WEIGHT BASED ON CALCULATIONS ABOVE
        totalPriceInput.value = totalPrice.toFixed(2) 
        totalWeightInput.value = totalWeight.toFixed(2)
        // HIGHLIGHT THE INPUT BOX WHEN SEND_QTY IS CHANGED
        if(sendQty[i].value < parseInt(itemQty[i].innerHTML)){
            sendQty[i].style.backgroundColor = '#1c89062e'
        }     
        else {
            sendQty[i].style.backgroundColor = '#ffffff'
        }          
    })       
}   
// 3. DISABLE SUBMIT BUTTON IF FIELDS ARE NOT SET
let deliveryMethodSelect = query('.deliveryMethodSelect')
    deliveryMethodDiv = query('.deliveryMethodDiv')
    submitShipment = query('.submitShipment')
    deliveryMethodDiv.style.backgroundColor = '#1c89062e'

    // DISABLE THE BUTTON IF NO METHOD IS SELECTED
    // SET THE COLOUR OF THE DELIVERY METHOD LABEL
    deliveryMethodSelect.addEventListener('change', () => {
        if(deliveryMethodSelect.value == 'Select Delivery Method') {
            deliveryMethodDiv.style.backgroundColor = '#1c89062e'
            submitShipment.setAttribute('disabled', 'disabled')
        } 
        else {
            submitShipment.removeAttribute('disabled', 'disabled')
            deliveryMethodDiv.style.backgroundColor = 'unset'
        }
    })
// 4. LOCAL STORAGE SAVE THE DATE
    let dateSent = query('.dateSent')
        savedDate = localStorage.getItem('savedDate')
    
        // GET TODAYS DATE
        today = new Date()
        date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate()
        console.log(date)
        // POPULATE THE DATE FILTER WITH THE VALUE IN LOCAL STORAGE
            dateSent.value = savedDate
        // SAVE THE DATE INTO LOCAL STORAGE
        dateSent.addEventListener('change', () => {
            localStorage.setItem('savedDate', dateSent.value)
        })

// 5. CHECK IF SHIPMENT HAS ALREADY BEEN CREATED
let trackedShipment = queryAll('.trackedShipment')
    confirmShipment = query('.confirmShipment')
    
    submitShipment.addEventListener('click', (e) => {
        if(trackedShipment.length > 0) {
            e.preventDefault()
            confirmShipment.style.display = 'block'
            submitShipment.setAttribute('disabled', 'disabled')
        }
    })