var query = document.querySelector.bind(document);
var queryAll = document.querySelectorAll.bind(document);

// SET THE COLOUR OF THE CELL TO GREEN IF CELL IS TICKED
let returnRow = queryAll('.returnRow')
    receivedCell = queryAll('.receivedCell')
    inspectionPassed = queryAll('.inspectionPassed')
    itemRefunded = queryAll('.itemRefunded')

    for(let i=0; i < returnRow.length; i++) {
        if(!receivedCell[i].innerHTML.includes('--')) {
            receivedCell[i].style.backgroundColor = '#2177051f'
        }
        if(!inspectionPassed[i].innerHTML.includes('--')) {
            inspectionPassed[i].style.backgroundColor = '#2177051f'
        }
        if(!itemRefunded[i].innerHTML.includes('--')) {
            itemRefunded[i].style.backgroundColor = '#2177051f'
            returnRow[i].style.backgroundColor = '#2177051f'
        }

    }
console.log(returnRow.length)