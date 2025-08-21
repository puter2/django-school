function calculate_averages(){
    let table_rows = document.querySelectorAll('tbody tr');
    console.log(table_rows)
    table_rows.forEach(function (row){
        let grades_cells = row.querySelectorAll('#grade')
        let average_cell = row.querySelector('#average')
        console.log(average_cell)
        let dividend = 0
        let divisor = 0
        grades_cells.forEach(function (grade){
            dividend += Number(grade.innerText)*Number(grade.dataset.weight)
            divisor += Number(grade.dataset.weight)
        })
        average_cell.innerText = (dividend/divisor).toFixed(2)

    })
}

document.addEventListener("DOMContentLoaded", calculate_averages)
document.querySelector('#searchbar').addEventListener('keyup', calculate_averages)