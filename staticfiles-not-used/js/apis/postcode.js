// POSTCODES.IO - VALIDATE THE POSTCODE
let postcode = document.querySelector('#postcode span').innerHTML
    isValid = document.querySelector('#postcode .postcode-valid')

    fetch('https://api.postcodes.io/postcodes/' + postcode)
    .then(response => response.json())
    .then((data) => {
        let status = JSON.stringify(data.status)
        if (status == '200'){
            isValid.innerHTML = '<img src="/static/img/icons/check-circle-solid.svg">'
        }
        else {
            isValid.innerHTML = '<img src="/static/img/icons/times-circle-solid.svg">'
            buttonPick.setAttribute('disabled', ''); // Disables the Create Picklist button
            buttonShip.setAttribute('disabled', ''); // Disables the Create Shipment button
        }
    });    


  

