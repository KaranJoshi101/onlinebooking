// select-detail-hospital;

select_slot_btn = document.querySelector(".select-slot-btn");
select_detail_hospital = document.querySelector(".select-detail-hospital");
form_slot = document.querySelector("#form-slot");
form_slot_back = document.querySelector("#form-slot-back");
select_book_btn = document.querySelector(".select-book-btn");
form_thank = document.querySelector("#form-thank");
book_appointment_txt = document.querySelector("#book-appointment");

select_slot_btn.addEventListener("click",()=>{
    select_detail_hospital.style.display = "none";
    form_slot_back.style.display = "block";
    form_slot.style.display = "block";
})

form_slot_back.addEventListener("click",()=>{
    select_detail_hospital.style.display = "block";
    form_slot_back.style.display = "none";
    form_slot.style.display = "none";
})

select_book_btn.addEventListener("click",()=>{
    select_detail_hospital.style.display = "none";
    form_slot_back.style.display = "none";
    form_slot.style.display = "none";
    form_thank.style.display = "block";
    book_appointment_txt.style.display = "none"

})

let state=document.querySelector('#state');
let city=document.querySelector('#city');
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


