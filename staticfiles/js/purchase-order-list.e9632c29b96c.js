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
