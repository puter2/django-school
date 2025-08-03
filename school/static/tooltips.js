/*
 <span class="tooltipText">Text tooltipa</span>
 */
document.addEventListener('DOMContentLoaded', function (){
    let tooltips = document.querySelectorAll('.tooltip');
    console.log(tooltips);
    const tooltip = document.createElement('div');
    tooltip.classList.add('tooltipText');
    document.body.appendChild(tooltip);

    tooltips.forEach(el=>{
        el.addEventListener('mouseover',function(){
            tooltip.innerText = el.dataset.tooltip;
            tooltip.style.display = 'block';
        });
        el.addEventListener('mouseout',function(){
            tooltip.style.display = 'none';
        });
        el.addEventListener('mousemove', function (e){
            tooltip.style.left = (e.pageX + 10) +'px';
            tooltip.style.top = (e.pageY + 10) + 'px'
        })
    });
});
