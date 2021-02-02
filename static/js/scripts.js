// MODAL COMPONENT
    let modalOpenButton = document.querySelectorAll('.modalOpenButton')
        modal = document.querySelectorAll('.modal')

    // OPEN THE MODAL        
    for(let i=0; i < modalOpenButton.length; i++){        
        modalOpenButton[i].addEventListener('click', () => {  
            modal[i].style.display = 'block'
        })
    }
    // CLOSE THE MODAL
    function closeModal() {
        for(let i=0; i < modal.length; i++) {
            console
            modal[i].style.display = 'none'
        }
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

// BUTTON DOUBLE CLICK DON'T ALLOW RE-SUBMIT

    
