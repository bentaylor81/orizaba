// OPEN MODAL COMPONENT
    let modalButton = document.querySelectorAll('.modal-button');
        modal = document.querySelectorAll('.modal');
        modalClose = document.querySelectorAll('.modal-close');

    for(let i=0; i < modalButton.length; i++){        
        modalButton[i].addEventListener('click', openModal);
        // Open the Modal
        function openModal(){
            modal[i].style.display = 'block';
        }
    }

    // Close the Modal
    for(let j=0; j < modalClose.length; j++){ 
        modalClose[j].addEventListener('click', closeModal);

        function closeModal() {
            modal[j].style.display = 'none';
        }
    }

// ADD PURCHASE ORDER REQUIRED FIELDS - SHOW REQUIRED ERROR MESSGE AND DISABLE BUTTON
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

    // CLOSE THE MESSAGE BAR AFTER 3 SECONDS
        let messageBar = document.querySelector('.messages')

        if (messageBar != null) {
            setTimeout(function(){ 
                messageBar.classList.add('fade-out')
            }, 1000);
            setTimeout(function(){ 
                messageBar.style.display = 'none';
            }, 2000);
        }

    
