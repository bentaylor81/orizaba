// COMMON COMMANDS

var query = document.querySelector.bind(document);
var queryAll = document.querySelectorAll.bind(document);
var cn = console.log.bind(document);

// FILTERING
let bigCities = cities.filter(city => city.population > 3000000);
console.log(bigCities);

// EVENT LISTENERS
myClass.addEventListener('change', () => {
})

// PREVENT DEFAULT
todayButton.addEventListener('click', (event) => {
    event.preventDefault()
})

// GET TODAY IN INPUT DATE FORMAT
today = new Date();
date = today.getFullYear()+'-'+('0'+(today.getMonth()+1)).slice(-2)+'-'+('0'+today.getDate()).slice(-2);





// let movementRefFilter = query('.movementRefFilter')
//     movementTypeFilter = query('.movementTypeFilter')
//     noItems = query('.noItems')
//     movementRow = queryAll('.movementRow')
//     movementRef = queryAll('.movementRef')
//     movementType = queryAll('.movementType')



//     // FILTER BY FUNCTION
//     function DropdownFilterRows() {
//         filteredRowCount = 0
//         for(let i=0; i < movementRow.length; i++){
//             // FILTER LIST BASED ON DROPDOWN SEARCH     
//             if(movementType[i].innerText.includes(movementTypeFilter.value)) {
//                 movementRow[i].classList.add('activeRow')   
//                 movementRow[i].classList.add('filteredRow')  
//                 filteredRowCount = 1  
//             } else {
//                 movementRow[i].classList.remove('activeRow')  
//                 movementRow[i].classList.remove('filteredRow') 
//             }
//         }
//         currentPage = 1
//     }


// // //// 1C. FILTERING EVENT LISTENERS ////

// //     // DROPDOWN TYPE FILTER - ADJUST THE RESULTS ON EACH KEY PRESS
// //     movementTypeFilter.addEventListener('change', () => {
// //         // CLEAR ALL EXISTING ROWS FIRST
        
// //         ClearAllRows();
// //         DropdownFilterRows()
// //         PaginationStats()
// //         // paginateRows()
// //         // dropdownFilterRows()
// //         // noResultsFound(filteredRowCount)
        
// //         cn(activeRow.length)
// //     });
//     // SEARCH REF FILTER - ADJUST THE RESULTS ON EACH KEY PRESS
//     movementRefFilter.addEventListener('keyup', function() {
//         filteredRowCount = 0
//         for(let i=0; i < movementRow.length; i++){
//             // FILTER LIST BASED ON KEYED SEARCH            
//             if(movementRef[i].innerText.toLowerCase().includes(movementRefFilter.value.toLowerCase()) && movementType[i].innerText.includes(movementTypeFilter.value)) {
//                 movementRow[i].style.display = 'table-row'  
//                 filteredRowCount = 1         
//             } else {
//                 movementRow[i].style.display = 'none'
//             }    
//         }
//         noResultsFound(filteredRowCount)
//     });

//     // DISPLAY NO RESULT FOUND MESSAGE
//     function NoResultsFound(filteredRowCount) {
//         if(filteredRowCount == 0) {
//             noItems.style.display = 'table-row'
//         }    
//         else {
//             noItems.style.display = 'none'
//         } 
//     }


// //// 2B. PAGINATION FUNCTIONS ////  

// let rowsPerPage = 10
//         currentPage = 1
//         totalPages = Math.ceil(tableRow.length/rowsPerPage)
//         pageNext = query('.pageNext')
//         pagePrev = query('.pagePrev')
//         pageSelect = query('.pageSelect')
    // 

//     // DISPLAY PAGINATED ROW - DISPLAY BASED ON THE PAGE SELECTED
//     function DisplayRows(currentPage) {
//         startRow = rowsPerPage * (currentPage - 1)
//         endRow = startRow + rowsPerPage 
//         paginatedRow = tableRow.slice(startRow, endRow) 
//         // FILTER THE PAGE ITEMS    
//         for(let i = 0; i < paginatedRow.length; i++){
//             paginatedRow[i].classList.add('activeRow')
//         }    
//     }
//     // DISPLAY STATS - 'TOTAL: X' AND 'SHOWING X OF X'
//     function PaginationStats() {
//         // DISPLAY TOTAL COUNTER NUMBER BASED ON IF FILTERING IS APPLIED OR NOT
//         filteredRow = queryAll('.filteredRow')
//         if(filteredRow.length == 0) {
//             query('.totalRows').innerHTML = tableRow.length
//         }
//         else {
//             query('.totalRows').innerHTML = filteredRow.length
//         }
//         // DISPLAY PAGINATION COUNTER STATS
//         query('.startRowDisplayed').innerHTML = startRow + 1
//         // DISPLAY END ROW
//         if (endRow < tableRow.length) { 
//             query('.endRowDisplayed').innerHTML = endRow
//         } else {
//             query('.endRowDisplayed').innerHTML = tableRow.length
//         }
//     }
//     // DISPLAY PAGINATION - 'PREVIOUS | X | NEXT'
//     function DisplayPagination() {  
//         for(let i = 0; i < totalPages; i++) {
//             pageSelect.options[pageSelect.options.length] = new Option(i+1, i+1)
//         }
//     }
//     // PREVIOUS BUTTON - SET THE STATE - DISABLE IF ON PAGE 1
//     function PrevBtnState() {
//         if(currentPage == 1) {
//             pagePrev.setAttribute('disabled', 'disabled');
//         } else {
//             pagePrev.removeAttribute('disabled', 'disabled')
//         }
//     }
//     // NEXT BUTTON - SET THE STATE - DISABLE IF ON LAST PAGE
//     function NextBtnState() {
//         if(currentPage == totalPages) {
//             pageNext.setAttribute('disabled', 'disabled')
//         } else {
//             pageNext.removeAttribute('disabled', 'disabled')
//         }
//     }
//     // CLEAR ALL ROWS - CLEAR THE ROWS BEFORE AN EVENT, SO THAT THE ROWS DON'T BUILD
//     function ClearAllRows() {
//         for(let i = 0; i < tableRow.length; i++){
//             tableRow[i].classList.remove('activeRow')
//         }
//     }
//     // MAIN FUNCTION TO FILTER ALL ROWS
//     function PaginateRows() {
//         // CLEAR ALL EXISTING ROWS FIRST
//         ClearAllRows();
//         // SET NEW CURRENT PAGE VALUE
//         DisplayRows(currentPage)
//         // UPDATE STATS
//         PaginationStats()
//         // DISABLE AND ENABLE BUTTONS
//         NextBtnState()
//         PrevBtnState()
//         // SET PAGE NUMBER DROPDOWN
//         pageSelect.value = currentPage
//     }

// //// 2C. PAGINATION EVENT LISTENERS ////

//     
//     // NEXT PAGE
//     pageNext.addEventListener('click', () => {
//         currentPage++
//         PaginateRows()
//     })
//     // PREVIOUS PAGE
//     pagePrev.addEventListener('click', () => {
//         currentPage--
//         PaginateRows()
//     })

// //// 2D. PAGELOAD RUN FUNCTIONS ////
//     DisplayRows(currentPage)
//     PaginationStats()
//     DisplayPagination() // SHOW PAGE NUMBER DROPDOWN
//     PrevBtnState() // DISABLED PREVIOUS BUTTON AS LANDING PAGE WILL BE FIRST PAGE




    