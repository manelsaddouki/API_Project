document.addEventListener('DOMContentLoaded', function () {
    
    var form = document.querySelector('.details');
    var countryInput = document.getElementById('name');

    
    form.addEventListener('submit', function (event) {
        
        event.preventDefault();

        
        var countryName = countryInput.value;

       
        if (countryName.trim() !== '') {
            
            var jsonData = { "name": countryName };

            //POST request 
            fetch('/donor', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(jsonData),
            })
                .then(response => response.json())
                .then(data => {
                    
                    console.log('Response from /donor endpoint:', data);
                })
                .catch(error => {
                    console.error('Error sending POST request:', error);
                });
        } else {
            console.error('Country name is empty');
        }
    });
});