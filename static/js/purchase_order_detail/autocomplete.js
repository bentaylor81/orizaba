var query = document.querySelector.bind(document)
var queryAll = document.querySelectorAll.bind(document)

const search = query('.autocomplete input')
const matchList = query('#match-list')
const matchItem = queryAll('#match-list .match-item')

// Search /api/product/?format=json and filter
const searchProducts = async searchText => {
const res = await fetch('/api/product-simple/?format=json')
const products = await res.json();

    // Get matches to current text input
    let matches = products.filter(products => {
        const regex = new RegExp(`^${searchText}`, 'gi')
        return products.sku.match(regex)
    });

    // If everything is removed from the input, show no list
    if (searchText.length === 0) {
        matches = [];
        matchList.style.display = 'none';
        matchList.innerHTML = '';
    }

    outputHtml(matches);

    // Add to the seach input box when choice is clicked
    let item = queryAll('.match-item')
        addPartButton = query('.addPartButton')

    for (let i=0; i < item.length; i++) {
        item[i].addEventListener('click', selectProduct)

        function selectProduct(){
            // Set the search box value with the SKU - cosmetic only, not submitted     
            sku = queryAll('.match-item .item-sku')[i].innerHTML
            search.style.fontWeight = '900'
            search.value = sku
            addPartButton.removeAttribute('disabled', 'disabled')
            // Set the hidden text field with the ProductId to be submitted
            productId = queryAll('.match-item .product-id')[i].innerHTML
            productSku = queryAll('.match-item .item-sku')[i].innerHTML        
            query('.po-item-product').setAttribute('value', productId) 
            query('.po-item-product-sku').setAttribute('value', productSku) 
        }
    }
};

const outputHtml = matches => {
    // Show the dropdown list on the 2nd character added to the input box 
    if (search.value.length > 2) {
        if (matches.length > 0) {
            matchList.style.display = 'block';
            const html = matches.map(match => `
                <div class="match-item">
                    <b><span class="item-sku">${match.sku}</span></b> - <span class="item-product-name">${match.product_name}</span>
                    <span class="product-id">${match.product_id}</span>
                </div>
            `).join('');       
            matchList.innerHTML = html;
        }  
    }  
}

search.addEventListener('input', () => searchProducts(search.value))








