// STATUS COLOUR - Set the Colour of the Status based on it's state
let status = document.querySelectorAll('.status');

for (let i=0; i < status.length; i++) {
    if (status[i].innerHTML == 'Complete') {
        status[i].classList.add('complete')
    }
    else if (status[i].innerHTML == 'Part Receipt') {
        status[i].classList.add('partial-complete')
    }
    else if (status[i].innerHTML == 'Unleashed') {
        status[i].classList.add('unleashed')
    }
}

// ADD PURCHASE ORDER REQUIRED FIELDS - SHOW REQUIRED ERROR MESSAGE AND DISABLE BUTTON
let requiredField = document.querySelectorAll('.required-field')
    requiredNotice = document.querySelector('.required-notice')
    addPoButton = document.querySelector('#submit-button')

    // When the button is clicked, check if the form is valid 
    // If it's not valid set the button to disabled and display message
    addPoButton.addEventListener('click', checkRequired);

    function checkRequired() {
        for(let i=0; i < requiredField.length; i++){
            if(requiredField[i].value == '') {
                requiredNotice.style.display = 'block';
                addPoButton.setAttribute('disabled', 'disabled')                
            }
        }
    }

    // Re-enables the button when an input is re-selected
    for(let j=0; j < requiredField.length; j++) {
        requiredField[j].addEventListener('click', enableButton);
        
        function enableButton() {
            addPoButton.removeAttribute('disabled')  
            requiredNotice.style.display = 'none'; 
        }
    }