var catBtn=document.querySelectorAll('.catBtn');
var hospitals=document.querySelector('#hospitals');
var docBtn=document.querySelectorAll('.docBtn');
var deptbackbtn=document.querySelectorAll('.deptback');
var backbtn=document.querySelectorAll('.back');
var l=[];
var m=[];
for(let c of catBtn){
    c.addEventListener("click",()=>{
        hospitals.style.display="none";
        try{
            let servcat=document.getElementById(`${c.value}`);
            servcat.style.display="block";
            l.push(servcat);
        }
        catch(exp){

        }
        
    })
}
for(let back of backbtn){
    back.addEventListener("click",()=>{
        hospitals.style.display="block";
        if(l.length){
            servcat=l.pop()
            servcat.style.display="none";
        }
        
    })
}
for(let d of docBtn){
    d.addEventListener('click',()=>{
        l[0].style.display="none";
        try{
            let servcat=document.getElementById(`${d.value}`);
            servcat.style.display="block";
            m.push(servcat);
        }
        catch(exp){

        }
    })
}
for(let back of deptbackbtn){
    back.addEventListener("click",()=>{
        l[0].style.display="block";
        if(m.length){
            servcat=m.pop()
            servcat.style.display="none";
        }
        
    })
}