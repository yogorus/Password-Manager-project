let input = document.querySelector('#input');
// Ajax request to search user passwords
input.addEventListener('keyup', async function() {
    let response = await fetch('/search?q=' + input.value);
    let passwords = await response.text();
    document.querySelector('#content').innerHTML = passwords;

    // Add button functionality
    let box = document.querySelectorAll("#box");

    let pwd = document.querySelectorAll('#pwd');

    let copy = document.querySelectorAll('#copy');
                
    for (let i = 0; i < box.length; i++) {
                    
        box[i].addEventListener('mouseout', function() {
            pwd[i].style.visibility = 'hidden';
            });
                    
        box[i].addEventListener('mouseover', function() {
            pwd[i].style.visibility = 'visible';
            });
        
        copy[i].addEventListener('click', function() {
            // Select pwd element
            pwd[i].select;
            // Copy password to clipboard
            navigator.clipboard.writeText(pwd[i].innerHTML);
        });
    }
    });

window.addEventListener('DOMContentLoaded', function () {
    let evt = new Event('keyup');
    input.dispatchEvent(evt);
});

