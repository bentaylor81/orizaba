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
