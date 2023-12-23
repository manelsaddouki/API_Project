async function submitForm() {
    // Get form element
    var form = document.getElementById('myForm');

    // Create objects to store data separately
    var formData = {};
    var donationData = [];
    var typeData=[];
    var countryData = [];
    var donorData = [];

    // Iterate through form elements
    for (var i = 0; i < form.elements.length; i++) {
        var element = form.elements[i];

        // Check if the element is a text input, checkbox, or radio button
        if (
            (element.type === 'text' || element.type === 'textarea') ||
            (element.type === 'checkbox' && element.checked) ||
            (element.type === 'radio' && element.checked)
        ) 
        {
            // Determine which data object to store the value in
            if (element.name === 'donation') {
                // Parse donation as float
                donationData.push (parseFloat(element.value));
            } 
            else if (element.name === 'donationType') {
                typeData.push(element.value);
            }
            else if (element.name === 'countries') {
                // Store countries as a list of strings
                countryData.push(element.value);

            } 
            else if (element.name === 'donors') {
                // Store donors as a list of strings
                donorData.push(element.value);
            }

            // Store the value in the general formData object
            formData[element.name] = element.value;
        }
    }
    
    const countryResponse = await fetch(`/affected/${countryData[0]}`);
    const countryDataResponse = await countryResponse.json();
    const affectedId = countryDataResponse.id;

    fundData = {"type": typeData[0] , "donation": donationData[0]}

    // Make a POST request to the /fund/<int:affected_id> endpoint
    const fundResponse = await fetch(`/fund/${affectedId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(fundData),
    });

    const fundDataResponse = await fundResponse.json();

    // Handle the response from the server
    const newFundId = fundDataResponse.id;

    console.log(`Fund added for affected ID ${affectedId}. New Fund ID: ${newFundId}`);

    // Now, iterate over the list of donor IDs and link each donor to the new fund
    for (let j = 0; j < donorData.length; j++) {
        const donorname = donorData[j];
        const donorResponse = await fetch(`/donor/${donorname}`);
        const donorDataResponse = await donorResponse.json();
        const donorId = donorDataResponse.id;

        // Make a POST request to the /donor/<int:donor_id>/fund/<int:fund_id> endpoint
        const linkResponse = await fetch(`/donor/${donorId}/fund/${newFundId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        const linkData = await linkResponse.json();
        // Handle the response from the server
        console.log(`Donor ${donorId} linked to Fund ${newFundId}:`, linkData);
    }

    // Log the collected data to the console
    console.log('All Form Data:', formData);
    console.log('Donation Data:', donationData);
    console.log('Country Data:', countryData);
    console.log('Donor Data:', donorData);
}

const formClick = document.querySelector("#submitForm");
formClick.addEventListener("click", submitForm);
