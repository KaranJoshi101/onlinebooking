function check(str){
    str=str.toLowerCase()
    newstr=''
    for(s of str){
        if(s==' '){
            continue;
        }
        newstr+=s
    }
    return newstr
}
let select=document.querySelector('#select');
let search=document.querySelector('#search');
let table=document.querySelector(`#${select.value}`);
search.placeholder=`Enter ${select.value} details`
table.style.display='';
var rows=document.querySelectorAll(`.${select.value}`);
select.addEventListener('click',()=>{
    if(select.value){
        search.placeholder=`Enter ${select.value} details`
        table.style.display='none'
        table=document.querySelector(`#${select.value}`);
        table.style.display='';
        rows=document.querySelectorAll(`.${select.value}`)
        for (let row of rows){
            row.style.display=''
        }
    }
})

search.addEventListener('keyup',()=>{
    
        let srh=check(search.value)
        for(let row of rows){
            if(check(row.id).includes(srh)){
                row.style.display=''
            }
            else{
                row.style.display='none';
            }
        }

})

