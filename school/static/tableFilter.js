
function tableFilter(){
    let table = document.getElementsByTagName('table')
    let input = document.getElementById('searchbar')
    let filter = input.value.toLowerCase();
    let rows = document.querySelectorAll('tr')
    for (let i = 0; i<rows.length; i++){
        let cells = rows[i].getElementsByTagName('td');
        let found = false

        for (let j=0; j<cells.length; j++){
            let cell = cells[j]
            if (cell && cell.textContent.toLowerCase().includes(filter)) {
                found = true;
                break;
            }
        }
        rows[i].style.display = found ? '' : 'none';
    }

}

document.addEventListener('DOMContentLoaded', function (){
    let table = document.getElementsByTagName('table')[0]
    let table_parent = table.parentNode
    let form = document.createElement('form')
    let searchbar = document.createElement('input')
    searchbar.type = 'text'
    searchbar.id = 'searchbar'
    searchbar.addEventListener('keyup', tableFilter)
    searchbar.placeholder="type student name"
    form.appendChild(searchbar)
    table_parent.insertBefore(form, table)
})
