//// CONTENTS - FILTERING AND PAGINATION ////

//// VARIABLES ////

var query = document.querySelector.bind(document)
var queryAll = document.querySelectorAll.bind(document)
var cn = console.log.bind(document)

let tableRow = Array.from(queryAll('.tableRow')) // All rows in the table
    currentPageRow = Array.from(queryAll('.activeRow')) // Row which is in the current page
    // FILTER VARIABLES
    textFilter = query('.textFilter')
    dropDownFilter = query('.dropDownFilter')
    noItems = query('.noItems')
    // PAGINATION VARIABLES
    rowsPerPage = 30
    currentPage = 1
    totalPages = Math.ceil(tableRow.length/rowsPerPage)
    pageNext = query('.pageNext')
    pagePrev = query('.pagePrev')
    pageSelect = query('.pageSelect')

//// FUNCTIONS ////
    
    // CALLED WHEN ANY OF THE FILTERS OR PAGE SELECTORS ARE USED
    function filterRows() {
        // REMOVE PREVIOUS CLASSES
        noItems.style.display = 'none'
        for(let i = 0; i < tableRow.length; i++) {
            tableRow[i].classList.remove('curPageRow')
            tableRow[i].classList.remove('nonCurPageRow')
        }
        // FILTER TABLEROW ITEMS
        let filteredRow = tableRow.filter(row => row.innerText.toLowerCase().includes(textFilter.value.toLowerCase()) && row.innerText.includes(dropDownFilter.value))
            startRow = rowsPerPage * (currentPage - 1)
            endRow = startRow + rowsPerPage 
            paginatedRow = filteredRow.slice(startRow, endRow) 
        // PAGINATE THE FILTERED ROWS
        for(let i = 0; i < paginatedRow.length; i++) {
            paginatedRow[i].classList.add('curPageRow')
        } 
        // DISPLAY NO ROWS MESSAGE IF NO RESULTS
        if(filteredRow.length == 0) {
            noItems.style.display = 'table-row'
        }
        // DISPLAY STATS - 'TOTAL: X' AND 'SHOWING X OF X' 
        query('.totalRows').innerHTML = filteredRow.length
        if(filteredRow.length > endRow) {
            query('.startRowDisplayed').innerHTML = startRow + 1
            query('.endRowDisplayed').innerHTML = endRow
        } else if(filteredRow.length == 0) {
            query('.startRowDisplayed').innerHTML = 0
            query('.endRowDisplayed').innerHTML = 0
        } else {
            query('.startRowDisplayed').innerHTML = startRow + 1
            query('.endRowDisplayed').innerHTML = filteredRow.length
        }
        // DISPLAY PAGINATION - 'PREVIOUS | X | NEXT'
        totalFilteredPages = Math.ceil(filteredRow.length/rowsPerPage)
        pageSelect.length = 0
        for(let i = 0; i < totalFilteredPages; i++) {
            pageSelect.options[pageSelect.options.length] = new Option(i+1, i+1)
        }
        pageSelect.value = currentPage
        // DROPDOWN, PREVIOUS, NEXT BUTTONS
        BtnStates(currentPage, totalFilteredPages)
    }
    
    // ALTERS THE BUTTON STATES DEPENDING ON THE PAGE NUMBER
    function BtnStates(currentPage, allTotalPages) {
        // PAGE DROPDOWN
        if(allTotalPages == 1) {
            pageSelect.setAttribute('disabled', 'disabled')
        } else {
            pageSelect.removeAttribute('disabled', 'disabled')
        }
        // PREVIOUS BUTTON
        if(currentPage == 1) {
            pagePrev.setAttribute('disabled', 'disabled')
        } else {
            pagePrev.removeAttribute('disabled', 'disabled')
        }
        // NEXT BUTTON
        if(currentPage == allTotalPages) {
            pageNext.setAttribute('disabled', 'disabled')
        } else {
            pageNext.removeAttribute('disabled', 'disabled')
        }
        // DIASABLE ALL IF EQUAL 0
        if(allTotalPages == 0) {
            pageSelect.options[pageSelect.options.length] = new Option(1, 1)
            pageSelect.value = 1
            pagePrev.setAttribute('disabled', 'disabled')
            pageNext.setAttribute('disabled', 'disabled')
            pageSelect.setAttribute('disabled', 'disabled')
        }
    }

    // FUNCTION CALLED ON PAGE LOAD TO SET INITAL TABLE CONTENT
    function PaginateRows(currentPage) {
        startRow = rowsPerPage * (currentPage - 1)
        endRow = startRow + rowsPerPage 
        paginatedRow = tableRow.slice(startRow, endRow) 
        // FILTER THE PAGE ITEMS    
        for(let i = 0; i < paginatedRow.length; i++){ 
            tableRow[i].classList.add('curPageRow')
        } 
        // DISPLAY STATS - 'TOTAL: X' AND 'SHOWING X OF X'
        query('.totalRows').innerHTML = tableRow.length
        if(tableRow.length > endRow) {
            query('.startRowDisplayed').innerHTML = startRow + 1
            query('.endRowDisplayed').innerHTML = endRow
        } else if(tableRow.length == 0) {
            query('.startRowDisplayed').innerHTML = 0
            query('.endRowDisplayed').innerHTML = 0
        } else {
            query('.startRowDisplayed').innerHTML = startRow + 1
            query('.endRowDisplayed').innerHTML = tableRow.length
        } 
        // DISPLAY PAGINATION - 'PREVIOUS | X | NEXT'
        for(let i = 0; i < totalPages; i++) {
            pageSelect.options[pageSelect.options.length] = new Option(i+1, i+1)
        }
        // DROPDOWN, PREVIOUS, NEXT BUTTONS
        BtnStates(currentPage, totalPages)
    }

PaginateRows(currentPage)

//// EVENT LISTENERS ////
    // DROPDOWN FILTER
    dropDownFilter.addEventListener('change', () => {
        currentPage = 1
        filterRows()
    })
    // TEXT FILTER
    textFilter.addEventListener('keyup', (event) => {
        currentPage = 1
        filterRows()          
    })
    // SET THE SELECTED OPTION BASED ON THE PAGE NUMBER
    pageSelect.addEventListener('change', () => {
        currentPage = pageSelect.value
        filterRows()
    })
    // NEXT PAGE
    pageNext.addEventListener('click', () => {
        currentPage++
        filterRows()
    })
    // PREVIOUS PAGE
    pagePrev.addEventListener('click', () => {
        currentPage--
        filterRows()
    })

//// NOTES ////

// 1. CREATE TABLE - Add in <tr class="tableRow">
// 2. NO DISPLAY HTML - Add in <tr class="noItems"><td>No Items to Display</td></tr>
// 3. ADD HTML FILE
    //  <!-- PAGINATE AND FILTER TABLE COMPONENT -->
    //  {% include 'app_products/global/pag-filter-table.html' %}
    //  <!-- END -->  
// 4. ADD JS FILE
    // <script type="text/javascript" src="{% static 'js/general/pag-filter-table.js' %}"></script>