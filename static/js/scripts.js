// OPEN MODAL COMPONENT
    let modalButton = document.querySelectorAll('.modal-button')
        modal = document.querySelectorAll('.modal')
        modalContainer = document.querySelectorAll('.modal-container')
        modalClose = document.querySelectorAll('.modal-close')
        modalCloseCancel = document.querySelectorAll('.modalCloseCancel')
        poItemModal = document.querySelectorAll('.poItemModal')

    // Open the Modal        
    for(let i=0; i < modalButton.length; i++){        
        modalButton[i].addEventListener('click', () => {  
            modal[i].style.display = 'block'
        })
    }
    // Close the Modal with X
    for(let j=0; j < modalClose.length; j++){ 
        modalClose[j].addEventListener('click', () => {
            modal[j].style.display = 'none'
        })       
    }
    // Close the Modal with Cancel
    for(let j=0; j < poItemModal.length; j++){ 
        modalCloseCancel[j].addEventListener('click', () => {
            console.log(poItemModal.length)
            poItemModal[j].style.display = 'none'
            poItemModal[j].style.background = '#000'
        })
    }

// CLOSE THE MESSAGE BAR AFTER 3 SECONDS
    let messageBar = document.querySelector('.messages')

    if (messageBar != null) {
        setTimeout(function(){ 
            messageBar.classList.add('fade-out')
        }, 4000);
        setTimeout(function(){ 
            messageBar.style.display = 'none';
        }, 5000);
    }

    
