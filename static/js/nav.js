let menuItem = document.querySelectorAll('nav .menu-item');
    menuItemDropdown = document.querySelectorAll('nav .dropdown');
    menuItemActive = document.querySelectorAll('nav .menu-item > div');
    menuItemArrow = document.querySelectorAll('nav .menu-item span');
    pageName = document.querySelector('section').dataset.page;
    subMenuItem = document.querySelectorAll('nav .dropdown a li');
    subPageName = document.querySelector('section').dataset.subPage;

// MENU ITEM ACTIVE STATES
for(let i=0; i < menuItem.length; i++){
    menuItemCurrent = menuItem[i].dataset.menu;
    if (menuItemCurrent == pageName) { 
        menuItemActive[i].classList.add("menu-item-active");       
        if (menuItemDropdown[i]) { // Check if the main menu has a dropdown
            console.log(menuItemDropdown[i])
            menuItemDropdown[i].classList.add('expanded'); // Expand the sub list dropdowns
        }
    }
}
    
// SUB MENU ITEM ACTIVE STATES 
for(let i=0; i < subMenuItem.length; i++){
    subMenuItemCurrent = subMenuItem[i].dataset.subMenu;
    if (subMenuItemCurrent == subPageName) {
        subMenuItem[i].classList.add('sub-menu-item-active')
    }
}

// SELECT MAIN MENU DROPDOWNS WHEN CLICKED
for(let i=0; i < menuItemArrow.length; i++){                    
    // Call the function and open the dropdown on click
    menuItemArrow[i].addEventListener('click', openDropdown);
    
    function openDropdown(){
        menuItemDropdown[i].classList.toggle("expanded");
        menuItemActive[i].classList.toggle("menu-item-active")
    }
}

