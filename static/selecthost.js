// select-detail-hospital;
const classmaking=(s)=>{
    let snew='';
    for(let i of s){
        if(i==' '){
            snew+='.'
        }
        else{
            snew+=i
        }
    }
    return snew;
}

select_slot_btn = document.querySelector(".select-slot-btn");
select_detail_hospital = document.querySelector(".select-detail-hospital");
form_slot = document.querySelector("#form-slot");
form_slot_back = document.querySelector("#form-slot-back");
select_book_btn = document.querySelector(".select-book-btn");
form_thank = document.querySelector("#form-thank");
book_appointment_txt = document.querySelector("#book-appointment");
bookdate=document.querySelector('#bookdate')
slot=document.querySelector('#slot')

nextBtn=document.querySelector('#nextBtn');
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

let hospital=document.querySelector('#hospital');
city.addEventListener('click',()=>{
    if(city.value){
        hospital.removeAttribute('disabled')
        h=document.querySelectorAll(`.${classmaking(city.value)}`)
        for(i of h){
            i.style.display='block';
        }
    }
})

let dept=document.querySelector('#dept');
hospital.addEventListener('click',()=>{
    if(hospital.value){
        dept.removeAttribute('disabled')
        h=document.querySelectorAll(`.${classmaking(hospital.value)}`)
        for(i of h){
            i.style.display='block';
        }
    }
})
var doctor=document.querySelector('#doctor');
dept.addEventListener('click',()=>{
    if(dept.value){
        nextBtn.removeAttribute('disabled')
        doctor.removeAttribute('disabled')
        h=document.querySelectorAll(`.${classmaking(dept.value)}`)
        for(i of h){
            i.style.display='block';
        }
    }
})
var msg
let docday=document.querySelectorAll('.docday')
doctor.addEventListener('click',()=>{
    if(doctor.value){
        msg=document.querySelector(`#${doctor.value}`)
       msg.style.display='block'
    }
    
})

bookdate.addEventListener('click',()=>{
    
    if(bookdate.value){

        slot.removeAttribute('disabled')
        let day=new Date(bookdate.value)
        day=day.getDay();
        slots=document.querySelectorAll(`.${doctor.value}`)
        for(s of slots){
            if(s.classList.contains(day))
                s.style.display='block';
        }
    }
})

slot.addEventListener('click',()=>{
    if(slot.value){
        document.querySelector('#bookBtn').removeAttribute('disabled')
        patient=document.querySelector('#patient')
members=document.querySelectorAll('.member')
for(member of members){
    if(member.innerText=='selected'){
        patient.value=member.id
        break;
    }
}
    }
})

