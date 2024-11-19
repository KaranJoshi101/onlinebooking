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
var doc
let docday=document.querySelectorAll('.docday')
doctor.addEventListener('click',()=>{
    if(doctor.value){
        doc=document.querySelector(`#${doctor.value}`)
       doc.style.display='block'
    }
    
})
let msg=document.querySelector('#msg');
var date;
bookdate.addEventListener('change',()=>{
    
    if(bookdate.value){
        msg2.style.display='none';
        slot.removeAttribute('disabled')
        date=new Date(bookdate.value)
        
        day=date.getDay();
        slots=document.querySelectorAll(`.${doctor.value}`)
        let count=false
        for(s of slots){
            if(s.classList.contains(day)){

            
                s.style.display='';
                count=true
            }
            else{
                s.style.display='none';
            }
        }
        if(!count){
            msg.style.display=''
            slot.disabled=true
        }
        else{
            msg.style.display='none'
        }
    }
})

slot.addEventListener('click',()=>{
    if(slot.value){
        msg2.style.display='none';
        async function getData() {
            const url =`http://127.0.0.1:5000/api/appointment/${slot.value}/${date.getDate()}/${date.getMonth()+1}/${date.getFullYear()}`;
            try {
              const response = await fetch(url);
              if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
              }
          
              const json = await response.json();
              return json
            } catch (error) {
              console.error(error.message);
            }
          }
          data=getData()
          data.then((value)=>{if(value[0].avail){
            document.querySelector('#bookBtn').removeAttribute('disabled')
            patient=document.querySelector('#patient')
          }
          else{
            msg2=document.querySelector('#msg2')
            msg2.innerText='Sorry! Doctor is unavailable in this slot. Try another slot or date.'
            msg2.style.display='';
          }})
            
           
          
        
members=document.querySelectorAll('.member')
for(member of members){
    if(member.innerText=='selected'){
        patient.value=member.id
        break;
    }
}
    }
})

