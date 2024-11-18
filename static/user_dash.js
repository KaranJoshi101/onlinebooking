let appointmentBtn=document.querySelector('#appointmentBtn');
let profileBtn=document.querySelector('#profileBtn');
let bookAppointmentBtn=document.querySelector('#bookAppointmentBtn');
let patientsappointment=document.querySelectorAll('.patient-appointment')

let appointment=document.querySelector('#appointment');
let bookAppointment=document.querySelector('#bookAppointment');
let profile=document.querySelector('#profile');
let member=document.querySelectorAll('.member');

appointmentBtn.addEventListener('click',()=>{
    appointment.style.display='block'
    profile.style.display='none'
    bookAppointment.style.display='none'
})

bookAppointmentBtn.addEventListener('click',()=>{
    bookAppointment.style.display='block'
        appointment.style.display='none'
        profile.style.display='none'
})
profileBtn.addEventListener('click',()=>{
    bookAppointment.style.display='none'
        appointment.style.display='none'
        profile.style.display='block'
})
var l=[member[0]];
for(let m of member){
    m.addEventListener('click',()=>{
        m.setAttribute('disabled',true);
        m.innerText='selected'
        prev=l.pop()
        prev.innerText='select'
        
        prev.removeAttribute('disabled')
        l.push(m)
        app()
        
    })
}

function app(){
    for (let patient of patientsappointment){
        if(patient.id==l[0].id){
            patient.style.display='block';
        }
        else{
            patient.style.display='none';
        }
    }
}

app()



