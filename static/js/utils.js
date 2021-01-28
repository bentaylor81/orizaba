var query = document.querySelector.bind(document);
var queryAll = document.querySelectorAll.bind(document);

// MAGENTO PRODUCT SYNC

let magentoRow = queryAll('.magentoRow')
    magentoSynced = queryAll('.magentoSynced')

    for(let i=0; i < magentoRow.length; i++) {
        console.log(magentoSynced[i].innerHTML)
        if(magentoSynced[i].innerHTML == 'True') {
            magentoRow[i].style.background = '#1c8c0552'
        }
    }
    console.log(magentoRow)
