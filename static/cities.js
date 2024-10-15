let state=document.querySelector('#state');
var city=document.querySelector('#city');
    state.addEventListener('click',()=>{
        if(state.value){
        
            city.removeAttribute('disabled');
            let cities=document.querySelectorAll('.cities');
            for(let c of cities){
                
                if(c.id==state.value){
                    c.style.display='block';
                
                }
                else{
                    c.style.display='none';
                }
            }
        }
            
    })