// SET THE COLOUR OF THE ROWS DEPENDING ON THE UNLEASHED STATUS ROW

let row = document.querySelectorAll('#unleashed tr.unleashed-row')
    rowPending = document.querySelectorAll('.unleashed-status')

for(let i=0; i < row.length; i++) {
    if(rowPending[i].innerHTML == 'Unleashed Updated') {
        row[i].style.backgroundColor = '#1c8c0559';
    }
}
